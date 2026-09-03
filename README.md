# Blare ads

Jeden súbor riadi všetky reklamné sloty v Blare (iOS aj web): **`ads.json`**.
Appka aj web si ho stiahnu pri štarte a potom každých `refresh_hours`
hodín; bez siete použijú poslednú stiahnutú kópiu, a ak žiadna nie je,
banery zabudované v appke.

URL, z ktorej sa ťahá:

    https://raw.githubusercontent.com/agik66/blare-ads/main/ads.json

Zmena = upraviť `ads.json`, `python3 validate.py`, commit, push. Do 6 hodín
(alebo po reštarte appky) ju vidia všetci. Žiadna nová verzia appky.

## Sloty a formáty

| slot | kde | formát | rozmer kreatívy |
|---|---|---|---|
| `lib` | iOS LIB nad zoznamom | **narrow** | 640×120 px (zobrazí sa ~320×60 pt) |
| `find` | iOS FIND za odpoveďou | narrow | 640×120 |
| `landscape-banner` | iOS iPad landscape bez zoznamu, pod ovládaním | **wide** | 1456×180 (728×90 pt) |
| `ipad-column` | iOS iPad landscape, pravý stĺpec | **tall** | 600×1200 (300×600 pt) |
| `web-leaderboard` | web nad prehrávačom | wide | 1456×180 |
| `web-inline` | web LIB nad zoznamom | narrow | 640×120 |
| `web-side` | web pravý stĺpec (široké okno) | tall | 600×1200 |
| `web-find` | web FIND za odpoveďou | narrow | 640×120 |

Formát = tvar boxu. Každá reklama má `creative.narrow / wide / tall`:
buď `null` (vykreslí sa **text**: kicker, title, line, cta — vždy v štýle
appky), alebo objekt s obrázkom:

```json
"creative": {
  "narrow": { "image": "https://…/syenit-narrow.png" },
  "wide":   { "image": "https://…/syenit-wide.png" },
  "tall":   null
}
```

Obrázok sa vpasuje do boxu (fit, bez orezania); kde je `null`, ide text.
Obrázky hostuj tu v repe (`creatives/`) — URL potom je
`https://raw.githubusercontent.com/agik66/blare-ads/main/creatives/<subor>.png`.
Len HTTPS. PNG alebo JPEG, do 300 KB.

## Polia reklamy

| pole | význam |
|---|---|
| `id` | jedinečný kľúč (slug) |
| `enabled` | `false` = vypnutá, zostane v súbore |
| `weight` | pomer zobrazovania (2 = dvakrát častejšie než 1) |
| `platforms` | `["ios"]`, `["web"]` alebo obe |
| `slots` | v ktorých slotoch smie byť (zoznam vyššie) |
| `from` / `until` | `"2026-12-01"` / `"2026-12-31"` alebo `null` — kampaň v čase |
| `kicker` | malý nadpis (VEĽKÝMI, napr. `APP · SAME DEVELOPER`) |
| `title` | názov |
| `line` | jedna veta |
| `cta` | text tlačidla (`APP STORE ↗`) |
| `url` | kam vedie ťuk (HTTPS) |
| `creative` | obrázky per formát, viď vyššie |

Výber v slote: z povolených reklám (platforma, slot, dátum, `enabled`)
sa vyberá podľa `weight`, striedanie po dňoch a slotoch — jedna reklama
sa v jednej obrazovke neopakuje v dvoch slotoch, ak je z čoho vybrať.

## Pravidlá, ktoré appka vynucuje

- Používateľ, ktorý kúpil „Remove ads", nevidí NIČ z tohto súboru.
- Text v slote je vždy v monospace štýle appky; obrázok nikdy nemení
  layout (box má pevný rozmer, obrázok sa doň vpasuje).
- Súbor sa sťahuje bez akýchkoľvek identifikátorov — je to obyčajný GET,
  privacy odpovede appky sa nemenia.

## Platené reklamy na webe (AdSense)

V `ads.json` je blok `web_networks.adsense`: `client` (tvoje `ca-pub-…`),
`slots` (slot → id reklamnej jednotky) a `house_share` (0–1: aký podiel
načítaní stránky ukáže tvoj house baner namiesto platenej jednotky).
Prázdny `client` = len house banery. Web načíta AdSense skript až keď je
`client` vyplnený. iOS appka tento blok ignoruje (tam nie je žiadna sieť).
