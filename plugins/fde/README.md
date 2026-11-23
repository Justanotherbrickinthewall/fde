# fde

fde is a Claude Code plugin that packages the forward deployed engineering method as twelve skills. Forward deployed engineering means engineers work beside the client, against the client's own documents and screens. They keep a written record of what they learn.

An engagement is one piece of that work for one client, from the first call to delivery. The plugin is for a team that runs engagements with Claude Code. It gives that team one sequence of sessions, and each session leaves a record behind. No application code lives here, because every engagement owns its own stack in its own repositories.

## The method has two roles, and each skill belongs to one or both

The method splits the work between a forward deployed consultant (FDC) and an AI engineer (AIE).

The FDC keeps the engagement record true and cuts the milestones. The FDC's output is the record, not a branch. Only the FDC marks a milestone `ready`, and an FDC session never touches the code repositories. The target is for the FDC to stay two milestones ahead of the AIE.

The AIE builds a `ready` milestone in the code repositories. The AIE walks the result in a browser, fixes what the walk finds and merges the branch. Only the AIE session sets a milestone to `building` and `built`.

| Skill | Role |
|---|---|
| `fde:fdc-session` | FDC |
| `fde:aie-session` | AIE |
| `fde:brain-dump` | Both |
| `fde:ux-log` | Both |
| `fde:init`, `fde:file`, `fde:prototype`, `fde:smoke-test`, `fde:bug-hunt`, `fde:qa-session`, `fde:session-sync`, `fde:explain` | The skill files name no role |

`fde:init` does stand in for the FDC once, because it marks the first milestone `ready` on day one before any record exists.

## Twelve skills cover an engagement from first call to delivery

The table follows one engagement in order. The second column is the skill to run at that point.

| When | Skill | What it leaves behind |
|---|---|---|
| Day one, with an empty folder | `fde:init` | The umbrella, the docs repository, `.engagement`, a conventions table and milestone m01 marked `ready` |
| Client documents arrive | `fde:file` | A copy in `raw/`, a ledger row with a tier, a page-anchored specimen store and a wiki |
| A call or a conversation happens | `fde:brain-dump` | Dated, tagged, sourced entries in `project/brain-dumps/dN-<slug>.md` |
| Material needs to reach the record | `fde:fdc-session` | A `digest.md`, record changes with dated notes, and the questions for the next meeting |
| The client needs something to react to | `fde:prototype` | One HTML file in `project/prototypes/` and a brief marked `complete` |
| A milestone is `ready` | `fde:aie-session` | A merged branch, a walked scenario store and a milestone marked `built` |
| An interface problem shows up mid-build | `fde:ux-log` | One entry in `project/ux-log.md` |
| Before a delivery | `fde:smoke-test` | A `bugs-and-improvements.md` file in a session folder |
| A pile of bugs has built up | `fde:bug-hunt` | A tracker and a merged `hardening/<name>` branch |
| After the smoke test and the bug hunt, before a delivery | `fde:qa-session` | `test-cases.md`, `results.md`, a findings file, and checks merged from `qa/<slug>` |
| Any time | `fde:session-sync` | Session folders for chats nobody scaffolded |
| Any time | `fde:explain` | A plain-English explanation in chat |

The order is the usual one, and the early steps repeat. A new document or call sends the FDC back to `fde:file`, `fde:brain-dump` and `fde:fdc-session`. `fde:ux-log` and `fde:brain-dump` run beside a build. The smoke test, the bug hunt and `fde:qa-session` follow it, in that order, before a delivery. `fde:session-sync` and `fde:explain` can run at any point, in any project.

## The skills

### fde:init starts the engagement

It makes the umbrella folder, the docs repository and any code repositories, writes `.engagement`, and walks the four conventions one at a time. Run it once per engagement, on day one, before any other fde command.

```
/fde:init <slug>
```

The slug is lowercase letters, digits and dashes. If you omit it, phase 1 asks. It writes `<slug>-docs`, the code repositories you ask for, `.engagement`, `my-sessions/`, `setup/conventions.md` and a rewritten m01 and ADR-001. It never writes application code.

