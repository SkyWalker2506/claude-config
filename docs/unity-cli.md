# Unity CLI + Pipeline — reference (all projects)

> Unity'yi terminalden yönetmenin ve **çalışan editörü komut/komut-satırından sürmenin** resmi yolu. Unity 6.x ve üzeriyle çalışır. Hub'a alternatif + AI ajan/CI için native köprü. **Deneysel/beta** (2026-07 itibarıyla `0.1.0-beta.7`).
>
> Bu doküman bir referanstır — Unity otomasyonu gereken HER projede geçerlidir (sadece tek proje değil). Ajan bir Unity işini otomatikleştirecekse computer-use ile GUI tıklamak yerine önce bunu değerlendir.

## İki katman

| Katman | Ne | Kurulum | Kapsam |
|---|---|---|---|
| **Unity CLI** (`unity` binary) | Standalone yürütülebilir; Hub'sız editör/modül/proje/auth yönetimi | Sistem geneli install script | Editör indir/sil, proje aç, modül, login, CI |
| **Unity Pipeline** (`com.unity.pipeline`) | Projeye kurulan paket; **çalışan editörde** lokal HTTP API açar | `unity pipeline install` (proje içinde) | `command`, `eval`, `mcp` — canlı editörü sür |

Pipeline paketi olmadan CLI sadece Hub-benzeri yönetim yapar. Paket kurulunca CLI **çalışan editöre** bağlanıp komut çalıştırır, C# eval eder, MCP köprüsü olur. Pipeline batchmode'dan üstündür: **focus yönetimi**, **domain reload** dayanıklılığı, **birden çok editöre** aynı anda bağlanma.

## Kurulum

```bash
# macOS / Linux (Windows'ta PowerShell'den aynı script)
curl -fsSL https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.sh | UNITY_CLI_CHANNEL=beta bash
# terminali kapat-aç, sonra:
unity --version
unity upgrade            # CLI'yi kendini günceller
```

Tek yürütülebilir dosya: macOS/Windows/Linux × x64/Arm64. Beta kanalı; stable henüz yok.

## Editör / proje / modül / auth (Hub yerine)

```bash
unity editors -r                       # indirilebilir sürümler
unity editors -i                       # kurulu editörler   (-i = --installed)
unity editors add /path/to/editor      # elle kurulu editörü kaydet
unity editors default 6000.3.7f1       # varsayılan sürüm

unity install 6000.3.7f1               # sürüm indir
unity install lts -m ios android webgl # modüllerle birlikte
unity install 6000.3.7f1 -c 9b001d489a54   # changeset ile
unity install-modules -e 6000.3.7f1 -m android ios   # sonradan modül ekle
unity install-modules -e 6000.3.7f1 -l               # kurulabilir modülleri listele

unity open ./MyProject                 # projeyi doğru editör sürümüyle aç
unity ./MyProject                      # kısayol (open)
unity projects                         # Hub registry'deki projeler (list/create/clone/link/upgrade)

unity auth login                       # tarayıcı ile giriş (CI için service-account var)
unity auth status
```

Sürüm alias'ları: `latest`, `lts`, `default`, `6`, `6.5`, `2022`.

### Yapısal çıktı + exit code (otomasyon/CI dostu)

```bash
unity editors -i --format json    # veya --json  -> jq'ya uygun
unity editors -i --format tsv     # boru/dosya -> makine-okur
unity editors -i --format human   # renkli, hizalı (varsayılan: interaktif terminal)
unity install 6000.3.7f1 > install.log 2>&1
```

- Hatalar **stderr**'e (stdout veri için temiz kalır); JSON modda `{"error":"..."}`.
- Exit: `0` başarı · `1` genel hata · `130` iptal (Ctrl+C).
- Loglar (macOS): `~/Library/Application Support/UnityHub/logs`.

## Pipeline: çalışan editörü sürmek

```bash
# proje içinde, editör açıkken, login sonrası:
unity pipeline install     # com.unity.pipeline paketini kurar + bağımlılıklar
                           # (editör recompile eder)
unity pipeline list        # doğrulama -> "Pipeline: Installed"
unity status               # bağlı editörler: port, proje yolu, sürüm, PID, bağlantı
```

### `unity command` — editör komutları

```bash
unity command                              # çalışan editörü keşfet + komutları listele
unity command --project-path=<path>        # BELİRLİ projeye bağlan (çoklu editör varsa şart)
unity command --help                       # ~140+ komut
```

Yerleşik komut örnekleri (video + duyurudan; tam liste `unity command --help`):
`open scene`, `editor play` / `editor stop`, `console` (konsolu terminale dök), `search "type:camera"` (JSON döner), `run tests`, `list shaders`, `set serialized field`, `set import settings`, `capture game view`, `create gameobject`/`prefab`, `bake lighting`, `clear console`, `set quality settings`, `set layer`.

