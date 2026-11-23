# fde: Claude Code skills for forward deployed engineering

fde is a Claude Code plugin of twelve skills that run a forward deployed engineering engagement, from the first client call to a tested delivery.

Forward deployed engineering means an engineer works inside a client's business. The engineer finds the real problem, agrees what will be built, builds it and proves that it works.

Coding agents build well. On client work they fail in the parts around the build. The skills put a method around the agent. That method has a record of what was agreed, sessions that can be resumed, gates where a person decides, and evidence before anything is called done.

## Three files show the plugin in two minutes

1. [`plugins/fde/skills/aie-session/SKILL.md`](./plugins/fde/skills/aie-session/SKILL.md) shows one build session, from an empty folder to a merged branch.
2. [`plugins/fde/skills/qa-session/SKILL.md`](./plugins/fde/skills/qa-session/SKILL.md) shows the QA loop and the lanes that run its checks.
3. [`plugins/fde/README.md`](./plugins/fde/README.md) is the full reference for every skill, script and rule.

## Install takes two commands

```bash
claude plugin marketplace add Justanotherbrickinthewall/fde
```

```bash
claude plugin install fde@people-equation
```

The skills then appear as `/fde:<name>`. Run `/fde:init` to start an engagement.

## Why the skills exist

An agent fails in four ways on client work. Each failure below has a fix in the plugin.

### The agent builds what was said and misses what was agreed

A client says many things in a call. Some are wishes, some are constraints and some are corrections of an earlier call. An agent that builds from the last message builds a mix of them.

The fix is a record. [`fde:file`](./plugins/fde/skills/file/SKILL.md) and [`fde:brain-dump`](./plugins/fde/skills/brain-dump/SKILL.md) capture what arrived. [`fde:fdc-session`](./plugins/fde/skills/fdc-session/SKILL.md) turns it into a charter, milestones and open questions. [`fde:aie-session`](./plugins/fde/skills/aie-session/SKILL.md) builds only from that record and says the scope back first.

### What was agreed is lost between sessions

A chat closes and its context goes with it. The next session starts from memory, and memory drifts.

The fix is the session folder. Each session keeps a phase marker, notes that make it resumable, and gates. A skill that starts again reads the marker and carries on from the single next action.

A session is a folder at `my-sessions/<type>/<date>-<slug>/`. Its `notes.md` holds a status, a summary and what the session still owes. The gates are the points where a person reads before the work goes on. `fde:fdc-session` shows its digest before the grill, and `fde:aie-session` waits for approval of the spec and then the plan. It asks again before it starts the build.

### Done arrives without evidence

An agent that wrote the code tends to report that the code works. Nobody has checked that claim against what was agreed.

The fix is three skills. [`fde:smoke-test`](./plugins/fde/skills/smoke-test/SKILL.md) walks the running application with a person and writes down each finding. [`fde:qa-session`](./plugins/fde/skills/qa-session/SKILL.md) checks a built feature against the agreed facts and fixes no product code. [`fde:bug-hunt`](./plugins/fde/skills/bug-hunt/SKILL.md) works the findings from a tracker to a merged branch.

### The method gets tied to one tool

A method written around one tool dies when the tool changes.

The fix is a core that does not know the tool. `aie-session` hands design and plan to a method pack, and the default pack is superpowers. `qa-session` runs its checks through lanes for Postman, Playwright, Claude Code's own review skills and SQL. A new tool is a new file.

`fde:fdc-session` uses the same split. It hands its digest, confirmation, grill and update to a method pack, and the default pack is `grill`. A flag such as `--quick` picks another pack for `fde:aie-session`.

## Twelve skills cover an engagement from first call to delivery

The table follows the order in which an engagement meets each skill. The method splits the work between two roles. The forward deployed consultant keeps the record true and cuts the milestones. The AI engineer builds a ready milestone and merges it.

| Skill | What it does |
|---|---|
| [`fde:init`](./plugins/fde/skills/init/SKILL.md) | Starts an engagement. It builds the folders and repositories and leaves the first milestone ready to build. |
| [`fde:file`](./plugins/fde/skills/file/SKILL.md) | Files client documents into the wiki with a ledger row and an authority tier, and builds the knowledge graph. |
| [`fde:brain-dump`](./plugins/fde/skills/brain-dump/SKILL.md) | Splits a call or a stream of thought into dated, tagged, sourced entries and appends them. |
| [`fde:fdc-session`](./plugins/fde/skills/fdc-session/SKILL.md) | Takes whatever arrived into the record, grills the consultant for holes and closes with questions for the next meeting. |
| [`fde:prototype`](./plugins/fde/skills/prototype/SKILL.md) | Builds one clickable HTML demonstrator and loops on feedback until the user calls it done. |
| [`fde:aie-session`](./plugins/fde/skills/aie-session/SKILL.md) | Runs one build session from an empty folder to a merged branch, with design and plan in a method pack. |
| [`fde:ux-log`](./plugins/fde/skills/ux-log/SKILL.md) | Parks an interface problem as a dated entry so the build carries on. |
| [`fde:smoke-test`](./plugins/fde/skills/smoke-test/SKILL.md) | Walks the running application with a person, one scenario at a time, and records what it finds. |
| [`fde:bug-hunt`](./plugins/fde/skills/bug-hunt/SKILL.md) | Takes a pile of bugs to a merged branch, with one fix subagent per bug. |
| [`fde:qa-session`](./plugins/fde/skills/qa-session/SKILL.md) | Checks one built feature against the agreed facts before delivery, and fixes no product code. |
| [`fde:session-sync`](./plugins/fde/skills/session-sync/SKILL.md) | Writes up Claude Code chats that nobody scaffolded as session folders. |
| [`fde:explain`](./plugins/fde/skills/explain/SKILL.md) | Explains one complicated thing in plain English, in chat, so it can be followed in one read. |

