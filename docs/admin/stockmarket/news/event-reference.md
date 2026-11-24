---
title: "Event file reference"
description: "Every field of a news event file: headline, text, impact, markets, announce delay and validation."
---

# Event file reference

This page lists every field a news event can have. Where the files go and in which order they load is on [News config files](config-files.md). For a gentle start, follow [Writing your first event](tutorial.md).

## File formats

A file holds either **one event** or **a list of events**.

One event per file, like the files in `DefaultEvents/`:

```json title="config/StockMarket/news/MyServer/iron_shortage.json"
{
  "id": "iron_shortage",
  "headline": "Iron runs short!",
  "text": "The smelters can't keep up with demand.",
  "impact": { "type": "shock", "peakFactor": 0.3 },
  "markets": [ { "item": "minecraft:iron_ingot" } ]
}
```

Several events in one file, with an optional `scheduler` block:

```json title="config/StockMarket/news/my_events.json"
{
  "scheduler": {
    "minSecondsBetweenEvents": 3600
  },
  "events": [
    {
      "id": "iron_shortage",
      "headline": "Iron runs short!",
      "text": "The smelters can't keep up with demand.",
      "impact": { "type": "shock", "peakFactor": 0.3 },
      "markets": [ { "item": "minecraft:iron_ingot" } ]
    },
    {
      "id": "iron_glut",
      "headline": "Iron floods the market",
      "text": "A new mine doubles the supply.",
      "impact": { "type": "trend", "peakFactor": -0.2 },
      "markets": [ { "item": "minecraft:iron_ingot" } ]
    }
  ]
}
```

A file with an `id` at the top and no `events` or `scheduler` is read as one event. Everything else must have an `events` list.

## Event fields

