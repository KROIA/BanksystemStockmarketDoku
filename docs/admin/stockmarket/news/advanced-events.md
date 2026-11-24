---
title: "Advanced events"
description: "Multi-step sequences, trigger requirements, the world-event registry and event chains."
---

# Advanced events

A simple event ramps up, holds and fades. This page shows how to tell longer stories: events in several steps, events that depend on earlier news, and events that start other events. Read the [Event file reference](event-reference.md) first.

## Sequences

Instead of `impact`, an event can have `sequences`: a list of story variants. Each time the event fires, the server picks one variant by its `weight` and plays its steps one after another.

This shortened version of the shipped `gold_rush_rumor` has two variants. Two times out of three the rumour pumps the price and then crashes it. One time out of three it fizzles out:

```json title="config/StockMarket/news/MyServer/gold_rumor.json"
{
  "id": "gold_rumor",
  "headline": "Rumours of a huge gold strike!",
  "text": "Nobody has seen the nugget yet.",
  "weight": 6,
  "cooldownSeconds": 10800,
  "sequences": [
    {
      "name": "pump_and_dump",
      "weight": 2,
      "steps": [
        { "name": "hype", "durationSeconds": { "min": 450, "max": 1200 }, "targetFactor": 0.4, "curve": "linear", "noise": 0.05 },
        { "name": "peak", "durationSeconds": { "min": 300, "max": 600 }, "curve": "hold" },
        { "name": "sell_off", "durationSeconds": { "min": 100, "max": 300 }, "targetFactor": -0.15, "curve": "exponential" },
        { "name": "recover", "durationSeconds": 1500, "targetFactor": 0.0, "curve": "linear" }
      ]
    },
    {
      "name": "fizzle",
      "weight": 1,
      "steps": [
        { "name": "stir", "durationSeconds": { "min": 300, "max": 600 }, "targetFactor": 0.15, "curve": "linear" },
        { "name": "denial", "durationSeconds": { "min": 300, "max": 900 }, "targetFactor": 0.0, "curve": "exponential" }
      ]
    }
  ],
  "markets": [ { "item": "minecraft:gold_ingot" } ]
}
```

### Sequence fields

| Field | Needed | What it does |
|---|---|---|
| `name` | yes | Name of the variant. It shows in the event details. |
| `weight` | no | How often this variant is picked, compared to the others. Must be above `0`. Default `1`. |
| `steps` | yes | The steps, in order. At least one. |

### Step fields

| Field | Needed | What it does |
|---|---|---|
| `name` | yes | Name of the step, unique within its variant. Chains can start at a step by its name. |
| `durationSeconds` | yes | How long the step takes: a number, or `{ "min": …, "max": … }` for a random length. |
| `targetFactor` | yes, except for `hold` | Where the effect should be at the end of the step. `0.4` = 40% above normal, `-0.15` = 15% below. Must be above `-1`. |
| `curve` | no | How the effect gets there, see below. Default `linear`. |
| `noise` | no | Random wobble during this step, like in `impact`. Default `0`. |
| `markets` | no | Other markets for this step only, in the same format as the event's `markets`. Without it, the step uses the event's markets. |
| `permanent` | no | `true` on the **last** step makes its end value permanent. Only allowed on the last step. |

Each step starts where the step before ended. The first step starts at `0`.

| Curve | What the effect does |
|---|---|
| `linear` | Moves in a straight line to `targetFactor`. |
| `instant` | Jumps to `targetFactor` at once and stays there for the step. |
| `exponential` | Moves fast at first, then slower. It has almost arrived when the step ends. |
| `hold` | Stays where it is. `targetFactor` is ignored. |

The last step should end at `0`. If it doesn't and isn't `permanent`, the effect jumps back to `0` when the sequence ends, and the reload report warns you.

A `permanent` last step works like `"reversal": "none"`: when the sequence ends, its end value is written into the market's default price for good.

