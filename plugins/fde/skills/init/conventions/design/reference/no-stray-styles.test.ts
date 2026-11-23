// Group 3: no stray styles.
//
// The two non-negotiables of the design language, enforced rather than
// hoped for.
//
//   1. Tailwind utilities only. No component CSS class written here, no
//      component CSS file, and one place where component markup is
//      written, which is packages/ui -- so this suite also checks apps/web
//      writes none.
//   2. Every design value is a token. No hard-coded hex, no arbitrary pixel
//      or rem size, no inline style attribute.
//
// Datum changed what rule 1 can mean and it is worth being exact about it.
// HeroUI is component CSS: `@heroui/styles` ships a `.button` and a `.card`
// and Datum leans on them, which is the point of adopting a library. What
// this suite still holds is that none of that is written here. The two
// stylesheets in this repository declare tokens, fonts and base rules, and
// nothing that styles a component by name.

import { readFileSync, readdirSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const UI_SRC = resolve(import.meta.dirname, "..");
const APP_SRC = resolve(import.meta.dirname, "../../../../apps/web/src");
const REPO = resolve(import.meta.dirname, "../../../..");

const SKIP_DIRS = new Set(["__tests__", "vendor", "generated", "node_modules"]);
const SCANNED_EXTENSIONS = [".ts", ".tsx", ".css"];

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) out.push(...walk(join(dir, entry.name)));
    } else if (SCANNED_EXTENSIONS.some((ext) => entry.name.endsWith(ext))) {
      out.push(join(dir, entry.name));
    }
  }
  return out;
}

const SOURCES = [...walk(UI_SRC), ...walk(APP_SRC)];

const named = (path: string) => relative(REPO, path);
const read = (path: string) => readFileSync(path, "utf8");

/**
 * The file with its comments taken out.
 *
 * The value scans below check what ships, and a comment ships nothing. A
 * comment naming a colour in prose -- a brand hex an accent was derived
 * from, say -- is a record worth keeping, and losing it to keep a scan
 * happy would be the wrong trade.
 *
 * Both comment forms, because the scan covers `.ts`, `.tsx` and `.css`. A
 * `//` inside a string is not stripped, which would matter for a URL --
 * `https://...` -- so the line form requires whitespace or a line start in
 * front of it.
 */
