#!/usr/bin/env bash
# Builds an engagement's umbrella, its repositories and its .engagement file.
#
# Usage:
#   scaffold.sh --slug <slug> --umbrella <path> \
#               [--org <github-org>] \
#               [--docs-template <owner/repo | local path>] \
#               [--be <url | path | reference | none>] \
#               [--fe <url | path | reference | none>]
#
# fde:init phase 1 calls this and nothing else does. The skill holds the
# conversation; this script holds the mechanics, so the mechanics can be
# tested without a conversation.
#
# --docs-template defaults to templates/docs inside the plugin. --org is
# needed only when the docs template is written as owner/repo.
#
# What it does, in order:
#
#   1. Makes the umbrella folder if it is missing.
#   2. Makes <slug>-docs from the docs template. With none given, the
#      template bundled in the plugin is copied. A template written as
#      owner/repo goes through `gh repo create --template --clone` when gh
#      is signed in. A template that is a local directory is copied and
#      `git init` runs in the copy.
#   3. Makes <slug>-be and <slug>-fe the same way, when given. The word
#      `reference` means PeopleEquation/fde-be or PeopleEquation/fde-fe.
#   4. Renames fde-docs, fde-be, fde-fe and fde-os inside every text file
#      in <slug>-docs, umbrella/ included. It skips .git and binaries.
#   5. Writes .engagement at the umbrella root, with an empty `stack=`.
#      ADR-001 fills that in later.
#   6. Makes my-sessions/ with a README. When ~/.claude-shared exists, the
#      folder is ~/.claude-shared/records/<slug>/ and my-sessions is a link
#      to it.
#   7. Writes a CLAUDE.md map in <docs>/umbrella/ and a stub in each code
#      repository, never over one that exists.
#   8. Runs bootstrap.sh, which links the umbrella's shared files.
#
# It prints one line for each of those.
#
# It runs once per engagement. Step 2 refuses an existing <slug>-docs and
# stops the script there, rather than merging into one, so a whole re-run
# never gets past that check. Step 1 is the only step before it, and an
# umbrella that already exists is left alone.

set -euo pipefail

slug=""
org=""
umbrella=""
docs_template=""
be_spec=""
fe_spec=""

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_root="$(dirname "$script_dir")"

usage() {
    sed -n '2,37p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

die() {
    echo "scaffold.sh: $1" >&2
    exit 1
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --slug) slug="${2:-}"; shift 2 ;;
        --org) org="${2:-}"; shift 2 ;;
        --umbrella) umbrella="${2:-}"; shift 2 ;;
        --docs-template) docs_template="${2:-}"; shift 2 ;;
        --be) be_spec="${2:-}"; shift 2 ;;
        --fe) fe_spec="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) die "unknown argument $1" ;;
    esac
done

[ -n "$slug" ] || die "--slug is required"
[ -n "$umbrella" ] || die "--umbrella is required"
[ -n "$docs_template" ] || docs_template="$plugin_root/templates/docs"

case "$slug" in
    *[!a-z0-9-]*) die "the slug is lowercase letters, digits and dashes only" ;;
esac

command -v git >/dev/null 2>&1 || die "git is not on the path"

gh_ready() {
    command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1
}

# Copy a directory into a new one, leaving .git and __pycache__ behind.
copy_tree() {
    local src="$1" dest="$2"
    mkdir -p "$dest"
    ( cd "$src" && tar cf - --exclude .git --exclude __pycache__ . ) \
        | ( cd "$dest" && tar xf - )
}

# git init, on main where this git can name the branch.
init_repo() {
    local dir="$1"
    if ! git init -q -b main "$dir" 2>/dev/null; then
        git init -q "$dir"
        git -C "$dir" symbolic-ref HEAD refs/heads/main
    fi
}

# ---------------------------------------------------------------- umbrella

if [ -d "$umbrella" ]; then
    echo "umbrella: ok, $umbrella already exists"
