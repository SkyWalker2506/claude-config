# Antigravity (agy) tarafi

Bu dizin **Antigravity'nin bizim yazdigimiz konfigurasyonudur.** Google'in kendi
kurulu skill'leri (`bigquery-*`, `gcp-*`, `dbt-*`, `antigravity-guide` …) buraya
girmez — onlar Antigravity ile birlikte gelir ve `install.sh` onlara dokunmaz.

```
gemini/AGENTS.md          ->  ~/.gemini/config/AGENTS.md        (global kurallar)
gemini/skills/<ad>/       ->  ~/.gemini/config/skills/<ad>/      (bizim skill'ler)
~/Projects/img2threejs    ->  ~/.gemini/config/skills/img2threejs (symlink)
```

`./install.sh` bu esleme icin yeterlidir; `--skip-gemini` ile atlanir.

## Neden Claude'unkinden ayri dosyalar

Ayni ismi tasiyan `prototype` skill'i iki tarafta **ayni sey degildir**. Antigravity
surumu kendi araclarini kullanir — `generate_image`, `define_subagent`,
`invoke_subagent`, `/teamwork-preview` — ve Claude'un `Agent` tool'unu bilmez.
Claude surumu `global/skills/prototype/` altindadir. Birini digerine kopyalama.

| Skill | Nerede | Not |
|---|---|---|
| `prototype-full` | **sadece Antigravity** | uctan uca otonom orkestrator, coklu ajan |
| `prototype` | iki tarafta, ayri metin | zanaat kurallari |
| `goal` | iki tarafta, ayri metin | kabul kriteri dongusu |
| `img2threejs` | symlink, tek checkout | iki host ayni kodu kosar |