## One engagement runs in eight steps

1. `/fde:init <slug>` builds the umbrella folder, the docs repository and the first milestone.
2. `/fde:file` puts each client document into the wiki as it arrives.
3. `/fde:brain-dump` records what was heard in each call.
4. `/fde:fdc-session` turns the material into the charter, the milestones and the open questions.
5. `/fde:prototype` gives the client something to click, when the client needs it.
6. `/fde:aie-session` builds a ready milestone to a merged branch, with `/fde:ux-log` running beside it.
7. `/fde:smoke-test` walks the running application, and `/fde:bug-hunt` fixes the pile of bugs that the walk and the build left behind.
8. `/fde:qa-session` checks the built feature against the record before the delivery. Each fact it fails goes back to a bug hunt, and then the delivery goes out.

## A closer look at qa-session

`/fde:qa-session` answers one question before a delivery. Does the built feature match what was agreed? It runs six steps.

1. Understand: the session rebuilds the agreed facts from the record alone, without the builder's notes or the code.
2. Ask: it writes test cases for each fact and a one-page test plan with exit criteria stated before anything runs.
3. Review: a person decides which test cases stand.
4. Execute: the lanes write one check per kept test case and run them side by side.
5. Validate: each failure is analysed from its evidence, and each fact gets pass, fail or not checked.
6. Improve: the session adds a coverage table, one extra round for the gaps and a regression set.

| Lane | Tool | What it checks |
|---|---|---|
| `postman` | The Postman plugin's skills | The API |
| `playwright` | Playwright's planner, generator and healer agents | The interface, in a browser |
| `anthropic` | Claude Code's `/code-review` and `/security-review` | The code and the running application |
| `sql` | Read-only queries built from the real schema | Stored data |

The session generates and a person decides. A root cause is a hypothesis until it is reproduced.

Four rules keep the evidence honest.

1. An expected result comes from the record and never from what the application does today.
2. A priority 1 check is shown failing once before its pass counts.
3. No check is skipped to get a green run.
4. Nothing leaves the machine without the person's yes.

The loop follows Arpit Choubey's article [Claude Code for QA: From Writing Test Cases to Building an AI-Powered Testing Workflow](https://medium.com/@ArpitChoubey9/claude-code-for-qa-from-writing-test-cases-to-building-an-ai-powered-testing-workflow-436d12b37696).

## Running a full engagement needs six things this repository does not carry

Every skill can be read here. Running one needs the things below. Three of them are private today: the default docs template, the reference stacks and the `sessions` skill.

So an outside engineer can read the whole method now. Running a session means supplying a docs template and a session scaffold of their own.

1. A docs template repository and the guardrails it defines. `fde:init` builds the docs repository from it, and the default template is private. The skills cite numbered guardrails, and the template's `setup/guardrails.md` holds them. `--docs-template` takes another template.
2. The reference stacks `PeopleEquation/fde-be` (Django and DRF) and `PeopleEquation/fde-fe` (React and Vite). Both are private and optional. They affect `fde:init`.
3. The `sessions` skill at `~/.claude/skills/sessions`. The session skills call its `sessions.py` to make, check and index session folders. It is not published yet.
4. The superpowers plugin. The default method pack of `fde:aie-session` uses it.
5. Two voice files for `fde:explain`: `~/.claude-shared/VOICE.md` and `~/.claude-shared/registers/learner.md`.
6. Outside tools for the lanes of `fde:qa-session`. Each is installed only if its lane runs. They are the Postman plugin, `@playwright/test` in the frontend and the `claude-security` plugin.

## Status

The plugin is at version 0.1.0.

The method comes from daily client work. This plugin is the general version of that method, with the client's names and rules taken out. Its first full client engagement as a plugin is still ahead.

These points say what is proven and what is not.

1. `fde:qa-session` is new. None of its four lanes has been run in a real session yet.
2. The plugin assumes a Django and React reference stack in places. Some convention files are written for Vitest, Tailwind, HeroUI, Django and pytest.
3. `fde:init` cannot run without a docs template, and the default one is private.
4. Only one method pack exists for `fde:fdc-session` and two for `fde:aie-session`.

## The repository holds one marketplace and one plugin

```
.claude-plugin/marketplace.json   the catalogue that the install command reads
install.sh                        links the plugin into ~/.claude/skills
plugins/fde/
  .claude-plugin/plugin.json      the plugin's name and version
  README.md                       the full reference
  ENGAGEMENT.md                   the format of the .engagement file
  scripts/                        the scaffold, record lint and link check scripts
  skills/                         one folder per skill, each with a SKILL.md
```

## Working on the skills

Clone the repository and run `./install.sh`. The script links the plugin into `~/.claude/skills`, so an edit to a skill is live at once.

```bash
git clone https://github.com/Justanotherbrickinthewall/fde.git
cd fde
./install.sh
```

Restart Claude Code after the first run.

Do not pull a new version in the middle of a milestone.

The plugin is written at People Equation.
