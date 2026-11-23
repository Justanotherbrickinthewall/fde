#!/usr/bin/env bash
# Links the umbrella's shared files to the copies kept in the docs
# repository, the way .claude/skills used to link to fde-docs/skills.
#
# Usage: bootstrap.sh [docs-name]
#
# Run this with the working directory set to the docs repository (or a
# worktree of it) -- this script now ships in the fde plugin, so it no
# longer lives inside the repository it links.
#
# The umbrella root is worked out from git: the docs checkout's .git
# directory always sits two levels below the umbrella
# (<umbrella-root>/<docs-name>/.git), and `git rev-parse
# --git-common-dir` points at that same .git directory whether this
# script runs from the main checkout or from a linked worktree such as
# `.claude/worktrees/<docs-name>-workbooks`. That makes one formula work
# unmodified in both places, run from either.
#
# The docs repository's folder name is never assumed to be "fde-docs" or
# any other fixed name. It comes from `.engagement`'s `docs=` line when
# that file already exists at the umbrella root, or from the argument
# otherwise. fde:init runs this script before writing `.engagement`, so
# it always passes the name on that first run; a later, idempotent
# re-run needs no argument.
#
# Every link it creates is relative, so a link survives the whole
# umbrella being moved or cloned elsewhere, which matters once this same
# script runs against a cloned template.
#
# It is idempotent. A link that already points at the right relative
# target is left alone. A real file at the target is moved to <name>.bak
# once; if a .bak already exists, the script stops rather than overwrite
# it. A link pointing somewhere else is replaced. settings.local.json is
# never touched.
#
# A name whose source does not exist yet under umbrella/ (settings.json,
# until something is copied there) is skipped rather than linked, so the
# script never leaves a dangling link.

set -euo pipefail

# The umbrella root: worked out from the current directory via git, the
# same two-levels-below-umbrella formula as before. If git cannot answer
# (no repository at all, git missing), fall back to the current
# directory's own parent, which is correct for a plain, non-worktree
# checkout.
start_dir="$(pwd)"
common_git_dir=""
if command -v git >/dev/null 2>&1; then
    common_git_dir="$(git -C "$start_dir" rev-parse --git-common-dir 2>/dev/null || true)"
fi
if [ -n "$common_git_dir" ]; then
    case "$common_git_dir" in
        /*) : ;;
        *) common_git_dir="$start_dir/$common_git_dir" ;;
    esac
    main_checkout="$(cd "$(dirname "$common_git_dir")" && pwd)"
    root="$(dirname "$main_checkout")"
else
    root="$(dirname "$start_dir")"
fi
root="$(cd "$root" && pwd)"

# The docs repository's folder name: from .engagement when it already
# exists at the umbrella root, else from the argument.
docs_name=""
if [ -f "$root/.engagement" ]; then
    docs_name="$(sed -n 's/^docs=\(.*\)$/\1/p' "$root/.engagement" | head -n1)"
fi
if [ -z "$docs_name" ]; then
    if [ "$#" -ge 1 ]; then
        docs_name="$1"
    else
        echo "bootstrap.sh: no .engagement at $root and no docs name given" >&2
        exit 1
    fi
fi
docs="$root/$docs_name"
if [ ! -d "$docs" ]; then
    echo "bootstrap.sh: $docs is not a directory" >&2
    exit 1
fi

# The relative path from directory <from> to path <to>. Both must
# already be absolute, canonical paths (no "." or ".." components),
# which is what "cd ... && pwd" produces everywhere else in this script.
relpath() {
    from="$1"
    to="$2"

    IFS='/' read -r -a from_parts <<< "$from"
    IFS='/' read -r -a to_parts <<< "$to"

    common=0
    max=${#from_parts[@]}
    if [ "${#to_parts[@]}" -lt "$max" ]; then
        max=${#to_parts[@]}
    fi
    i=0
    while [ "$i" -lt "$max" ] && [ "${from_parts[$i]}" = "${to_parts[$i]}" ]; do
        common=$((i + 1))
        i=$((i + 1))
    done

    rel=""
    up=$(( ${#from_parts[@]} - common ))
    j=0
    while [ "$j" -lt "$up" ]; do
        rel="../$rel"
        j=$((j + 1))
    done

    k=$common
    while [ "$k" -lt "${#to_parts[@]}" ]; do
        rel="$rel${to_parts[$k]}"
        k=$((k + 1))
        if [ "$k" -lt "${#to_parts[@]}" ]; then
            rel="$rel/"
        fi
    done

    printf '%s\n' "$rel"
}

# Link <link_path> to <target_abs> (an absolute path), using the
# relative form, reporting one line of what it did. The idempotency
# check compares the raw symlink text against that same relative form,
# since this script only ever writes relative links.
#
# Skips a name whose source does not exist under umbrella/ yet, rather
# than creating a link with nothing at the other end of it.
link_one() {
    link_path="$1"
    target_abs="$2"
    label="$3"
    source_desc="$4"

    if [ ! -e "$target_abs" ]; then
        echo "$label: skipped, $source_desc does not exist"
        return
    fi

    target_rel="$(relpath "$(dirname "$link_path")" "$target_abs")"

    if [ -L "$link_path" ]; then
        current="$(readlink "$link_path")"
        if [ "$current" = "$target_rel" ]; then
            echo "$label: ok, already linked to $target_rel"
            return
        fi
        rm "$link_path"
        ln -s "$target_rel" "$link_path"
        echo "$label: was linked elsewhere, now linked to $target_rel"
        return
    fi

    if [ -e "$link_path" ]; then
        backup="${link_path}.bak"
        if [ -e "$backup" ]; then
            echo "$label: a real file is at $link_path and $backup already exists, stopping" >&2
            exit 1
        fi
        mv "$link_path" "$backup"
        ln -s "$target_rel" "$link_path"
        echo "$label: backed up the existing file to $backup, now linked to $target_rel"
        return
    fi

    ln -s "$target_rel" "$link_path"
    echo "$label: linked to $target_rel"
}

for name in CLAUDE.md justfile docker-compose.yml .env.example; do
    link_one "$root/$name" "$docs/umbrella/$name" "$name" "umbrella/$name"
done

mkdir -p "$root/.claude"
link_one "$root/.claude/settings.json" "$docs/umbrella/settings.json" "settings.json" "umbrella/settings.json"
link_one "$root/.claude/skills" "$docs/skills" "skills" "skills"
