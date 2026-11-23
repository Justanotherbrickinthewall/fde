# How a hunt ships the wrong thing

Read this before your first task, and again before you report a fix as
landed. Every item below happened on an earlier hunt, and most happened more
than once. The pattern underneath all of them is the same. A check ran, it
said something, and what it said was not what it appeared to say.

## 1. A fix is not live until the worker's start time post-dates the commit

A prompt file is read on every call, so it is live at once. Python is dead in
the worker until it restarts. So the two halves of one task land at different
moments, and a prompt narrowed while the code that gave the narrowing meaning
is not running gets reported as one landed fix. That costs a night and several
false bug reports.

Check the start time, not the clock:

```bash
docker inspect --format '{{.State.StartedAt}}' <worker-container>
git -C <be> log -1 --format='%h %cI'
```

Measuring waits for two conditions together: the last task is committed, and
the worker restarted after that commit. The backend web process may run under
a reloader and pick up a save without a restart. Do not carry the worker's
rule across to it.

## 2. Absence is not an answer

A worker that was not restarted is not a worker carrying the fix. An
attribute missing from a dataclass is not an attribute that is empty:
`getattr(node, "preprint", ())` returns `()` whether the field is empty or
does not exist. A minute's silence is not consent.

The habit that catches all three: ask what the absence would look like if the
answer were the other way, then check your method can tell the two apart.

## 3. Check what a claim could not have seen

A report is evidence of what the reporter believes. Ask what its method could
observe before you believe its conclusion. `git log -8` reaches back only so
far, and "the commits are not in the log" read off a window that never
contained them proves nothing. Name the run's own timestamp, not only the head
it was named for.

## 4. Confirm the enumeration can express the answer

Two sessions enumerated the constants that list computed fields. Those
constants held leaf paths, so computed columns could not have appeared in the
list whatever the truth was. The answer was structurally unavailable and the
method never said so. The same shape: a test named after a field the catalogue
does not have, which skips and reads green.

## 5. Run the real input through the real function before you write the test

This caught the most. A regex whose bounded gap cannot cross a decimal point
matched nothing, and the rule it enforced never fired. A fixture wrote a
citation unquoted, though the model wraps one about two thirds of the time, so
the check could not fail. A money-guard check used a number that fails the
checksum, so nothing would have masked it either way. Three tests proved their
own fixture rather than the code.

```bash
docker compose exec -T be python -c "from <module> import <function>; print(repr(<function>('...')))"
```

## 6. A rule about words loses to a model with other words

A prompt that says never propose a computed field is obeyed for the fields
someone thought of. When the payload contradicts the prompt, the model
resolves the contradiction its own way. A word filter refuses every phrasing
somebody thought of, and the model writes one nobody had.

The move is to stop describing what the model should say and have the
application state what it knows. Compute the flag from the registry. Build the
note from the rows actually written. A word rule may still be needed as a
backstop, but it may not be the authority.

## 7. A number that is not credible means the method is broken

A comparison that printed "ALL 135 DEFINITIONS IDENTICAL" from two empty files
had broken shell quoting. One hundred and thirty-five definitions cannot
render as zero lines. The guard it should have had refuses to compare at all
when either side reads fewer than a hundred rows. Differences reported
against a copy made by a dump piped into the client can be artefacts of the
copy. Check against the live database.

## 8. Say which command produced the green

The compose `test` service may run the test runner alone, while CI also runs
the linter, the framework check, the migration check and the schema checks.
"Suite green, 1832 passed" can be true and much narrower than it sounds, and
it can be repeated fifteen times while the main branch's CI is red.

## 9. What actually happens beats what a file claims

If a catalogue calls a column `entered` while the step registry writes it, the
gate trusts the catalogue, the model fills the cell, and accept-all takes it.
Where a file and the running system disagree about what the system does, the
running system is right and the file is a bug.

## 10. Verify a report where its claim is load-bearing

The orchestrator does not read every diff. It does read the removals a report
says it made and the tests it says now fail, whenever the next decision rests
on them. Ask the session for its last-landed commit alongside its remaining
queue, because a queue line naming only what is left reads like a skip.