### fde:file puts client material into the wiki

It copies each document into `raw/` with a ledger row and an authority tier. It builds a page-anchored specimen store, then builds the knowledge graph from that store. Run it whenever material arrives or a source changes.

The first two jobs are the cheap layer, and the graph is the expensive layer. After the cheap layer it asks once whether to run the expensive one now.

```
/fde:file raw/docs/handbook.pdf
/fde:file raw/docs/
/fde:file
/fde:file --investigate raw/docs/handbook.pdf
/fde:file --app <app> raw/other/brief.pdf
```

The flags are `--afk`, `--hitl`, `--investigate` and `--app <app>`. With no argument it reconciles `raw/` against `raw/ledger.md` and files what is missing. It writes `raw/`, `raw/ledger.md` and `wiki/`, plus the open-question rows a superseded document raises. It never alters `raw/`, which is immutable.

### fde:brain-dump records what was heard

It splits a conversation, a transcript or a stream of thought into single entries. Each entry has one tag (`pain`, `idea`, `constraint`, `fact` or `question`), a source and the speaker's own words. Use it for raw notes about a delivery.

```
/fde:brain-dump
```

The file documents no flags. It appends to `project/brain-dumps/dN-<slug>.md` and mirrors each question into `project/open-questions.md`. It has no go-ahead step, so it writes first and reports the line numbers afterwards. It never writes `wiki/`, and it never rewrites an entry.

### fde:fdc-session gets what arrived into the record

It reads what arrived and the state of the record, splits the material, confirms the split with you and grills you for holes. Then it writes the record, lints it, and closes with the questions for the next meeting. Use it when a transcript, a document, brain dumps or your own research must reach the record.

```
/fde:fdc-session <what arrived> <detail>
/fde:fdc-session raw/meetings/Meeting3-120926.md third meeting
/fde:fdc-session research the regulator's submission rules
```

The first argument can be a path in `raw/`, a transcript, `brain dumps`, `research` or nothing. The only flag is `--<method>`, and `--grill` is the default. Phases 0 to 4 write to `my-sessions`, phases 5 and 6 write to `<docs>`, and phase 7 writes to `my-sessions`. It never touches the code repositories, and the orchestrator never edits the record inline.

### fde:prototype builds one clickable demonstrator

It takes one disposable HTML file from a brief, a delivery, an idea or an existing screen to a version you call done. Use it when the client needs something to click. A prototype attaches to a delivery, never to a milestone.

```
/fde:prototype
```

The skill has no flag and no second mode. It writes `project/prototypes/<slug>.html`, and `project/artifacts/prototype-brief-<slug>.md` at close. It also adds a row to `project/artifacts/index.md`. The file is never promoted into a code repository.

### fde:aie-session builds one piece of work to a merged branch

It scaffolds a session and scopes the work in plain words. It reconciles the milestone, then hands design and plan to a method pack. It builds on a branch, walks the result, fixes what the walk finds and merges. A milestone is optional, but if you name one it must read `ready`.

```
/fde:aie-session [<milestone>] <detail> [--afk]
```

The flags are `--afk` and `--<method>`. `--superpowers` is the default and `--quick` picks the lighter pack. Phases 0 to 4 write to `my-sessions`, phase 5 writes to `<be>` and `<fe>`, and phases 6 to 8 write to `my-sessions` and `<docs>`. It never builds inline, and it never merges into `release`.

### fde:ux-log parks an interface problem

It appends one dated, tagged, sourced entry to `project/ux-log.md` so the build carries on. Use it for a screen that confuses or a step that takes too many clicks. Tags are `pain` and `idea`.

```
/fde:ux-log
/fde:ux-log done <what>
```

It stops for your go-ahead after it splits what you gave it. It routes a defect, a client question or a feature request elsewhere and says where. It never fixes anything.

### fde:smoke-test walks the running application with a person

It brings the stack up, proves the login, then gives one scenario per message and records each finding as it arrives. Use it before a delivery, or to walk a milestone.

```
/fde:smoke-test
```

