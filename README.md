# fde

This repository is the public copy of the `fde` plugin, written at
People Equation. The plugin lives under `plugins/`, in one folder per
plugin, and today there is one.

`fde` is the forward deployed engineering method, packaged as skills a
pod installs once and runs on every engagement. It carries the method
and the shared conventions. It carries no application code, because
each engagement owns its own stack in its own repositories.

## Installing it

Clone this repository and run the install script.

```
git clone https://github.com/Justanotherbrickinthewall/fde.git
cd fde
./install.sh
```

Restart Claude Code. Every skill is then available as `/fde:<name>`.

The script links each plugin folder into `~/.claude/skills/`. Claude
Code loads any folder there that holds a `.claude-plugin/plugin.json`,
and it does that on its own at the start of a session. There is no
install command to type and no marketplace to add. Check it worked with
`claude plugin list`, which should show `fde@skills-dir` as loaded.

Keep the clone somewhere permanent, because the link points at it. To
remove a plugin, delete its link: `rm ~/.claude/skills/fde`.

## What the plugin needs that this repository does not carry

The plugin references several things that live outside this repository.
Without them, some skills stop at the point where they need the missing piece.

1. A docs template repository. `fde:init` defaults to
   `PeopleEquation/fde-docs`, which is private. `--docs-template` takes
   another `owner/repo` or a local path. The template must hold
   `setup/guardrails.md`, an `umbrella/` folder and a `skills/` folder.
   The skills cite numbered guardrails, such as "Guardrail 15", and the
   template's `setup/guardrails.md` defines them.
2. The reference stacks `PeopleEquation/fde-be` (Django and DRF) and
   `PeopleEquation/fde-fe` (React and Vite). Both are private and optional.
   `--be` and `--fe` each take a URL, a local path, `reference` or `none`.
   The word `reference` selects the matching private repository.
3. The `sessions` skill at `~/.claude/skills/sessions`. Several skills run
   `python3 ~/.claude/skills/sessions/scripts/sessions.py`, and `fdc-session`
   runs `wiki_lint.py` from the same place. That skill is not in this
   repository.
4. The superpowers plugin. The default `aie-session` method uses its
   `brainstorming` and `writing-plans` skills.
5. Two voice files for `fde:explain`: `~/.claude-shared/VOICE.md` and
   `~/.claude-shared/registers/learner.md`.

## Access

This repository is public, so anyone can clone it. The docs template and
the two reference stacks above are private. Pass your own with
`--docs-template`, `--be` and `--fe`, or the skills that need them will fail.

## Updating

Run `git pull` in the clone and restart Claude Code. The links point at
the clone, so every plugin updates at once.

The clone is a working copy, not a cache. An engineer who improves a
skill mid-engagement edits it in the clone, sees the change on the next
session, and pushes it when it has proved itself. That is the reason
this route beats a published package while the method is still being
written.

## Pinning a version

An engagement records the version it started on in `.engagement` at the
umbrella root, as `plugin_version`. Do not pull mid-milestone. A skill
that changes under a running build is a skill that invalidates the
record it just wrote.

This public copy carries no release tags yet. The version is the one in
`plugins/fde/.claude-plugin/plugin.json`. To put an engagement back on the
version it started on, check out the commit that holds that version.

## Adding a plugin

Make a folder under `plugins/`, give it a `.claude-plugin/plugin.json`
with at least a `name`, and add one row to
`.claude-plugin/marketplace.json`. Then run `./install.sh` again.

`claude plugin validate ./plugins/<name>` checks the folder before you
push it.

The `marketplace.json` file is the catalogue of what lives here. It also
lets anyone who prefers it add this repository as a Claude Code
marketplace, but that is not the route these instructions take.

## The fde plugin

The plugin lives at `plugins/fde`. Its own README,
[`plugins/fde/README.md`](plugins/fde/README.md), lists its skills, its
conventions and its scripts.
