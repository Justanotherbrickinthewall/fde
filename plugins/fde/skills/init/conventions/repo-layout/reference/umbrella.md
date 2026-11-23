# The umbrella

## The tree

```
<slug>/                        the umbrella. No .git, and it never gets one.
├── .engagement                who this engagement is, and what it runs on.
├── CLAUDE.md                  where things are. No rules of its own.
├── justfile                   the commands that run the whole stack.
├── docker-compose.yml         includes each repository's own compose file.
├── .claude/                   settings and any local hooks.
│
├── <slug>-docs/               the record. A repository. Always on main.
│   ├── raw/                   what the client sent. Immutable.
│   ├── wiki/                  what we derived from it.
│   ├── project/               charter, milestones, decisions, open questions.
│   └── setup/                 guardrails, conventions, design, glossary.
│
├── <slug>-be/                 the backend. A repository. Branches per milestone.
│   ├── src/                   the application.
│   ├── tests/
│   ├── bin/                   check-openapi, no-secrets.
│   ├── model-tasks/           one TOML file per model task, if adopted.
│   ├── openapi.json           committed, and checked against the code.
│   └── CLAUDE.md              this repository's rules.
│
├── <slug>-fe/                 the frontend. A repository. Same branch names.
│   ├── packages/ui/           components, DESIGN.md and the token file.
│   ├── apps/web/              the screens. Composes, never styles.
│   ├── src/generated/         the API client, built from openapi.json.
│   └── CLAUDE.md              this repository's rules.
│
└── my-sessions/               session records. No .git. Committed nowhere.
```

The three repositories are siblings. The umbrella is their parent and it is
not a repository itself.

## Why the umbrella is untracked

Everything it holds is either generated, linked in from the record
repository, or three lines long. `docker-compose.yml` only includes each
repository's own compose file and adds a proxy. `.claude/skills` is a
symlink. So the umbrella costs nothing to lose and would cost a fourth
repository to keep.

Never run `git init` here.

## Why the record does not branch

The record changes every time somebody talks to the client. The application
changes on a milestone branch. Put both on one branch and planning the next
milestone lands inside the current milestone's history, which is a cost paid
every week.

## Why sessions sit outside every repository

A session record is working memory. It is honest about what broke and what
was tried. That is exactly what should not sit in a repository the client
may one day read. The record repository never links to a session file.

## `.engagement`

One file at the umbrella root. Every skill reads it, so no skill carries a
fixed repository name or a home path of its own. It is plain text, one
`key=value` line per field, with no quoting and no sections. It carries seven
fields.

| Field | What it holds |
| --- | --- |
| `slug` | The engagement's short id. Every folder is named from it. |
| `docs` | The record repository's folder name, relative to the umbrella. |
| `be` | The backend repository's folder name. Empty until one exists. |
| `fe` | The frontend repository's folder name. Empty until one exists. |
| `stack` | What ADR-001 picked. Empty until it is decided. |
| `plugin_version` | The `fde` plugin version this engagement is pinned to. |
| `plugin_root` | The plugin's install directory when `fde:init` ran. |

`fde:init` writes it once, in phase 1. Every other skill reads it before
doing anything else. The version is pinned and bumped on purpose, so a skill
never changes under a running milestone. `plugin_root` is the same value
`${CLAUDE_PLUGIN_ROOT}` resolves to at run time.

`be` or `fe` may be empty, but the line is still there. A skill that finds an
empty `be` knows there is no backend. A missing line only tells it the file
is old.

`plugins/fde/ENGAGEMENT.md` in the plugin is the authority on this format.
Read it if this table and the file on disk disagree.

## How a skill finds the umbrella

The umbrella is the nearest ancestor of the working directory that holds an
`.engagement` file. A skill walks upward from wherever it was invoked until
it finds one, the same way it would look for a `.git` directory.

So a skill works from a worktree, from inside a repository, or from the
umbrella root, and none of them has to be named anywhere.

## Example

```
slug=acme
docs=acme-docs
be=acme-be
fe=acme-fe
stack=django-react
plugin_version=0.1.0
plugin_root=/Users/you/.claude/plugins/cache/fde/fde/0.1.0
```
