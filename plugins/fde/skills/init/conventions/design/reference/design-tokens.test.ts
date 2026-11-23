// Group 1: token coverage, both directions.
//
// Datum keeps its values in CSS, because HeroUI reads its theme as custom
// properties and a JS config cannot write those. So this test parses
// `../theme.css` rather than importing a config. A token `DESIGN.md`
// declares and the theme lacks fails as missing, and a token the theme
// invented fails as extra.
//
// The transcriptions below are literals, not derivations. A test that
// computed the expected values from the file it is checking would agree with
// itself no matter what the file said.
//
// Where the line is drawn, and why. `@theme inline` is the contract the
// components consume -- it is what turns a token into a Tailwind utility --
// so every name and every value in it is transcribed. The two palettes are
// transcribed by name, plus the values of the twelve state tokens in each,
// because the states are the only colours the language assigns meaning to
// and the rest are a surface ramp whose exact lightness is not a decision
// this document makes.

import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { FIELD_STATES } from "../field-states";

const THEME = readFileSync(resolve(import.meta.dirname, "../theme.css"), "utf8");

// --- reading the file -------------------------------------------------------

/**
 * The custom properties declared in the block a selector opens.
 *
 * Brace counting rather than a regular expression, because the light and
 * dark blocks sit inside `@layer base` and a lazy match would stop at the
 * first `}` it found, which is inside a `color-mix()` in neither file today
 * and would be the moment somebody added one.
 */
function block(selector: string): Record<string, string> {
  const at = THEME.indexOf(selector);
  expect(at, `theme.css declares no ${selector} block`).toBeGreaterThan(-1);

  let i = THEME.indexOf("{", at);
  let depth = 0;
  const start = i + 1;
  for (; i < THEME.length; i += 1) {
    if (THEME[i] === "{") depth += 1;
    else if (THEME[i] === "}") {
      depth -= 1;
      if (depth === 0) break;
    }
  }

  const body = THEME.slice(start, i);
  const found: Record<string, string> = {};
  for (const match of body.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/g)) {
    found[match[1] as string] = (match[2] as string).replace(/\s+/g, " ").trim();
  }
  return found;
}

const theme = block("@theme inline");
// `:root` carries dark, because dark is the default and the palette the
// language is designed in. Light is the counterpart and has to win over it,
// which is why it is a class and an attribute and never the root.
const dark = block(':root,\n  .dark,\n  [data-theme="dark"]');
const light = block('.light,\n  [data-theme="light"]');

// --- what DESIGN.md declares ------------------------------------------------

/** The Tailwind-facing contract. Every name, and every value. */
const THEME_BLOCK: Record<string, string> = {
  // Type. IBM Plex Sans for the interface, IBM Plex Mono for every value.
  "--font-sans": "Inter, ui-sans-serif, system-ui, sans-serif",
  "--font-mono": '"Geist Mono", ui-monospace, "SF Mono", monospace',

  // The six states, a foreground and a soft ground each, published through
  // the palette variables so one utility follows both themes.
  "--color-state-open": "var(--state-open)",
  "--color-state-open-soft": "var(--state-open-soft)",
  "--color-state-awaiting": "var(--state-awaiting)",
  "--color-state-awaiting-soft": "var(--state-awaiting-soft)",
  "--color-state-inferred": "var(--state-inferred)",
  "--color-state-inferred-soft": "var(--state-inferred-soft)",
  "--color-state-entered": "var(--state-entered)",
  "--color-state-entered-soft": "var(--state-entered-soft)",
  "--color-state-conflict": "var(--state-conflict)",
  "--color-state-conflict-soft": "var(--state-conflict-soft)",
  "--color-state-settled": "var(--state-settled)",
  "--color-state-settled-soft": "var(--state-settled-soft)",

  // The hairline. There is no ruled-ground token any more: the grid the
  // first cut painted on `body` was drawing-office texture and it went.
  "--color-rule": "var(--rule)",

  // The type ramp. Inter, tightened at the display sizes and left alone at
  // reading sizes. `caption` is sentence case in the sans now, so it lost
  // the wide tracking the uppercase monospace version needed.
  "--text-display": "3rem",
  "--text-display--line-height": "1.05",
  "--text-display--letter-spacing": "-0.04em",
  "--text-h1": "2.125rem",
  "--text-h1--line-height": "1.12",
  "--text-h1--letter-spacing": "-0.032em",
  "--text-h2": "1.625rem",
  "--text-h2--line-height": "1.2",
  "--text-h2--letter-spacing": "-0.026em",
  "--text-title": "1.0625rem",
  "--text-title--line-height": "1.35",
  "--text-title--letter-spacing": "-0.014em",
  "--text-lead": "1.0625rem",
  "--text-lead--line-height": "1.55",
  "--text-caption": "0.75rem",
  "--text-caption--line-height": "1.4",

  // One entrance, and it is short. An instrument does not swoop.
  "--animate-rise": "rise 0.24s cubic-bezier(0.2, 0.8, 0.3, 1) both",

  // Layout. The dock's width when it opens, and the range a person may
  // drag it to.
  "--height-viewer": "70vh",
  "--width-dock": "44rem",
  "--width-dock-min": "20rem",
  "--width-dock-max": "64rem",
};

