# Site structure plan

Status: applied on 2026-11-24 (nav, stubs, merges, placeholders, home page). The page texts are still stubs except the pilots and the home page.
Checked against the code of StockMarket 2.2.1 and BankSystem 2.2.1 (MC 1.21.1). The shot list for every image named here is in [images.md](images.md).

## 1. The three parts

The site has a home page and three parts, one per reader. Each part is a tab in the top bar.

| Tab | Reader | Question it answers |
|---|---|---|
| **Home** | everyone | What are these mods, what can they do, where do I start? |
| **Player Guide** | players | How do I bank, trade, run a company? |
| **Server Admin** | server owners and operators | How do I install, configure, secure and audit it? |
| **Developers** | mod authors | How do I use the APIs and write a StockMarket plugin? |

Inside each part, the mods are sections (BankSystem first, because you need a bank account before you can trade). A future mod becomes one more section in each part, so the "per mod" rule still holds.

**File paths stay as they are.** Player pages stay in `docs/banksystem/` and `docs/stockmarket/`, so moving them into the Player Guide tab is a nav change only and no link breaks. The new pages below are added next to them.

### Rules for "only relevant information"

- Every page answers one question of one reader. If a section would repeat another page, it links there instead.
- Player and admin pages show what the reader sees and does: no class names, no internal design, no version history.
- The docs never promise what the code doesn't do. Neither mod has fees, taxes or interest; StockMarket has no JEI integration (the JEI plugin is an empty stub) and no event API.
- One image per screen a page explains. A GIF only where movement explains something a still image can't. At most about five images per page.
- Short pages are fine. A page that would be a single paragraph is merged into its neighbour instead.

## 2. Home page (`index.md`)

A landing page with no side navigation (`hide: [navigation, toc]`), readable in one screen and a short scroll. Built with Material grid cards (needs `pymdownx.emoji` in `mkdocs.yml` for the card icons).

```text
┌──────────────────────────────────────────────────────────────┐
│ BankSystem & StockMarket                                     │
│ A bank and a stock market for your Minecraft server: one     │
│ shared economy, played with real items.                      │
│ [Download BankSystem] [Download StockMarket]                 │
│ ┌──────────────── hero picture ─────────────────┐            │
│ └───────────────────────────────────────────────┘            │
├──────────────────────────────┬───────────────────────────────┤
│ BankSystem card              │ StockMarket card              │
│ 6 feature lines, each a link │ 6 feature lines, each a link  │
├──────────────────────────────┴───────────────────────────────┤
│ How they fit together: diagram + 3 sentences                 │
├──────────────────────────────────────────────────────────────┤
│ Built for servers: 4 short lines (multi-server, permissions, │
│ audit, integrations)                                         │
├───────────────────┬───────────────────┬──────────────────────┤
│ I play            │ I run a server    │ I write mods         │
│ → Getting started │ → Installation    │ → Project setup      │
├───────────────────┴───────────────────┴──────────────────────┤
│ Requirements: Minecraft versions · Fabric / NeoForge ·       │
│ ModUtilities                                                 │
└──────────────────────────────────────────────────────────────┘
```

Card content (checked against the code):

**BankSystem**
- A bank account for every player, plus shared accounts with **Deposit**, **Withdraw** and **Manage** rights.
- Store items, not only money: the **Bank Terminal Block** deposits, withdraws and even crafts from your bank.
- Cash you can hold: banknotes and coins from the **ATM**.
- Redstone automation with the **Bank Upload Block** and **Bank Download Block**.
- Companies: workers, wages, dividends and printed shares from the **Share Stamper**.
- Works with Create: Numismatics and Lightman's Currency.

**StockMarket**
- A market for any item, with a real order book: market and limit orders, matched between players.
- Swap one item for another in **Item / Item** mode.
- Candlestick charts in the trading screen, on the **Stock Market Display** and on an optional web page.
- Markets stay alive without players: plugins add volume, price movement and a trading bot.
- Market news that moves prices, read in the **Newspaper**.
- Company shares from BankSystem trade like any item, and villager prices follow the market.

