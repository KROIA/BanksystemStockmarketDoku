---
title: "Writing your first event"
description: "Step-by-step tutorial from a minimal event to chains and testing."
---

# Writing your first event

In this tutorial you write a news event about a wheat shortage, test it, and then turn it into a small story with a follow-up event. You need the StockMarket admin flag and a market for wheat that is subscribed to the NewsPlugin. All fields are explained on the [Event file reference](event-reference.md).

## 1. Create the file

Make a folder for your own events in `config/StockMarket/news/`, for example `MyServer/`. Put this file in it:

```json title="config/StockMarket/news/MyServer/wheat_shortage.json"
{
  "id": "wheat_shortage",
  "headline": "Wheat runs short!",
  "text": "A wet summer has ruined half the harvest. Bakers are paying whatever farmers ask.",
  "adminOnly": true,
  "impact": {
    "type": "shock",
    "peakFactor": 0.3
  },
  "markets": [
    { "item": "minecraft:wheat" }
  ]
}
```

This event raises the wheat price by up to 30% and then lets it fade, with the timing of a `shock`. `adminOnly` keeps it from firing at random while you test it.

## 2. Load it

Run:

```text
/stockmarket news reload
```

The chat shows a report. If it lists a problem for `wheat_shortage.json`, fix it and reload again. Most problems are typos: a missing comma, a missing quote, or a misspelt field name, which the report shows as an *unknown field*.

## 3. Test it

Start the event:

```text
/stockmarket news trigger wheat_shortage
```