/**
 * The palette, by name.
 *
 * These are HeroUI's own variable names. Overriding them is what re-skins
 * every HeroUI component at once, so the list is also a statement of which
 * parts of HeroUI's theme Datum has an opinion about. A name HeroUI adds in
 * a later version and this file does not override is not a failure; a name
 * this file overrides and DESIGN.md never mentioned is.
 */
const PALETTE = [
  "--background",
  "--foreground",
  "--surface",
  "--surface-foreground",
  "--surface-secondary",
  "--surface-secondary-foreground",
  "--surface-tertiary",
  "--surface-tertiary-foreground",
  "--overlay",
  "--overlay-foreground",
  "--muted",
  "--border",
  "--separator",
  "--rule",
  "--accent",
  "--accent-foreground",
  "--focus",
  "--link",
  "--default",
  "--default-foreground",
  "--field-background",
  "--field-foreground",
  "--field-placeholder",
  "--field-border",
  "--success",
  "--success-foreground",
  "--warning",
  "--warning-foreground",
  "--danger",
  "--danger-foreground",
  "--segment",
  "--segment-foreground",
  "--backdrop",
  "--surface-shadow",
  "--overlay-shadow",
  "--field-shadow",
];

/** Geometry, declared once in the dark block and inherited by the light one. */
const GEOMETRY: Record<string, string> = {
  "--radius": "0.25rem",
  "--field-radius": "var(--radius)",
  "--border-width": "1px",
  "--field-border-width": "1px",
  "--ring-offset-width": "2px",
  "--disabled-opacity": "0.4",
};

/** The six states, light. Nothing recorded, blocked, machine, person, disagreement, resolved. */
const STATES_LIGHT: Record<string, string> = {
  "--state-open": "oklch(0.52 0.015 265)",
  "--state-open-soft": "oklch(0.955 0.004 265)",
  "--state-awaiting": "oklch(0.53 0.13 72)",
  "--state-awaiting-soft": "oklch(0.958 0.035 82)",
  "--state-inferred": "oklch(0.52 0.2 300)",
  "--state-inferred-soft": "oklch(0.958 0.03 300)",
  "--state-entered": "oklch(0.47 0.105 232)",
  "--state-entered-soft": "oklch(0.953 0.025 232)",
  "--state-conflict": "oklch(0.545 0.21 27)",
  "--state-conflict-soft": "oklch(0.955 0.032 25)",
  "--state-settled": "oklch(0.5 0.13 158)",
  "--state-settled-soft": "oklch(0.958 0.035 160)",
};

/** The six states, dark. Brighter foregrounds, and softs that are tints of themselves. */
const STATES_DARK: Record<string, string> = {
  "--state-open": "oklch(0.685 0.014 265)",
  "--state-open-soft": "oklch(0.3 0.01 265)",
  "--state-awaiting": "oklch(0.8 0.13 78)",
  "--state-awaiting-soft": "oklch(0.32 0.055 72)",
  "--state-inferred": "oklch(0.75 0.16 300)",
  "--state-inferred-soft": "oklch(0.31 0.075 300)",
  "--state-entered": "oklch(0.755 0.115 232)",
  "--state-entered-soft": "oklch(0.31 0.055 232)",
  "--state-conflict": "oklch(0.71 0.17 27)",
  "--state-conflict-soft": "oklch(0.32 0.08 25)",
  "--state-settled": "oklch(0.74 0.13 160)",
  "--state-settled-soft": "oklch(0.3 0.06 160)",
};