```bash
unity command open-scene Scenes/Garden/Garden.unity
unity command editor play
unity command editor stop
unity command console                      # editör konsolunu stdout'a
unity command search "type:camera"         # sahnede ara -> JSON
unity command run-tests
```

### `unity command eval` / `unity eval` — canlı C#

Çalışan editörde **Roslyn ile C# çalıştırır, sonucu döner — project recompile / domain reload YOK.** Diskteki `.cs`'i de eval edebilir. `-executeMethod` batchmode'un canlı, hızlı karşılığı: mevcut menü/builder metodlarını doğrudan çağırabilirsin.

```bash
unity eval "UnityEngine.Debug.Log(UnityEditor.EditorApplication.applicationVersion)"
unity command eval --file ./MyEditorScript.cs
```

### Kendi komutunu tanımla — `[CliCommand]`

Kod tarafında bir metoda `[CliCommand]` attribute'u koyarsan CLI onu bir komut olarak sunar. Yani proje-özel build/pipeline adımlarını (ör. sahne bake, level import, capture) terminalden çağrılabilir komutlara çevirebilirsin.

### `unity mcp` — native MCP köprüsü (ayrı MCP paketi GEREKMEZ)

```bash
unity mcp        # stdio üzerinden MCP sunucusu; client bekler
unity mcp --help
```

Claude Desktop / Cursor / VS Code / MCP Inspector doğrudan bağlanır. Unity 7 yol haritasında **ücretsiz native MCP** olarak geliyor — 3. parti Unity-MCP paketlerine (asmdef sızıntısı, WebGL derdi) ihtiyaç kalmıyor.

### `unity shell` — interaktif REPL

```bash
unity shell      # komutları interaktif yaz; çıkış: exit
```

## ⚠️ GÜVENLİK — makineyi tamamen açar

Pipeline kurulu + bir ajan bağlıysa ajan **her şeyi** yapabilir: Unity kurar/siler, editörde **keyfi C# çalıştırır**, dosya sistemine erişir. `unity eval` = editör süreç ayrıcalıklarıyla rasgele kod. Sadece güvenilen ortamda/agent ile aç; CI'da service-account izinlerini daralt; repo'ya `unity mcp` açık bırakan bir launch bırakma.

## Ne zaman kullan (AI ajan / CI perspektifi)

| İhtiyaç | Eski yol | Unity CLI yolu |
|---|---|---|
| Editörü Play'e al / durdur | computer-use ile tıkla (focus çal, doğru pencere) | `unity command editor play/stop` |
| Sahne aç | GUI'de File>Open | `unity command open-scene ...` |
| Build/menü metodu çağır | `Unity -batchmode -executeMethod X -quit` (~2-4 dk soğuk başlangıç, GUI lockfile çakışır) | `unity eval "X()"` / `[CliCommand]` — **çalışan** editörde, anında |
| Testler | batchmode `-runTests` (2. açılış) | `unity command run-tests` |
| Konsol/hata oku | Editor.log parse | `unity command console` |
| Sahnede nesne ara | — | `unity command search` -> JSON |
| Çoklu editör (yanlış pencereye tıklama) | frontmost tahmini | `--project-path=<path>` ile hedefle |
| AI ajan köprüsü | 3. parti Unity-MCP paketi (asmdef/WebGL sızıntısı) | native `unity mcp` |

**Değerlendirme:** Unity otomasyonunda computer-use + batchmode'un yerini büyük ölçüde alır — özellikle çoklu-editör hedefleme, canlı `eval` (soğuk batchmode başlangıcı yok), ve native MCP (3. parti paket sızıntısı yok). **Deneysel/beta** olduğu için üretim CI'ında dikkatli; ama iç geliştirme/otomasyonda ciddi kazanç.

## Linkler (resmi)

- Giriş: https://docs.unity.com/en-us/unity-cli/unity-cli
- Kullanım: https://docs.unity.com/en-us/unity-cli/use-unity-cli
- Komut referansı: https://docs.unity.com/en-us/unity-cli/unity-cli-reference
- Sürüm notları: https://docs.unity.com/en-us/unity-cli/release-notes
- Pipeline paketi: https://docs.unity.com/en-us/unity-production-pipeline/local-tools-cli/unity-pipeline-package
- Blog (duyuru): https://unity.com/blog/meet-the-unity-cli
- Duyuru/tartışma: https://discussions.unity.com/t/announcing-the-unity-cli-a-new-way-to-connect-your-tools-and-agents/1731104
- Topluluk özeti (GameFromScratch): https://gamefromscratch.com/unity-cli-unity-pipeline-game-changers/

_Kaynak: resmi Unity docs'tan doğrulandı (2026-07). Sürüm/komut ayrıntıları beta ile değişebilir — `unity --help` ve `unity command --help` her zaman kaynak-of-truth._
