# Image list

Every image that [structure.md](structure.md) plans, grouped by who makes it. File names are paths under `docs/assets/images/`. Until an image exists, its page shows a placeholder (see the end of this file).

Totals: 46 plain screens (section 2) and 18 pictures and GIFs in the world (section 1), all scripted, plus 1 optional GIF. For you: the Discord feed picture (the home corner is built, see section 1). 4 diagrams (done), recipe images from the export command, and a few reused files.

User decision 2026-11-24: script every image except the Discord feed. Tracker items:
- BS-288 (24 BankSystem plain screens) and SM-358 (22 StockMarket plain screens): section 2.
- BS-291 (BankSystem pictures in the world and 1 GIF) and SM-361 (StockMarket and shared pictures in the world, 1–2 GIFs): section 1.
- TK-14: the test kit pieces these still miss (GIF recording with a drawn pointer, hover, crop, using an item on a block, extra mods in a cell, on-demand suites).

**Stand-ins from the old docs (2026-11-24).** 13 files below are copies of old pictures from the mod repos, checked for names, IDs and outdated labels. The scripted runs overwrite them under the same name (all of them are replaced, 2026-11-24):
- BankSystem (replaced): `money-items`, `money-stockpile`, `automation-setup` (HUD and hand visible), `server-history`, `mod-settings` (shows the **Suspicious activity** group), `share-stamper`, `share-visuals`.
- StockMarket (replaced): `web-interface`, `newspaper`, `news/active`, `news/all-events`, `news/scheduler`, `news/event-details`.
- Not used: the old `settingsGUI.png` (shows a removed setting), and every old picture with a real player name, "Dev", "Tester_1" or a UUID in it.

## Rules for every picture

- **Window 1920×1080, GUI scale 2** for every picture, BankSystem and StockMarket (user decision 2026-11-24: at 1280×720 buttons overlapped). English, vanilla resource pack. The pages stretch every picture to the text width (recipes and block icons excepted) and open the full size on click.
- **In the world:** HUD hidden unless the row says "HUD on", noon and clear weather, no overlays of other mods (JEI, minimap).
- **Names are invented:** players **Tavrik**, **Quenby** and **Brindle** (the same as in the Audit Tool pictures), the company **Acme Mining**, the accounts **Savings** (Tavrik) and **Farm Co-op** (Tavrik and Quenby). Never a real player name, never "Dev".
- **Numbers look real** but round: 12'450.00 $, 64 iron ingots.
- **GIFs:** one action each, 5–10 seconds, 10 frames per second, under about 5 MB (scaled down to about 800 px wide if needed; the pages stretch them to the text width). A drawn mouse pointer shows where the script clicks.
- Save each file under the exact name below. PNG for still images.

## 1. In the world, GIFs and outside the game (scripted: BS-291, SM-361)

### Common scene

- **Place:** the home corner below, for every picture in the world. No mobs except where listed.
- **Camera:** `/tp @s <x> <y> <z> <yaw> <pitch>` from the camera table below. Everything the row lists must be in the picture.
- **Settled markets:** about 10 markets (diamond, iron, gold, emerald, coal, copper, redstone, lapis, wheat, oak log) with the default plugins, run with `/tick sprint` until the charts show several hours of candles. The same world can serve the plain screens of section 2.
- **History by real time** (balance history, company statistics) can't be fast-forwarded: write invented history directly through a dev-only hook.
- These shots take minutes. They run on demand (`--only <topic>`), never in the normal test runs.

### The home corner

Built by the user on 2026-11-24: world `DemoCorner` (superflat, Prism instance "1.21.1 neoforge", BankSystem and StockMarket 2.2.0). All coordinates are world coordinates. The corner spans x 6..26, y -60..-55, z -13..6 (21×6×20), so its origin is (6, -60, -13).

