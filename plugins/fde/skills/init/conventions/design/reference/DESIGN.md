# Datum

Datum is the design language this template ships. It is built on HeroUI v3.

The document lives here rather than in `fde-docs/setup/`, because the values
it describes live here too. `fde-docs/setup/design.md` points at this file
and at `src/theme.css` as the live pair.

## The idea

The interface is built like an instrument rather than like a report. Hairline
rules instead of boxes, square corners, and every recorded value set in a
monospace so it reads as a measurement.

Dark is the default and the palette this is designed in. Light is its bright
counterpart. Light has to hold up, but it is not where the decisions get
made.

## The five rules

1. Colour means the state of a field. Nothing else in the product is
   saturated. A role, a file type and a key are all drawn in the neutral.
2. A value is set in the mono. Prose about a value is set in the sans. The
   `Value` component is the only way to print a reading.
3. Surfaces are told apart by a rule, not by a shadow. `--surface-shadow` is
   `none` and only a thing that genuinely floats gets `--overlay-shadow`.
4. Corners are near square. `--radius` is `0.25rem` and everything derives
   from it.
5. Every label is a `Caption`: small, sentence case, in the sans. The mono is
   for values, and a label is prose.

## Where the values live

`src/theme.css`, and nowhere else. It declares the Tailwind tokens in a
`@theme inline` block and then the two palettes as HeroUI's own CSS
variables.

Overriding HeroUI's variable names is what re-skins every HeroUI component at
once. A Button, a Table and a Popover all speak Datum without a single
component override, because they read `--surface`, `--accent`, `--rule` and
the rest from the theme.

`src/styles.css` loads three things and declares nothing beyond the vendored
`@font-face` blocks and the handful of rules that bind every element.

There is no `tailwind.config.ts`. A JS config cannot write CSS custom
properties, and HeroUI reads nothing else.

## Type

Inter for the interface, Geist Mono for every value.

The mono is doing real work here. It is how a recorded value is told apart
from prose about that value, so the pair had to agree at small sizes. Geist
Mono sits on Inter's rhythm without shouting.

Both are vendored under `src/vendor/fonts/` with the SIL Open Font Licence
1.1 beside them. One variable weight axis each, so the pair costs two
requests. Nothing is fetched at run time.

Every numeral in the product is tabular. That is set once on `body`, so no
component has to ask.

## The six states

The states are declared in `src/field-states.ts`. They read as a sequence
rather than as six unrelated colours.

| State | What it means | Hue |
| --- | --- | --- |
| `open` | Nothing recorded | neutral slate |
| `awaiting` | Blocked on a person | amber |
| `inferred` | The machine proposed it | violet |
| `entered` | A person recorded it | blue |
| `conflict` | Two sources disagree | red |
| `settled` | Signed off | green |

Each state has a foreground and a soft ground, in both palettes, as
`--state-<name>` and `--state-<name>-soft`. `design-tokens.test.ts` reads
`theme.css` and checks the pairs against `FIELD_STATES` in both directions.
A seventh state or a rename fails there.

Every foreground clears 4.5 to 1 against its own soft ground, in both
palettes. Colour is the only thing this language assigns meaning to, so the
six were picked by moving hue alone.

This template ships the palette and the names. It ships no component that
wears them, because what a state marker should look like is a decision each
engagement makes.

## The accent

The accent is a plain blue: `oklch(0.7 0.11 240)` in dark and
`oklch(0.462 0.1 240)` in light. It carries no brand. An engagement that has
one replaces these two values and nothing else.

The accent is focus, a primary action and a link. Never decoration.

`entered` sits at a neighbouring hue, which is deliberate. It is the one
state a person creates by hand, so it wears close to the product's own
colour.

## The shell

Three zones, and the split between the first two is the point.

The top bar carries the wordmark and the project switcher. Switching project
is rare and belongs where it cannot be lost.

