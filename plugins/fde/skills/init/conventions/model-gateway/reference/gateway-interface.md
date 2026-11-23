# The one interface

The gateway is one module and it exposes one call. Every other part of the
application reaches a model through that call and through nothing else. This
file says what the call takes, what it returns, what it raises, and what the
person sees when it refuses.

The shape below is described from the first worked example, which is still
the only one. It is Python and `httpx`. Names change on another
stack; the four parts of the contract do not.

## What goes in

| Part | What it is |
| --- | --- |
| task name | The name of a task file, without its extension. |
| payload | The text this call is about. One string. |
| attachments | Zero or more files, each a filename, a media type and bytes. |
| transport | Optional. A test passes a fake one so nothing reaches a network. |
| config | Optional. Overrides the module's own settings for one call. |

The task name is not a prompt. The caller names a task and the gateway loads
the prompt, the model identifier and the answer schema from that task's file.
No caller has ever seen a prompt.

## What comes out

A parsed answer, already checked against the schema the task file declares.
The provider is asked for that schema as a structured response, and the same
schema is what the answer is read back against. The shape asked for and the
shape parsed are one statement in one file, so they cannot drift.

## What it raises

One error type, for everything that stops a usable answer coming back.

- No key is configured.
- The provider answered with an error status.
- The provider could not be reached, or the call timed out.
- The answer came back and could not be read as the schema.

One type, because a caller should handle one thing rather than whatever the
HTTP library happened to raise. It is never an empty result. An empty result
lets a caller mistake a failed call for a genuine finding of nothing. That is
the mistake this whole layer exists to prevent.

Configuration failures are their own types under the same rule. Nothing has
told the gateway where the tasks live. The named task does not exist. The
file exists and is malformed. Each names itself, and none falls back to a
default. A guessed prompt is a call nobody wrote.

## How a refused call renders

The person sees that the call failed, in one short sentence, on the screen
they were working on. They do not see a spinner that never ends, an empty
list, or a field quietly filled with a plausible value.

The provider's own error body never reaches the screen and never reaches a
third-party error reporter. A provider quotes the request back in its error
body, and the request carries client material. The body goes to the
application log, truncated, and stays inside the application's own network.
Throwing it away instead would turn a diagnosable fault into a guess, so it
is logged rather than dropped.

## Why the transport is a parameter

Every test above the gateway hands it a canned answer, so the whole
application is testable with no network and no key. That is the only reason
this boundary is worth drawing at all.

## What the gateway does not do

It takes text and returns text. It never sees the product's own fields, its
catalogue or its records. Turning an answer into something the product can
use is the caller's work. That separation is what keeps the tests above this
module free of a provider.
