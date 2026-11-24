# Image list

Every image that [structure.md](structure.md) plans, grouped by who makes it. File names are paths under `docs/assets/images/`. Until an image exists, its page shows a placeholder (see the end of this file).

Totals: 20 for you to take (+1 optional), 46 plain screens scripted by the mod sessions, 4 diagrams by the docs agent, recipe images from the export command, and a few reused files.

## Rules for screenshots you take

- **Window 1280×720, GUI scale 2,** English, vanilla resource pack. The home picture is the exception: 1920×1080.
- **In the world:** HUD off (F1), noon and clear weather (`/time set noon`, `/weather clear`), no overlays of other mods (JEI, minimap).
- **Names are invented:** players **Tavrik**, **Quenby** and **Brindle** (the same as in the Audit Tool pictures), the company **Acme Mining**, the accounts **Savings** and **Farm Co-op**. Never a real player name, never "Dev".
- **Numbers look real** but round: 12'450.00 $, 64 iron ingots.
- **GIFs:** one action each, 5–10 seconds. Record the window with OBS, put the mp4 into `GifCreator/videos/` and run `convert.bat` (10 frames per second). Keep a GIF under about 5 MB.
- Save each file under the exact name below. PNG for still images.

## 1. Taken by you

| # | File | Page | What to show |
|---|---|---|---|
| 1 | `shared/home-hero.png` | Home | A small bank-and-market corner: Bank Terminal, ATM, Stock Market Block, a 3×2 Bank Display with a balance history, a Stock Market Display with a chart, a money stockpile on the counter. 1920×1080. Take it last, when the rest looks right. |
| 2 | `shared/program-terminal.gif` | Getting started | Holding **Banking Software**, right-click a **Terminal Block**: it turns into a Bank Terminal. Then **Trading Software** on a second Terminal Block: it becomes a Stock Market Block. About 8 s. |
| 3 | `shared/terminal-family.png` | How the two mods work together | Terminal Block, Bank Terminal Block, ATM and Stock Market Block in a row, front view. |
| 4 | `banksystem/blocks-overview.png` | BankSystem overview | Every BankSystem block placed: Terminal, Bank Terminal, ATM, Upload and Download blocks with chests, Bank Display, Share Stamper, a money stockpile. Replaces the old `overview.png`, which shows a player name. |
| 5 | `banksystem/bank-terminal-deposit.gif` | Bank Terminal, Getting started | Open the Bank Terminal, **Send items to bank** with a stack of iron, then take 10 back with the amount buttons. About 8 s. |
| 6 | `banksystem/money-items.png` | Money and the ATM | All banknotes (5 to 1'000'000) and the coins in a row, in item frames or in the inventory. |
| 7 | `banksystem/money-stockpile.png` | Money and the ATM | A money stockpile on a table, close up. |
| 8 | `banksystem/automation-setup.png` | Automation | Hopper into a Bank Upload Block with a lever; a Bank Download Block feeding a chest. Redstone visible. |
| 9 | `banksystem/display-in-world.png` | Bank Display | A 3×2 Bank Display on a wall showing **Balance History**. |
| 10 | `banksystem/share-items.png` | Shares | The inventory with two or three Company Shares of different designs, the tooltip of one open (shows the supply). |
| 11 | `banksystem/currency-bindings.png` | Currency bindings | The **Currency Bindings** screen with one bound slot. Needs Create: Numismatics or Lightman's Currency installed. |
| 12 | `banksystem/currency-bind-dialog.png` | Currency bindings | The **Bind...** dialog, picking the external account. Same setup as #11. |
| 13 | `stockmarket/trading-screen.gif` | Trading basics | Open the Stock Market Block, pick a market in the favourites bar, place a small market buy, the trade shows up in **My History**. About 10 s. Replaces the old `StockMarketTerminal.gif`. |
| 14 | `stockmarket/news-toast.png` | Market news | Playing in the world with a news popup in the corner (**Enable news popups** on). HUD on for this one. |
| 15 | `stockmarket/villager-trade.png` | Villager trading | A villager's trade screen with prices in money. |
| 16 | `stockmarket/display-in-world.png` | Stock Market Display, StockMarket overview | A 3×2 Stock Market Display with a price chart, next to a Stock Market Block. |
| 17 | `stockmarket/web-interface.png` | Web interface | The browser page with one market: chart, order book, recent trades. Crop the address bar if it shows a server address. |
| 18 | `shared/discord-feed.png` | Discord feed | A Discord channel with 4–5 feed messages (a buy, a sell, a deposit, an alert), sent to a test webhook. |
| 19 | `shared/alert-chat.png` | Alerts and suspicion flags | Chat with one BankSystem suspicion alert and one StockMarket profit alert. HUD on, cropped to the chat. |
| 20 | `stockmarket/dev/example-plugin.png` | Developers → Custom plugins | **Plugin Management** with the example plugin (`PriceFloorPlugin`) added and its settings open. Needs the example plugin mod installed. |
| 21 | `shared/load-refused.png` *(optional)* | Installation and updates | The "BankSystem did not load this world" screen. Only if it happens anyway; the page works without it. |