**Built for servers:** one economy across several servers (master and slaves) · admin roles and LuckPerms nodes · audit trail, suspicion alerts and the offline Audit Tool · TAB / Placeholder API, Discord feed, web view.

Images: `shared/home-hero.png`, `shared/economy-overview.svg`.

## 3. Player Guide

Type: **C** concept, **H** how-to, **R** reference, **O** overview. Status: **pilot** = finished, **new** = no stub yet, **merged** = absorbs another stub, **split** = takes part of an old stub.

### Start here

| Page | Type | Covers | Images |
|---|---|---|---|
| `getting-started.md` Getting started | H | Your first ten minutes across both mods: your account exists already → make a Bank Terminal from a Terminal Block and Banking Software → deposit items → make a Stock Market Block with Trading Software → place a first order → withdraw what you bought. | `shared/program-terminal.gif`, `banksystem/bank-terminal-deposit.gif`, `stockmarket/trading-screen.png` |
| `together.md` How the two mods work together **new** | C | Answers "how is the bank connected to the trading block": the Terminal Block family (Bank Terminal, ATM, Stock Market Block are one block with different software); your bank account is your trading wallet (which accounts can trade: Deposit + Withdraw rights; money and items are reserved while an order is open; frozen accounts can't trade); company shares become markets; villagers pay in money; your total wealth uses market prices. | `shared/economy-overview.svg`, `shared/terminal-family.png` |
| `glossary.md` Glossary | R | Market and bank words used on the site. | none |

### BankSystem

| Page | Type | Covers | Images |
|---|---|---|---|
| `banksystem/index.md` BankSystem | O | What the mod adds, one line per page. | `banksystem/blocks-overview.png` |
| `bank-accounts.md` Bank accounts | H | Personal account, `/bank create`, the account limit, the Account Management screen, adding users and their rights, deleting, frozen accounts. | `banksystem/account-management.png`, `banksystem/account-permissions.png` |
| `bank-terminal.md` Bank Terminal | H | Send items to the bank and get them back, amount buttons, filter, crafting with **Use Bank Items** and **Auto-deposit output**, transaction history, balance history chart. | `banksystem/bank-terminal.png`, `banksystem/bank-terminal-deposit.gif`, `banksystem/bank-terminal-crafting.png`, `banksystem/balance-history.png` |
| `money.md` Money and the ATM **merged** (absorbs `atm.md`) | H | Dollars in the bank vs. banknotes and coins, ATM **Withdraw** and **Convert** tabs, `/money send`, the Money Stockpile. | `banksystem/money-items.png`, `banksystem/atm-withdraw.png`, `banksystem/atm-convert.png`, `banksystem/money-stockpile.png` |
| `automation.md` Automation | H | Bank Upload Block (deposit while powered, drop unbankable items), Bank Download Block (withdraw orders with conditions), a sample setup. | `banksystem/upload-block.png`, `banksystem/download-block.png`, `banksystem/automation-setup.png` |
| `displays.md` Bank Display | H | Placing a multi-block display, **Balance Overview** vs **Balance History**, choosing the account. | `banksystem/display-in-world.png`, `banksystem/display-config.png` |
| `currency-bindings.md` Currency bindings | H | Linking a bank slot to a Numismatics or Lightman's Currency account, unbinding (where the money goes), what a suspended binding means. | `banksystem/currency-bindings.png`, `banksystem/currency-bind-dialog.png` |
| **Companies** (sub-section) | | | |
| `companies.md` Founding and running a company **split** | H | `/company create`, the Company Management tabs **Overview**, **Workers**, **Statistics**, **Danger Zone** (transfer founder, dissolve). | `banksystem/company-overview.png`, `banksystem/company-workers.png`, `banksystem/company-statistics.png` |
| `payouts.md` Payouts and dividends **new** | H | Recurring and one-time payouts (wages), dividend mode, **Pay Dividend**, missed payouts. | `banksystem/payout-edit.png`, `banksystem/pay-dividend.png` |
| `shares.md` Shares and the Share Stamper | H | Blank Share → Company Share, binding a stamper, **Stamp** / **Redeem**, hopper automation, supply, designing the share card, shares in the bank. | `banksystem/share-stamper.png`, `banksystem/share-visuals.png`, `banksystem/share-items.png` |
| `company-market.md` Your company on the stock market **new** | H | **Market** tab: **Create Market** with a start price, **Open in StockMarket**, pause and resume trading, closing the market for good. | `banksystem/company-market-tab.png` |
| `blocks-and-recipes.md` Blocks, items and recipes | R | Every block and item with its recipe. | recipe images (exported) |
| `commands.md` Commands | R | `/bank`, `/money`, `/company` for players. | none |

### StockMarket

| Page | Type | Covers | Images |
|---|---|---|---|
| `stockmarket/index.md` StockMarket | O | What the mod adds, one line per page. | `stockmarket/display-in-world.png` (shared with the display page) |
| `trading.md` Trading basics **pilot, merged** (absorbs the player `trading-hours.md`) | H | Already written. Add a short section "When a market is closed" (closed and maintenance banners, the clock). | existing GIFs + `stockmarket/market-closed.png`; retake `StockMarketTerminal.gif` as `stockmarket/trading-screen.gif` |
| `price-chart.md` Price chart and order book | C | Candles, timeframes, the order book histogram, your order markers, why a price moves. | `stockmarket/price-chart.png`, `stockmarket/candle.svg` |
| `pair-trading.md` Trading item for item | H | **Item / Item** mode, **I HAVE / I WANT**, **Exchange** and **Limit** tabs, the rate. | `stockmarket/item-item-mode.png` |
| `company-shares.md` Trading company shares **new** | H | The **Companies** tab, supply, what a share gives you (dividends), shares stay in your bank, paused or closed company markets. Links to the company pages. | `stockmarket/companies-tab.png` |
| `newspaper.md` Market news | H | The Newspaper item, the **News** button, `/stockmarket news`, news popups, how news moves prices. | `stockmarket/newspaper.png`, `stockmarket/news-toast.png` |
| `villager-trading.md` Villager trading | C | Villager prices follow the market, paid in banknotes with change. | `stockmarket/villager-trade.png` |
| `display-block.md` Stock Market Display | H | Placing displays, choosing a market or pair, the chart view. | `stockmarket/display-in-world.png`, `stockmarket/display-config.png` |
| `blocks-and-recipes.md` Blocks, items and recipes | R | Stock Market Block, Trading Software, Stock Market Display, Newspaper. | recipe images (exported) |

## 4. Server Admin

### Setup (both mods)

| Page | Type | Covers | Images |
|---|---|---|---|
| `admin/index.md` Server Admin | O | A first-setup checklist (install → make yourself admin → choose bankable items → create markets from presets → pick a market style → permissions → integrations → backups) and a "where is what" table of config and data folders. | none |
| `install.md` Installation and updates | H | Required and optional mods, matching versions, Fabric and NeoForge, client and server, updating, the "did not load this world" screen. | `shared/load-refused.png` |
| `features.md` Features you can turn on and off **new** | R | One table per area, every switch of both mods with default, where to change it, and a link. Areas: gameplay (villager trading, emerald replacement, allow all items, currency mods, account and company limits), markets (virtual order book, plugins, news per market and per event, trading hours, maintenance), protection (trade cooldown, max order size, profit and pump-and-dump alerts, suspicion flags, daily digest), integrations (placeholders, Discord, web interface, LuckPerms sync), logging. | none |
| `permissions.md` Admins and permissions | R | The admin flag of each mod vs. operator levels, `/banksystem op`, `/stockmarket op`, all permission nodes, LuckPerms sync, account rights (short, links the player page). | none |
| `commands.md` Admin commands | R | Every admin command of both mods with its permission. | none |
| `multi-server.md` Several servers, one economy | C+H | Master and slaves, `MultiServerConfig.json`, trusting slaves, what runs where, what players see on an untrusted or disconnected slave. | `shared/master-slave.svg` |
| `backups.md` Data files and backups | H | Data folders of both mods, `/banksystem backup` and `/stockmarket backup`, automatic safety copies, the export package. | none |
| `troubleshooting.md` Troubleshooting **new** | R | World load refused, missing items after removing a mod, untrusted-slave banners, "not connected to the master", screens that won't open. | none |

### Integrations (both mods)

| Page | Type | Covers | Images |
|---|---|---|---|
| `placeholders.md` Placeholders | R | TAB / Placeholder API placeholders of both mods. | none |
| `discord.md` Discord feed | H | Webhook files, message types of both mods, templates. | `shared/discord-feed.png` |
| `web-interface.md` Web interface **new** | H | StockMarket's read-only price page: turning it on, the port, what it shows, that it has no login. | `stockmarket/web-interface.png` |

### Audit and anti-cheat (both mods) **new group**

| Page | Type | Covers | Images |
|---|---|---|---|
| `admin/audit/index.md` What the mods record | C | Transaction ledger, balance history, admin action log, suspicion flags, StockMarket order origin and trade alerts: what each holds, where it is stored, who can read it. | none |
| `admin/audit/alerts.md` Alerts and suspicion flags **moved** (absorbs `admin/stockmarket/alerts.md`) | R | BankSystem's nine flags and their settings, StockMarket's profit and pump-and-dump alerts, who receives alerts, `/... alerts on|off`, restoring a suspended currency binding. | `shared/alert-chat.png` |
| `admin/audit/investigating.md` Investigating in game | H | `/banksystem audit` (filters, CSV export), `/banksystem history` with flag markers, server history; then freeze and correct (links to Managing accounts). | `banksystem/audit-screen.png`, `banksystem/balance-history-flags.png`, `banksystem/server-history.png` |
| `admin/audit/reports.md` Daily digest and reports | H | The daily digest, `/banksystem auditreport <hours>`, the audit log files. | none |
| `admin/audit/audit-tool.md` Audit Tool | H | The offline Windows tool: `/banksystem backup export` on every server, open the saves, follow findings, export the report. Links to its download page. | 3 existing Audit Tool screenshots |

### BankSystem

| Page | Type | Covers | Images |
|---|---|---|---|
| `admin/banksystem/index.md` BankSystem admin | O | The admin tools at a glance. | none |
| `settings.md` Mod Settings | R | Every setting of the screen and its `settings.json` key. | `banksystem/mod-settings.png` |
| `bankable-items.md` Bankable items **merged** (absorbs `item-components.md`) | H+R | The Bank Settings screen, allow and disallow commands, what removing an item does, items whose data changes (volatile and deposit-gated components). | `banksystem/bank-settings.png` |
| `accounts.md` Managing accounts | H | Admin mode in the account screen: edit balances, unlock, create banks, freeze; `/money add|set|remove`. | `banksystem/account-admin-mode.png` |
| `companies.md` Companies and shares **new** | H | Company limits, share symbols (`/banksystem symbols`), share alerts, removing share banks, closing a company market. | none |

### StockMarket

| Page | Type | Covers | Images |
|---|---|---|---|
| `admin/stockmarket/index.md` StockMarket admin | O | The admin tools and the setup order. | none |
| `setup-use-cases.md` Choosing a market style | C | Bot-driven market with a virtual order book vs. a player-driven market. | none |
| `markets.md` Markets | H | The Management screen: **Overview** and **Create Markets** tabs, **Market Settings**, maintenance, deleting, broken markets, `/stockmarket open|close`. | `stockmarket/management-overview.png`, `stockmarket/create-markets.png`, `stockmarket/market-settings.png` |
| `presets.md` Presets | H | The **Presets** tab and `/stockmarket preset add`. | `stockmarket/presets-tab.png` |
| `mod-settings.md` Mod Settings | R | Every setting and its key, including order limits and trade cooldown. | `stockmarket/mod-settings.png` |
| `trading-hours.md` Trading hours | H | Opening hours per market, in-game or real clock, manual open and close. | none |
| `villager-trading.md` Villager trading | R | The settings and the price table. | none |
| **Plugins**: `index.md` + 5 plugin pages | H+R | Plugin Management (add, order, subscribe markets, performance bar), plugins from other mods; one settings page per plugin (`order-book-volume.md` is the pilot). | `stockmarket/plugin-management.png`, one settings shot per plugin |
| **News**: 8 pages as in the current nav | H+R | Unchanged (`config-files.md` is the pilot). | `stockmarket/news/*.png` (4 shots) |

## 5. Developers

| Page | Type | Covers | Images |
|---|---|---|---|
| `developers/index.md` Developers | O | Which API for which job (table), a first call for each mod, the sync / async and master / slave rule in short. | none |
| `setup.md` Setting up your project **new** | H | JitPack repository, Gradle dependencies (`modCompileOnly`), version ranges in `fabric.mod.json` / `neoforge.mods.toml`, starting from the example plugin project. | none |
| **StockMarket → Custom plugins**: `plugins/index.md`, `getting-started.md`, `api-reference.md`, `examples.md` | C, T, R | How plugins work (life cycle, tick order, subscriptions, time budget); tutorial built on the example project (`PriceFloorPlugin`); the reference; more examples. | `stockmarket/dev/plugin-lifecycle.svg`, `stockmarket/dev/example-plugin.png` |
| `market-access-api.md` Market access API | R | Reading markets and placing orders: sync, async and client interfaces. | none |
| `market-creation-api.md` Market integration API | R | `IStockMarketIntegration` (open, close, pause markets) and the client integration (trade screen, price chart widget). | none |
| **BankSystem**: `api.md`, `events.md`, `transaction-ledger.md`, `currency-integration.md`, `item-price-provider.md` | R | As in the current nav. The ledger page also covers adding files to the export package. | none |
| `companies-api.md` Companies, payouts and dividends **new** | R | Payout manager, dividend payer, share visuals. | none |

## 6. Changes to the current skeleton

| Change | Pages |
|---|---|
| Nav regrouped into Home / Player Guide / Server Admin / Developers | `mkdocs.yml` only, no file moves for player pages |
| New pages (14) | `together.md`, `banksystem/payouts.md`, `banksystem/company-market.md`, `stockmarket/company-shares.md`, `admin/features.md`, `admin/troubleshooting.md`, `admin/web-interface.md`, `admin/audit/index.md`, `investigating.md`, `reports.md`, `audit-tool.md`, `admin/banksystem/companies.md`, `developers/setup.md`, `developers/banksystem/companies-api.md` |
| Merged away (4) | `banksystem/atm.md` → `money.md`; `stockmarket/trading-hours.md` → `trading.md`; `admin/banksystem/item-components.md` → `bankable-items.md`; `admin/stockmarket/alerts.md` → `admin/audit/alerts.md` |
| Moved | `admin/banksystem/audit.md` → split over `admin/audit/` |
| Follow-ups | `planning/inventory.md` target column, the style guide's trading-hours example, the placeholder rule in the style guide (see images.md) |

## 7. Order of work

1. Apply the structure: nav, new stubs, merges, the placeholder image, the home page.
2. Write the Start here pages and the home page first: they decide how the rest links together.
3. Player Guide, then Server Admin, then Developers. BankSystem pages in coordination with the BankSystem session.
4. Screenshots arrive in batches; each one replaces its placeholder.