- **Floor:** jungle planks at y -60, so players stand at y -59.
- **Walls:** stripped oak logs, 6 high. West wall at x 6, south wall at z 6. Open to the north and east, no roof, so sky shows above the walls.
- **West wall,** everything at x 7 facing east, from north to south:
  - z -9 to -8: chest on a hopper that feeds the **Bank Upload Block** (z -8), with a lever on its south side.
  - z -6 to -4: **Bank Download Block** (y -58) above a hopper into a chest (z -6), with a lever on its south side.
  - z -3: **Stock Market Block**. z -2: **Bank Terminal Block**. z -1: **Share Stamper**.
  - z 0 to 5: a counter of polished diorite slabs. Above it, four item frames with **Software**, **ATM Software**, **Banking Software** and **Trading Software**.
- **South wall,** everything at z 5 facing north, from west to east:
  - x 12: **Money Stockpile** on a slab, already filled, with a 2×1 **Bank Display** above it (x 11–12).
  - x 14–15: 2×2 **Bank Display**.
  - x 17–18: three 2×1 **Stock Market Displays** stacked, each with a price chart.
  - x 20–22: 3×2 **Stock Market Display** with a price chart.
- **Not in the corner:** ATM, a plain Terminal Block, a villager. The script places them where a row needs them.

**The structure file** `planning/structures/home-hero.nbt` (vanilla structure template, DataVersion 3955, 21×6×20, air included) was converted from the world on 2026-11-24 with `planning/structures/export_corner.py`. Run it again after changing the corner: `python planning/structures/export_corner.py "<world dir>" planning/structures/home-hero.nbt`.

