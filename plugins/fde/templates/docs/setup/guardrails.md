# Guardrails

Purpose: the hard rules of this engagement. Break one only after escalating.
Done when: client-specific rules are added below and confirmed with the
client where they originate there.

## The two kinds

There are two kinds of guardrail. Every one below is one or the other.

A client guardrail comes from the client, the law or the contract. A rule
that governs what reaches the client is one too, whoever wrote it. The FDC
owns it. The AIE cannot override one, on any milestone, for any reason.

A build guardrail is the FDC's suggestion about how to build. It applies
until the AIE overrides it. An override takes a conversation with the FDC
first, then a dated note on the guardrail giving the reason. The note reads
like this.

*Overridden 07-09-26, AIE: <reason>.*

The note stays. A later change is another note under it, never an edit to
the one above.

Every live guardrail carries a source line saying where it came from. That
line decides its kind. A guardrail with no source is a lint finding.

The numbers never change and they are never reused, because the record
cites guardrails by number. A withdrawn guardrail keeps its number and its
history. The next free number on this engagement is 11.

## Client guardrails

These come from the client, from the law or from the contract, or they
govern what reaches the client. The FDC owns them. The AIE cannot override
one.

Guardrails 4, 5 and 10 come with the method and hold on every engagement.
The skills cite them by number, so they are here from the start.

### 4. Nothing goes to the client without review

Plans, questions, decks, anything.

Source: ours, and it governs what reaches the client.

### 5. Client documents are private

Client documents contain private data. No pasting into external services or
public artefacts without explicit per-instance approval.

Source: the client. The documents are theirs and only they can approve one
leaving.

### 10. Client-stated requirements are changed only by the client

Disagreement gets recorded and raised, not silently dropped.

Source: the client. Only they can change what they asked for.

Numbers 11 onwards are this client's own: their regulator, their data,
their environment. There are none yet. `/fde:fdc-session` writes them as they
come out of the material, and each one names the person or the document it
came from.

## Build guardrails

These are the FDC's rules about how we work and how we build. The AIE may
override one with a dated note and a reason, after the conversation.

### 1. `raw/` is immutable

Derived work lives in `wiki/`.

Source: ours, the FDE method's filing doctrine.

### 2. No unsourced facts in the wiki

Cite the meeting, the file and page, or tag `(assumption)` and mirror it
into open-questions.

Source: ours, the FDE method's sourcing doctrine.

### 3. Do not invent domain facts

Unknown = open question, not plausible guess.

Source: ours, the FDE method's sourcing doctrine.

### 6. Decisions that constrain later work get an ADR

They live in `project/decisions/`.

Source: ours, the FDE method's decision record.

### 7. Every claim carries the tier of its source

`statutory` > `artefact` > `stated` > `ours`. Higher tier wins a
contradiction and the loser takes a dated correction note. Same-tier
contradiction is an open question, never a judgement call.

Source: ours, the FDE method's tier cascade.

### 8. Nothing is lost silently

A source that will not parse, a gap in coverage: each is recorded as
visible debt.

Source: ours, the FDE method's debt rule.

### 9. No product code during scoping

No framework or schema commitments either. Architecture thoughts are
drafts, clearly marked.

Source: ours, the FDE method's scoping phase.

### 15. No value is invented

No default, no fallback, no assumption promoted quietly. A missing fact
renders as a gap and a conflict renders as a conflict.

Source: ours, the FDE method's gap doctrine.

Add build-specific rules here when the code space is created. None
replaces a scoping guardrail, and guardrail 9 still governs everything
outside a bounded slice.