## 2. Plain screens: scripted (BS-288, SM-358)

These show one screen with no movement. TestKit can take them in a client GUI suite (`Screenshots.take(...)`, done in TK-4): fixed 1280×720 window, GUI scale 2, HUD hidden, invented data. BankSystem already writes `banksystem/bank_account_selection.png` this way. Scripted shots can be retaken in one run whenever a screen changes, and later in German for the German pages. Decided 2026-11-24: the BankSystem session scripts its 24 (BS-288), the StockMarket session its 22 (SM-358).

### BankSystem (24)

| File | Page | Screen and state |
|---|---|---|
| `banksystem/account-management.png` | Bank accounts | Account Management of **Farm Co-op** with two users. |
| `banksystem/account-permissions.png` | Bank accounts | **Edit Permissions** for one user: **Deposit** on, **Withdraw** and **Manage** off. |
| `banksystem/bank-terminal.png` | Bank Terminal | Bank Terminal with about 8 item banks and some inventory. |
| `banksystem/bank-terminal-crafting.png` | Bank Terminal | Crafting view, **Use Bank Items** and **Auto-deposit output** on. |
| `banksystem/balance-history.png` | Bank Terminal | **Balance History** over 7 days with a few changes. |
| `banksystem/atm-withdraw.png` | Money and the ATM | ATM **Withdraw** tab with a note combination picked. |
| `banksystem/atm-convert.png` | Money and the ATM | ATM **Convert** tab with money in the cache. |
| `banksystem/upload-block.png` | Automation | Bank Upload Block screen, connected to **Savings**. |
| `banksystem/download-block.png` | Automation | Bank Download Block screen with two orders, one with a condition. |
| `banksystem/display-config.png` | Bank Display | **Configure Display**. |
| `banksystem/company-overview.png` | Founding and running a company | Company Management **Overview** of **Acme Mining**. |
| `banksystem/company-workers.png` | Founding and running a company | **Workers** tab with two workers. |
| `banksystem/company-statistics.png` | Founding and running a company | **Statistics** tab, 7 days. |
| `banksystem/payout-edit.png` | Payouts and dividends | **Edit Payout**: a wage every Minecraft day. |
| `banksystem/pay-dividend.png` | Payouts and dividends | **Pay Dividend** with an amount per share. |
| `banksystem/share-stamper.png` | Shares and the Share Stamper | A bound Share Stamper in **Stamp** mode. |
| `banksystem/share-visuals.png` | Shares and the Share Stamper | **Share Visuals** editor with a finished design. |
| `banksystem/company-market-tab.png` | Your company on the stock market | **Market** tab with an open market (needs StockMarket loaded). |
| `banksystem/mod-settings.png` | Mod Settings (admin) | BankSystem Mod Settings, first group. |
| `banksystem/bank-settings.png` | Bankable items (admin) | **Bank Settings** with the item list and one item selected. |
| `banksystem/account-admin-mode.png` | Managing accounts (admin) | Account Management in admin mode: balance boxes, **Freeze**, **Audit**. |
| `banksystem/audit-screen.png` | Investigating in game (admin) | **Audit** screen, last 24 h, 15–20 rows. |
| `banksystem/balance-history-flags.png` | Investigating in game (admin) | Balance History with two flag markers. |
| `banksystem/server-history.png` | Investigating in game (admin) | **Balance History - Whole server**. |

### StockMarket (22)

