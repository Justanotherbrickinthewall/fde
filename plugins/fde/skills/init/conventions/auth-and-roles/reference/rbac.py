"""The RBAC predicates, and the gate every project route hangs off.

`project_for_user` refuses with 404, never 403. A person who is not on a
project must not learn that the project exists, so "you may not see this"
and "there is no such thing" have to read the same from outside. The
obvious spelling is a DRF permission class returning False, and that
renders as 403, which is the mistake this module exists to avoid.

## How this reaches a domain's models

`Project` and `ProjectMember` live in `domains/projects/`, and `core/`
may not import from a domain. So the models are reached lazily, by
label, through `settings.RBAC_PROJECT_MODEL` and
`settings.RBAC_PROJECT_MEMBER_MODEL` -- the same trick `AUTH_USER_MODEL`
uses. Nothing here imports a domain and nothing here runs at import time,
so this module loads with no domain app installed at all.

A domain that wants this gate needs two things and no more:

1. `Project` and `ProjectMember`, with the field names this module
   reads: `Project.pk`, `ProjectMember.project_id`,
   `ProjectMember.user_id`, `ProjectMember.role`.
2. Those two settings pointing at them.

The HTTP end: authenticate first, with DRF's `IsAuthenticated`, then
call `project_for_user(request.user, project_id)` in the view and use
what it returns. `Http404` is what DRF renders as a 404, so no exception
handler is needed.
"""

from typing import Protocol

from django.apps import apps
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404

# The only role the template ships with. The role is a per-project
# string on `ProjectMember`, not a Django group, because a group is
# global and a role on a project is not. A new role is a row, not a
# migration.
ROLE_OWNER = "owner"
ROLES = (ROLE_OWNER,)


class ProjectSource(Protocol):
    """Where projects and memberships come from.

    A seam, so the 404-not-403 decision can be tested in `core/` with no
    domain installed at all.
    """

    def get_project(self, project_id): ...

    def roles_in(self, *, project_id, user_id) -> set[str]: ...

    def owners_of(self, project_id) -> list: ...


class ModelProjectSource:
    """The real one: the models named in settings, resolved on each call."""

    def _project_model(self):
        return apps.get_model(settings.RBAC_PROJECT_MODEL)

    def _member_model(self):
        return apps.get_model(settings.RBAC_PROJECT_MEMBER_MODEL)

    def get_project(self, project_id):
        return self._project_model().objects.filter(pk=project_id).first()

    def roles_in(self, *, project_id, user_id) -> set[str]:
        rows = self._member_model().objects.filter(
            project_id=project_id, user_id=user_id
        )
        return set(rows.values_list("role", flat=True))

    def owners_of(self, project_id) -> list:
        rows = (
            self._member_model()
            .objects.filter(project_id=project_id, role=ROLE_OWNER)
            .select_related("user")
        )
        return [row.user for row in rows]


_source: ProjectSource = ModelProjectSource()


def set_project_source(source: ProjectSource) -> ProjectSource:
    """Swap the source. Returns the one it replaced, so a test can restore it."""
    global _source
    previous, _source = _source, source
    return previous


def project_source() -> ProjectSource:
    return _source


def roles_in(*, project_id, user_id) -> set[str]:
    return _source.roles_in(project_id=project_id, user_id=user_id)


def owners_of(project_id) -> list:
    return _source.owners_of(project_id)


def project_for_user(user, project_id):
    """The project, if this person may see it. Otherwise 404.

    A super admin sees every project. Everyone else sees the projects they
    are a member of, whatever their role. A non-member gets exactly what
    somebody asking after a project id that was never issued gets.
    """
    if not getattr(user, "is_authenticated", False):
        # Defensive. DRF's IsAuthenticated runs in front of this, so a
        # request reaching here anonymously is a wiring mistake, and 401
        # is the honest answer to it rather than a 404 that would hide it.
        raise PermissionDenied("Sign in first")
    project = _source.get_project(project_id)
    if project is None:
        raise Http404("No such project")
    if user.is_super_admin:
        return project
    if not _source.roles_in(project_id=project_id, user_id=user.id):
        raise Http404("No such project")
    return project
