# Image list

Every image that [structure.md](structure.md) plans, grouped by who makes it. File names are paths under `docs/assets/images/`. Until an image exists, its page shows a placeholder (see the end of this file).

Totals: 46 plain screens (section 2) and 18 pictures and GIFs in the world (section 1), all scripted, plus 1 optional GIF. For you: the Discord feed picture and building the home corner once. 4 diagrams (done), recipe images from the export command, and a few reused files.

User decision 2026-11-24: script every image except the Discord feed. Tracker items:
- BS-288 (24 BankSystem plain screens) and SM-358 (22 StockMarket plain screens): section 2.
- BS-291 (BankSystem pictures in the world and 1 GIF) and SM-361 (StockMarket and shared pictures in the world, 1–2 GIFs): section 1.
- TK-14: the test kit pieces these still miss (GIF recording with a drawn pointer, hover, crop, using an item on a block, extra mods in a cell, on-demand suites).

## Rules for every picture

- **Window 1280×720, GUI scale 2,** English, vanilla resource pack. This includes the home picture.
- **In the world:** HUD hidden unless the row says "HUD on", noon and clear weather, no overlays of other mods (JEI, minimap).
- **Names are invented:** players **Tavrik**, **Quenby** and **Brindle** (the same as in the Audit Tool pictures), the company **Acme Mining**, the accounts **Savings** (Tavrik) and **Farm Co-op** (Tavrik and Quenby). Never a real player name, never "Dev".
- **Numbers look real** but round: 12'450.00 $, 64 iron ingots.
- **GIFs:** one action each, 5–10 seconds, 10 frames per second, under about 5 MB (scaled down to about 800 px wide if needed; the pages show them at 600 px). A drawn mouse pointer shows where the script clicks.
- Save each file under the exact name below. PNG for still images.

## 1. In the world, GIFs and outside the game (scripted: BS-291, SM-361)

### Common scene

- **Place:** build on a calm floor (e.g. polished andesite or oak planks) with a wall behind (stone bricks or dark oak), so no sky line, void or test-area border shows. No mobs except where listed.
- **Camera:** `/tp @s <x> <y> <z> <yaw> <pitch>`, 3–5 blocks from the subject, about eye level, 10–25° down unless the row says otherwise. Everything the row lists must be in the picture.
- **Settled markets:** about 10 markets (diamond, iron, gold, emerald, coal, copper, redstone, lapis, wheat, oak log) with the default plugins, run with `/tick sprint` until the charts show several hours of candles. The same world can serve the plain screens of section 2.
- **History by real time** (balance history, company statistics) can't be fast-forwarded: write invented history directly through a dev-only hook.
- These shots take minutes. They run on demand (`--only <topic>`), never in the normal test runs.

### BankSystem (BS-291)

| File | Page | Scene | Needs |
|---|---|---|---|
| `banksystem/blocks-overview.png` | BankSystem overview | A small bank room: Terminal Block, Bank Terminal Block, ATM, a Bank Upload Block fed by a hopper, a Bank Download Block filling a chest, a 3×2 Bank Display on the back wall showing **Balance History**, a Share Stamper, a Money Stockpile on a counter. Camera at the entrance, about 20° down. | |
| `banksystem/money-items.png` | Money and the ATM | Every coin (**1 Cent** to **50 Cent**, **Dollar**) and every banknote (**5 Dollar** to **1'000'000 Dollar**) in item frames on a wall, sorted by value, coins in the top row. Camera straight in front. | |
| `banksystem/money-stockpile.png` | Money and the ATM | A Money Stockpile on a counter (e.g. smooth stone slabs): coin piles and a few upright banknotes. Close up, about 2 blocks away, 30° down. | |
| `banksystem/automation-setup.png` | Automation | Chest → hopper → Bank Upload Block with a lever on it, switched on. Next to it a Bank Download Block → hopper → chest, powered through visible redstone dust. Both connected to Savings. Camera diagonal, 25° down. | |
| `banksystem/display-in-world.png` | Bank Display | A 3×2 Bank Display on a stone brick wall showing **Balance History** of Savings over 7 days. Camera centred in front, about 4 blocks away. | |
| `banksystem/share-items.png` | Shares | The inventory screen with two or three Company Shares of different designs (Acme Mining and one more company). The mouse rests on one, so its tooltip with the supply shows. | TK-14: hover |
| `banksystem/bank-terminal-deposit.gif` | Bank Terminal, Getting started | The Bank Terminal of Savings, 64 iron ingots in its slots: click **Send items to bank**. Then **+10** on iron and **Receive items from bank**. About 8 s. | TK-14: GIF, pointer |
| `banksystem/currency-bindings.png` | Currency bindings | **Currency Bindings** of Tavrik's personal account: the Spur slot bound to Tavrik's Numismatics account, with a balance. | Numismatics in the cell (TK-14) |
| `banksystem/currency-bind-dialog.png` | Currency bindings | The **Bind...** dialog on the Spur slot, **Pick an account** showing Tavrik's Numismatics account. | same |

