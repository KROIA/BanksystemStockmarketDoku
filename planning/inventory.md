# Inventory of the existing documentation

Snapshot of 2026-11-17: StockMarket `mc_1.21.1` at `6e533a17`, BankSystem `mc_1.21.1`. This file lives in `planning/` and is not part of the site.

**Reader:** P = player, A = server admin, D = developer.
**Target:** page in the new site under `docs/` (see `mkdocs.yml` for the nav). Several old pages may feed one target, and one old page may be split.
**Status:**

- **ok** = content is current as far as checked; needs only the style rewrite.
- **outdated** = contradicts the current code or GUI (details in the Findings section).
- **duplicate** = the same topic is also covered elsewhere; merge into one target.
- **inconsistent** = contradicts another doc page, or uses names that differ from the GUI.
- **drop** = should not go on the site.
- *Not deep-checked* = only headings and a sample were compared with the code. The three pilot topics were checked line by line against the code.

## StockMarket

### README.md (709 lines, holds a large share of the player and admin content)

| Section | Reader | Target | Status |
|---|---|---|---|
| About, Features | P | `index.md`, `stockmarket/index.md` | ok |
| Dependencies, LuckPerms table | A | `admin/install.md` | ok |
| Downloads table | A | `admin/install.md` (link to CurseForge/Modrinth only) | outdated: lists only 1.3.1 and 2.1.0-alpha, Forge/Quilt columns for legacy builds |
| Blocks, Crafting Recipes | P | `stockmarket/blocks-and-recipes.md` | inconsistent: block called "Stock Market Block" and "Stock Market Terminal Block" (the game itself uses both, see F-7) |
| Matching Engine, Type of Trades | P | `stockmarket/trading.md` (pilot) | rewritten; old text has typos |
| How to use → For Players | P | `stockmarket/trading.md` (pilot), `stockmarket/price-chart.md`, `stockmarket/pair-trading.md` | inconsistent: tab and mode names differ from the GUI (F-5) |
| How to use → For Admins (Management GUI tabs, Presets) | A | `admin/stockmarket/markets.md`, `admin/stockmarket/presets.md` | duplicate of parts of `mod-settings.md` and `admin-setup.md` |
| How to use → Mod Settings | A | `admin/stockmarket/mod-settings.md` | duplicate of `documentation/user-guide/mod-settings.md` |
| Commands | A | `admin/commands.md` | contains the dev-only `/stockmarket test` (drop that row) |
| Access Control & Trust Model | A | `admin/permissions.md` | duplicate of `admin-setup.md#permissions` and of the BankSystem trust docs |
| Plugins (all five) + How the plugins work together | A | `admin/stockmarket/plugins/*.md` | duplicate of the plugin pages |
| Villager Trading | P + A | `stockmarket/villager-trading.md` (player view), `admin/stockmarket/villager-trading.md` (file + settings) | no separate page today; split by reader |
| JEI Integration | P | none | drop: the StockMarket JEI plugin registers nothing (F-11) |
| Why does a price move?, Terminology | P | `stockmarket/price-chart.md`, `glossary.md` | ok in substance, many typos |
| Development | D | `developers/index.md` | not deep-checked |
| Changelog links | — | not on the site (stays in the mod repos) | — |

### documentation/