The file documents no flags. It writes `bugs-and-improvements.md` in a `smoke` session folder under `my-sessions`. Each finding has a kind (`bug`, `improvement`, `constraint` or `decision`) and a status. It never fixes a finding, except one that blocks the rest of the walk, and then only if the person says yes.

### fde:bug-hunt takes a pile of bugs to a merged branch

The orchestrator holds a tracker, diagnoses each bug and sends one fix subagent per bug. Use it when bugs cross the backend, the worker and the frontend. A hunt earns its setup at about ten bugs, and one bug is fixed where you are.

```
/fde:bug-hunt <name>
```

The name gives the branch and the folder, so a hunt named `d1` branches `hardening/d1`. It writes `tracker.md` and `notes.md` in a `hardening` session folder, and commits fixes to `hardening/<name>`. It never merges into the base branch without your word on the day of the merge.

### fde:qa-session checks a built feature against what was agreed

It answers one question: does the built feature match what was agreed? It rebuilds the agreed facts from the record alone and turns them into test cases a person reviews. It then runs the approved ones through lanes side by side. Use it when a milestone is built and about to be delivered.

```
/fde:qa-session [<milestone>] <detail> [--afk] [--<lane> ...]
```

The flags are `--afk` and `--<lane>`. With no lane flag, every lane runs that has kept test cases and whose tool is installed. A lane flag runs only the lanes named. A milestone is optional, and the skill never refuses to start for want of one.

The loop has six steps. Phase 1 understands, 2 asks, 3 reviews, 5 executes, 6 validates and 7 improves. Phase 3 is the gate where a person decides which test cases stand. Phases 0, 4 and 8 scaffold, stand up the target and close.

It writes `test-plan.md`, `test-cases.md`, `results.md`, `evidence/<lane>/` and `bugs-and-improvements.md` in a `qa` session folder. It merges the checks from `qa/<slug>` at close. It never fixes product code, never changes a milestone's status, and never tests production.

### fde:session-sync writes up chats nobody scaffolded

It reads Claude Code transcripts for the engagement, skips trivial ones and writes a session folder for each substantive one. A ledger at `my-sessions/.harvest-ledger.json` records what it has already processed.

```
/fde:session-sync
```

The file documents no flags. Re-running with no new chats writes nothing. It never overwrites a `notes.md` that a person wrote, and nothing runs it automatically.

### fde:explain explains one complicated thing in chat

It explains a design, a process, a decision, a confusing reply or a whole document, in plain English and in order. For a document, it lets you read, question and approve without opening the file.

```
/fde:explain
```

It reads no engagement file and works in any project. It writes to chat and edits a document only when you ask for a change. It never turns later replies into explainers.

## A session is a folder with a phase marker and gates

Most skills run as a session. A session is a folder at `my-sessions/<type>/<DDMMYY>-<slug>/`, made by `sessions.py new --type <type> --slug <slug>`. The types the skills use are `aie`, `fdc`, `smoke`, `qa`, `misc`, `prototype` and `hardening`.

`my-sessions` sits beside the repositories and has no git. `fde:init` links it to `~/.claude-shared/records/<slug>/` when that folder exists. The record in `<docs>` never links to a session.

Every folder holds a `notes.md`. Its front fields include `Status` (`active`, `paused` or `done`), `Summary` and `Owes`. Each skill adds its own, such as `Milestone`, `Method`, `Flags`, `Repositories` and `Branch` for `fde:aie-session`. A session closes with `sessions.py check <folder>` and then `sessions.py index --write`.

The `Phase:` field in `notes.md` is the phase marker, and `▶ Resume here` names the single next action. A skill updates both the moment a phase ends. Start the skill again and it reads the marker and carries on, so a closed chat loses nothing.

A gate is a point where a person reads before the work goes on. The skills put them here:

1. `fde:fdc-session` shows the digest for confirmation before the grill, and shows the change before it reaches the record.
2. `fde:aie-session` waits for you to approve `spec.md`, then `plan.md`, then asks "Shall I start the build?".
3. `fde:aie-session` asks whether to re-walk before it closes.
4. `fde:file` stops at each of four checkpoints in the expensive layer unless you pass `--afk`.
5. `fde:ux-log` stops after it splits your input.
6. `fde:bug-hunt` asks again on the day of the merge and names the deployment.
7. `fde:qa-session` asks you to decide which test cases stand before anything runs. Under `--afk` it records that no person reviewed them.