Durations are rolled once when the event starts. They are stretched by `impactDurationMultiplier`, and every `targetFactor` is scaled by `impactStrengthMultiplier`, see [Scheduler values](event-reference.md#scheduler-values).

!!! tip "Step names of simple events"
    An `impact` event works like one variant with the steps `ramp`, `hold` and `reversal`. A permanent one has `ramp`, `hold` and `permanent`. You can use these names in chains.

## The world event registry

The server keeps a memory of what has happened in the world. It saves it with the world and keeps it through restarts and reloads. It holds two things:

- **Fire records.** For every event: how often it fired, when it first and last fired, and on which game day. An event counts as fired when its headline is published.
- **Your own values.** Key and value pairs that events write with `records`.

`records` writes values when the event's headline is published:

```json
{
  "records": {
    "era": "gold_standard",
    "luxury_tax": "active"
  }
}
```

Values are always text, but text like `"3"` can be compared as a number. A later write to the same key replaces the value. The registry holds at most 256 keys, and keys and values can be at most 256 characters long. The reload report warns you if `records` breaks these limits.

See what is stored with `/stockmarket news registry list`. You can delete entries with the `registry clear` commands, see [News commands](commands.md#registry).

## Requirements

`requires` is a list of conditions. The event can only fire when **all** of them hold:

```json
{
  "requires": [
    { "type": "firedBefore", "eventId": "luxury_goods_tax", "minSecondsAgo": 172800 },
    { "type": "keyEquals", "key": "luxury_tax", "value": "active" }
  ]
}
```

| Type | Fields | Holds when |
|---|---|---|
| `firedBefore` | `eventId`, `minTimes` (default 1), `minSecondsAgo`, `maxSecondsAgo` | The event fired at least `minTimes` times. With `minSecondsAgo` or `maxSecondsAgo`, its last fire must be at least or at most that long ago. An event that never fired always fails this, even with `minTimes` 0. |
| `notFired` | `eventId` | The event never fired. Use the event's own `id` for a one-time event. |
| `notFiredWithin` | `eventId`, `seconds` | The event never fired, or its last fire is more than `seconds` ago. |
| `countAtLeast` | `eventId`, `count` | The event fired at least `count` times. |
| `countAtMost` | `eventId`, `count` | The event fired at most `count` times. |
| `keyEquals` | `key`, `value` | The key has exactly this value. |
| `keyNotEquals` | `key`, `value` | The key has another value, or doesn't exist. |
| `keyExists` | `key` | The key exists. |
| `keyAbsent` | `key` | The key doesn't exist. |
| `keyAtLeast` | `key`, `value` (number) | The key holds a number of at least `value`. |
| `keyAtMost` | `key`, `value` (number) | The key holds a number of at most `value`. |

The times in requirements are real time: they keep counting while the server is off. Cooldowns don't, they only count while the server runs.

An unknown `type` or a missing field is an error, and the whole event is skipped. A condition that can't be checked must never let an event through.

The server checks requirements when it plans an event and again when the event is due. A chain checks them again when its delay is over. An admin trigger ignores them, but the News plugin window asks first if they aren't met.

## Undoing a permanent change

`undoes` takes back the permanent change of another event. The luxury tax lowers gem prices for good, and its repeal brings them back:

```json
{
  "id": "luxury_tax_repealed",
  "headline": "Council scraps the luxury tax on gems and gold",
  "text": "The trade council has repealed the luxury tax.",
  "weight": 2,
  "cooldownSeconds": 86400,
  "impact": { "type": "trend", "peakFactor": 0.22, "rampUpSeconds": 1200, "durationSeconds": 2700, "reversal": "none" },
  "markets": [
    { "item": "minecraft:diamond" },
    { "item": "minecraft:emerald", "weightFactor": 0.8 },
    { "item": "minecraft:gold_ingot", "weightFactor": 0.6 }
  ],
  "requires": [
    { "type": "firedBefore", "eventId": "luxury_goods_tax", "minSecondsAgo": 172800 },
    { "type": "keyEquals", "key": "luxury_tax", "value": "active" }
  ],
  "records": { "luxury_tax": "repealed" },
  "undoes": "luxury_goods_tax"
}
```

While it runs, the event moves prices like any other event. When it ends, it doesn't apply its own permanent change. Instead it adds back exactly what `luxury_goods_tax` changed on each market. A market the tax never changed stays as it is. The undoing event must be permanent itself, otherwise it has nothing to apply at its end.

## Chains

`chains` starts follow-up events. A forest fire can be followed by cheap lumber, a speculative mania by a crash:

```json
{
  "chains": [
    {
      "eventId": "great_forest_fire_recovery",
      "on": "completion",
      "chance": 0.7,
      "delaySeconds": { "min": 600, "max": 1800 }
    }
  ]
}
```

| Field | Needed | What it does |
|---|---|---|
| `eventId` | yes | The event to start. |
| `on` | yes | When: `publish` (when the headline comes out), `step` (when a step starts) or `completion` (when the event ends). |
| `step` | for `on: step` | The name of the step. The reload report warns you if no variant has a step of that name. |
| `chance` | no | How likely the follow-up is, from `0` to `1`. Default `1`. |
| `delaySeconds` | no | Wait before the follow-up starts: a number or `{ "min": …, "max": … }`. Default `0`. It only counts while the server runs. |
| `sameMarkets` | no | `true`: the follow-up moves the markets of the first event instead of its own. Default `false`. |

When the moment comes, the server rolls the chance once. If it wins, the follow-up waits for its delay and then starts. Waiting follow-ups survive restarts.

A follow-up ignores the cooldown and both limits of active events. Its own cooldown starts as usual. When it is due, it is skipped if:

- it is disabled or already running,
- its requirements don't hold,
- it matches no market.

A chain can't start an `adminOnly` event: that is an error, and the chain is dropped. `completion` chains don't fire when an admin stops the event. They do fire when **Skip phase** skips the last phase.

**Loop protection.** A chain can have at most 4 follow-ups in a row, and an event can't appear twice in the same chain. So A → B → A never happens. A chain from an event to itself with `chance` 1 and no `notFired` requirement gives a warning.

!!! tip "Events only chains should start"
    Give a follow-up `"weight": 0`. It is never picked at random, only by its chain or an admin. The shipped `margin_call_crash` and `grain_relief_convoy` work this way.

## Example: the gold standard storyline

The shipped politics events tell one story with the registry:

1. **`gold_reserve_standard`** raises gold for good. It requires `notFired` on itself, so it happens once per world. It records `era` = `gold_standard`. When its `hold` step starts, it has a 50% chance to start `gold_rush_rumor` 5 to 15 minutes later.
2. **`end_of_gold_standard`** lowers gold for good. It requires that the gold standard fired at least 3 hours ago, that `era` is still `gold_standard`, and that it never fired itself. It records `era` = `fiat`.

The luxury tax works the same way, but can repeat: `luxury_goods_tax` requires `luxury_tax` not to be `active` and sets it to `active`. `luxury_tax_repealed` requires `active` and at least two days since the tax, sets `repealed` and undoes the tax. Then the tax can come again.

## Related pages

- [Event file reference](event-reference.md): all basic fields.
- [Writing your first event](tutorial.md): a chain example step by step.
- [Default events](default-events.md): every shipped storyline.
- [News commands](commands.md): trigger, skip phases and the registry.
