# German translation: rules

Every English page `page.md` gets a German page `page.de.md` in the same folder. The German site is built from them (mkdocs-static-i18n, suffix layout). Pictures stay the same: they show the English game, and that's fine.

## Tone

- Address the reader with **du** (the mods' German texts do too). Lower-case "du", "dein".
- Same style as the English pages (planning/STYLE.md): short sentences, plain words, active voice, no idioms, no filler. Translate the meaning, not word by word. Natural German word order and compounds ("Bankkonto", not "Bank Konto").
- German quotation marks „…“ in running text. Inside code and in quoted game messages, see below.
- Numbers like the game writes them: thousands with an apostrophe (`1'000'000`, as on the banknotes), decimals with a point (`0.5`, `$500.00`), so a German reader can't take `1,440` for a decimal. Units in words are translated ("20 seconds" → "20 Sekunden").

## Game terms

- **Bold** game texts (buttons, tabs, screen titles, settings, item and block names) use the exact German text of the game. Look them up in `gui-terms.md` (generated from the language files). If a term isn't there, search the German language files listed at its end (`de_de.json`; the key with the same English value in `en_us.json` gives you the German). Keep them bold.
- Where `gui-terms.md` lists several German values, pick the one of the screen the sentence talks about.
- Quoted game messages (*"This bank account is frozen…"*) use the German message from `de_de.json`. A message the game shows only in English (no de_de key, text in the code, server log lines, messages of other programs such as TAB) stays English, so readers find what they see. Keep the italics.
- Vanilla Minecraft names in German (Eisenbarren, Trichter, Diamant…): the vanilla German file is listed at the end of `gui-terms.md`.
- Never add the English term in brackets.

## Terms in running text

Use these everywhere, so all pages agree:

| English | German |
|---|---|
| bank account / account | Bankkonto / Konto |
| personal account / shared account | persönliches Konto / gemeinsames Konto |
| balance | Kontostand |
| deposit / withdraw (verb) | einzahlen / abheben |
| deposit / withdrawal (noun) | Einzahlung / Abhebung |
| cash, banknote, coin | Bargeld, Banknote, Münze |
| money items: Dollar coin, 5 Dollar note | the game's names: Euro, 5 Euro (amounts keep the game's `$`: `$500.00`) |
| bankable item | bankfähiges Item |
| item | Item (the mods say "Item"; vanilla things can be "Gegenstand" where it reads better) |
| locked amount | reservierter Betrag |
| freeze / frozen | einfrieren / eingefroren |
| market | Markt |
| order, buy order, sell order | Order, Kauforder, Verkaufsorder |
| market order / limit order | Market-Order / Limit-Order |
| order book | Orderbuch |
| price chart / candle / candlestick chart | Preischart / Kerze / Kerzenchart |
| trade (noun / verb) | Handel / handeln |
| company | Unternehmen |
| share (the item) / shareholder | Aktie / Aktionär |
| dividend / payout / wage | Dividende / Auszahlung / Lohn |
| worker / founder | Mitarbeiter / Gründer |
| news event | News-Ereignis |
| newspaper | Zeitung (the item name from the game where it is meant) |
| plugin | Plugin |
| target price | Zielpreis |
| trading hours | Handelszeiten |
| preset | Vorlage (BankSystem) / Voreinstellung (StockMarket): as the game names it on that screen |
| server admin / admin mode | Server-Admin / Admin-Modus |
| master server / slave server | Master-Server / Slave-Server |
| trusted (slave) | vertrauenswürdig |
| transaction ledger | Transaktionsbuch |
| alert / suspicion flag | Alarm / Verdachtsmarkierung |
| audit | Audit |
| settings / Mod Settings | Einstellungen / the game's name for the screen |
| player | Spieler |
| developer, mod author | Entwickler, Mod-Autor |
| world, server, client | Welt, Server, Client |
| config file | Konfigurationsdatei |
| backup | Backup |
| webhook, placeholder, permission | Webhook, Platzhalter, Berechtigung |
| loader (Fabric / NeoForge) | Loader |

Names stay as they are: BankSystem, StockMarket, ModUtilities, Create: Numismatics, Lightman's Currency, LuckPerms, Placeholder API, TAB, Discord, Fabric, NeoForge, Architectury, CurseForge, Modrinth, the Audit Tool. Invented example names (Tavrik, Acme Mining, Farm Co-op, Oak & Iron Co., Brindle Timber, MinerMia…) stay too.

## What stays exactly as it is

- **Code blocks** (```` ``` ````), unchanged, including comments in them.
- **Inline code**: commands, config keys, file and folder names, JSON fields, permission nodes, placeholders, class and method names.
- **Link targets**: every `(...)` after a link stays byte for byte, anchors included (`accounts.md#freezing-an-account`). Translate only the link text. Never link to a `.de.md` file; the site maps `page.md` to the German page by itself.
- **Pictures**: path and `{ ... }` attributes unchanged. Translate the alt text in `![...]` and the `<figcaption>`.
- HTML and Markdown structure: `<div class="..." markdown>`, `<figure markdown="span">`, grid cards, tables (same rows and columns), lists, icons like `:material-bank:` and `:octicons-arrow-right-24:`, `{ .md-button }` attributes.
- **Headings**: the same headings in the same order and at the same levels. Translate their text. Don't add, merge or drop a heading, and don't add `{ #id }`: a script gives every German heading the English page's anchor afterwards, so all links keep working.
- **Admonitions** (`!!! note`, `??? tip`): keep the type. A quoted title is translated (`!!! warning "Vorsicht beim Entsperren"`). Admonitions without a title stay without one: the site gives them a German title.
- **Front matter**: translate the values of `title` and `description` and keep them in double quotes; every other key stays.

## Never on the site

The same as in English (STYLE.md section 11): no dev tools, no tracker, no real player or server names.

## Keeping both languages in step

- Change an English page → change its German page in the same commit. A new page gets its `page.de.md` right away (a page without one shows English on the German site).
- A new or renamed heading: build, then run `python planning/translation/add_ids.py`. It gives each German heading the anchor of the English heading at the same position, so links like `page.md#some-heading` work in both languages. German headings therefore always end in `{ #english-id }`; keep them when you edit.
- Before committing, run `python planning/translation/check.py`. It compares every German page with its English one (code blocks, links, pictures, headings, tables) and lists English pages without a German one. Then `mkdocs build --strict`.
- `default-events.de.md` is written by `planning/news-icons/sync_default_events.py` together with the English page. Only its hand-written parts are edited by hand.
- New nav section → add its German name under `nav_translations` in `mkdocs.yml`.
