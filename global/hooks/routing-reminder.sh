#!/usr/bin/env bash
# Fires on every user prompt. Keeps the model-routing order in front of Jarvis so it is never
# re-derived from memory and never forgotten. Written 2026-10-27 after the owner had to repeat
# the same reminder many times in one session.
# Keep this UNDER ~120 tokens. It is paid on every single prompt; a long version gets ignored.
cat <<'TXT'
[YONLENDIRME — her is icin, istisnasiz]
Uretim isini SEN yapmazsin. Sira: (1) $200 hediye API kredisi (Haiku/Sonnet, mumkunse Batch)
-> (2) Gemini 3.8 Flash (agy) -> (3) Codex/GPT orta kademe -> (4) Claude abonelik EN SON.
Kod, sprite, kontakt sayfasi, toplu tarama, gorsel inceleme = Gemini/GPT.
Sende kalan: olcum, teshis, kabul/red karari, kullaniciya rapor.
Her adimda model+effort'u ise gore sec; Opus/high sadece gercek karar icin.
Etiket: (Jarvis | Model | effort | HH:MM) — effort oturum ayarindan, saat `date +%H:%M` ile.
Ikisini de TAHMIN ETME; bilmiyorsan oku.
TXT

# Which lanes are usable right now. Expired cooldowns clear themselves, so a spent quota
# is retried after its window instead of being hammered or forgotten.
bash "$(dirname "$0")/lane.sh" status 2>/dev/null || true