| Page | Reader | Target | Status |
|---|---|---|---|
| `README.md` (index) | — | replaced by the site nav | drop |
| `user-guide/admin-setup.md` | A | `admin/stockmarket/setup-use-cases.md`, `admin/permissions.md`, `admin/discord.md`, `admin/audit/alerts.md`, `admin/backups.md` | duplicate (permissions, Discord, backups are shared with BankSystem); one page mixes five topics |
| `user-guide/candle-timebase.md` | A | section of `admin/stockmarket/mod-settings.md` | ok; too small for its own page |
| `user-guide/mod-settings.md` | A | `admin/stockmarket/mod-settings.md` | duplicate of the README section; not deep-checked |
| `user-guide/multi-server.md` | A | `admin/multi-server.md` | duplicate of BankSystem `MultiserverSetup.md`; links to the BankSystem GitHub instead of a page |
| `user-guide/placeholders.md` | A | `admin/placeholders.md` | duplicate topic with BankSystem `Placeholders.md` (different placeholders, same setup) |
| `user-guide/trading-hours.md` | A + P | `admin/stockmarket/trading-hours.md`, player part to `stockmarket/trading.md#when-a-market-is-closed` (done) | ok; split by reader |
| `user-guide/news-system/overview.md` | P + A | player part to `stockmarket/newspaper.md`, admin part to `admin/stockmarket/news/index.md` | ok; mixes readers |
| `user-guide/news-system/configuration.md` | A | `admin/stockmarket/news/config-files.md` (pilot), `event-reference.md`, `commands.md` | folder part checked: ok. Example event outdated (F-3). One page mixes folder, schema, commands and history storage |
| `user-guide/news-system/advanced-events.md` | A | `admin/stockmarket/news/advanced-events.md` | ok; its "Getting the New Default Events" section repeats the config page (moved to the pilot) |
| `user-guide/news-system/authoring-tutorial.md` | A | `admin/stockmarket/news/tutorial.md` | ok (folder layout part matches the code); not deep-checked otherwise |
| `user-guide/news-system/pictures.md` | A | `admin/stockmarket/news/pictures.md` | outdated + self-contradicting (F-1) |
| `user-guide/news-system/default-events-catalog.md` | A | `admin/stockmarket/news/default-events.md` | drop as is: an auto-generated internal review catalog (2,077 lines, picture status). Regenerate as a short table, or drop (decision D-6) |
| `user-guide/plugin-system/overview.md` | A | `admin/stockmarket/plugins/index.md` | duplicate of README Plugins |
| `user-guide/plugin-system/management.md` | A | `admin/stockmarket/plugins/index.md` | ok; not deep-checked |
| `.../plugins/net-flow-plugin.md` | A | `admin/stockmarket/plugins/net-flow.md` | not deep-checked |
| `.../plugins/news-plugin.md` | A | `admin/stockmarket/plugins/news.md` | outdated (F-2) |
| `.../plugins/orderbook-volume-distribution.md` | A | `admin/stockmarket/plugins/order-book-volume.md` (pilot) | checked: defaults, labels and ranges match the code. Wall text slightly imprecise (F-4) |
| `.../plugins/target-price-bot.md` | A | `admin/stockmarket/plugins/target-price-bot.md` | not deep-checked |
| `.../plugins/volatility-plugin.md` | A | `admin/stockmarket/plugins/volatility.md` | not deep-checked |
| `developer-guide/plugin-system/overview.md` | D | `developers/stockmarket/plugins/index.md` | not deep-checked |
| `developer-guide/plugin-system/getting-started.md` | D | `developers/stockmarket/plugins/getting-started.md` | not deep-checked |
| `developer-guide/plugin-system/api-reference.md` | D | `developers/stockmarket/plugins/api-reference.md` | not deep-checked (1,274 lines; consider generating parts from Javadoc) |
| `developer-guide/plugin-system/examples.md` | D | `developers/stockmarket/plugins/examples.md` | not deep-checked |
| `developer-guide/api/async-market-api.md` | D | `developers/stockmarket/market-access-api.md` | not deep-checked |
| `developer-guide/api/market-creation-api.md` | D | `developers/stockmarket/market-creation-api.md` | not deep-checked |

## BankSystem

### README.md (511 lines)

| Section | Reader | Target | Status |
|---|---|---|---|
| About, Features | P | `index.md`, `banksystem/index.md` | ok |
| Installation, Downloads | A | `admin/install.md` | not deep-checked |
| Usage (Terminal, ATM, automation, stockpile, displays) | P | `banksystem/*.md` | duplicate of `documentation/user-guide/Usage.md` |
| Usage → Currency Mod Bindings | P | `banksystem/currency-bindings.md` | duplicate of `CurrencyBindings.md` |
| Usage → Mod Settings Screen | A | `admin/banksystem/settings.md` | duplicate of `Configuration.md` |
| Usage → Discord Feed | A | `admin/discord.md` | duplicate topic with StockMarket `admin-setup.md#discord-feed` |
| Blocks, Items, Money | P | `banksystem/blocks-and-recipes.md`, `banksystem/money.md` | ok |
| Commands, Permissions (LuckPerms) | P + A | `banksystem/commands.md` (player), `admin/commands.md`, `admin/permissions.md` | duplicate of `Commands.md` |
| Crafting Recipes (components, software, modules, blocks, company, money) | P | `banksystem/blocks-and-recipes.md` | ok; images in `documentation/images/recipes/` |
| Changelog | — | not on the site | — |