| Field | Needed | Default | What it does |
|---|---|---|---|
| `id` | yes | | Unique name of the event. Commands, chains and requirements use it. Use lower case and `_`, for example `iron_shortage`. |
| `headline` | yes | | The title in the newspaper. Text, or one text per language, see [below](#headline-and-text). |
| `text` | yes | | The story under the headline. Same format as `headline`. |
| `impact` | one of the two | | A simple price effect, see [Impact](#impact). |
| `sequences` | one of the two | | A story in several steps, see [Advanced events](advanced-events.md#sequences). |
| `markets` | yes | | The items the event moves, see [Markets](#markets). |
| `category` | no | `general` | A label for your own overview. It shows in `/stockmarket news info` and changes nothing else. |
| `weight` | no | `1` | How likely the event is picked, see [Weight and cooldown](#weight-and-cooldown). |
| `cooldownSeconds` | no | `0` | How long the event can't fire again after it started. |
| `adminOnly` | no | `false` | `true`: the event only fires when an admin triggers it. |
| `announceDelayMs` | no | no delay | Publishes the headline before or after the price starts to move, see [Announce delay](#announce-delay). |
| `picture` | no | no picture | The file name of a PNG in `news/pictures/`, see [News pictures](pictures.md). |
| `requires` | no | | Conditions that must hold before the event can fire. See [Advanced events](advanced-events.md#requirements). |
| `records` | no | | Values the event writes into the world memory when it is published. See [Advanced events](advanced-events.md#the-world-event-registry). |
| `chains` | no | | Follow-up events. See [Advanced events](advanced-events.md#chains). |
| `undoes` | no | | Takes back the permanent change of another event. See [Advanced events](advanced-events.md#undoing-a-permanent-change). |

An event has either `impact` or `sequences`, never both. There is no `enabled` field: you switch events on and off with `/stockmarket news enable` and `disable` or in the News plugin window.

## Headline and text

Write a plain text, or one text per language:

```json
{
  "headline": {
    "en_us": "Iron runs short!",
    "de_de": "Eisen wird knapp!"
  }
}
```

Each player sees the text in their game language. If it's missing, they see `en_us`, and if that is missing too, the first entry. The shipped events have English, German and Simplified Chinese (`en_us`, `de_de`, `zh_cn`).

Keep headlines short. If headline and text together are larger than 32 KB, the reload report warns you.

## Weight and cooldown

When the timer runs out, the server picks one event at random from all events that can fire right now. `weight` sets the odds: an event with weight `10` is picked ten times as often as one with weight `1`. An event with weight `0` is never picked at random. Only a chain or an admin can start it.

An event can only be picked if:

- it is enabled, not `adminOnly` and not running already,
- its cooldown is over,
- its `requires` conditions hold,
- at least one of its markets is subscribed, has **News enabled** on and is below the limit of events per market.

`cooldownSeconds` starts when the event starts. It only counts while the server runs. An admin can still trigger an event during its cooldown.

## Announce delay

Without `announceDelayMs`, the headline comes out the moment the price starts to move. With it, the server picks a random delay between `min` and `max` milliseconds each time the event fires:

```json
{
  "announceDelayMs": { "min": 15000, "max": 90000 }
}
```

- **Positive values:** the headline comes first, the price follows later. Quick players can react before the market does.
- **Negative values:** the price moves first, the headline follows. Players who watch the charts can spot it before the news is out, like insider trading.

In the **Active** tab, an event whose price effect hasn't started yet shows as **Pending**, and an event whose headline isn't out yet shows *pending publication*. The reload report warns you if a negative delay is so long that the effect is over before the headline appears.

## Impact

`impact` describes a simple effect: ramp up, hold, go back.

```json
{
  "impact": {
    "type": "shock",
    "peakFactor": 0.45,
    "rampUpSeconds": 5,
    "durationSeconds": 300,
    "reversal": "exponential",
    "reversalSeconds": 300,
    "noise": 0.05
  }
}
```

| Field | Needed | What it does |
|---|---|---|
| `type` | no | `shock`, `trend` or `crash`. Sets the default timing below. Default `shock`. |
| `peakFactor` | yes | The strongest effect. `0.45` = 45% above the normal price, `-0.3` = 30% below. Must be above `-1`. |
| `rampUpSeconds` | no | How long the effect takes to grow to its peak. |
| `durationSeconds` | no | How long the effect stays at its peak. |
| `reversal` | no | How the effect goes away: `ramp` (straight line), `exponential` (fast first, then slower) or `none` (permanent). |
| `reversalSeconds` | no | How long the reversal takes. For `exponential`, see below. |
| `noise` | no | Random wobble on the effect. `0.05` makes it jump by up to 5% of its size each tick. Default `0`. |

Each `type` fills in the timing you leave out:

| Type | `rampUpSeconds` | `durationSeconds` | `reversal` | `reversalSeconds` |
|---|---|---|---|---|
| `shock` | 5 | 300 | `exponential` | 300 |
| `trend` | 120 | 600 | `ramp` | 600 |
| `crash` | 10 | 120 | `exponential` | 900 |

With `exponential`, `reversalSeconds` is the time in which about two thirds of the effect fade. The event ends after six times that, when almost nothing is left.

With `"reversal": "none"`, the effect never fades. When the hold ends, the change is written into the market's default price for good. A permanent event can be taken back with [`undoes`](advanced-events.md#undoing-a-permanent-change).

All durations are in seconds of server running time and are stretched by the scheduler's `impactDurationMultiplier`. Every `peakFactor` is scaled by `impactStrengthMultiplier`. With the shipped [scheduler.json](config-files.md#schedulerjson), every event lasts three times as long and moves prices half as far as its file says.

### How the effect is calculated

For each running event and each of its markets:

```text
factor = 1 + effect × weightFactor × Sensitivity × (1 + wobble)
```

- `effect` is the current value of the event: it grows to `peakFactor` and goes back.
- `weightFactor` comes from the [market entry](#markets).
- **Sensitivity** is the market's setting in the [News plugin](../plugins/news.md).
- `wobble` is a random number between −`noise` and +`noise`.

If several events move the same market, their factors are multiplied. The result is kept between 0.1 and 10, and the market's target price is multiplied by it.

## Markets

`markets` lists the items the event moves. Each entry has an `item` and an optional `weightFactor`:

```json
{
  "markets": [
    { "item": "minecraft:diamond" },
    { "item": "minecraft:diamond_block", "weightFactor": 0.8 },
    { "item": "#c:ores", "weightFactor": 0.3 },
    { "item": "minecraft:*_ore", "weightFactor": 0.5 },
    { "item": "minecraft:emerald", "weightFactor": -0.4 }
  ]
}
```

| Form | Example | Matches |
|---|---|---|
| Item id | `minecraft:diamond` | Exactly this item. Without a `:`, `minecraft:` is added. |
| Tag | `#c:ores` | Every item in the tag. |
| Pattern | `minecraft:*_ore` | Every item whose id fits the pattern. `*` stands for any text. |
| Item id with `components` | see below | One variant of an item, for example one enchanted book. |

`weightFactor` scales the effect for this entry (default `1`). `0.5` gives half the effect. A negative value turns it around: in the example above, emeralds get cheaper when diamonds get dearer.

If an item matches several entries, the **first** entry counts. Put exact items before tags and patterns.

For items with extra data, add `components` in the same format as in [market presets](../presets.md). Tags and patterns can't have `components`.

The event only moves markets that exist and are subscribed to the NewsPlugin with **News enabled** on. An item from a mod that isn't installed gives a warning and is skipped. If no entry is usable, the event can never fire.

## Scheduler values

These values go in `scheduler.json` or in the `scheduler` block of any events file. For each value, the file loaded last wins. Values you leave out keep their built-in default.

| Value | Built-in default | Shipped `scheduler.json` | What it does |
|---|---|---|---|
| `minSecondsBetweenEvents` | 7200 | 7200 | Shortest wait between two random events. |
| `maxSecondsBetweenEvents` | 16200 | 16200 | Longest wait. The real wait is random between the two. |
| `maxActiveEventsGlobal` | 3 | 3 | How many events may run at once. |
| `maxActiveEventsPerMarket` | 1 | 1 | How many events may move one market at once. |
| `historyMaxEntries` | 1000 | 1000 | How many news stay in the history. Older ones are deleted. `0` keeps none. |
| `impactDurationMultiplier` | 1.0 | 3.0 | Stretches every duration of every event. |
| `impactStrengthMultiplier` | 1.0 | 0.5 | Scales every effect of every event. |

The waiting times count only while the server runs. The two limits only apply to random events: admin triggers and chains ignore them.

If `minSecondsBetweenEvents` is larger than `maxSecondsBetweenEvents`, both go back to the built-in defaults. The multipliers must be above `0`. You can override the first four values while the server runs, see [News commands](commands.md#scheduler).

## Validation

Every reload checks all files and prints a report, grouped by file, errors first. Problems come in two kinds:

- **Errors** skip something. A broken file is skipped, the other files still load. Most errors in an event skip that event: a missing `id`, `headline` or `text`, both or neither of `impact` and `sequences`, a wrong value type, or a broken `requires` entry. Errors in `picture`, `records`, `chains` and `undoes` only drop that field, and the event still loads.
- **Warnings** load the event anyway, but tell you that something looks wrong: an unknown field (often a typo), an item that isn't installed, a missing picture, or an event that can never fire, for example because its `markets` list is missing or matches nothing.

The same `id` in two files is an error: the file loaded later wins, see [Load order](config-files.md#load-order).

If a reload finds no valid event at all, the events from before stay loaded. Running events are never changed by a reload: they finish with the values they started with.

## Related pages

- [Writing your first event](tutorial.md): build an event step by step.
- [Advanced events](advanced-events.md): sequences, requirements and chains.
- [Default events](default-events.md): 73 working examples.
- [News config files](config-files.md): where the files go.
