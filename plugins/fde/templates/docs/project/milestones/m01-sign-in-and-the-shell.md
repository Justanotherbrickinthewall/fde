---
status: built 07-09-26
target: 07-09-26
built: 07-09-26
delivery: none
waits-on: none
---
# A person signs in, sees an empty project list, and a super admin adds people and creates projects

Why now: this is the floor every later milestone stands on. Nothing can be
drafted, filed or signed until a person has somewhere to sign in and a
project has somewhere to live. It ships with the template, so a pod starts
its first client milestone against a running application rather than an
empty repository.

## In scope

Authentication. Sessions held server-side, password hashing, and roles held
as data rather than as code. One permission rule, not one rule per role.

People. A super admin creates a person, lists them and assigns a role.

Projects. A project exists, it lists its members, and it carries one named
owner a super admin assigns.

The shell. Every signed-in screen sits inside one frame: the top bar, the
navigation rail and the content area. The design language is applied and
its tokens are the only source of colour, spacing and type.

## Out of scope

No domain. There is no record, no field, no module and no document. The
first client milestone cuts those.

No model call. There is no gateway, no key and no provider.

No connection to any client system. No access path has been exercised and
no owner has been named.

## Guardrails

Guardrail 6 binds this milestone. The stack constrains everything after it,
so it is written as [ADR-001](../decisions/adr-001-the-stack.md) rather than
left in a commit message.

Guardrail 9 does not bind it. This is product code and the code space is
open, because the template ships built.

Guardrail 15 binds every screen it adds. An empty project list renders as
an empty list that says so, never as a placeholder row.

## Rests on

[ADR-001](../decisions/adr-001-the-stack.md). It decides the three
repositories, the Django backend and the React frontend. Its decision 9 is
the branch rule: one name in both code repositories, and the backend merges
first.

## Exit criteria

1. Sign-in works, and a wrong password is refused.
2. A signed-out request to a protected endpoint is refused with a 401.
3. A super admin creates a person and a project.
4. A project shows its owner, and a super admin assigns one.
5. `core/` imports nothing from a domain, and a test proves it.
6. Both suites pass, and `openapi.json` matches the generated client.

## Walk this

The manual pass. Do it in a browser, in this order. `/fde:smoke-test`
automates this list later; until then it is the gate.

1. Open the application signed out. You land on sign-in.
2. Sign in with a wrong password. It is refused and says so.
3. Sign in correctly. You reach the projects list and it is empty.
4. As a super admin, open Users and create a person.
5. Create a project. It appears in the list.
6. Open the project and assign the new person as owner.
7. Reopen the project. The owner's name is shown.
8. Sign out. The projects list is no longer reachable.

## Risks and unconfirmed

Where this runs is undecided, and so is what it authenticates against.
Both are questions for the client's IT owner, and neither has been asked.

This milestone is a horizontal layer and it proves nothing about the
domain. The first client milestone should carry a walking skeleton: one
real field, end to end, that the client would recognise.
