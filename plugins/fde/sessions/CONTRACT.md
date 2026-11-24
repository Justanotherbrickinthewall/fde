# The session contract

A session is one piece of work with a folder and a `notes.md`. Every session type follows the same contract. This file states it, and the session types come last.

`SESSIONS` below means `${CLAUDE_PLUGIN_ROOT}/sessions`. The script is `SESSIONS/scripts/sessions.py`. It uses only the Python standard library and writes only inside the project's `my-sessions/` folder.

## Where a session lives

The folder is `<root>/my-sessions/<type folder>/<ddmmmyy>-<slug>/`. For example, `my-sessions/hardening/07nov26-auth-fixes/`.

The root is the folder you are in, when it holds `my-sessions/`. Failing that, it is the nearest folder above you that holds `my-sessions/` beside a `CLAUDE.md` or an `.engagement` file. Failing that, it is the main checkout of the git repository you are in, or your own folder when there is no repository. It is never your home folder or `/`.

A skill may keep its own folder rule. Where it does, its rule wins.

The `my-sessions/` folder is private working space. The script writes a `.gitignore` that ignores everything inside it.

## The four commands

1. `python3 SESSIONS/scripts/sessions.py root` prints the sessions folder that applies. With `--init` it also creates the folder, with its `.gitignore` and a short `README.md`. With `--cwd D` it starts from `D`.
2. `python3 SESSIONS/scripts/sessions.py new --type <type> --slug <slug>` finds the root, makes the folder and fills `notes.md` from the template. It prints the folder path.
3. `python3 SESSIONS/scripts/sessions.py check <folder>` checks the notes. It prints each problem and exits 1 when there is one.
4. `python3 SESSIONS/scripts/sessions.py index --write` rebuilds `INDEX.md` in `my-sessions/`. Without `--write` it prints the index.

`new` also takes `--root`, `--title`, `--picks-up`, `--flat` and `--triggers`. `--flat` puts the folder directly under `my-sessions/`. `--picks-up` fills the `Picks up:` line.

To find earlier work, read `INDEX.md` in `my-sessions/`. Then search the `notes.md` files for the topic. Report the folder, its status and its `Owes:` line.

## The four moments

1. At start, read the skill for your type. Read `INDEX.md` when you continue earlier work or when an open hand-off exists.
2. During the session, keep `notes.md` current. Write each rejected approach as a `Rejected:` line.
3. At close, set `Status`, `Summary` and `Owes`, and put a marker on every decision. Run the `check` command. If it exits 1, fix the gap and run it again. Then run `index --write`.
4. To hand on, write the next session's job in `Owes:`. The next session names your folder in its `Picks up:` line. That closes the hand-off.

## The notes contract

`notes.md` opens with a title and a front block of bullets.

- `Folder:` is the absolute path.
- `Type:` is one of the types below.
- `Started:` and `Last updated:` are dates like 7 November 2026.
- `Phase:` is the phase name from the session's own skill.
- `Status:` is `active`, `paused` or `done`.
- `Flags:` is empty by default. A skill may write a flag there, such as `afk`. Old records have no line, and `check` accepts both.
- `Summary:` is one sentence of at most 200 characters.
- `Owes:` is what the next session must do, or `none`.
- `Picks up:` is the folder, relative to `my-sessions`, that this session continues, or `none`.

`Supersedes:` is optional. It names an older session whose conclusions this one replaces. A skill may add its own fields after `Picks up:`, such as `Milestone:` or `Branch:`.

The sections come in this order.

1. `## Resume here`, at most 10 lines.
2. `## Carry forward`. Write a rejected approach as `Rejected: <option>, because <reason>, <date>, <who>.`
3. `## Open items`.
4. `## Decisions`. End each bullet with one marker.
5. `## Findings`. Optional. Bug hunts, smoke tests and QA use it.
6. `## For <owner>`. The owner is the `SESSIONS_OWNER` environment variable. It defaults to the operating system user name.
7. `## Progress log`. Past 400 lines, move it to `progress-log.md` beside the notes.

The three decision markers mean this.

- `Graduated: <path>` says the decision already lives somewhere durable, such as an ADR, a skill or `CLAUDE.md`.
- `To wiki` says the decision belongs in the project's knowledge wiki.
- `Stays local` says the decision stays in these notes.

## What check enforces

The `check` command reports each of these.

- A front field from `Folder` to `Picks up`, other than `Flags`, is missing or empty.
- `Summary:` still reads "Not yet written."
- `Summary:` is longer than 200 characters.
- `Status:` is not `active`, `paused` or `done`.
- A `recurring` session has `Status: done`.
- A bullet under `## Decisions` has no marker.
- `## Resume here` is longer than 10 lines.

