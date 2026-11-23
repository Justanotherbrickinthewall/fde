# The .engagement file

`.engagement` sits at the umbrella root, one level above every
repository in the engagement. It is plain text: one `key=value` line
per field, no quoting, no sections.

`fde:init` writes the file in phase 1, with `stack=` empty. Its phase 6
may set `stack=` where ADR-001 is accepted at init time, and it changes
no other line. Every other skill reads the file before doing anything
else, so no skill carries a fixed repository name or a home path of its
own.

Two writes are allowed after init, and only these two.
`fde:fdc-session`'s design check writes `stack=` when an ADR picks the
stack. Any skill may write `plugin_root=` when `${CLAUDE_PLUGIN_ROOT}`
is unset and the user gives the path. Nothing else edits the file once
init has finished.

## Fields

- `slug` — the engagement's short id, the same one the docs repository
  is named after.
- `docs` — the docs repository's folder name, relative to the
  umbrella.
- `be` — the backend repository's folder name, relative to the
  umbrella. Empty when there is no backend yet.
- `fe` — the frontend repository's folder name, relative to the
  umbrella. Empty when there is no frontend yet.
- `stack` — the stack ADR-001 picked, once it has been decided. Empty
  until then.
- `plugin_version` — the fde plugin version this engagement is pinned
  to. A skill bumps this on purpose; it never changes on its own.
- `plugin_root` — the plugin's own folder at the time `fde:init` ran,
  the same value `${CLAUDE_PLUGIN_ROOT}` resolves to at run time.
  Normally `~/.claude/skills/fde`, which is a link into the clone of
  this repository.

- `apps` — the apps in the engagement, comma-separated. When it is set,
  a skill resolves the app first. Empty for a one-app engagement.
- `record` — the record's path inside `<docs>`, with `<app>` standing for
  the app. Empty means the `<docs>` root. `$REC` in a skill is
  `<docs>/<record>` with the app filled in.
- `merge_into` — where a milestone branch merges, with `<app>` filled in.
  Empty means `main`.
- `integration` — the branch the app branch merges up into, such as
  `develop`. Empty means there is no such step.
- `release` — the branch that deploys. In away mode nothing touches it.
  Empty means there is none.
- `worktree` — the naming pattern for a worktree beside its repository.
  Empty means the skill picks the name.

`be` or `fe` may be empty, but the line itself is still present. The six
keys from `apps` on are empty for a one-app engagement, and the skills
then behave as they did before the keys existed. Longer branching rules
stay in `<docs>/setup/branching.md`, which a skill reads when it exists.

## Where the umbrella is

The umbrella is the nearest ancestor of the working directory that
holds a `.engagement` file. A skill walks upward from wherever it is
invoked until it finds one, the same way it would look for a `.git`
directory.

## Example

```
slug=acme
docs=acme-docs
be=acme-be
fe=acme-fe
stack=django-react
plugin_version=0.1.0
plugin_root=~/.claude/skills/fde
apps=web,admin
record=apps/<app>
merge_into=development/<app>
integration=develop
release=main
worktree=<repo>-<id>
```