The rail carries a project's own screens. Moving between them is constant, so
it belongs where the eye already is. The template hands the shell no nav
items, so the rail renders nowhere until an engagement supplies some.

The rail has three states, not two, because "collapsed" and "expands when I
reach for it" are different wants. A toggle makes one of them unavailable.
`Expand on hover` is the default: the rail sits narrow and widens over the
page, so the labels are a glance away and the page never reflows. The choice
is remembered in `localStorage`.

The item you are on gets a filled glyph. Lucide draws in outline, so the fill
is the stroke colour at low opacity behind the same path. The shape stays
identical and only its weight changes, which is what makes a filled icon read
as selected rather than as a different icon. An item whose name no icon
covers gets its own initial in a box, filled the same way.

## The dock

`Workspace` draws the screen and, when a screen asks for one, a companion
panel beside it. The panel resizes and its width is remembered.

The width is a custom property rather than an inline style. A dragged width
is application state, so it cannot be a token and it cannot be a Tailwind
class, and the stray-styles test bans the inline style that most codebases
would reach for. The element carries `w-(--dock-width)` and the drag writes
one value.

`useDocked()` tells a screen it is being drawn in the dock, so it can drop
the heading the dock's own header has already said.

## Dark

Datum ships both palettes and the dark one is not an inversion. It is a
graphite console: the ground darkens, the states brighten, and their soft
grounds become tints of themselves so the six stay tellable apart.

`useTheme()` writes `<html data-theme>` and `.dark`, and remembers the choice
in `localStorage`. The toggle sits in the top bar.

## What HeroUI supplies, and what it does not

HeroUI supplies behaviour: React Aria's press handling, focus management, the
listbox and popover contracts, the disabled and invalid states. Datum
supplies the look, through the theme.

So the components in `src/components/` are mostly mappings. `Button` maps
three kinds onto three HeroUI variants. `SelectInput` translates the empty
string to React Aria's "no key" and back. Where a component overrides a
HeroUI class it is for one of the five rules above, usually the corner or the
mono.

Two things are deliberately not HeroUI.

The select is native. HeroUI's is React Aria's, whose trigger is a button
with a listbox, so its role is `button` and never `combobox`. Swapping it
changes what assistive technology is told the control is, which is behaviour
rather than look.

`IconButton` is a native button wearing HeroUI's classes. React Aria filters
the props it forwards to the DOM and `title` is not among them, and a tooltip
is the entire reason an icon may stand in for a word.

Datum's own rule is that an icon never takes the place of a word that fits.

The three menus, project, account and sidebar control, are HeroUI Popovers.
The first cut built them as `<details>`, on the reasoning that they should
work before JavaScript has decided anything. That is not a state a
client-rendered SPA has, and what it bought instead was menus that do not
close when you click away from them.

## The components Datum adds

`Value` and `NoValue` — a reading, and the em dash that stands for one that
was never recorded.

`Caption` — the micro-label every provenance line is built from.

`KeyValue` — a caption and what it holds, which is the shape most of this
product is.

`Rule` — a hairline, and the one way the product draws one.

`SectionHeader` — a heading inside a screen, ruled at the same height on
every screen.

`ListWithForm` — a list and the form that adds to it, side by side or
stacked.

`SnackBar` — the whole of the warning that unsaved values exist.

## What the tests hold

`no-stray-styles.test.ts` — Tailwind utilities only, one stylesheet plus the
theme, no hex, no arbitrary px or rem, no inline style, and no `className`
written in `apps/web`.

`design-tokens.test.ts` — `theme.css` against this document, in both
directions and both palettes.

`shell.test.tsx` — the top bar renders, the user menu opens, and sign out
calls back.

`design-build.test.ts` — a real `vite build`, then: every class the frontend
uses compiles to a rule, the theme's own values reach the stylesheet, no
third-party host appears anywhere in the bundle, and the fonts are bundled
rather than fetched.