### documentation/

| Page | Reader | Target | Status |
|---|---|---|---|
| `README.md` (index) | — | replaced by the site nav | drop; its "Development & Testing" section is dev-only (F-8) |
| `user-guide/Usage.md` | P | `banksystem/bank-terminal.md`, `money.md` (incl. ATM), `automation.md`, `displays.md`, `shares.md` (Share Stamper) | duplicate of README Usage |
| `user-guide/BankAccounts.md` | P | `banksystem/bank-accounts.md` | ok |
| `user-guide/Commands.md` | P + A | `banksystem/commands.md`, `admin/commands.md` | duplicate of README Commands |
| `user-guide/Companies.md` | P | `banksystem/companies.md`, `payouts.md`, `shares.md`, `company-market.md`, `stockmarket/company-shares.md` | not deep-checked; long (441 lines), split |
| `user-guide/CurrencyBindings.md` | P | `banksystem/currency-bindings.md` | not deep-checked |
| `user-guide/Administration.md` | A | `admin/banksystem/bankable-items.md`, `accounts.md`, `admin/audit/*.md`, `admin/backups.md`, `admin/permissions.md` | ok; one page mixes eight topics |
| `user-guide/Configuration.md` | A | `admin/banksystem/settings.md`, `admin/banksystem/bankable-items.md` (item components) | ok; organised by JSON key, not by GUI name (style difference S-3) |
| `user-guide/MultiserverSetup.md` | A | `admin/multi-server.md` | duplicate of StockMarket `multi-server.md` |
| `user-guide/Placeholders.md` | A | `admin/placeholders.md` | duplicate topic with StockMarket |
| `developer-guide/API.md` | D | `developers/banksystem/api.md` | not deep-checked |
| `developer-guide/EventsAndSignals.md` | D | `developers/banksystem/events.md` | not deep-checked |
| `developer-guide/CurrencyIntegration.md` | D | `developers/banksystem/currency-integration.md` | names test classes and the `testing/` folder as examples (F-8) |
| `developer-guide/ItemPriceProviderAPI.md` | D | `developers/banksystem/item-price-provider.md` | not deep-checked; written "for StockMarket" (internal integration notes) |
| `developer-guide/TransactionLedger.md` | D | `developers/banksystem/transaction-ledger.md` | not deep-checked |
| `developer-guide/AsyncForwardingArchitecture.md` | D (contributor) | none | drop (decision D-5): internal RPC design and "how to add a forwarded method" for BankSystem contributors, not API users |

## Findings

**F-1 `pictures.md` contradicts itself and the code.** The first section says default pictures are generated only when `pictures/` has no PNG, and "a folder that already contains any .png is never touched". The code (and the same page further down) writes each missing default picture on every reload. The page also says the defaults are "procedurally generated placeholders". In fact 73 real pictures ship in the jar (`news/pictures/<id>.png`); the generator is only a fallback.

**F-2 `news-plugin.md` names the old file.** "Impact duration and strength" says "the shipped `default_events.json` also sets two multipliers". Since commit 9d61a232 the multipliers are in `scheduler.json`. It also says "about 7 attempts per real day", while `configuration.md` says "about 6 news per real day" (both are right, 7 attempts give about 6 news, but say it one way).

**F-3 `configuration.md` example event is stale.** The `diamond_rush` example in "File Format" shows `rampUpSeconds 120`, `durationSeconds 600`, `reversalSeconds 900`. The shipped `DefaultEvents/diamond_rush.json` has 600 / 3000 / 4500 and an extra `picture` field. Either mark it as a shortened example or use the real values.

**F-4 Wall description is a little off.** The old page says "as long as the price stays within the dead zone nothing changes". In the code every price level beyond the dead zone (measured from the slow average) on the side facing away gets wall volume, whether or not the price is there yet. The visible effect is the same; the pilot page describes it per level.

**F-5 README uses old GUI names.** README: "Market Order / Limit Order tabs", "Money Mode / Pair Mode", "Market Exchange / Limit Exchange". GUI (`en_us.json`): tabs **Market** / **Limit**, modes **Item / Money** / **Item / Item**, pair tabs **Exchange** / **Limit**. The README also doesn't mention the bank account selector on the trading screen.

