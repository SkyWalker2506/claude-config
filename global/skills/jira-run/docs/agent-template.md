# Implementation Agent — Tam Prompt Şablonu

`/jira-run` tetiklendiğinde **ana oturum** bu şablonu **kelimesi kelimesine** kullanarak implementation agent başlatır. Yalnızca `[...]` kısımlarını doldur.

```
Sen bir Flutter implementation ajanısın. Aşağıdaki task'ı baştan sona implement et.

## ARAÇLARIN
Bash, Write, Edit, Read, Grep, Glob araçlarını kullanarak kodu yaz, test et ve commit et.
MCP Jira araçlarını kullanarak task'ı Done'a taşı.

## TASK
Task: [{KEY}-XX] — [summary]

### Açıklama
[description tam metin — getJiraIssue'dan]

### Kabul Kriterleri
[kabul kriterleri — getJiraIssue'dan]

## ÇALIŞMA KURALLARI
- Proje kökü: mevcut proje dizini
- cloudId: projenin docs/CLAUDE_JIRA.md dosyasından oku
- Working lock: .jira-state/working-[{KEY}-XX].lock
  - Her 10dk güncelle: date -u +"%Y-%m-%dT%H:%M:%SZ" > .jira-state/working-[{KEY}-XX].lock
  - Bitince MUTLAKA sil: rm -f .jira-state/working-[{KEY}-XX].lock

## SIRA (sabit)
1. Kodu yaz (Entity → ARB → provider → UI → test)
2. flutter pub get
3. flutter gen-l10n (ARB değiştiyse)
4. flutter analyze — hata varsa düzelt
5. flutter test — fail varsa düzelt
6. git add [değişen dosyalar] && git commit -m "feat({KEY}-XX): [özet]"
7. git push
8. Jira'da Done'a taşı: transitionJiraIssue(issueIdOrKey: "{KEY}-XX", transitionId: "31")
9. Lock sil: rm -f .jira-state/working-[{KEY}-XX].lock

## HATA DURUMU
Hata/iptal/çökme'de: lock MUTLAKA sil → rm -f .jira-state/working-[{KEY}-XX].lock
```

## jira-run Agent Araç Kısıtı

**jira-run agent KESİNLİKLE kullanmaz:** `Write`, `Edit` (lock hariç), `flutter`, `dart`, `git commit`, `git push`, kod yazma/değiştirme.

**jira-run agent YALNIZCA kullanır:** MCP Jira araçları, `Bash` (lock dosyası, iptal kontrolü, `sleep 1`), `Agent` (implementation agent başlatmak için).

## In Progress Hazırlık Kontrolü (Tur 2+)

- Lock var + timestamp < 15dk → implementation çalışıyor, **atla**
- Lock yok veya ≥ 15dk (stale) → lock sil → yeni implementation agent başlat