## The hand-off rule

An open hand-off is a notes file whose `Owes:` is not `none`, where no other notes file names its folder in `Picks up:`. The index lists these first.

Read the open hand-offs at the start of any session that continues work. Never leave `Owes:` as `none` when work remains. When you pick up a hand-off, put its folder in your `Picks up:` line.

## Rules

- Keep `notes.md` current as you go. Do not rebuild it from memory at close.
- Never write a secret into notes. Name where it lives instead.
- Do not edit another session's notes except to fix its `Status` or `Owes:`.

## Session types

The types are `fdc`, `aie`, `hardening`, `smoke`, `qa`, `prototype`, `misc` and `recurring`. Each section says what a session of that type reads, writes and hands on. When a type has its own skill, that skill adds its own phases and front fields. It still follows the notes contract and the close step.

### fdc

Skill: `fde:fdc-session`. Folder: `fdc/`.

1. Read the open hand-offs, the knowledge index and the raw ledger.
2. Write notes, record files, ADRs and milestone files during the session.
3. At close, set the marker on every decision. In the record lint phase, run the wiki lint beside the record lint where the wiki lint is installed.
4. Hand on by owing the AIE a ready milestone.

### aie

Skill: `fde:aie-session`. Folder: `aie/`.

1. Read the milestone, the FDC folder named in `INDEX.md` and the code-area pages.
2. Write notes and `Rejected:` lines. Commit on the branch.
3. At close, set the markers. Give each ADR a `Graduated:` path.
4. Hand on by owing a smoke test on the merged branch.

### hardening

Skill: `fde:bug-hunt`. Folder: `hardening/`.

1. Take the findings from the smoke or QA sessions that `INDEX.md` names. Read the code-area pages and any `Rejected:` lines before you touch code.
2. Copy each finding into a tracker in `## Findings`. Give each row an id, the symptom, the root cause once known, and a status of `open`, `fixing` or `fixed`.
3. Make a branch for the fixes. Diagnose a bug before you fix it. Fix one bug at a time and run the tests for the files you touched.
4. Record each root cause as a decision marked `To wiki`.
5. At close, every tracker row is `fixed` or has a reason it is not.
6. Hand on by owing a smoke rerun when a fix is risky.

### smoke

Skill: `fde:smoke-test`. Folder: `smoke/`.

1. Read the scenarios and the open hand-offs.
2. Write the result of each scenario in `## Findings`. Write bugs and improvements to `bugs-and-improvements.md`.
3. At close, list every failure.
4. Hand on by owing a bug hunt. Name the findings file in `Owes:`.

### qa

Skill: `fde:qa-session`. Folder: `qa/`. QA asks one question: does the built feature match what was agreed? It runs after the smoke test and the bug hunt, before a delivery. The session gets only the feature or milestone name.

1. Read only `INDEX.md`, the knowledge index and the milestone file. Rebuild the list of agreed facts from those alone. Do not read the builder's notes yet.
2. Write your list into `## Findings` before you go on.
3. Check the running system and the code against each fact. Collect evidence for each.
4. Write one Findings row per fact: the fact, its source, `pass` or `fail`, and the evidence.
5. Now read the builder's notes. Every fact you could not recover in step 1 is a memory gap. Log each one in Findings with the word `memory-gap`.
6. At close, record pass or fail per fact and list each memory gap.
7. Hand on by owing a bug hunt for each fail.

### prototype

Skill: `fde:prototype`. Folder: `prototypes/`.

1. Read the knowledge index.
2. Write notes as you build.
3. At close, record what you learnt as decisions marked `To wiki`.
4. Hand on by owing an FDC when the prototype becomes scope.

### misc

Ad-hoc chat has no skill. Write a `misc/` note only when the chat makes decisions.

1. Read `INDEX.md` for related work.
2. Write nothing unless a decision is made.
3. At close, put the decisions in a `misc/` note, each with a marker.
4. There is nothing to hand on.

### recurring

There is no skill. Start one with `new --type recurring --slug <slug> --triggers "a,b"`. Folder: `recurring/<slug>/`, with no date prefix.

A recurring record is one long-lived note for work that comes round again, such as a weekly review. It lists the commands that feed it in `Triggers:`. Starting it again reuses the same folder. Its Status stays `active` or `paused`, and `check` flags `done`.

### Skills with no session folder

File intake (`fde:file`) writes `raw/` and client facts and keeps its own ledger. It writes no session notes of its own.

## A machine with the full skill

A machine that has the full `sessions` skill at `~/.claude/skills/sessions` uses that skill's `SKILL.md` as the contract. On that machine the bundled script hands every command to that skill's script.
