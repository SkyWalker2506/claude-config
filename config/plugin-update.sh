#!/bin/bash
# plugin-update.sh — Kurulu plugin'leri güncelle
# Kullanım: plugin-update.sh [plugin-id]
#   plugin-id verilmezse tüm plugin'leri günceller

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"

update_plugin() {
    local plugin_id="$1"
    local plugin_dir="$PLUGINS_DIR/$plugin_id"

    if [ ! -d "$plugin_dir" ]; then
        echo "❌ Plugin bulunamadı: $plugin_id"
        return 1
    fi

    # Git repo ise pull yap
    if [ -d "$plugin_dir/.git" ]; then
        echo "  ↻ $plugin_id (git pull)..."
        git -C "$plugin_dir" pull --quiet && echo "  ✅ $plugin_id" || echo "  ⚠️  $plugin_id pull hatası"
    # install.sh varsa --update ile çalıştır
    elif [ -f "$plugin_dir/install.sh" ]; then
        echo "  ↻ $plugin_id (install.sh --update)..."
        bash "$plugin_dir/install.sh" --update 2>/dev/null && echo "  ✅ $plugin_id" || echo "  ⚠️  $plugin_id güncelleme hatası"
    else
        echo "  ℹ️  $plugin_id — güncelleme yöntemi yok"
    fi
}

if [ -n "$1" ]; then
    update_plugin "$1"
else
    echo "── Plugin Güncelleme ──"
    for plugin_dir in "$PLUGINS_DIR"/*/; do
        [ -d "$plugin_dir" ] || continue
        update_plugin "$(basename "$plugin_dir")"
    done
    echo "── Tamamlandı ──"
fi
