# Auth and roles

## What this layer is

This layer decides who is signed in and what they may see. A person signs in
with an email and a password and gets a session cookie. The server holds the
session, so signing out really ends it. Everyone belongs to an organisation.
One flag marks a super admin, who sees everything. Everyone else sees a
project only if they are a member of it, and membership carries a role. A
person who is not on a project is told the project does not exist. They are
not told that they may not see it. So nobody learns what work is going on by
guessing at addresses. The auth code knows nothing about the client's own
domain, and a test keeps it that way.

## The rules

1. A session cookie is the credential, and the session store is server-side.
2. Signing out deletes the stored session, so a cookie captured beforehand
   stops working.
3. Every unsafe request carries a CSRF token that the client reads from a
   cookie the server set.
4. One gate answers 401 for every route that needs a session.
5. Sign-in and sign-out are the only routes exempt from that gate.
6. A 401 is a 401 with a body, never a redirect to a sign-in page.
7. An unknown email and a wrong password give the same answer and take the
   same time.
8. Every user belongs to an organisation, and one boolean flag marks a super
   admin.
9. Access to a project is a membership row carrying a role, and `owner` is
   the only role shipped.
10. A role is a value in a row, so a new role is a row rather than a
    migration.
11. A person who is not a member of a project gets 404, never 403.
12. A super admin sees every project, whatever the membership rows say.
13. The first super admin is made by a seed command that reads its password
    from the environment.
14. The auth layer imports nothing from any domain, and reaches a domain's
    models by name rather than by import.
15. A test reads the auth layer's source and fails the build on an import of
    a domain.

## The checklist

1. Does signing in set a cookie rather than return a token to store?
   `curl -i -X POST <base>/api/sign-in` and look at `Set-Cookie`.
2. Is the session store server-side, and does signing out delete the row?
   Read the sign-out handler and the session settings.
3. Does an unsafe request without the CSRF token get refused?
   `curl -i -X POST <base>/api/sign-out -b <session cookie>` with no token
   header.
4. Does a protected route with no session answer 401 with a body, and not a
   redirect? `curl -i <base>/api/session`.
5. Are sign-in and sign-out the only routes exempt from the gate? Read the
   route list and the permission on each view. Sign-out is exempt because
   ending a session nobody has is not an error.
6. Do a wrong password and an unknown email give the same body, the same
   status and the same timing? Call sign-in ten times with each and compare
   the bodies, then compare the median of
   `curl -o /dev/null -s -w '%{time_total}\n' ...` for the two.
7. Does the user table carry an organisation and one super-admin flag? Read
   the user model or the first migration.
8. Is project access a membership row with a role column? Read the
   membership model, and check the unique constraint on person, project and
   role.
9. Does a signed-in non-member asking for a project get 404 rather than 403?
   Read the gate function, and run the test that pins it.
10. Does the gate short-circuit for a super admin? Read the same function.
11. Is there a seed command, and does it read the password from the
    environment rather than from an argument or a file? Read the command.
12. Does a search of the auth layer find no import of a domain package?
    `grep -rn "domains" <auth layer>`.
13. Does a test fail the build when the auth layer imports a domain? Run the
    layering test and read what it asserts.

## Reference

The files under `auth-and-roles/reference/` come from `fde-be`, the Django
and DRF reference implementation. Django supplies the session, the password
hashing and the CSRF middleware. So the code here is mostly the decisions on
top of them. Another stack writes different code for the same rules.

- `rbac.py` — the gate. It refuses with 404 rather than 403, and it
  short-circuits for a super admin. It reaches the domain's models by
  settings label, so the auth layer imports no domain. Django.
- `test_layering.py` — the test that enforces rule 15. It parses the source
  tree rather than importing it, so an import inside a function is caught
  too. pytest, Django.
- `models.md` — the four tables and their fields. They are written out
  rather than shown as code, so any stack can build the same shape.
