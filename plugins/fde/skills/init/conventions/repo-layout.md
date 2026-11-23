# Repository layout

## What this layer is

An engagement has three repositories and they sit side by side in one folder.
One holds the record of the engagement, which changes every time somebody
talks to the client. One holds the backend and one holds the frontend, and
both change on a milestone branch. The folder holding all three is not itself
a repository, so nothing has to be committed twice. A milestone opens one
branch, and it carries the same name in the backend and in the frontend. The
backend merges first, because the frontend builds its API client from a file
the backend produces. One person or agent works in one checkout at a time, so
two of them never fight over the same files.

## The rules

1. An engagement has three repositories: the record, the backend and the
   frontend.
2. They sit as siblings inside an umbrella folder that has no git and never
   will.
3. The umbrella carries `.engagement`, the CLAUDE.md, the task runner and the
   compose file, and owns nothing else.
4. A fourth sibling holds the session records, and it is committed nowhere.
5. The record repository is always on its main branch and never branches.
6. A milestone opens one branch, named for the milestone id, and the name is
   identical in both code repositories.
7. The backend merges first, so a frontend pull request opens only once the
   backend one it needs has merged.
8. A delivery is tagged `dN-DDMMYY` in both code repositories.
9. Two agents on one repository means two worktrees, and a working tree or a
   test database is never shared.
10. `git stash`, `git checkout .` and `git reset --hard` are never run.
11. The API description file is committed in the backend, and the frontend's
    API client is generated from it and never hand-edited.
12. A check fails the build when the committed API description differs from
    what the code generates.
13. One origin serves the whole application, so the API path goes to the
    backend and everything else goes to the bundle.
14. Each repository's CLAUDE.md states the rules that govern it, and the
    umbrella's says only where things are.

## The checklist

1. Does the umbrella hold the three repositories as siblings, and does the
   umbrella itself have no `.git`? `ls -a` at the umbrella root.
2. Does `.engagement` sit at the umbrella root and carry all seven fields?
   `cat .engagement` and expect `slug`, `docs`, `be`, `fe`, `stack`,
   `plugin_version` and `plugin_root`, one `key=value` line each.
3. Does the session folder sit beside them, holding no `.git` and committed
   nowhere? `ls -a <umbrella>/my-sessions`.
4. Is the record repository on main, with no other branch? `git -C <docs>
   branch -a`.
5. Does each code repository the milestone touches carry a branch named for
   it, with the same name in both? `git -C <be> branch` and
   `git -C <fe> branch`. A milestone that touches one repository opens one
   branch, and the other repository having none is correct.
6. Did the backend branch merge before the frontend one? Compare the merge
   dates on the two pull requests. Skip this where only one repository moved.
7. Is the API description file committed at the backend root?
   `ls <be>/openapi.json` or the equivalent.
8. Does the check pass, so the committed file matches what the code
   generates? Run `bin/check-openapi`, or the equivalent, from the backend
   root.
9. Is the frontend's API client generated rather than hand-edited? Read the
   generator config and the header comment on the generated files.
10. Is the delivery tagged `dN-DDMMYY` in both code repositories?
    `git -C <be> tag` and `git -C <fe> tag`.
11. Does the edge serve one origin, with the API path to the backend? Read
    the proxy config in the compose stack.
12. Does each code repository's CLAUDE.md state the branch rule, the merge
    order and the one-agent rule? Read both files.
13. How many rules does the umbrella's CLAUDE.md state that a repository's
    own CLAUDE.md also states? Read both and count the duplicates. Expect
    zero, because a rule stated twice will disagree with itself.

## Reference

The files under `repo-layout/reference/` are written for this convention
rather than lifted. The tree they show is the `fde-os` shape: `fde-docs`,
`fde-be` on Django and `fde-fe` on React and Vite. The layout itself is
stack-neutral, and only the folder names inside each repository change.

- `umbrella.md` — the folder tree, what each sibling holds, the seven fields
  `.engagement` carries, and how a skill walks up to find the umbrella.
- `branch-rule.md` — one branch per milestone, the merge order and why it
  runs that way, the tag, and the one-agent-per-checkout rule.
