#!/usr/bin/env bash
# Links every plugin in this repository into your Claude Code skills
# directory, so Claude Code loads it on the next session.
#
# Usage: ./install.sh
#
# Run it from anywhere; it works out its own location. It links, it does
# not copy, so `git pull` in this clone updates every plugin at once.
#
# Claude Code loads any folder under ~/.claude/skills that holds a
# .claude-plugin/plugin.json as a plugin, named `<plugin>@skills-dir`.
# That is the whole mechanism. There is no marketplace and no install
# command, and access to a plugin is access to this repository.
#
# It is idempotent. A link already pointing at the right plugin is left
# alone. A link pointing somewhere else is replaced. A real directory in
# the way stops the script rather than being overwritten.

set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skills_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"

mkdir -p "$skills_dir"

linked=0
for plugin_dir in "$repo"/plugins/*/; do
    plugin_dir="${plugin_dir%/}"
    name="$(basename "$plugin_dir")"

    if [ ! -f "$plugin_dir/.claude-plugin/plugin.json" ]; then
        echo "$name: skipped, no .claude-plugin/plugin.json"
        continue
    fi

    link="$skills_dir/$name"

    if [ -L "$link" ]; then
        if [ "$(readlink "$link")" = "$plugin_dir" ]; then
            echo "$name: ok, already linked"
            linked=$((linked + 1))
            continue
        fi
        rm "$link"
        ln -s "$plugin_dir" "$link"
        echo "$name: was linked elsewhere, now linked to $plugin_dir"
        linked=$((linked + 1))
        continue
    fi

    if [ -e "$link" ]; then
        echo "$name: a real directory is at $link, stopping" >&2
        echo "Move it aside and run this again." >&2
        exit 1
    fi

    ln -s "$plugin_dir" "$link"
    echo "$name: linked to $plugin_dir"
    linked=$((linked + 1))
done

if [ "$linked" -eq 0 ]; then
    echo "Nothing linked. Is $repo/plugins empty?" >&2
    exit 1
fi

echo
echo "Linked $linked plugin(s) into $skills_dir."
echo "Restart Claude Code, then run: claude plugin list"