const withoutComments = (text: string) =>
  text.replace(/\/\*[\s\S]*?\*\//g, "").replace(/(^|\s)\/\/.*$/gm, "$1");

// A three or six digit hex colour. Every colour is a token in theme.css,
// declared as an oklch value, so a hex anywhere is a colour written outside
// the language.
const HEX = /#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b/;

// A Tailwind arbitrary-value bracket whose whole content is a bare px or rem
// length: w-[37px], mt-[13px], text-[15px], p-[1.5rem]. That is a spacing or
// type value standing in for a token.
//
// Anchoring on the unit is what keeps this precise rather than a blanket
// "no brackets" rule, and it leaves the legitimate arbitrary values alone
// without special-casing them: bg-charcoal/[0.04] has no unit,
// tracking-[-0.01em] and max-w-[42ch] have units that are not px or rem,
// and md:grid-cols-[15rem_1fr] carries more than a length in the bracket, so
// it is layout structure rather than a design token.
const ARBITRARY_PX_OR_REM = /-\[-?\d+(?:\.\d+)?(?:px|rem)\]/g;

// Basecoat's component classes, and the shape of a component CSS rule.
const BANNED_CLASSES = [
  "btn",
  "card",
  "input",
  "form",
  "table",
  "badge",
  "alert",
];

it("still sees a value once the comments are gone", () => {
  // `withoutComments` is doing real work in the scan above, so it needs its
  // own check: a bug there would empty every file and the colour scan would
  // pass by finding nothing at all.
  const theme = withoutComments(read(SOURCES.find((p) => p.endsWith("theme.css")) as string));
  expect(theme).toContain("--accent:");
  expect(theme).toContain("oklch(");

  expect(withoutComments('const a = "x"; // #ffffff')).not.toContain("#ffffff");
  expect(withoutComments('/* #ffffff */ const a = "y";')).not.toContain("#ffffff");
  // A URL is not a comment, and stripping one would be a silent hole.
  expect(withoutComments('src: url("https://a/b.woff2");')).toContain("https://a/b.woff2");
});

it("reads the files it claims to read", () => {
  // Without this the scans below collect nothing and report success while
  // checking nothing. A scan over an empty list always passes.
  expect(SOURCES.length).toBeGreaterThan(8);
  expect(SOURCES.some((path) => path.endsWith("app-shell.tsx"))).toBe(true);
  expect(SOURCES.some((path) => path.endsWith("App.tsx"))).toBe(true);
});

it("hard-codes no colour and no arbitrary pixel or rem size", () => {
  for (const path of SOURCES) {
    const text = withoutComments(read(path));
    expect(HEX.test(text), `${named(path)} hard-codes a colour`).toBe(false);
    expect(
      text.match(ARBITRARY_PX_OR_REM) ?? [],
      `${named(path)} hard-codes an arbitrary size`,
    ).toEqual([]);
  }
});

it("carries no inline style attribute", () => {
  // There is no exception. The avatar takes one size and two utilities, and
  // the dock's width is a custom property rather than an inline style.
  for (const path of SOURCES) {
    const text = read(path);
    expect(/\bstyle\s*=\s*[{"]/.test(text), `${named(path)} has an inline style`).toBe(
      false,
    );
  }
});

it("defines no component CSS", () => {
  const stylesheets = SOURCES.filter((path) => path.endsWith(".css"));
  // Two stylesheets in the frontend and no more. `styles.css` holds the
  // three imports, the vendored font faces and the base rules;
  // `theme.css` holds every token. Nothing else may add one.
  expect(stylesheets.map(named).sort()).toEqual([
    "packages/ui/src/styles.css",
    "packages/ui/src/theme.css",
  ]);

  for (const path of stylesheets) {
    const css = read(path);
    for (const name of BANNED_CLASSES) {
      expect(css.includes(`.${name}`), `${named(path)} defines .${name}`).toBe(
        false,
      );
    }

    // A class selector means component CSS, with one exception, and the
    // exception is named rather than pattern-matched. `.light` and `.dark`
    // are how a palette is chosen, and HeroUI keys its own variables off
    // both of them, so the theme has to write them. Any other class in
    // either file is a component being styled by name.
    const THEME_SELECTORS = new Set([".light", ".dark"]);
    for (const match of css.matchAll(/^\s*(\.[a-z][a-z0-9-]*)/gim)) {
      const selector = match[1] as string;
      expect(
        THEME_SELECTORS.has(selector),
        `${named(path)} styles ${selector} by name`,
      ).toBe(true);
    }
  }
});

it("keeps the tokens in the theme and the rules in the stylesheet", () => {
  // The split is the whole reason there are two files, and without this it
  // would erode inside a week: a colour dropped into styles.css because it
  // was the file already open, and the design language stops having one
  // place again.
  const theme = read(
    SOURCES.find((path) => path.endsWith("theme.css")) as string,
  );
  const styles = read(
    SOURCES.find((path) => path.endsWith("styles.css")) as string,
  );

  // theme.css declares and never imports. styles.css imports and never
  // declares a token of its own.
  expect(theme).not.toMatch(/@import/);
  expect(theme).toMatch(/@theme inline/);
  expect(styles).not.toMatch(/@theme/);

  // A `--token: value` line in styles.css is a token in the wrong file.
  // `var(--token)` reading one is not, so the match is anchored on the
  // colon that makes it a declaration.
  const declarations = [...styles.matchAll(/^\s*(--[a-z0-9-]+)\s*:/gim)].map(
    (match) => match[1],
  );
  expect(declarations, "styles.css declares a token").toEqual([]);
});

it("keeps every component in packages/ui, so apps/web only composes", () => {
  // design.md's rule is "one place for component markup", and the one place
  // is now packages/ui. A className written in apps/web is a component
  // being defined in the wrong package, which is how two design languages
  // start.
  for (const path of walk(APP_SRC)) {
    const text = read(path);
    expect(text.includes("className"), `${named(path)} writes markup`).toBe(false);
    expect(path.endsWith(".css"), `${named(path)} is a stylesheet`).toBe(false);
  }
});