`--afk` means the user is away and nothing waits on them. `fde:aie-session`, `fde:file` and `fde:qa-session` take it. The rule that says how an away session answers its own questions lives in the user's global `CLAUDE.md`, not in this plugin. In `fde:aie-session`, `--afk` changes who answers a question and never how the walk runs.

The orchestrator decides, and subagents do the work. The orchestrator never builds inline, never edits the record inline and never drives a browser. Every dispatch names its model, and each subagent is told the same rule for its own subagents. A subagent's report is evidence of what it believes, so a load-bearing claim gets checked against the tree.

## Method packs swap how the work is done

A method pack is one file that owns the middle phases of a session. The skill around it stays the same, so a new way of working costs one file. Two skills have packs.

| Skill | Pack | Phases it owns | Hands work to |
|---|---|---|---|
| `fde:aie-session` | `superpowers` (default) | 3 design, 4 plan, 5 build | The superpowers skills `brainstorming`, `writing-plans`, `subagent-driven-development` and `finishing-a-development-branch` |
| `fde:aie-session` | `quick` | 3 design, 4 plan, 5 build | Claude plan mode, then one implementer subagent per task |
| `fde:fdc-session` | `grill` (default) | 2 digest, 3 confirm, 4 grill, 5 update | `fde:file` for client documents |

A pack's file lives in the skill's `methods/` folder. `--<method>` picks a pack other than the default, and only if `methods/<method>.md` exists. Any other flag is an error, and the skill lists what exists and stops. `grill` is modelled on the superpowers `brainstorming` skill but does not call it.

Two rules bind every `fde:aie-session` pack. A pack never builds inline and never chooses where the work lands. A pack never opens a branch or a worktree, because the orchestrator owns those. A `fde:fdc-session` pack writes nothing to the record before phase 5, and it never guesses.

## QA lanes split a test session by tool, and each lane writes and runs its own checks

A QA lane is one tool family that proposes test cases for its surface, writes the checks and runs them. Lanes live in `skills/qa-session/lanes/`, and `lanes/README.md` is the contract. A fifth lane is a fifth file with its own `--<lane>` flag.

| Lane | Flag | Tool | What it checks | Where its checks live |
|---|---|---|---|---|
| `postman` | `--postman` | The Postman plugin's skills | The API: status codes, schemas, validation, access by identity, error handling | `<be>/postman/` on `qa/<slug>` |
| `playwright` | `--playwright` | The Playwright Test Agents and `npx playwright test` | The interface, in a browser | `.spec.ts` files in `<fe>` on `qa/<slug>` |
| `anthropic` | `--anthropic` | Claude Code's `/code-review`, `/security-review`, `/verify` and `/run`, plus plugins | Review of the code and the running app | Nothing in a code repository; evidence stays in the session folder |
| `sql` | `--sql` | The backend's own database command | Stored data, with `SELECT` statements only | `<session>/sql/<TC-id>.sql` |

A lane writes one check per kept test case and names it with the test case id. The expected result comes from the test case and never from what the application does today. Every priority 1 check must be shown failing once, or it is reported as `weak`.

A lane reports evidence but names no root cause, edits no product code and opens no branch. Nothing leaves the machine without the person's yes in chat.

Two things are called a lane. In `fde:aie-session` a lane is a build in its own worktree, described in `skills/aie-session/lanes.md`. In `fde:qa-session` a lane is a tool family.

## The umbrella holds three repositories and a session folder

The umbrella is one folder that holds everything and is not itself a repository. Every skill finds it by walking up from the working directory until it meets a `.engagement` file.

The umbrella holds:

1. `<slug>-docs`, the record repository. It stays on `main` and never branches.
2. `<slug>-be`, the backend, if one exists yet.
3. `<slug>-fe`, the frontend, if one exists yet.
4. `my-sessions`, the session folder.

