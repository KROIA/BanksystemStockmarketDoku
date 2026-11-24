# Style guide: BankSystem & StockMarket documentation

This guide applies to every page under `docs/`. It lives in `planning/`, outside `docs/`, so it is never part of the site.

The three pilot pages are the reference examples:

- How-to / concept for players: `docs/stockmarket/trading.md`
- Concept + how-to for admins: `docs/admin/stockmarket/news/config-files.md`
- Settings reference: `docs/admin/stockmarket/plugins/order-book-volume.md`

## 1. Who reads what

Every page is written for exactly one reader group. The nav tab tells you which:

| Tab | Reader | Knows | Wants |
|---|---|---|---|
| Home, Player Guide | Player | Minecraft, not markets or config files | to do something in the game |
| Server Admin | Server owner or operator | config files, commands, mods folder | to set up and tune the server |
| Developers | Mod author | Java, Architectury, Gradle | to call the API |

If a topic matters to two groups, write two pages and link them. Example: players read [Trading basics → When a market is closed](../docs/stockmarket/trading.md) (what a closed market looks like), admins read [Trading hours](../docs/admin/stockmarket/trading-hours.md) (how to set the hours).

## 2. Tone

- **Plain language.** Write for a player whose first language may not be English. Prefer everyday words: "use" not "utilise", "about" not "approximately".
- **Second person.** "You place an order", not "the player places an order" or "one can place".
- **Short sentences.** One idea per sentence. Aim for 15 words, rarely above 25.
- **Active voice.** "The mod writes the file", not "the file is written".
- **Lead with the task or the answer.** The first paragraph says what the page is for. Background comes after.
- **Explain jargon on first use**, or link to the [Glossary](../docs/glossary.md).
- **No internal history.** No task IDs (SM-123), no "since version X fixed Y", no developer reasoning. A version is mentioned only when the reader must act on it (upgrade notes).
- Contractions are fine ("don't", "you're").
- Use a real minus sign or "−" in formulas, "×" for multiplication, and "→" for menu paths.

## 3. Page types and templates

Pick one type per page. If a page needs two, split it or use the order shown in the pilot pages (concept first, then steps, then reference).

### 3.1 Concept

Explains what something is and how it behaves. No steps.

```markdown
---
title: <Thing>
description: <One sentence: what the reader learns.>
---

# <Thing>

<What it is and why it matters, 2-4 sentences.>

## How it works
<Short paragraphs, a diagram if it helps.>

## What this means for you
<Consequences in play, as a list.>

## Related pages
- [..](..): <why to go there>
```

### 3.2 How-to

Gets the reader from A to B. Numbered steps, one action each.

```markdown
---
title: <Verb phrase, e.g. "Placing an order">
description: <One sentence.>
---

# <Title>

<Goal in one or two sentences.>

## Before you start
- <What the reader needs.>

## Steps
1. <One action.> <Result, if not obvious.>
2. ...

## If something goes wrong
| Message | What it means | What to do |
|---|---|---|

## Related pages
```

### 3.3 Settings reference

Lists every setting of one screen, plugin or file.

```markdown
---
title: <Plugin or screen name>
description: Settings reference for <...>.
---

# <Name>

*In the plugin list: **<RegisteredName>*** (plugins only)

<What it does, when to use it, 2-4 sentences.>

## How it works with ... (optional)

## Changing the settings
<Where the screen is: command → button. Buttons table.>

## Settings
| Setting | Default | Range | What it does |
|---|---|---|---|
| **<GUI name>** | `<value>` | <range> | <one sentence> |

## <Group> : <what it is for>
<One section per group of related settings: explanation, example, tuning tips.>

## Generic settings (plugins only)

## Related pages
```

For files without a screen (for example `settings.json` keys with no GUI field), add a **Key** column with the key in code.

### 3.4 Troubleshooting

One problem per section, written as the symptom the reader sees.

```markdown
## <Symptom, e.g. "My order says 'Trading too fast'">

**Cause:** <one or two sentences>

**Fix:**
1. <step>
```

Short troubleshooting lists can be a table (Message | What it means | What to do) at the end of a how-to page instead.

## 4. Names, settings and keys

- **GUI names exactly as in `en_us.json`,** in bold: **Volume Scale**, **Reset Volume**, **Pending Orders**. Copy the casing, units and punctuation, e.g. **Trend Period (min)**, **Trade cooldown (ms)**.
- **Messages** the game prints go in italics with quotes off: *Order too large: max N items per order*. Replace `%s` with a capital letter or a word (N, <market>).
- **Config keys, JSON fields, IDs and values** go in code: `TRADE_COOLDOWN_MS`, `peakFactor`, `minecraft:diamond`, `2880`.
- A setting that has both a GUI name and a key: GUI name first, key in code after it, once per page:
  **Trade cooldown (ms)** (`TRADE_COOLDOWN_MS`).
- Block and item names as the game shows them: **Stock Market Block**, **Bank Terminal Block**, **Trading Software**. Don't invent short forms.
- Mod names: **StockMarket**, **BankSystem**, **ModUtilities** (one word each). The site is **BankSystem & StockMarket**.
- Server roles: **master** and **slave** (lower case), as in the config file.

When the docs and the code disagree, the code wins. Check the default values in the code, not in old docs.

## 5. Admonitions

Use the Material syntax. Keep them rare: at most three per page. A page full of boxes has no emphasis left.