| File | Page | Screen and state |
|---|---|---|
| `stockmarket/trading-screen.png` | Getting started | Trade screen, **Item / Money**, **Market** tab, a lively chart. |
| `stockmarket/market-closed.png` | Trading basics | Trade screen with the **Market Closed** banner and opening hours. |
| `stockmarket/price-chart.png` | Price chart and order book | Chart with candles, the order book histogram and two own order markers. |
| `stockmarket/item-item-mode.png` | Trading item for item | **Item / Item**, **Exchange** tab, I HAVE iron / I WANT diamond. |
| `stockmarket/companies-tab.png` | Trading company shares | Market selector on **Companies** with two company markets. |
| `stockmarket/newspaper.png` | Market news | **The Market Times** with three news items, one with a picture. |
| `stockmarket/display-config.png` | Stock Market Display | **Configure Display** with a pair chosen. |
| `stockmarket/management-overview.png` | Markets (admin) | Management **Overview** tab with about 10 markets. |
| `stockmarket/create-markets.png` | Markets (admin) | **Create Markets** tab with a few items selected. |
| `stockmarket/market-settings.png` | Markets (admin) | **Market Settings** of one market. |
| `stockmarket/presets-tab.png` | Presets (admin) | **Presets** tab, category **Ore**. |
| `stockmarket/mod-settings.png` | Mod Settings (admin) | StockMarket Mod Settings, **Market** group. |
| `stockmarket/plugin-management.png` | Plugins (admin) | **Plugin Management** with the five default plugins. |
| `stockmarket/plugins/net-flow-settings.png` | Net Flow plugin | Its settings screen. |
| `stockmarket/plugins/volatility-settings.png` | Volatility plugin | Its settings screen. |
| `stockmarket/plugins/target-price-bot-settings.png` | Target Price Bot | Its settings screen. |
| `stockmarket/plugins/order-book-volume-settings.png` | Order book volume plugin | Its settings screen. |
| `stockmarket/plugins/news-settings.png` | News plugin | **Per-Market News Settings**. |
| `stockmarket/news/active.png` | News (admin) | News plugin **Active** tab with one running event. |
| `stockmarket/news/all-events.png` | News (admin) | **All events** tab. |
| `stockmarket/news/scheduler.png` | News (admin) | **Scheduler** tab. |
| `stockmarket/news/event-details.png` | News (admin) | **News event details** of one event. |

The four news shots exist in the old StockMarket docs (`news_screen_*.png`, `news_event_details_screen.png`). They are recent; if they still match the game, they are copied instead of retaken.

## 3. Diagrams (made by the docs agent)

| File | Page | Content |
|---|---|---|
| `shared/economy-overview.svg` | Home, How the two mods work together | Inventory ⇄ Bank Terminal / ATM / automation ⇄ bank account ⇄ Stock Market Block ⇄ markets (players and bots); company → shares → markets. |
| `shared/master-slave.svg` | Several servers, one economy | One master with the data, two slaves, what each runs. Redrawn from the old `MasterSlaveArchitecture.drawio`. |
| `stockmarket/candle.svg` | Price chart and order book | One candle labelled open, close, high, low. |
| `stockmarket/dev/plugin-lifecycle.svg` | Custom plugins | The calls a plugin gets per tick and when it is subscribed, saved and loaded. |

## 4. Recipe images

Rendered by the dev-only recipe export command of each mod (one PNG per recipe, same look for all). The BankSystem set in `documentation/images/recipes/` came from it and is copied if still current; StockMarket needs the Stock Market Display and Newspaper recipes next to the existing `recipe_trading_software.png`. Nothing for you to take.

## 5. Reused as they are

| File | Source | Page |
|---|---|---|
| `shared/audit-tool/overview.png`, `findings.png`, `take-back.png` | `AuditTool/docs/screenshots/` (invented data) | Audit Tool |
| order book GIFs, `stockMarketTerminalBlock.png`, `recipe_trading_software.png`, the three volume SVGs | already in `docs/assets/images/stockmarket/` | pilot pages |

## Placeholders

Until a picture exists, the page uses the shared placeholder image and names the missing file:

```markdown
<figure markdown="span">
  ![The Bank Terminal with the item banks on the left](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/bank-terminal.png</figcaption>
</figure>
```

The alt text is already the final one. When the file arrives, the path replaces `placeholder.svg` and the `figcaption` line goes. Searching for `placeholder.svg` lists every open image. The build stays clean (`--strict`) the whole time because the placeholder file exists.
