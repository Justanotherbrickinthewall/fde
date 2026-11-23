---
name: explain
description: "Explain one complicated thing to the user in plain English, in order, in chat, so they can follow it in one read. The thing can be a design, a process, a decision, a reply they did not follow, or a document they want to understand and approve without opening it. Use only when they ask for an explainer: \"/fde:explain\", \"explain\", \"explain it in plain English\", \"plain English please\", \"explain it like a child\", \"explain it to me simply\", \"walk me through this doc\", \"what does this doc need from me\". Do not use for ordinary working replies, which stay as they are. Works in any project."
---

# Explain it in plain English

The user asks for this when a reply or a document has turned into a wall of
text. The usual cause is that it was too technical and too full of jargon to
follow. They do not want everything explained. Most of a session is working
talk, and that stays as it is. This skill is for the one complicated thing they
have asked about.

It has two uses.

1. Explain a complicated thing, such as a design, a process or a decision.
2. Let them understand and approve a document by talking about it in chat,
   without opening the file.

The skill works in any project. It reads no engagement file and assumes no
client.

## The writing rules live elsewhere

Write every explainer to `~/.claude-shared/VOICE.md`. Overlay
`~/.claude-shared/registers/learner.md` for depth: define a term the first
time it appears, write the chain of reasoning out in full, and give a
concrete example. Do not restate their numbers here. If a rule needs to
change, it changes in those files.

## Explaining a thing

1. Read what the thing is before explaining it. Open the code, the plan or
   the earlier reply that confused them. Never explain from memory.
2. Start with the answer in one or two sentences. Say what the thing is and
   why it matters to them, the way you would tell a smart friend.
3. Then go through it in order, as numbered steps. Use the order things
   actually happen, or the order they need to understand them. One idea per
   step.
4. Name things concretely. Use the real table, the real column, the real
   file and the real endpoint. A user once asked to "talk in terms of the DB
   values and repos", and that is the default.
5. Give the reason with each step. They ask "why" more than anything else, so
   answer it before they have to.
6. Use plain words. Where a technical term is needed, give its plain meaning
   in the same sentence. A comparison may open a point, but the literal
   statement must follow it straight away.
7. Never state a conclusion without its middle. Write each link in the chain.
8. Close with what is open or risky, and what you would do. Give one
   recommendation.

If they asked a question and want an answer too, explain first. Then give the
answer on its own, short and tight. One user asked for exactly that shape: "explain
it to me, then give me a tightened answer".

If the explanation needs more than one screen, split it. Give the first part,
then ask whether to carry on. Do not squeeze it into shorthand to make it fit.

## Explaining a document

The aim is that they never have to open the file. The chat becomes where they
read, question and approve it.

1. Read the whole document first. If there are several, treat them as one
   body of knowledge and note which document each point came from.
2. Open with what the document is, what it says and why it matters. Use one
   or two short paragraphs, in everyday words, not the document's own
   phrases.
3. Say what it needs from them. List each decision, approval or open question
   as a numbered point, with the section it sits in. This is the part they
   act on, so make each point something they can answer with yes, no or a
   change.
4. Give a short numbered map of its parts in everyday words. Keep it to a
   few items, so they can say "tell me about 3".
5. Walk the parts in order when they ask, one part per reply. Explain each
   one plainly and point to where it sits, by heading and `path:line`. Flag
   anything they should not miss, such as a number that matters, an unusual
   choice or a contradiction. Then stop and let them ask.
6. Answer their questions from the document first, and say where the answer
   came from. If the document does not cover it, say so before answering
   from general knowledge.
7. When they approve or ask for a change, make the change in the file and
   tell them what changed and where. Their approval in chat is the approval.

If they seem short on time, offer to cover the remaining parts in one pass.
If a file cannot be read, say so at once rather than guessing.

## Rules

- Explain only the thing they asked about. Do not turn every later reply into
  an explainer.
- The source is the truth. Never fill a gap with a guess dressed as fact.
- Keep their words for their things. If they call it the brief, it stays the
  brief.
- They check understanding with "right?" and welcome pushback. If their
  summary back is wrong, say so plainly and say which part.
- No emoji, and no bold inside paragraphs.
