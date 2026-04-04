#!/bin/bash
# plugin.sh — Claude Config Plugin Manager
# Kullanım:
#   plugin.sh list                    — kurulu + mevcut pluginler
#   plugin.sh install <id|repo_url>   — plugin kur
#   plugin.sh remove <id>             — plugin kaldır
#   plugin.sh update <id>             — güncelle
#   plugin.sh info <id>               — detay

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$SCRIPT_DIR/config/plugin-registry.json"
INSTALLED_FILE="$HOME/.claude/plugins/installed.json"
mkdir -p "$HOME/.claude/plugins"
[ ! -f "$INSTALLED_FILE" ] && echo '{}' > "$INSTALLED_FILE"

python3 "$SCRIPT_DIR/config/plugin_manager.py" "$SCRIPT_DIR" "$@"
