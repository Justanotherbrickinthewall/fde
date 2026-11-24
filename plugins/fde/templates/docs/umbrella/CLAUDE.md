# fde-os

This directory is the umbrella. Claude is always started here, and every `just`
recipe runs from here.

## The three repositories and one folder

`fde-docs` is the engagement record. It holds the raw material, the wiki and
the project plan.

`fde-be` is the Django API. It holds the domain code, the Celery worker and
`openapi.json`.

`fde-fe` is the React frontend. Its API client is generated from that
`openapi.json`.

`my-sessions` holds the session records, the working memory each session
leaves behind. It is a plain folder with no git, kept on this machine only.
It is not the source of truth, and `fde-docs` never links to it.

Each repository has its own `CLAUDE.md`, and that is where its rules live. Read
the one for the repository you are about to change. This file only says where
things are.

## Rename the three before the engagement starts

The template ships with these names and it runs as cloned. `/fde:init
<slug>` renames the three folders to `<slug>-docs`, `<slug>-be` and
`<slug>-fe`. It replaces every occurrence of the old names in every text
file, sets the compose project name to `<slug>`, runs `bootstrap.sh` from
the plugin, and writes `.engagement` at this root. It refuses to run
twice.

## This directory is untracked on purpose

It holds no `.git` and it never will. Do not run `git init` here.

`CLAUDE.md`, `justfile` and `docker-compose.yml` sit here as links. The real
files are carried in `fde-docs/umbrella/`, and `bootstrap.sh`, now part of the
`fde` plugin, links them into this root when `/fde:init` runs. The skills are
not linked in here at all. Each teammate installs the plugin once, per user,
by following the plugin's README.
`settings.local.json` stays out, because it is this machine's own.

`docker-compose.yml` is the whole stack. It `include:`s
`fde-be/docker-compose.yml`, `fde-be/deploy/proxy.yml` and
`fde-fe/docker-compose.yml`, and it owns nothing else. Everything it
names is tracked in one repository or another.

## Where commands run

The engagement commands are the skills in the `fde` plugin, run as
`/fde:<name>`. `/fde:fdc-session` keeps the record true and `/fde:aie-session`
builds a milestone, and `fde-docs/CLAUDE.md` holds the table saying whose
each one is. Run them from `fde-docs/`, because the skills resolve their
paths from there.

Everything else runs from here. `just setup` installs both repositories.
`just up` starts the whole stack. `just --list` shows the rest. The ports
come from `.env`, and `.env.example` lists them with their defaults.

## Branches

`fde-docs` is always on `main` and it never branches.

A build opens a branch in `fde-be` and in `fde-fe`, named for the
milestone id. The name is the same in both. The backend merges first, so open a
frontend pull request only once the backend one it needs has merged.

## One agent per checkout

Two agents on one repository means two worktrees. Never share a working tree,
and never share a test database.

Never run `git stash`, `git checkout .` or `git reset --hard`.

## Where we are

Nothing has started. m01 ships built: a person signs in, a super admin adds
people, and projects exist behind the shell. The record is empty and waiting
for its first `/fde:fdc-session`.

The milestone index is `fde-docs/project/milestones/index.md`. The stack is
decided in `fde-docs/project/decisions/adr-001-the-stack.md`.