- **No player data:** the Bank Terminal Block's `PlayerData` (the builder's UUID) is emptied, and the item frames' own UUIDs are left out.
- **Place it at its origin:** copy it to `<test world>/generated/docs/structures/home-hero.nbt` and run `/place template docs:home-hero 6 -60 -13` in a superflat world. Display blocks point to their screen's main block by absolute coordinates (`ctrlX/Y/Z`), so anywhere else the script must rebuild the displays.
- **Set the displays again:** their settings use market IDs of the old world (Savings' **Balance History** on the Bank Displays; on the Stock Market Displays diamond on the 3×2 one and lapis, redstone and emerald on the three 2×1 ones; gold and iron looked flat because of running news events).
- **Refill the Money Stockpile:** it stores BankSystem's internal item numbers of the old world, which can point to other items in a new world.

**Camera spots.** Feet position for `/tp`, eyes are 1.62 higher. Yaw 0 looks south, 90 west. Rows marked *tuned* are the values the StockMarket and BankSystem runs used (2026-11-24); the others are start values worked out from the block positions, to fine-tune in the first run.

| File | Position (x y z) | Yaw | Pitch | Before the shot |
|---|---|---|---|---|
| `shared/home-hero` *(tuned)* | 27.0 -58.52 1.0 | 69.5 | -4 | FOV 40, FOV effects off |
| `banksystem/blocks-overview` *(tuned)* | 15.5 -58 -7.0 | 53 | 10 | ATM and Terminal Block as for terminal-family |
| `banksystem/automation-setup` | 11.5 -59 -3.5 | 127 | 13 | both levers on, both blocks connected to Savings |
| `shared/terminal-family`, `stockmarket/news-toast` *(tuned)* | 11.5 -59 -2 | 90 | 14 | Terminal Block at (7, -59, -4), ATM at (7, -59, -1) in place of the Share Stamper, both facing east |
| `banksystem/display-in-world` *(tuned)* | 15.0 -58.62 1.5 | 0 | -6 | FOV 50; 2×2 Bank Display: Balance History |
| `stockmarket/display-in-world` *(tuned)* | 23.99 -58.82 -2.37 | 17 | -1 | FOV 30, FOV effects off; 3×2 display: diamond chart, Stock Market Block below it |
| `banksystem/money-stockpile` *(tuned)* | 12.5 -58.7 3.6 | 0 | 25 | FOV 50 |
| `shared/program-terminal.gif` | 11.5 -59 1.5 | 90 | 3 | Terminal Blocks on the counter at (7, -58, 3) and (7, -58, 2), each below its software item frame, facing east; HUD on; the camera pans right between the two |

### BankSystem (BS-291)

| File | Page | Scene | Needs |
|---|---|---|---|
| `banksystem/blocks-overview.png` | BankSystem overview | The west wall of the home corner with ATM and Terminal Block added, and the Bank Displays on the south wall showing **Balance History**. | |
| `banksystem/money-items.png` | Money and the ATM | Every coin (**1 Cent** to **50 Cent**, **Dollar**) and every banknote (**5 Dollar** to **1'000'000 Dollar**) in item frames on a wall, sorted by value, coins in the top row. Camera straight in front. | |
| `banksystem/money-stockpile.png` | Money and the ATM | The Money Stockpile on its slab in the home corner, close up. | |
| `banksystem/automation-setup.png` | Automation | Chest → hopper → Bank Upload Block and Bank Download Block → hopper → chest in the home corner, both levers on, both blocks connected to Savings. | |
| `banksystem/display-in-world.png` | Bank Display | The 2×2 Bank Display in the home corner showing **Balance History** of Savings over 7 days. Camera centred in front. | |
| `banksystem/share-items.png` | Shares | The inventory screen with two or three Company Shares of different designs (Acme Mining and one more company). The mouse rests on one, so its tooltip with the supply shows. | TK-14: hover |
| `banksystem/bank-terminal-deposit.gif` | Bank Terminal, Getting started | The Bank Terminal of Savings, 64 iron ingots in its slots: click **Send items to bank**. Then **+10** on iron and **Receive items from bank**. About 8 s. | TK-14: GIF, pointer |
| `banksystem/currency-bindings.png` | Currency bindings | **Currency Bindings** of Tavrik's personal account: the Spur slot bound to Tavrik's Numismatics account, with a balance. | done 2026-11-24, see the note below |
| `banksystem/currency-bind-dialog.png` | Currency bindings | The **Bind...** dialog on the Spur slot, **Pick an account** showing Tavrik's Numismatics account. | done 2026-11-24 |

Currency bindings shots (taken 2026-11-24): BankSystem's on-demand suite `banksystem/bs_docs_shots/DocsCurrencyShotsSuite`, run in the user's Prism instance `1.21.1 currencyIntegration_numismatics` (Create 6.0.10, Numismatics 1.0.20) instead of a test cell. Retake: put BankSystem's dev jar (the suite inside, ModUtilities bundled) and the TestKit jar into the instance's `mods`; close Prism; set the instance's Java arguments `-Dmodutilities.autotest=client -Dmodutilities.autotest.mods=banksystem -Dmodutilities.tests.include=banksystem/bs_docs_shots/DocsCurrencyShotsSuite -Dmodutilities.autotest.world=new -Dmodutilities.autotest.results=<dir>/results.json -Dmodutilities.autotest.screenshots=<dir>`; launch with `prismlauncher.exe --launch "1.21.1 currencyIntegration_numismatics" --offline Tavrik` (the suite expects that name, and no real account name shows); the client makes a world `autotest-new`, takes both shots and quits; then remove the arguments again.

### StockMarket and shared (SM-361)

The shared pictures show both mods, so they are taken in the StockMarket cells, which load BankSystem too.

| File | Page | Scene | Needs |
|---|---|---|---|
| `shared/home-hero.png` | Home | The whole home corner, placed from `planning/structures/home-hero.nbt` with `/place template`, displays filled by the script. | the structure file |
| `shared/terminal-family.png` | How the two mods work together | Terminal Block, Stock Market Block, Bank Terminal Block and ATM in a row on the west wall, fronts to the camera. | |
| `shared/program-terminal.gif` | Getting started | Two Terminal Blocks side by side on the counter, below the software in the item frames, HUD on (the held item shows). Holding Banking Software, right-click the first: it becomes a Bank Terminal Block. Switch to Trading Software, right-click the second: it becomes a Stock Market Block. About 8 s. | TK-14: GIF, use item on block |
| `shared/alert-chat.png` | Alerts and suspicion flags | HUD on. With low thresholds, trigger one BankSystem suspicion alert and one StockMarket **Profit alert**, so both show in chat. Cropped to the chat. | TK-14: crop |
| `stockmarket/display-in-world.png` | Stock Market Display, StockMarket overview | The Stock Market Displays in the home corner, the 3×2 one with the diamond chart. Camera diagonal. | |
| `stockmarket/news-toast.png` | Market news | HUD on, **Enable news popups** ticked, standing in the terminal-family scene. Start a news event and shoot while its popup is in the top-right corner. Cropped to the popup, 360×100; the page shows it at its own size. | |
| `stockmarket/villager-trade.png` | Villager trading | A villager with several trades (e.g. a toolsmith) and prices in money, its trade screen open. Daylight, cropped to the trade window (560×340). | |
| `stockmarket/web-interface.png` | Web interface | **Web interface (read-only)** on. While the server runs, a headless browser (e.g. `firefox --headless --screenshot --window-size=1920,1080 <url>`) opens `http://127.0.0.1:<port>/` showing one market (diamond): chart, order book, recent trades. | a browser on the test PC |
| `stockmarket/dev/example-plugin.png` | Developers → Your first plugin | **Plugin Management** with the example plugin (`PriceFloorPlugin`) added to diamond, its entry open with its settings form. | done 2026-11-24, see the note below |
| `stockmarket/trading-screen.gif` *(optional, done)* | Trading basics | Open a Stock Market Block, pick diamond in the favourites bar, place a small market buy; the trade shows in **My History**. About 10 s. Replaces the old `StockMarketTerminal.gif`. | TK-14: GIF, pointer |

Example plugin shot (taken 2026-11-24): StockMarket's on-demand suite `stockmarket/sm_docs_plugin` (SM-361), run in the Prism instance `1.21.1 currencyIntegration_numismatics` like the currency shots above. Retake: put StockMarket's dev jar and the example plugin's `stockmarketplugin-neoforge-1.21.1-1.1.0.jar` (from `mods/StockMarketPlugin/StockMarketExamplePlugin/neoforge/build/libs/`) into the instance's `mods` next to BankSystem, TestKit and Architectury; close Prism; set the Java arguments as for the currency shots but with `-Dmodutilities.autotest.mods=stockmarket -Dmodutilities.tests.include=stockmarket/sm_docs_plugin`; launch offline as Tavrik; then remove the arguments and the example plugin jar. Known flaw: the NewsPlugin description above the entry is cut off at the right ("...move ma"), a StockMarket label bug; retake once it wraps.

### Your part

1. **The home corner:** built (world `DemoCorner`, see above). No armor stands needed: the camera spots come from the block positions. Still open: the structure file `planning/structures/home-hero.nbt`.
2. **`shared/discord-feed.png`** (Discord feed page): a Discord channel with 4–5 feed messages (a buy, a sell, a deposit, an alert), sent to a test webhook. Crop to the messages; no server name, no real names. 2026-11-24 (user): the TestKit session posts them with invented names (player MinerMia, company Oak & Iron Co.) to the user's webhook-test channel; the user takes the screenshot.

## 2. Plain screens (scripted: BS-288, SM-358)

These show one screen with no movement. TestKit can take them in a client GUI suite (`Screenshots.take(...)`, done in TK-4): fixed 1920×1080 window, GUI scale 2, HUD hidden, invented data. BankSystem already writes `banksystem/bank_account_selection.png` this way. Scripted shots can be retaken in one run whenever a screen changes, and later in German for the German pages. Decided 2026-11-24: the BankSystem session scripts its 24 (BS-288), the StockMarket session its 22 (SM-358).

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