### StockMarket and shared (SM-361)

The shared pictures show both mods, so they are taken in the StockMarket cells, which load BankSystem too.

| File | Page | Scene | Needs |
|---|---|---|---|
| `shared/home-hero.png` | Home | Your corner, placed from `planning/structures/home-hero.nbt` with `/place template`. The script fills the displays: the Bank Display with Savings' **Balance History**, the Stock Market Display with the diamond chart. Camera at the armor stand named `camera`, which is removed before the shot. Without the file: the blocks-overview room plus a Stock Market Block and a Stock Market Display. | the structure file (your part) |
| `shared/terminal-family.png` | How the two mods work together | Terminal Block, Bank Terminal Block, ATM and Stock Market Block in a row, one block apart, fronts to the camera. Camera in front, about 4 blocks away, 10° down. | |
| `shared/program-terminal.gif` | Getting started | Two Terminal Blocks side by side, HUD on (the held item shows). Holding Banking Software, right-click the first: it becomes a Bank Terminal Block. Switch to Trading Software, right-click the second: it becomes a Stock Market Block. About 8 s. | TK-14: GIF, use item on block |
| `shared/alert-chat.png` | Alerts and suspicion flags | HUD on. With low thresholds, trigger one BankSystem suspicion alert and one StockMarket **Profit alert**, so both show in chat. Cropped to the chat. | TK-14: crop |
| `stockmarket/display-in-world.png` | Stock Market Display, StockMarket overview | A 3×2 Stock Market Display on a wall with the diamond chart, a Stock Market Block in front of it. Camera diagonal. | |
| `stockmarket/news-toast.png` | Market news | HUD on, **Enable news popups** ticked, standing in the terminal-family scene. Start a news event and shoot while its popup is in the top-right corner. | |
| `stockmarket/villager-trade.png` | Villager trading | A villager with several trades (e.g. a toolsmith) and prices in money, its trade screen open. | |
| `stockmarket/web-interface.png` | Web interface | **Web interface (read-only)** on. While the server runs, a headless browser (e.g. `firefox --headless --screenshot --window-size=1280,720 <url>`) opens `http://127.0.0.1:<port>/` showing one market (diamond): chart, order book, recent trades. | a browser on the test PC |
| `stockmarket/dev/example-plugin.png` | Developers → Your first plugin | **Plugin Management** with the example plugin (`PriceFloorPlugin`) added to diamond, its entry open with its settings form. | the example plugin jar in the cell (TK-14) |
| `stockmarket/trading-screen.gif` *(optional)* | Trading basics | Open a Stock Market Block, pick diamond in the favourites bar, place a small market buy; the trade shows in **My History**. About 10 s. Replaces the old `StockMarketTerminal.gif`. | TK-14: GIF, pointer |

### Your part

1. **The home corner, built once.** In a creative world with both mods, build a small bank and trading corner: Bank Terminal Block, ATM, Stock Market Block, a 3×2 Bank Display, a 3×2 Stock Market Display, a Money Stockpile on a counter. The displays can stay unconfigured; the script fills them. Place an armor stand named `camera` (name tag) where the picture should be taken from, facing the scene. Save everything with a structure block in **Save** mode, **Include entities** on (for the armor stand), at most 48×48×48. Then copy `<world>/generated/minecraft/structures/<name>.nbt` to `planning/structures/home-hero.nbt` in this repo.
2. **`shared/discord-feed.png`** (Discord feed page): a Discord channel with 4–5 feed messages (a buy, a sell, a deposit, an alert), sent to a test webhook. Crop to the messages; no server name, no real names.

## 2. Plain screens (scripted: BS-288, SM-358)

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