`.engagement` is plain text with one `key=value` line per field. Its fields are `slug`, `docs`, `be`, `fe`, `stack`, `plugin_version` and `plugin_root`. Six more are empty for a one-app engagement: `apps`, `record`, `merge_into`, `integration`, `release` and `worktree`. [`ENGAGEMENT.md`](ENGAGEMENT.md) holds the exact format and the two writes allowed after init.

The record lives inside the docs repository.

| Folder | Holds |
|---|---|
| `raw/` | Client material as exchanged, with `raw/ledger.md` giving each file a tier: `statutory`, `artefact`, `stated` or `ours` |
| `wiki/` | The specimen store and the knowledge graph that `fde:file` builds |
| `project/` | The charter, milestones, open questions, deliveries, brain dumps, the UX log, prototypes and ADRs |
| `setup/` | The guardrails, the conventions table, and the rules for filing and planning |
| `backlog/tasks/` | One file per plan task from `fde:aie-session` |
| `tests/scenarios/` | The scenario store that the walk reads and updates |

A milestone is a file in `project/milestones/` with a status of `draft`, `ready`, `building`, `built` or `dropped`. It is the handoff between the two roles.

Guardrails live in `setup/guardrails.md`, and the skills cite them by number. A client guardrail comes from the client, the law or the contract, and the FDC owns it. A build guardrail is a suggestion the AIE may override with a dated note and a reason. Every guardrail names its source, and the record lint checks that line.

## Four conventions are adopted one at a time

`skills/init/conventions/` holds four conventions that `fde:init` offers in phases 2 to 5. Each is a spec, a checklist and a `reference/` folder of portable files. `fde:init` asks yes or no for each, never skips one, and records the answer in `setup/conventions.md`.

A yes copies the reference files into the matching repository, if it exists. A no is recorded with its reason.

- Design: one token file of CSS custom properties, with no hex colour or raw pixel size outside it.
- Auth and roles: a session cookie over a token, one 401 gate, project-scoped membership, and 404 over 403 for a non-member.
- Model gateway: keys only in the environment, one gateway module, and a refused call that renders visibly.
- Repo layout: three repositories in an umbrella, one branch per milestone, and the backend merges first.

Adopting a convention means its checklist becomes a gate. Phase 8 of `fde:aie-session` runs every adopted checklist against what merged, and a failing checklist blocks `built`. Where there is no repository yet, the files wait and the rules become part of m01's scope.

## Scripts

`scripts/` holds six files that skills call as `${CLAUDE_PLUGIN_ROOT}/scripts/<name>`. The plugin's folder is not the engagement's working directory. Where the variable is unset, a skill reads `plugin_root` from `.engagement`.

| Script | What it does |
|---|---|
| `scaffold.sh` | Builds the umbrella, the repositories, `.engagement` and `my-sessions`. Only `fde:init` calls it |
| `bootstrap.sh` | Links the umbrella's shared files to the copies in the docs repository, using relative links. `scaffold.sh` runs it |
| `lint_record.py` | Checks milestone status, `waits-on`, `delivery:`, the parts of a `ready` milestone, open-question owners, guardrail sources and unlinked pages |
| `check_links.py` | Fails on any relative link in the record that points at a missing file |
| `no-secrets` | A commit hook that refuses a staged OpenRouter key and nothing else |
| `test_check_links.py`, `test_lint_record.py` | Tests for the two checkers |

`lint_record.py` takes the docs root and an optional record root for an app. `check_links.py` takes the docs root. Both default to the working directory.

`skills/file/scripts/` holds the capture machinery that `fde:file` uses: `pdfspec.py`, `rtfgrid.py` and `coverage.py`. Per-document driver scripts are engagement work and live in `<docs>/scripts/`.

## What the plugin needs from outside this repository

The plugin cannot run on its own. Each item below sits outside it.

