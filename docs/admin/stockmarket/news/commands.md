---
title: "News commands"
description: "The /stockmarket news admin commands and their buttons in the management window."
---

# News commands

All news commands start with `/stockmarket news`. Most of them have a button in the [News plugin window](index.md#the-news-plugin-window), so you can also do the same with the mouse.

`/stockmarket news` without anything after it opens the newspaper. Every player can use that, see [Market news](../../../stockmarket/newspaper.md). All other commands are for admins.

## Who can use them

You need the StockMarket admin flag, which you get with `/stockmarket op`. With a permission mod, you also need the node `stockmarket.admin.command.news`. The console can use the commands too. See [Admins and permissions](../../permissions.md).

On a network, the commands work on every server: a slave passes them on to the master, where the news run. Tab completion of event names only works on the master.

The command output is always in English.

## All commands

| Command | What it does | In the window |
|---|---|---|
| `/stockmarket news reload` | Reads all news files again and prints the report. | **Reload** |
| `/stockmarket news list` | Lists all loaded events with their markers and all running events with phase, time left and effect per market. | **All events** and **Active** tabs |
| `/stockmarket news info <eventId>` | Shows everything about one event: texts, markets, timing, cooldown, and whether it is enabled or running. | Click the event |
| `/stockmarket news trigger <eventId> [market]` | Starts the event now. | **Trigger** |
| `/stockmarket news stop <eventId>` | Stops a running event at once. | **Stop** |
| `/stockmarket news stop all` | Stops all running events. | **Stop all** |
| `/stockmarket news skipphase <eventId>` | Jumps a running event to its next phase or step. | **Skip phase** |
| `/stockmarket news enable <eventId>` | Switches an event back on. | Checkbox in **All events** |
| `/stockmarket news disable <eventId>` | Switches an event off. | Checkbox in **All events** |
| `/stockmarket news resetcooldown <eventId>` | Ends the event's cooldown, so it can be picked again at once. | **Reset CD** |
| `/stockmarket news scheduler show` | Shows the scheduler values and the next planned events. | **Scheduler** tab |
| `/stockmarket news scheduler set <key> <value>` | Overrides one scheduler value. | **Apply** in **Scheduler** |
| `/stockmarket news scheduler reset [key]` | Removes one override, or all of them. | **Reset to file** (all) |
| `/stockmarket news registry list` | Shows the world event registry. | |
| `/stockmarket news registry clear <eventId>` | Deletes one event's fire record. | |
| `/stockmarket news registry clear key <key>` | Deletes one of your own registry values. | |
| `/stockmarket news registry clear all` | Deletes the whole registry. | |

## Trigger

`trigger` starts an event at once and ignores its weight, its cooldown, `adminOnly`, its requirements and the limits of active events. It still refuses if:

- the event is disabled or already running,
- the NewsPlugin is switched off,
- the event matches no subscribed market with **News enabled** on.

With `[market]`, the event only moves that one market. Write the market's item id in quotes, for example `"minecraft:wheat"`. Tab completion offers the names. If several markets share an item id, for example enchanted books, it also offers their numbers.

The trigger starts the event's cooldown as usual. The headline follows the event's announce delay. In the window, **Trigger** asks first if the cooldown is still running or the requirements aren't met.

## Stop and skip phase

These two commands end an event in different ways:

- **`stop`** cancels the event. Its effect is removed at once, in any phase, and its full cooldown starts again. A permanent event is cancelled before it writes its change, so nothing stays. Chains that wait for the event's end don't start.
- **`skipphase`** moves the event on: from **Pending** to the ramp-up, then to the hold, the reversal and the end, or to the next step of a sequence. Skipping the last phase ends the event normally: a permanent event writes its change, and end chains can start.

To test a whole event quickly, trigger it and use `skipphase` until it ends.

## Enable and disable

A disabled event never fires: not at random, not by a chain and not by `trigger`. It shows as **[disabled]** in the **All events** tab. Disabling doesn't stop an event that is running; use `stop` for that.

The on/off state is saved with the world and survives reloads and restarts. It's the way to switch off a shipped event, because a deleted shipped file comes back, see [Changing a shipped event](config-files.md#changing-a-shipped-event).

## Scheduler

`scheduler set` changes a value while the server runs, without editing a file. These keys can be set:

| Key | What it does |
|---|---|
| `minSecondsBetweenEvents` | Shortest wait between two random events. |
| `maxSecondsBetweenEvents` | Longest wait. |
| `maxActiveEventsGlobal` | How many events may run at once. |
| `maxActiveEventsPerMarket` | How many events may move one market at once. |

The value must be a whole number of at least 1, and the shortest wait can't be longer than the longest. Overrides are saved with the world: they stay through reloads and restarts until you reset them. `scheduler show` and the **Scheduler** tab mark them as overridden.

The other scheduler values, such as the multipliers, can only be changed in the files, see [Scheduler values](event-reference.md#scheduler-values).

## Registry

The [world event registry](advanced-events.md#the-world-event-registry) remembers which events fired and holds the values events write with `records`. Requirements read it.

- `registry list` shows every fire record (how often, first and last time, game day) and every value.
- `registry clear <eventId>` deletes one fire record. The event then counts as never fired, so a one-time event can happen again.
- `registry clear key <key>` deletes one value.
- `registry clear all` deletes everything.

## Other admins see what you do

Every command that changes something is announced in chat to the other StockMarket admins who are online: triggers, stops, skipped phases, enabling and disabling, cooldown resets, scheduler changes, registry deletes and reloads. So nobody can start news secretly and trade on it.

## Related pages

- [News system](index.md): the News plugin window.
- [Writing your first event](tutorial.md): testing an event step by step.
- [Advanced events](advanced-events.md): requirements and the registry.
- [Admins and permissions](../../permissions.md): the admin flag and permission nodes.
