# The branch rule

## One branch per milestone, one name across two repositories

A milestone opens one branch in the backend and one in the frontend. Both
carry the milestone id as their name, and the two names are identical. So
`m01` in the backend and `m01` in the frontend are the same piece of work,
and anyone can see that without asking.

The record repository opens nothing. It is always on main.

## The backend merges first

Open the frontend pull request only once the backend one it needs has merged.

The reason is the generated client. The frontend builds its API client from
the backend's committed API description. A frontend branch can be green
against a backend branch and red against main, because the description it
built against has not landed yet. Merging the backend first removes that
window.

Where the generated client records the backend commit it was built from, a
mismatch is at least visible. It is still a mismatch.

A milestone that touches only one repository merges that one and nothing
else. The order only matters where both move.

## The tag

A delivery is tagged `dN-DDMMYY` in both code repositories. `d3-120326` is
the third delivery, on 12 March 2026. Not every milestone is a delivery, and
one delivery may cover several milestones.

## One agent per checkout

Two agents on one repository means two worktrees. Never share a working tree
and never share a test database.

Never run `git stash`, `git checkout .` or `git reset --hard`. One agent
running `git stash` to check whether a failure pre-dated its own change took
two other agents' work with it.

Work is invisible to a running stack until it merges to main, because the
containers mount the primary checkout only. A change that looks missing in
the browser is usually a change sitting in a worktree.

## What each CLAUDE.md says

Each repository's CLAUDE.md states the rules that govern that repository: its
layering, its branch rule, its merge order, its tests, its ports. The
umbrella's CLAUDE.md says only where things are, and points at the other
three. A rule stated twice is a rule that will disagree with itself.