/** Tokens an earlier language carried and Datum does not. */
const REMOVED = [
  "--color-cream",
  "--color-charcoal",
  "--color-offwhite",
  "--color-line",
  "--color-brand-teal",
  "--color-brand-teal-bright",
  "--color-brand-orange",
  "--color-clay",
  "--color-clay-soft",
  "--color-pine",
  "--color-pine-soft",
  "--shadow-btn",
  "--shadow-focus",
  "--shadow-pop",
  // Dropped along the way. The ruled ground went with the drawing-office
  // look, and the rail's width is the shell's business now that it
  // collapses.
  "--color-grid",
  "--grid",
  "--width-nav",
];

// --- the tests --------------------------------------------------------------

it("publishes exactly the utilities DESIGN.md declares, and no others", () => {
  // One assertion, both directions. A token DESIGN.md declares and the theme
  // lacks shows as missing; a token the theme invented shows as extra.
  //
  // It also pins the type ramp's companions: every size token's line height
  // and letter spacing is transcribed above, and `--text-lead` declares no
  // letter spacing, so adding one to it fails here.
  expect(theme).toEqual(THEME_BLOCK);
});

it("overrides exactly the HeroUI variables DESIGN.md names", () => {
  // Dark is `:root`, so it carries the geometry and light inherits it.
  const expected = [
    ...PALETTE,
    ...Object.keys(GEOMETRY),
    ...Object.keys(STATES_DARK),
  ].sort();
  expect(Object.keys(dark).sort()).toEqual(expected);

  // Light redeclares the palette and the states and nothing else. A radius
  // that differed between the two themes would be two design languages, so
  // this asserts the geometry is absent rather than merely equal.
  expect(Object.keys(light).sort()).toEqual(
    [...PALETTE, ...Object.keys(STATES_LIGHT)].sort(),
  );
  for (const name of Object.keys(GEOMETRY)) {
    expect(light, `the light theme redeclares ${name}`).not.toHaveProperty(name);
  }
});

it("carries the geometry and the state colours DESIGN.md sets out", () => {
  for (const [name, value] of Object.entries(GEOMETRY)) {
    expect(dark[name], name).toBe(value);
  }
  for (const [name, value] of Object.entries(STATES_LIGHT)) {
    expect(light[name], `${name}, light`).toBe(value);
  }
  for (const [name, value] of Object.entries(STATES_DARK)) {
    expect(dark[name], `${name}, dark`).toBe(value);
  }
});

it("names its state colours after the six field states, not after strings", () => {
  // A hand-typed state name is the bug this catches. A JS config could
  // generate its keys from FIELD_STATES; CSS cannot, so the check lives
  // here and reads the file instead. A seventh state, or a rename, fails in
  // three places at once.
  const expected = FIELD_STATES.flatMap((state) => [
    `--state-${state}`,
    `--state-${state}-soft`,
  ]).sort();

  const declared = (names: string[]) =>
    names.filter((name) => name.startsWith("--state-")).sort();

  expect(declared(Object.keys(light))).toEqual(expected);
  expect(declared(Object.keys(dark))).toEqual(expected);
  expect(
    Object.keys(theme)
      .filter((name) => name.startsWith("--color-state-"))
      .sort(),
  ).toEqual(expected.map((name) => name.replace("--state-", "--color-state-")));
});

it("does not carry a token the design language dropped", () => {
  const names = [...Object.keys(theme), ...Object.keys(light), ...Object.keys(dark)];
  for (const gone of REMOVED) {
    expect(names, `${gone} survived into Datum`).not.toContain(gone);
  }
});

it("keeps every colour in a wide gamut space, so the two themes stay comparable", () => {
  // Datum is written in oklch throughout. That is not decoration: the state
  // colours were picked by holding lightness and chroma steady and moving
  // only the hue, which is the property that makes the six read as one
  // family, and it is only expressible in a perceptual space. A hex or an
  // rgb() creeping in would break the family quietly.
  const colours = [
    ...Object.entries(light),
    ...Object.entries(dark),
  ].filter(([name]) => !name.endsWith("-shadow") && !name.startsWith("--backdrop"));

  for (const [name, value] of colours) {
    if (!/^(oklch|var|color-mix|\d|none)/.test(value)) {
      expect.fail(`${name} is ${value}, which is not oklch or a reference`);
    }
  }
});
