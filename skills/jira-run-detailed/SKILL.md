---
name: jira-run-detailed
description: Jira board'unu detayli incele ve bakim yap — routing, kalite, oneriler, duzeltmeler. Odak parametrik.
argument-hint: "[odak] — security, ux, performance, tech-debt, test-coverage, accessibility, analytics, l10n, monetization, offline"
disable-model-invocation: true
---

## Ne yapar

Arka plan agent ile **tek seferde** Jira board'unun tum bakimini yapar. Her karti derinlemesine okur, duzeltir, onerir.

**Kapsam (hepsi tek calistirmada):**

1. **Board routing & temizlik** — yanlis durumda kart duzelt, stale IP temizle
2. **Kart kalite kontrolu** — description, kabul kriterleri, priority, label
3. **Kart duzeltmeleri** — eksik description tamamla, yanlis priority/label duzelt
4. **WAITING/BLOCKED analizi** — neden bekliyor, cozum onerisi
5. **Yeni task onerileri** — eksik feature, UX, teknik borc, test coverage
6. **Oncelik siralamasi** — hangi sirayla calisilmali

**Odak verilirse** o perspektiften bakar. **Verilmezse** genel audit + bakim.

## Arguman

| Input | Davranis |
|-------|----------|
| `/jira-run-detailed` | Genel audit + bakim |
| `/jira-run-detailed security` | OWASP, API key, guvenlik |
| `/jira-run-detailed ux` | UX akislari |
| `/jira-run-detailed performance` | Performans |
| `/jira-run-detailed tech-debt` | Teknik borc |
| `/jira-run-detailed test-coverage` | Test kapsami |
| `/jira-run-detailed accessibility` | WCAG, a11y |
| `/jira-run-detailed analytics` | Analytics strateji |
| `/jira-run-detailed l10n` | Coklu dil, RTL |
| `/jira-run-detailed monetization` | Premium, IAP |
| `/jira-run-detailed offline` | Offline sync |
| Herhangi bir konu | O konu odakli |

## Çalıştırma

**Model:** Opus Max — arka plan agent.

**Tek tur:** Döngü değil, tek seferlik derinlemesine analiz + bakım.

Ana oturum şu agent'ı başlatır:

```python
Agent(
  prompt=<aşağıdaki şablon>,
  model="opus",
  run_in_background=True,
  description="jira-run-detailed audit"
)
```

### Agent prompt şablonu

```
Sen bir Jira uzman danismanisin. Projeyi derinlemesine analiz et VE bakimini yap.

Proje bilgisi icin projenin docs/CLAUDE_JIRA.md dosyasini oku — proje anahtari, cloudId, JQL sorgulari oradan alinir.

ODAK: [varsa kullanicinin verdigi odak, yoksa "Genel audit + bakim"]

## ADIMLAR

### 1. TUM aktif kartlari cek (Done HARIC)
Projenin docs/CLAUDE_JIRA.md dosyasindaki JQL sorgularini kullan.
Yoksa genel JQL: project = PROJECT_KEY AND status != Done

### 2. Her kartın DETAYINI oku (getJiraIssue)
Description, acceptance criteria, comments, labels, priority, subtask ilişkileri.

### 3. BOARD ROUTING & TEMİZLİK (hemen uygula)
- IP'de stale kart (lock yok, >1 saat) → WAITING veya To Do'ya taşı
- Yanlış durumda kart → doğru duruma taşı (transition)
- Tüm subtask'ları Done olan parent → Done'a taşı
- Duplikasyon → düşük priority olanı Backlog'a veya kapat
- Label tutarsızlığı → düzelt

### 4. KART KALİTE KONTROLÜ & DÜZELTMELERİ (hemen uygula)
Her kart için kontrol et ve gerekirse editJiraIssue ile düzelt:
- Description eksik/yetersiz → tamamla (yapılacaklar, teknik notlar)
- Kabul kriterleri yok → ekle
- Priority yanlış (ör. kritik bug Low'da) → düzelt
- Label eksik/yanlış → düzelt
- Tahmini efor çok büyük → parçalama önerisi (description'a not)

### 5. WAITING/BLOCKED ANALİZİ
- Neden bekliyor? Hala geçerli mi?
- Çözüm önerisi (comment olarak ekle)
- Açılabilecekler varsa → To Do'ya taşı

### 6. YENİ TASK ÖNERİLERİ (sadece raporla, oluşturma)
Odak perspektifinden (veya genel):
- Eksik feature'lar
- UX iyileştirmeleri
- Teknik borç
- Test coverage boşlukları
- Performans / erişilebilirlik
Her öneri: başlık, kısa açıklama, öncelik, tahmini efor

### 7. ÖNCELİK SIRASI ÖNERİSİ
Mevcut To Do kartları hangi sırayla çalışılmalı ve neden.

### 8. RAPOR YAZ (çıktı olarak)

## Board Sağlığı
- Genel durum (1 paragraf)
- Yapılan düzeltmeler listesi

## Kart Bazlı Notlar
- Sorun/düzeltme yapılan kartlar

## WAITING/BLOCKED Durumu
- Kart bazlı analiz ve öneriler

## Yeni Task Önerileri
| # | Başlık | Açıklama | Öncelik | Efor |
(tablo formatında)

## Öncelik Sırası
1. VOC-XXX — sebep
2. VOC-YYY — sebep
...

## KURALLAR
- Done kartlarına DOKUNMA
- Yeni task OLUŞTURMA — sadece öner (kullanıcı onaylarsa sonra oluşturulur)
- Mevcut kartlarda description/label/priority DÜZELT (editJiraIssue)
- Status transition YAPABILIRSIN (routing/temizlik için)
- Kod yazma, dosya düzenleme YAPMA
- Raporu detaylı ama okunabilir yaz
```

## Çıktı

Agent tamamlandığında rapor döner. Ana oturum:

1. Raporu kullanıcıya gösterir
2. Yapılan düzeltmeleri özetler
3. Yeni task önerileri varsa **3 seçenek** sunar:

```
Ne yapalım?
  1) Jira'da task olarak aç (onaylananları WAITING FOR APPROVAL'da oluşturur)
  2) Kenara not al (docs/tavsiyeler.md'ye ekler, Jira'ya dokunmaz)
  3) Hiçbir şey yapma (sadece rapor bilgi amaçlı)
```

- **Secenek 1:** Jira aktifse onaylanan onerileri WAITING FOR APPROVAL'da olusturur
- **Secenek 2:** Onerileri `docs/tavsiyeler.md`'ye tarih ve kaynak ile ekler
- **Secenek 3:** Hicbir islem yapmaz, rapor bilgi amaclidir
