# Design system

Purpose: how every screen in this system looks, decided once.
Done when: never. Every module reads this file before it renders anything.

## The live pair is in the frontend repository

This file is not the design language. It points at it.

The language lives in `fde-fe`, as two files that sit beside each other:

- `packages/ui/DESIGN.md` — the written rules. What the tokens mean, when
  each one is used, and what a component may not do.
- `packages/ui/src/theme.css` — the values. Every colour, radius, shadow
  and step of the type ramp.

They are the pair, and they are the source of truth. Where this file and
those two disagree, those two win. A change to the language is a change to
them, made in `fde-fe` on a milestone branch. This file only records what
the engagement decided about it.

Prototypes in [`../project/prototypes/`](../project/prototypes/README.md)
read the same values. A prototype is one self-contained file with no build
step, so it copies the tokens into its own `:root` rather than importing
them. What must match is the values. A client seeing one look in the
demonstrator and another in the product learns that neither is real.

## Two non-negotiables

Both bind every screen, from the first commit.

1. **Utilities only.** No `.btn`, no `.card`, no custom component CSS.
   `packages/ui/src/components/` is the one place a utility string is
   written, and `apps/web` composes those components.
2. **Every design value is a token.** No hard-coded hex and no arbitrary
   pixel padding, anywhere under `packages/ui/src/` or `apps/web/src/`.

A test in `packages/ui` fails the suite if either rule breaks. It scans both
workspaces. It fails on a hex, an arbitrary px or rem value, an inline style
attribute, a second stylesheet, or a raw `className` under `apps/web`.

## Nothing is fetched at run time

Fonts and icons are vendored into the bundle. The browser fetches nothing
from a third-party host. Two reasons hold on most engagements. The
application may have to work with no internet, and a screen showing a
client's own figures should not open a request to somebody else.

## What this engagement decided

Record here anything the engagement settled about the language. A colour the
client rejected. A state the record needs and the tokens do not carry. A
licence question about a vendored font. Each entry is dated, and each says
which of the two live files it changed.

(none yet)

## The drift risk

If the language was copied in from another codebase, the copy is one-way
and there is no shared ancestor. That codebase can change its tokens
tomorrow and nothing here notices. Keeping the two aligned is a manual job.
Name who owns it, or say plainly that nobody does.
