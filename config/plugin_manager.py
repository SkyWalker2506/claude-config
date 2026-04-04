#!/usr/bin/env python3
"""Claude Config Plugin Manager"""
import json, sys, os, subprocess
from datetime import datetime

script_dir  = sys.argv[1]
action      = sys.argv[2] if len(sys.argv) > 2 else "list"
arg         = sys.argv[3] if len(sys.argv) > 3 else ""

registry_path  = os.path.join(script_dir, "config", "plugin-registry.json")
installed_path = os.path.expanduser("~/.claude/plugins/installed.json")
plugins_dir    = os.path.join(script_dir, "plugins")

registry  = json.load(open(registry_path))  if os.path.exists(registry_path)  else {"plugins": {}}
installed = json.load(open(installed_path)) if os.path.exists(installed_path) else {}

def save_installed():
    json.dump(installed, open(installed_path, "w"), indent=2)

def save_registry():
    json.dump(registry, open(registry_path, "w"), indent=2, ensure_ascii=False)

def run_hook(hook_path):
    if os.path.exists(hook_path):
        subprocess.run(["bash", hook_path])

# ── list ──────────────────────────────────────────────────────────────────────
if action == "list":
    print("\n📦 Claude Config Plugin Marketplace\n")
    print(f"{'ID':<16} {'Ad':<26} {'Kategori':<14} {'Durum':<10} {'Ver'}")
    print("─" * 78)
    for pid, p in sorted(registry["plugins"].items()):
        status = "✅ Kurulu" if pid in installed else "○  Mevcut"
        print(f"{pid:<16} {p['name']:<26} {p['category']:<14} {status:<10} {p['version']}")
    print(f"\n{len(installed)}/{len(registry['plugins'])} plugin kurulu")
    print("Komutlar: plugin.sh [install|remove|update|info] <id>")
    print()

# ── info ──────────────────────────────────────────────────────────────────────
elif action == "info":
    if arg not in registry["plugins"]:
        print(f"❌ Plugin bulunamadı: {arg}"); sys.exit(1)
    p = registry["plugins"][arg]
    print(f"\n{'─'*50}")
    print(f"  {'ID':<16} {arg}")
    for k, v in p.items():
        print(f"  {k:<16} {v}")
    print(f"  {'kurulu':<16} {'✅ Evet' if arg in installed else '○  Hayır'}")
    if arg in installed:
        print(f"  {'kurulum tarihi':<16} {installed[arg].get('installed_at','?')[:10]}")
    print()

# ── install ───────────────────────────────────────────────────────────────────
elif action == "install":
    if arg.startswith("http"):
        repo_name = arg.rstrip("/").split("/")[-1]
        if repo_name.startswith("ccplugin-"):
            repo_name = repo_name[len("ccplugin-"):]
        dest = os.path.join(plugins_dir, repo_name)
        if os.path.exists(dest):
            print(f"⚠️  {repo_name} zaten var. Güncellemek için: plugin.sh update {repo_name}")
        else:
            print(f"⬇️  Klonlanıyor: {arg}")
            r = subprocess.run(["git", "clone", "--quiet", arg, dest])
            if r.returncode != 0:
                print("❌ Clone başarısız."); sys.exit(1)
        pjson = os.path.join(dest, "plugin.json")
        if os.path.exists(pjson):
            p = json.load(open(pjson))
            arg = p["id"]
            registry["plugins"][arg] = {
                "name": p.get("name", arg), "version": p.get("version","0.1.0"),
                "description": p.get("description",""), "category": p.get("category","other"),
                "complexity": p.get("complexity","simple"), "repo": arg,
                "local": f"plugins/{repo_name}"
            }
            save_registry()
        else:
            print("⚠️  plugin.json bulunamadı."); sys.exit(1)

    if arg not in registry["plugins"]:
        print(f"❌ Plugin bulunamadı: {arg}"); sys.exit(1)
    if arg in installed:
        print(f"ℹ  {arg} zaten kurulu."); sys.exit(0)

    p = registry["plugins"][arg]
    local = os.path.join(script_dir, p.get("local", f"plugins/{arg}"))
    print(f"📦 {p['name']} kuruluyor...")
    run_hook(os.path.join(local, "install.sh"))
    installed[arg] = {"version": p["version"], "installed_at": datetime.now().isoformat()}
    save_installed()
    print(f"✅ {p['name']} kuruldu.")

# ── remove ────────────────────────────────────────────────────────────────────
elif action == "remove":
    if arg not in installed:
        print(f"ℹ  {arg} kurulu değil."); sys.exit(0)
    p = registry["plugins"].get(arg, {})
    local = os.path.join(script_dir, p.get("local", f"plugins/{arg}"))
    print(f"🗑  {p.get('name', arg)} kaldırılıyor...")
    run_hook(os.path.join(local, "uninstall.sh"))
    del installed[arg]
    save_installed()
    print("✅ Kaldırıldı.")

# ── update ────────────────────────────────────────────────────────────────────
elif action == "update":
    if arg not in registry["plugins"]:
        print(f"❌ Plugin bulunamadı: {arg}"); sys.exit(1)
    p = registry["plugins"][arg]
    local = os.path.join(script_dir, p.get("local", f"plugins/{arg}"))
    if os.path.exists(os.path.join(local, ".git")):
        print(f"🔄 {p['name']} güncelleniyor...")
        subprocess.run(["git", "-C", local, "pull", "--quiet"])
        run_hook(os.path.join(local, "install.sh"))
        if arg in installed:
            installed[arg]["version"] = p["version"]
            save_installed()
        print("✅ Güncellendi.")
    else:
        print(f"ℹ  {arg} git repo değil.")

else:
    print("Kullanım: plugin.sh [list|install|remove|update|info] [id|url]")
    sys.exit(1)
