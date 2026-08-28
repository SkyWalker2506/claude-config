
## Compilation Rule
Always verify compilation errors after making any code changes by checking Unity's Editor.log or using a build command. Never assume the code works without verifying compilation.

## Otonomi Kurali
Plan/GDD onaylandiktan sonra onay icin durma. Karar gerektiginde en makul varsayimi
sec, secimini tek satirla not et, devam et. "Devam edeyim mi", "hangisini tercih
edersin" gibi sorular plan asamasina aittir; uygulama asamasina degil. Soru sorman
gerekiyorsa hepsini TEK mesajda topla. Tek istisna: veri kaybi riski (dosya silme,
force push, repo sifirlama) ve para harcayan islemler — onlari her zaman sor.

## Muhakeme Derinligi
Uzun/karmasik islerde en yuksek reasoning kademesini kullan. Kod yazmadan once
cozumlemeyi TEK seferde derinlemesine yap ve PLAN.md'ye yaz; sonra uygulama sirasinda
muhakemeyi kis ve hizli ilerle. Her satirda yeniden dusunme.

## Dil
Kullaniciya Turkce yaz. Kod, degisken adlari ve commit mesajlari Ingilizce.

## Rapor Kurali — ciktilar dokumana yazilir
Her is bitiminde raporunu **calistigin repo icinde** `docs/runs/<YYYY-MM-DD-HHMM>-<slug>.md`
dosyasina yaz. Kendi scratch/brain dizinine yazma — orada yazilan rapor kaybolur.

Raporda su alt basliklar bulunur: Gorev · Yapilanlar (her maddede dosya yolu) ·
Degisen dosyalar (`git diff --stat`) · Dogrulama (ne calistirdin, cikti neydi;
calistirmadiysan acikca "calistirilmadi") · Yapilmayanlar (yoksa "yok", bos birakma).

Rapor yazilmadan is bitmis sayilmaz. Raporda yazdigin her iddia diskteki gercek
durumla uyusmali; yapmadigin bir seyi yaptim diye yazma.

Uzun/cok fazli isler (prototip, migration, sprint) icin ayrica `PLAN.md` ve
`README.md` guncellenir — plan basta, README sonda.

## Çıktı Konumu Kuralı (Outputs to Documents)
Üretilen nihai teslimat çıktıları (yalnızca tekil PDF, nihai export/rapor dosyası vb.) kullanıcının `~/Documents` (`/Users/musabkara/Documents/`) dizini altına yerleştirilmelidir. Proje kaynak kodları, ara dosyalar, asset'ler ve scriptler kendi proje/çalışma dizininde kalmalı; Documents klasörü gereksiz dosya ve klasörlerle doldurulmamalıdır.

