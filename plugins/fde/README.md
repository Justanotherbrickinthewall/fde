# fde

The forward deployed engineering method, packaged as a Claude Code
plugin. No application code lives here, because every engagement owns
its own stack in its own repositories.

Install it by cloning this repository and running `./install.sh` at the
root. See the [repository README](../../README.md) for the detail.

## Skills

| Command | What it does |
|---|---|
| `/fde:init` | Starts an engagement: scaffold, conventions, m01. |
| `/fde:fdc-session` | Runs one forward deployed consultant session. |
| `/fde:aie-session` | Runs one milestone end to end, to a merged branch. |
| `/fde:file` | Files client material into the wiki. |
| `/fde:brain-dump` | Captures raw notes into dated, tagged entries. |
| `/fde:ux-log` | Logs an interface problem found mid-build. |
| `/fde:prototype` | Builds one clickable HTML demonstrator. |
| `/fde:smoke-test` | Walks the running application by hand. |
| `/fde:bug-hunt` | Takes a pile of bugs to a merged branch from one session. |
| `/fde:session-sync` | Harvests session transcripts into records. |
| `/fde:explain` | Explains one complicated thing, or a document, in plain English in chat. |

## The four conventions

`skills/init/conventions/` holds the four conventions `fde:init` can
adopt into an engagement:

- Design: one token file, CSS custom properties, nothing hex or raw
  pixel outside it.
- Auth and roles: session cookie over JWT, one 401 gate, project-scoped
  membership, 404 over 403 for a non-member.
- Model gateway: keys only in the environment, one gateway module, a
  refused call renders visibly.
- Repo layout: three repositories in an umbrella, one branch per
  milestone, backend merges first.

Each convention is a spec, a checklist, and a `reference/` folder of
portable files a skill can drop into a code repository.

## Scripts

`scripts/` holds `lint_record.py`, `check_links.py`, `bootstrap.sh` and
`no-secrets`. A skill calls one of these as
`${CLAUDE_PLUGIN_ROOT}/scripts/<name>`, because the plugin's folder is
not the engagement's working directory. Where that variable is unset, a
skill reads `plugin_root` from `.engagement` instead.

`lint_record.py` and `check_links.py` take the docs repository's root
as an optional argument, defaulting to the working directory, so a
skill can run either from inside that repository or point at it
explicitly.

## Finding the engagement

Every skill reads `.engagement`, at the umbrella root, before doing
anything else — the slug, the repository names, the stack and the
pinned plugin version. See [`ENGAGEMENT.md`](ENGAGEMENT.md) for the
file's exact format.