1. A docs template repository. `fde:init` builds `<slug>-docs` from it. The default is `PeopleEquation/fde-docs`, which is private. `scaffold.sh --docs-template` takes another, as `owner/repo` or a local path.
2. `gh`, signed in, when the docs template is written as `owner/repo`.
3. Optional reference stacks. `PeopleEquation/fde-be` is Django and DRF, and `PeopleEquation/fde-fe` is React and Vite. Both are private and neither is part of the method.
4. The `sessions` skill at `~/.claude/skills/sessions`. The session skills call its `scripts/sessions.py` to make, check and index session folders.
5. The superpowers skills, for the default `superpowers` pack.
6. Two voice files for `fde:explain`: `~/.claude-shared/VOICE.md` and `~/.claude-shared/registers/learner.md`.
7. The QA lanes' tools, each needed only if its lane runs. For `postman`, run `claude plugin marketplace add anthropics/claude-plugins-official` and then `claude plugin install postman@claude-plugins-official`. For `playwright`, `@playwright/test` must already be in the frontend. For the deeper scan in `anthropic`, run `/plugin install claude-security@claude-plugins-official` and then `/reload-plugins`. The `sql` lane needs no install.
8. Files in the docs template that the skills read by name: `setup/guardrails.md`, `setup/planning-rules.md`, `setup/filing-rules.md`, `setup/scoping-rules.md`, `setup/artifact-templates.md` and `project/brain-dumps/README.md`.

## Install and versions

The repository that holds this plugin is also a marketplace. Its root carries `.claude-plugin/marketplace.json`, which names the marketplace `people-equation` and lists one plugin, `fde`. The root README of the repository gives the real `<owner>/<repo>`.

The first route adds the marketplace, then installs the plugin.

```bash
claude plugin marketplace add <owner>/<repo>
```

```bash
claude plugin install fde@people-equation
```

On Claude Code 2.1.275 or later, one line does both.

```
/plugin install fde --marketplace <owner>/<repo>
```

The second route is for someone who edits the skills. Clone the repository and run `./install.sh` at its root, then restart Claude Code. The script links the plugin into `~/.claude/skills`, so an edit is live at once.

Use one route and never both. Both together list every skill twice.

`.engagement` records the version the engagement started on, as `plugin_version`. Do not pull mid-milestone, because a skill that changes under a running build invalidates the record it just wrote. The plugin is at version 0.1.0.

## Limits

These are the gaps the files show.

1. The numbered guardrails are defined in the docs template's `setup/guardrails.md`, not here. The skills cite them by number, and this repository cannot say what they contain. `lint_record.py` checks only that each live guardrail has a `Source:` line.
2. `fde:init` cannot run end to end without a docs template. `PeopleEquation/fde-docs` is private, so an outside engineer must supply their own and match the files in item 8 of the section above.
3. The `--afk` rule and the subagent-model rule live in the user's global `CLAUDE.md`. The plugin cites them and does not carry them.
4. `fde:qa-session` is new, and none of its four lanes has been run in a real session. Their commands come from the tools' own documents.
5. The `playwright` lane runs only if the frontend already uses `@playwright/test`. Adding a test framework is the person's decision, and under `--afk` the lane reports `not installed` and stops.
6. The `anthropic` lane's `webapp-testing` skill comes from `https://github.com/anthropics/skills`, and the lane file gives no install command for it.
7. The `sql` lane has no command of its own. It needs the backend's database command from its compose file, justfile or README, and reports blocked if it finds none.
8. Only one pack exists for `fde:fdc-session` and two for `fde:aie-session`.
9. The reference files for the conventions are partly stack-specific. The design test is written for Vitest, Tailwind and HeroUI. `rbac.py` and `test_layering.py` are Django and pytest. On another stack those rules become m01 scope.
10. `fde:smoke-test` assumes a `just up` command, a Docker Compose stack with a proxy on port 80, and Django management commands for the first account. `fde:bug-hunt` reads the project's `CLAUDE.md` for the start command.
11. `fde:file` marks the ledger row of a binary it cannot read, such as dwg, as blocked and needing conversion. `rtfgrid.py` depends on `textutil` output.
12. The checklist in the repo-layout convention says `.engagement` carries seven fields. `ENGAGEMENT.md` defines thirteen, so that checklist item is out of date.
13. The files do not say what `fde:explain` does when its voice files are missing.
14. Neither marketplace command has been run against this repository yet. `claude plugin validate` passes for the plugin and for the marketplace.
