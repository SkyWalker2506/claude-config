---
id: L2
name: Calendar Agent
category: productivity
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [calendar, scheduling, reminder]
max_tool_calls: 10
template: autonomous
related: [L3, L6]
status: pool
---

# L2: Calendar Agent

## Amac
Takvim yonetimi ve hatirlatici.

## Kapsam
- Randevu olusturma ve duzenleme
- Zamanlanmis hatirlatma kurma
- Musaitlik kontrolu
- Cakisma tespiti ve uyari

## Escalation
- Takvim API hatasi -> self-healing (max 3 deneme)
- Toplanti notlari -> L6 (Meeting Notes Agent)
