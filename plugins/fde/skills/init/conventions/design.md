# Design

## What this layer is

Every screen in the product should look like it came from one place. This
layer is how that happens. One file holds every colour, every corner, every
type size and every spacing step the product may use. Screens do not invent
values; they spend the ones that file declares. A second file, in prose,
says what each value means and when it is used. The two are checked against
each other by a test, so the written rules and the live values cannot drift
apart. The fonts ship inside the application, so a screen showing a client's
own figures never opens a request to somebody else's server.

## The rules

1. One token file holds every design value, and no design value is declared
   anywhere else.
2. No colour literal appears outside the token file.
3. No raw pixel or rem size appears outside the token file.
4. The six field states are declared once, each as a foreground and a soft
   ground, in every palette the product ships.
5. Colour carries one meaning, which is the state of a field, and nothing
   else in the product is saturated.
6. Component styling is written in one package, or one directory, and the
   screens only compose what it exports.
7. A written design document sits beside the token file and says what each
   token means.
8. Fonts and icons are vendored into the bundle rather than fetched from a
   third-party host.
9. The application fetches nothing from a third-party host at run time.
10. A test reads the token file against the design document in both
    directions, so a token either one lacks fails the build.
11. A test scans the frontend and fails on a stray colour, a stray size, an
    inline style, or a second stylesheet.

The six states are `open`, `awaiting`, `inferred`, `entered`, `conflict` and
`settled`. They mean nothing recorded, blocked on a person, the machine
proposed it, a person recorded it, two sources disagree, and signed off.

## The checklist

1. Is there exactly one token file, and does the design document name it?
   Read the design document and look for the file it points at.
2. Does a search for a hex colour outside that file come back empty?
   `grep -rniE '#[0-9a-f]{3}([0-9a-f]{3})?\b' <frontend source>`, ignoring
   the token file and comments.
3. Does a search for a hard-coded pixel or rem size outside that file come
   back empty? On a utility-class frontend,
   `grep -rnE '\-\[-?[0-9.]+(px|rem)\]' <frontend source>`. Otherwise
   `grep -rnE '[0-9](px|rem)\b' <frontend source> --exclude=<token file>`,
   which has to exclude the token file because that file is where every size
   is declared.
4. Are the six field states declared once each, with a foreground and a soft
   ground, in every palette? Read the token file.
5. Does the token file declare zero colour tokens beyond the six states, the
   one accent, the status trio and the neutral ramp? List every colour
   declaration with `grep -nE '^\s*--[a-z-]+:\s*(oklch|rgb|hsl|#)' <token
   file>` and count what is left over. Expect zero.
6. Is there a written design document beside the token file? Look for
   `DESIGN.md` or the equivalent in the same package, or directory.
7. Does a test read the token file against that document and fail on a token
   either one lacks? Run the suite and look for the token test by name.
8. Does a test fail on a stray colour, a stray size, an inline style or a
   second stylesheet? Run the suite and look for the stray-styles test.
9. Are the font files committed in the repository? `ls` the vendored fonts
   folder, and check a licence file sits beside them.
10. Does the source name no third-party host? `grep -rn "https://"` over the
    frontend source and the built bundle.
11. Is component markup confined to one package, or one directory? Count the
    styling attributes in the screens directory with
    `grep -rcE 'className=|class=|style=' <screens directory>`. Expect zero.

## Reference

The files under `design/reference/` come from `fde-fe`, the React and Vite
reference implementation. It uses Tailwind and HeroUI, so the enforcement
reads CSS custom properties. Another stack declares its tokens differently
and the rules above still hold.

- `DESIGN.md` — the written design language. It states the five rules, the
  six field states, the type pairing and what the tests hold. React, Vite,
  Tailwind, HeroUI.
- `theme.css` — the token file itself. Every colour, radius, type size,
  shadow and motion value, in two palettes. Same stack.
- `no-stray-styles.test.ts` — the test behind rule 11. It scans both
  frontend packages. It fails on a hex, an arbitrary pixel or rem size, an
  inline style, a second stylesheet, or markup written in the screens
  package. Vitest, in the same stack.
- `design-tokens.test.ts` — the test behind rule 10. It parses the token file
  and checks it against the design document, in both directions and in both
  palettes. Vitest, in the same stack.

`DESIGN.md` names three more files that are not carried here:
`field-states.ts`, `shell.test.tsx` and `design-build.test.ts`. The first
holds the six state names in code, and the other two test the shell and the
built bundle. Read them in `fde-fe` if you want them.