else
    mkdir -p "$umbrella"
    echo "umbrella: created $umbrella"
fi
umbrella="$(cd "$umbrella" && pwd)"

if [ -d "$umbrella/.git" ]; then
    die "$umbrella holds a .git directory, and the umbrella never does"
fi

# ------------------------------------------------------------------- docs

docs_name="$slug-docs"
docs_dir="$umbrella/$docs_name"

[ ! -e "$docs_dir" ] || die "$docs_dir already exists, and this script will not overwrite it"

if [ -d "$docs_template" ]; then
    docs_template="$(cd "$docs_template" && pwd)"
    copy_tree "$docs_template" "$docs_dir"
    init_repo "$docs_dir"
    echo "$docs_name: copied from $docs_template, and git init ran in the copy"
elif [[ "$docs_template" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
    [ -n "$org" ] || die "--org is required when --docs-template is owner/repo"
    gh_ready || die "the template $docs_template is a GitHub repository and gh is not signed in"
    ( cd "$umbrella" && gh repo create "$org/$docs_name" --private --template "$docs_template" --clone >/dev/null )
    [ -d "$docs_dir" ] || die "gh repo create did not leave $docs_dir behind"
    echo "$docs_name: created $org/$docs_name from the template $docs_template, and cloned it"
else
    die "--docs-template is neither a directory nor owner/repo: $docs_template"
fi

# --------------------------------------------------------- code repositories

# Places one code repository and sets `placed` to its folder name, or to
# the empty string when the spec asked for none.
placed=""
place_code_repo() {
    local kind="$1" spec="$2"
    local name="$slug-$kind"
    local dir="$umbrella/$name"
    placed=""

    case "$spec" in
        ""|none)
            echo "$name: none for now, and .engagement leaves the line empty"
            return 0
            ;;
    esac

    if [ -e "$dir" ]; then
        echo "$name: ok, $dir already exists"
        placed="$name"
        return 0
    fi

    local is_reference="no"
    if [ "$spec" = "reference" ]; then
        spec="PeopleEquation/fde-$kind"
        is_reference="yes"
    fi

    if [ -d "$spec" ]; then
        spec="$(cd "$spec" && pwd)"
        copy_tree "$spec" "$dir"
        init_repo "$dir"
        echo "$name: copied from $spec, and git init ran in the copy"
    elif [[ "$spec" =~ ^(https?://|git@|ssh://) ]]; then
        git clone -q "$spec" "$dir"
        echo "$name: cloned from $spec"
    elif [[ "$spec" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
        if gh_ready; then
            gh repo clone "$spec" "$dir" -- -q
        else
            git clone -q "https://github.com/$spec.git" "$dir"
        fi
        echo "$name: cloned from $spec, and its remote still points there"
    else
        die "--$kind is neither a directory, a URL, owner/repo, reference nor none: $spec"
    fi

    # The reference implementation is somebody else's repository. Drop the
    # remote, so a stray push from this engagement cannot reach it. The pod
    # adds the engagement's own remote before its first push.
    if [ "$is_reference" = "yes" ]; then
        git -C "$dir" remote remove origin 2>/dev/null || true
        echo "$name: removed the origin remote, so no push can reach $spec"
    fi

    placed="$name"
}

place_code_repo be "$be_spec"
be_name="$placed"

place_code_repo fe "$fe_spec"
fe_name="$placed"

# ----------------------------------------------------------------- renaming

# Rewrites the four template names inside every text file under a
# directory. .git is skipped, and grep -I skips anything binary.
changed=0
while IFS= read -r -d '' f; do
    grep -Iq . "$f" 2>/dev/null || continue
    grep -Eq 'fde-(docs|be|fe|os)' "$f" || continue
    tmp="$(mktemp)"
    sed -e "s/fde-docs/$slug-docs/g" \
        -e "s/fde-be/$slug-be/g" \
        -e "s/fde-fe/$slug-fe/g" \
        -e "s/fde-os/$slug/g" \
        "$f" > "$tmp"
    cat "$tmp" > "$f"
    rm -f "$tmp"
    changed=$((changed + 1))
done < <(find "$docs_dir" -name .git -prune -o -type f -print0)

echo "names: rewrote fde-docs, fde-be, fde-fe and fde-os in $changed files under $docs_name"

# --------------------------------------------------------------- .engagement

plugin_version="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    "$plugin_root/.claude-plugin/plugin.json" 2>/dev/null | head -n1)"
[ -n "$plugin_version" ] || plugin_version="unknown"

cat > "$umbrella/.engagement" <<ENGAGEMENT
slug=$slug
docs=$docs_name
be=$be_name
fe=$fe_name
stack=
plugin_version=$plugin_version
plugin_root=$plugin_root
apps=
record=
merge_into=
integration=
release=
worktree=
ENGAGEMENT

echo ".engagement: written at $umbrella/.engagement, with stack empty"

# --------------------------------------------------------------- my-sessions

sessions_dir="$umbrella/my-sessions"
if [ -e "$sessions_dir" ] || [ -L "$sessions_dir" ]; then
    echo "my-sessions: ok, $sessions_dir already exists"
elif [ -d "$HOME/.claude-shared" ]; then
    mkdir -p "$HOME/.claude-shared/records/$slug"
    ln -s "$HOME/.claude-shared/records/$slug" "$sessions_dir"
    echo "my-sessions: linked $sessions_dir to $HOME/.claude-shared/records/$slug"
else
    mkdir -p "$sessions_dir"
    echo "my-sessions: created $sessions_dir"
fi

if [ ! -f "$sessions_dir/README.md" ]; then
    cat > "$sessions_dir/README.md" <<SESSIONS
# my-sessions

This folder holds the session records for the $slug engagement. Each session
writes one folder here, and that folder is its working memory: what arrived,
what phase it reached, what it decided and what it left for the next person.
It has no git and it is kept on this machine only. It is never the source of
truth, and $docs_name never links to a file in it. Anything that has to
outlive the session gets extracted into the record instead.
SESSIONS
    echo "my-sessions: wrote $sessions_dir/README.md"
fi

# ---------------------------------------------------------------- CLAUDE.md

mkdir -p "$docs_dir/umbrella"
if [ ! -e "$docs_dir/umbrella/CLAUDE.md" ]; then
    {
        echo "# $slug umbrella"
        echo
        echo "This file is a map. It holds no rules. Each repository's own CLAUDE.md"
        echo "holds the rules for that repository."
        echo
        echo "- $docs_name: the record. Run record commands from here. See $docs_name/CLAUDE.md."
        [ -z "$be_name" ] || echo "- $be_name: the backend. Run backend commands from here. See $be_name/CLAUDE.md."
        [ -z "$fe_name" ] || echo "- $fe_name: the frontend. Run frontend commands from here. See $fe_name/CLAUDE.md."
        echo
        echo "Session records are in my-sessions/. Run git commands inside a"
        echo "repository, never at this level, because the umbrella is not one."
    } > "$docs_dir/umbrella/CLAUDE.md"
    echo "CLAUDE.md: wrote $docs_dir/umbrella/CLAUDE.md"
fi

for repo in "$be_name" "$fe_name"; do
    [ -n "$repo" ] || continue
    if [ ! -e "$umbrella/$repo/CLAUDE.md" ]; then
        printf '# %s\n\nThe branch rule is in [BRANCHING.md](BRANCHING.md).\n' "$repo" > "$umbrella/$repo/CLAUDE.md"
        echo "CLAUDE.md: wrote $umbrella/$repo/CLAUDE.md"
    fi
done

# ----------------------------------------------------------------- bootstrap

echo "bootstrap:"
( cd "$docs_dir" && "$script_dir/bootstrap.sh" "$docs_name" ) | sed 's/^/  /'

echo "done: the umbrella is $umbrella, and init phase 2 starts the conventions"
