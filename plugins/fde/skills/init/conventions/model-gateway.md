# Model gateway

## What this layer is

The application asks a language model for help in exactly one place. That
place is the gateway. Everything else in the codebase calls the gateway and
never talks to a provider itself. So there is one thing to secure, one thing
to log and one thing to fake in a test. The words we send the model live in
files rather than in code, one file per task. So a person can read and
change a prompt without touching a program. The key that pays for the calls
lives only in the environment, and a commit hook refuses to let one into the
history. When a call fails, the person sees that it failed. Nothing is
guessed, and no blank is quietly filled in.

## The rules

1. A provider key lives only in the environment, and never in a tracked file.
2. The environment names are `OPENROUTER_API_KEY` and `OPENROUTER_BASE_URL`.
3. A commit hook refuses any commit carrying something shaped like an
   OpenRouter key, which is `sk-or-` and a long token.
4. The hook matches that one key shape and nothing else, so a real client
   document may still be committed as a test fixture.
5. One module is the only code in the application that knows a model provider
   exists.
6. That module exposes one interface: a task name, a payload and any
   attachments go in, and a parsed answer comes back.
7. Every prompt and every model identifier lives in a file outside the code,
   one file per task.
8. A task file also carries the schema the answer must take, so the shape
   asked for and the shape parsed are one statement.
9. There is no default prompt and no default model, so a missing file or key
   is an error rather than a fallback.
10. A call that produces no usable answer raises one typed error, never an
    empty result.
11. A refused call renders visibly to the person, and never as a silent gap
    or an invented value.
12. The person sees one short sentence, and the provider's own error body
    goes to the application log only.
13. The gateway takes its transport as a parameter, so every test above it
    runs with no network.
14. A deployment that never configured the gateway refuses on the first call
    rather than making one.

## The checklist

1. Does the hook exist and is it wired to run before every commit? Read
   `.pre-commit-config.yaml` or the equivalent, and check `bin/no-secrets` is
   executable.
2. Does the hook actually refuse a key? Write a key-shaped string into a
   scratch file and run `bin/no-secrets <that file>`; expect exit 1.
3. Does the hook pass a real document? Run it against a committed fixture and
   expect exit 0.
4. Does a scan of the tracked files find no key? Run the hook over every
   tracked path.
5. Are `OPENROUTER_API_KEY` and `OPENROUTER_BASE_URL` the names used?
   `grep -rn "OPENROUTER_" <source>`, and check `.env.example` lists both.
6. Is the key absent from every tracked file, including compose files and
   CI? `grep -rn "OPENROUTER_API_KEY=" .` and expect only empty or example
   values.
7. Is there exactly one module that names the provider? Search the source for
   the provider host and for the HTTP client, and expect one file.
8. Does every caller reach the model through that one interface? Search for
   the gateway's call function and read each call site.
9. Is every prompt and every model identifier outside the code? Run
   `grep -rniE 'gpt|claude|gemini|llama|mistral' <source>` and count the hits
   outside the task directory. Expect zero.
10. Does each task file carry a model, a prompt and a schema? Read them.
11. Does a failed call raise one typed error rather than return an empty
    result? Read the module and the exception it defines.
12. Does a refused call reach the screen as a visible message? Unset the key,
    run the stack, and trigger the call.
13. Does the provider's error body stay out of the response? Read the error
    branch and confirm it logs rather than returns.
14. Do the tests above the gateway run with no network? Run the suite with
    networking off.

## Reference

The files under `model-gateway/reference/` come from two places. `no-secrets`
is `fde-be`'s hook, a standalone Python script that works on any repository.
The interface and the task-file shape are described from the first worked
example, which is still the only one. That one is Django, Python and
`httpx`. The shape carries to any stack.

- `no-secrets` — the commit hook, verbatim. It takes staged paths as
  arguments, refuses a key shape, and prints what to do instead. Python 3,
  no dependencies, runs anywhere.
- `gateway-interface.md` — the one interface the gateway exposes, what it
  raises, and how a refused call renders on a screen. Written for any stack.
- `task-file.toml` — an empty example of the prompt-file shape. The three
  keys, with comments saying what each holds and why. TOML, because the
  reference loads TOML; the shape matters and the format does not.