| Type | Use for | Example |
|---|---|---|
| `!!! note` | Extra information that is easy to miss | Frozen accounts can't trade |
| `!!! tip` | A shortcut or better way | Reload without a restart |
| `!!! warning` | Something that loses data, money or work, or surprises the reader | Deleting a shipped event brings it back |
| `!!! danger` | Data loss or a broken world that can't be undone | Deleting all markets |
| `!!! info "Not written yet"` | Stub pages only | |

Don't use `!!! example`, `!!! question` or collapsible boxes (`???`) unless the content is genuinely optional (a long JSON example may go in `??? example`).

## 6. Commands, JSON and file paths

- **Commands** in inline code, with the slash: `/stockmarket news reload`. Arguments in angle brackets for required, square brackets for optional: `/stockmarket news trigger <eventId> [market]`.
- A command the reader should copy goes in its own block:

  ````markdown
  ```text
  /stockmarket news reload
  ```
  ````

- **JSON** in a fenced block with the `json` language and, if it is a whole file, a title:

  ````markdown
  ```json title="config/StockMarket/news/scheduler.json"
  { ... }
  ```
  ````

  Show complete, valid JSON. Use `...` only outside the JSON block, never inside it.
- **Folder trees** in a `text` block with box-drawing characters (see the news config page) and a short comment per line.
- **File paths** in inline code with forward slashes, relative to the folder the reader knows: `config/StockMarket/news/`, `world/data/StockMarket/settings.json`. Put placeholders in angle brackets: `<server folder>/config/...`. End folders with `/`.
- **Menu paths** with arrows: `/stockmarket manage` → **Manage Plugins**.
- **Formulas** in a `text` block, with words, not code variable names.

## 7. Images

- Images go in `docs/assets/images/<mod>/` (`stockmarket/`, `banksystem/`, `shared/`). Copy only images a page uses.
- New file names are kebab-case and say what they show: `banksystem/bank-terminal-crafting.png`. [images.md](images.md) lists every planned image with its file name.
- Every image is a centred figure with a width and a real alt text (what the image shows, for readers who can't see it):

  ```markdown
  <figure markdown="span">
    ![The trading screen with the price chart on the left](../assets/images/stockmarket/StockMarketTerminal.gif){ width="600" }
  </figure>
  ```

- **Width 600** by default. **Recipes 350.** Small block icons 100. Small order book animations 350.
- All images can be clicked to zoom (glightbox). Add `{ .no-zoom }` for tiny icons.
- Screenshots: GUI scale 2 or 3, English game language, no personal player names or server names in the shot.
- Charts: SVG with a light background. Keep the colours readable in dark mode (the site rounds the corners).
- **Missing images** use the placeholder and name the planned file in a caption. The alt text is already the final one:

  ```markdown
  <figure markdown="span">
    ![The Bank Terminal with the item banks of the account](../assets/images/placeholder.svg){ width="600" }
    <figcaption>Image missing: banksystem/bank-terminal.png</figcaption>
  </figure>
  ```

  When the file arrives, its path replaces `placeholder.svg` and the `figcaption` line goes. Search for `placeholder.svg` to list the open ones.

## 8. Links

- **Relative links to `.md` files**, never to the built `.html` or to GitHub: `[Bank Terminal](../banksystem/bank-terminal.md)`. The build checks them (`mkdocs build --strict`).
- **Link to a section** with its anchor: `[scheduler.json](config-files.md#schedulerjson)`. The anchor is the heading in lower case, spaces as `-`, punctuation dropped.
- **Cross-links between mods** are normal links, not "see the other mod's docs". When a StockMarket page needs a bank concept, link the BankSystem page at the point of need, e.g. "your [BankSystem bank account](../banksystem/bank-accounts.md)". Shared topics (multi-server, permissions, placeholders, Discord, backups) live once under **Server Admin → Both mods**; mod pages link there instead of repeating them.
- Link text says where the link goes. Never "click here" or "this page".
- Each page ends with a **Related pages** list of 2-4 links, each with a few words on why.
- External links (CurseForge, Modrinth, GitHub) only on the Home, Installation, Audit Tool and Developers → Setting up your project pages.

## 9. Front matter

Every page starts with:

```yaml
---
title: Trading basics          # shown in the nav and the browser tab
description: One sentence.    # shown in search results and link previews
---
```

- `title` matches the page's `# Heading`.
- `description` is one sentence, under 160 characters.
- Optional: `hide: [toc]` on short pages, `hide: [navigation]` on the home page.

## 10. Translations (German later)

- English pages are `page.md`. A German page is `page.de.md` in the same folder. Images are shared.
- Missing German pages fall back to English automatically.
- Nav titles are translated in `mkdocs.yml` under the `de` language's `nav_translations`.
- Write English with translation in mind: short sentences, no idioms, no puns, GUI names in bold so the translator can swap them for the German `de_de.json` names.

## 11. What never goes on the site

- Development and test tools: the autotest, the test matrix, `run_matrix`, the tracker, dev-only commands (`/stockmarket test`, `/banksystem test`, `exportrecipes`), `enable_dev_features`, test suites, test classes.
- Task and issue IDs, changelog history, internal class names on player and admin pages (developer pages may name API classes).
- Real player names, server names, UUIDs or IP addresses.
- "Buy me a coffee" and download tables are for the Home page only.