**F-6 README Commands lists a dev command.** `/stockmarket test` is in the public command table.

**F-7 Block name differs between item and block (mod issue, not docs).** `en_us.json`: `item.stockmarket.stock_market_block` = "Stock Market Block", `block.stockmarket.stock_market_block` = "Stock Market Terminal Block". Players see one name in the inventory and another in WAILA/Jade. The pilot uses "Stock Market Block". Suggest an SM inbox item.

**F-8 Dev tools in BankSystem docs.** `documentation/README.md` "Development & Testing" (`enable_dev_features`, `/banksystem test`, `exportrecipes`) and `CurrencyIntegration.md` sections 4.5, 10 and 16 (in-game test suite, `StubCurrencyProvider`, `testing/tests/...`). Not moved to the site.

**F-9 Shared topics are written twice.** Multi-server, placeholders, Discord feed, backups, permissions/LuckPerms and commands exist in both mods with different wording and structure. Each becomes one page under Server Admin → Both mods.

**F-10 READMEs carry content that belongs in pages.** Both READMEs repeat large parts of the docs (SM: plugins, villager trading, commands, admin GUI; BS: usage, commands, settings). After the site goes live, the READMEs should shrink to an intro, install links and a link to the site (decision D-7).

**F-11 StockMarket has no JEI integration.** The README's "JEI Integration" section (marked ok above) describes a plugin that the code doesn't fill: `StockMarketJeiPlugin` is an empty stub that registers nothing. BankSystem has a real JEI plugin. Don't mention JEI on StockMarket pages.

**F-12 No fees, taxes or interest.** Neither mod charges trading fees, taxes or bank interest (code check 2026-11-24). Pages must not suggest otherwise.

**F-13 Dead or unreachable code that a reader could stumble on (mod issues, not docs).** StockMarket: `CreateMarketScreen` ("Create new Market") has no caller; the "Player" settings group (`STARTING_BALANCE`) is unused. BankSystem: a doc comment mentions `/company stamper-bind`, which isn't registered (binding happens at the Share Stamper block).

## Style differences between BankSystem and StockMarket

| # | Topic | BankSystem | StockMarket |
|---|---|---|---|
| S-1 | File names | PascalCase (`BankAccounts.md`) | kebab-case (`trading-hours.md`) |
| S-2 | Callouts | GitHub admonitions (`> [!NOTE]`, `> [!WARNING]`), 33 in total | none; bold text and plain paragraphs |
| S-3 | Settings pages | organised by `settings.json` section and key | organised by Mod Settings screen group and GUI name, tables "Setting (UI name) / Default / Allowed / What it controls" |
| S-4 | Dashes | em dash `—` | double hyphen `--` (336 times) |
| S-5 | Images | `<div align="center"><img src=...></div>`, usually no width | `<p align="center"><img width="600" alt=...>`, SVG charts with alt text |
| S-6 | Navigation | "Chapters" lists in the READMEs only | "Chapters" lists at the top of most user pages |
| S-7 | Page scope | one page per screen or block (Usage, Companies) | one page per system (news, plugins), long multi-topic pages |
| S-8 | Commands | dedicated `Commands.md` | commands inside the README and inside topic pages |
| S-9 | Version notes | many "(since 2.2.0)" markers in headings | version notes inline in the text ("in 2.2.0 ...", "raised from 500 in v2.0.4") |
| S-10 | Tone | mostly second person, some passive | mixed: "the player", "admins", passive; very long sentences in news and plugin pages |

The new style guide (`planning/STYLE.md`) settles each of these: kebab-case files, Material admonitions, GUI-name-first settings tables with keys in code, figures with width, short pages per task, one commands page per reader, version notes only in upgrade sections, second person.

## Biggest gaps (no page today)

- A player **getting started** page across both mods (bank account → deposit → trading block → first trade).
- A **glossary**.
- **Stock Market Display** block configuration (only lang strings exist).
- **Villager trading** for players.
- A **pair trading** (Item / Item) page; today it is two paragraphs in the README.
- A **developer landing page**: how to add the mods as a Gradle dependency (JitPack/flatDir), which API to use when.
- An **admin install page** that covers both mods and ModUtilities together, with matching versions.
