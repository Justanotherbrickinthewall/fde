# The end-to-end checker

Dispatch a checker subagent when the thing being hunted is model behaviour. A
test suite cannot tell you that a model stopped proposing a field, and a
person cannot run nineteen files four times each.

It runs at the umbrella, drives the real application over HTTP, and never
edits code. It writes its findings to a file and reports the headline to the
orchestrator, which routes them. Its report to the orchestrator is the
verdict and the numbers, and the evidence goes in the file. Lead with the line
that matters: a stopper, or join, or the rate that was asked for.

Fire it three times on a hunt with a prompt change in it. Once to build the
files and take a baseline before the change, once after, and once on the merge
candidate. Without a before, a prompt change has no after.

If you dispatch it, pass its model explicitly, as the global subagent rule says. It is a
search and mapping job, or a judgement job where the call is hard.

## The test files

Build realistic messy files for one fictional project. Messy means what a
client actually sends: a spreadsheet with a hidden sheet and three error
cells, a chat export with mixed languages, a scanned PDF with no text layer, a
mail thread whose newest message corrects the oldest, a photograph, a map
file, a form filled in by hand with "B1 i think" in one cell.

Plant deliberate disagreements between files, and make some subtle. A letter
that swaps two costs against the mail, keeping the same total, so a
total-only check misses it. A plan claiming 8 trees against a scan's
hand-corrected 6. Building the files finds bugs on its own.

## The answer key

An `ANSWER-KEY.md` sits beside the files. It holds the traps in each file, a
row per field saying what a good run puts there, and a closing list of the
fields no document can ever fill. That last list stops a checker calling an
empty field a defect. A project category that is the client's own judgement,
and a wet signature, belong on it.

## One file per report

Never one rolling document. A report is cited weeks later and has to still
mean what it said. Every report names three things in its first paragraph.

1. The head the code was at, with its commit time.
2. The worker container's start time, from `docker inspect --format
   '{{.State.StartedAt}}' <worker-container>`.
3. The run's own timestamps, and a range where the report covers several
   runs.

The run's own time is the one that gets forgotten and the one that matters. A
report named for a head can cover runs that finished before the fixes landed,
and sessions that reason from the head then reach different wrong conclusions.

Say plainly where a run was interrupted, and whether any number is void.

## The harness

A small Python script signs in, creates the project, enables the module, posts
each file as a chat turn, polls the job, and runs accept-all after each. It
stamps every line with the time, the head and the worker's start time. Keep
the project fresh per pass, because a record carrying yesterday's facts
changes what today's proposals clash with.

## The final pass

Run it on the merge candidate, once both build queues are empty and the worker
has been restarted on the committed head. It answers one question in one line,
near the top of the report under the provenance paragraph: does this join or
does it stop.

The rest of the report carries four things.

1. What is wrong on the record, with every wrong value named and routed to a
   task or to the accepted list.
2. Which fields are still empty, split into the ones a file states and the
   ones no document could fill.
3. How many files do materially better than the last pass, how many the same,
   and how many worse.
4. One closing sentence saying what the branch is good for and what it is not.

## Routing what the checker finds

The checker reports to the orchestrator, which cuts the task, gives it an id,
and dispatches a fix subagent. The checker never fixes what it finds, and
never briefs the agent that will. A stopper found on the merge candidate goes
ahead of everything in the queue.

A checker can be wrong, and the orchestrator says so rather than routing it.
Stale-worker findings can rest on facts that are not true.