The headline is published to all players, and the event shows in the **Active** tab of the [News plugin window](index.md#the-news-plugin-window), with its phase and its effect on wheat. To test faster:

- `/stockmarket news skipphase wheat_shortage` jumps to the next phase.
- `/stockmarket news stop wheat_shortage` ends it at once and removes its effect.

You can trigger the event again as soon as it isn't running any more, also during its cooldown.

!!! tip "Testing on one market"
    Add a market to limit the event to it: `/stockmarket news trigger wheat_shortage "minecraft:wheat"`. Tab completion offers the market names.

## 4. Move more markets

Bread gets dearer too, but less. And with expensive wheat, people buy more potatoes instead. Replace `markets` with:

```json
{
  "markets": [
    { "item": "minecraft:wheat" },
    { "item": "minecraft:bread", "weightFactor": 0.6 },
    { "item": "minecraft:potato", "weightFactor": 0.3 }
  ]
}
```

`weightFactor` scales the effect: bread rises by up to 18%, potatoes by up to 9%. A negative `weightFactor` makes a market move the other way.

## 5. Add other languages

Write `headline` and `text` once per language. Players see their game language, or English if it's missing:

```json
{
  "headline": {
    "en_us": "Wheat runs short!",
    "de_de": "Weizen wird knapp!"
  },
  "text": {
    "en_us": "A wet summer has ruined half the harvest. Bakers are paying whatever farmers ask.",
    "de_de": "Ein nasser Sommer hat die halbe Ernte verdorben. Die Bäcker zahlen jeden Preis."
  }
}
```

## 6. Add a picture

Put a PNG of at most 128 KiB and 16 to 512 pixels per side into `config/StockMarket/news/pictures/`, for example `wheat_shortage.png`. Then add:

```json
{
  "picture": "wheat_shortage.png"
}
```

Square pictures work best. See [News pictures](pictures.md).

## 7. Publish the news first

Give players a head start: the headline comes out, and the price only starts moving 30 to 90 seconds later.

```json
{
  "announceDelayMs": { "min": 30000, "max": 90000 }
}
```

Negative values do the opposite: the price moves first and the news follows.

## 8. Tell a story in steps

Replace `impact` with `sequences`. Now the shortage builds slowly, peaks, eases a bit and then fades:

```json
{
  "sequences": [
    {
      "name": "shortage",
      "steps": [
        { "name": "worry", "durationSeconds": { "min": 300, "max": 600 }, "targetFactor": 0.15, "curve": "linear" },
        { "name": "panic", "durationSeconds": 300, "targetFactor": 0.35, "curve": "exponential", "noise": 0.05 },
        { "name": "peak", "durationSeconds": 600, "curve": "hold" },
        { "name": "imports", "durationSeconds": 900, "targetFactor": 0.0, "curve": "linear" }
      ]
    }
  ]
}
```

The last step ends at `0`, so the price goes back to normal. See [Sequences](advanced-events.md#sequences).

## 9. Add a follow-up

After the shortage, farmers plant extra wheat, and the price drops for a while. Write a second file:

```json title="config/StockMarket/news/MyServer/wheat_recovery.json"
{
  "id": "wheat_recovery",
  "headline": "Farmers plant record wheat fields",
  "text": "After last season's shortage, every farmer sowed wheat. The granaries are full.",
  "weight": 0,
  "impact": {
    "type": "trend",
    "peakFactor": -0.2
  },
  "markets": [
    { "item": "minecraft:wheat" },
    { "item": "minecraft:bread", "weightFactor": 0.6 }
  ],
  "requires": [
    { "type": "firedBefore", "eventId": "wheat_shortage" }
  ]
}
```

`weight` `0` means it never fires at random. The requirement makes sure it only follows a real shortage. Now let the shortage start it. Add to `wheat_shortage.json`:

```json
{
  "chains": [
    { "eventId": "wheat_recovery", "on": "completion", "chance": 0.8, "delaySeconds": { "min": 600, "max": 1200 } }
  ]
}
```

When the shortage ends normally, there is an 80% chance that the recovery starts 10 to 20 minutes later. See [Chains](advanced-events.md#chains).

To test the chain, trigger `wheat_shortage` and use `skipphase` until it ends. A stopped event doesn't start its chain.

## 10. Go live

Remove `"adminOnly": true` from `wheat_shortage.json` (or set it to `false`). Add a `weight` and a `cooldownSeconds` that fit how often you want the news, for example:

```json
{
  "weight": 5,
  "cooldownSeconds": 14400
}
```

Reload. From now on the event can come at random. Check it any time with `/stockmarket news info wheat_shortage`.

## The full event

```json title="config/StockMarket/news/MyServer/wheat_shortage.json"
{
  "id": "wheat_shortage",
  "headline": {
    "en_us": "Wheat runs short!",
    "de_de": "Weizen wird knapp!"
  },
  "text": {
    "en_us": "A wet summer has ruined half the harvest. Bakers are paying whatever farmers ask.",
    "de_de": "Ein nasser Sommer hat die halbe Ernte verdorben. Die Bäcker zahlen jeden Preis."
  },
  "picture": "wheat_shortage.png",
  "weight": 5,
  "cooldownSeconds": 14400,
  "announceDelayMs": { "min": 30000, "max": 90000 },
  "sequences": [
    {
      "name": "shortage",
      "steps": [
        { "name": "worry", "durationSeconds": { "min": 300, "max": 600 }, "targetFactor": 0.15, "curve": "linear" },
        { "name": "panic", "durationSeconds": 300, "targetFactor": 0.35, "curve": "exponential", "noise": 0.05 },
        { "name": "peak", "durationSeconds": 600, "curve": "hold" },
        { "name": "imports", "durationSeconds": 900, "targetFactor": 0.0, "curve": "linear" }
      ]
    }
  ],
  "markets": [
    { "item": "minecraft:wheat" },
    { "item": "minecraft:bread", "weightFactor": 0.6 },
    { "item": "minecraft:potato", "weightFactor": 0.3 }
  ],
  "chains": [
    { "eventId": "wheat_recovery", "on": "completion", "chance": 0.8, "delaySeconds": { "min": 600, "max": 1200 } }
  ]
}
```

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| *invalid JSON syntax* in the report | A comma, quote or bracket is wrong. | Check the file with a JSON validator. |
| *unknown field* | A field name is misspelt, for example `peakfactor`. | Use the exact spelling from the reference. |
| The event never fires | `weight` is `0`, it is `adminOnly` or disabled, its requirements don't hold, or no market matches. | Run `/stockmarket news info <eventId>`. |
| *matches no subscribed (news-enabled) market* on trigger | The item has no market, the market isn't subscribed to the NewsPlugin, or **News enabled** is off. | Check the market in the [News plugin](../plugins/news.md) settings. |
| The price jumps back at the end | The last step doesn't end at `0`. | End with `"targetFactor": 0.0`, or mark the last step `permanent`. |
| The effect is weaker and longer than written | The shipped `scheduler.json` halves strength and triples duration. | Expected. Change the multipliers in [scheduler.json](config-files.md#schedulerjson) if you want. |
| The picture is missing | The file isn't in `pictures/`, is too large, or the name doesn't match. | Check the reload report. |

## Sharing events

An event is just its JSON file plus its picture. To give an event to another server, copy both into its `news/` and `news/pictures/` folders and reload. Items from mods that server doesn't have are skipped with a warning.

## Related pages

- [Event file reference](event-reference.md): every field.
- [Advanced events](advanced-events.md): sequences, requirements and chains in detail.
- [News commands](commands.md): all test commands.
- [Default events](default-events.md): more examples to copy from.
