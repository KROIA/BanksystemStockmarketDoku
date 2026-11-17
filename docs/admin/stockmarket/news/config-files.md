---
title: News config files
description: Where the news event files live, which files the server loads and in which order, how the shipped events update themselves, and how old installs are migrated.
---

# News config files

All news events are plain JSON files in one folder. You add news by dropping a file in, and you change a shipped event by editing its file. This page explains the folder: what goes where, what the server loads, and what happens when you update the mod.

What goes *inside* an event file is on the [Event file reference](event-reference.md) page. If you've never written an event, start with the [tutorial](tutorial.md).

## Where the folder is

The news folder is in the game's `config` folder, not in the world folder:

| Setup | Folder |
|---|---|
| Dedicated server | `<server folder>/config/StockMarket/news/` |
| Single player | `<game folder>/config/StockMarket/news/` |

!!! note "Master and slave servers"
    News runs only on the master server. It picks the events, moves the prices and sends the headlines to the slaves. Edit the news files on the master. See [Master and slave servers](../../multi-server.md).

## What's in the folder

On the first start the mod creates the folder and fills it. A typical folder looks like this:

```text
config/StockMarket/news/
├── scheduler.json              # how often news happen (created on first start)
├── DefaultEvents/              # the shipped events, one file per event (created on first start)
│   ├── diamond_rush.json
│   ├── gold_rush_rumor.json
│   └── ...
├── pictures/                   # event pictures (PNG)
│   ├── diamond_rush.png
│   └── ...
├── MyServer/                   # your own folder, any name
│   ├── harvest.json
│   └── old/                    # two levels deep: ignored
│       └── draft.json
├── my_events.json              # files directly in news/ load too
└── default_events.json.migrated   # only after an update from an older version
```

## Which files are loaded

The server loads every `.json` file:

- directly in `news/`, and
- in every folder **one level** below `news/`, for example `news/MyServer/`.

It skips:

- folders two or more levels deep, for example `news/MyServer/old/`. Move a file there to switch it off without deleting it.
- files and folders whose name starts with a dot.
- files that don't end in `.json`, for example `.bak` copies or `default_events.json.migrated`.

File and folder names don't matter. Organise your events however you like, for example one folder per theme or per event pack.

A file holds either one event (like the files in `DefaultEvents/`) or several events in an `events` list. All files are merged into one pool of events. See [Event file reference](event-reference.md) for both formats.

!!! tip "Apply changes without a restart"
    After you add or change a file, run `/stockmarket news reload`. The command prints a report of every problem it found, grouped by file. A broken file never crashes the server: the server skips what it can't read and loads the rest. If a reload finds no valid event at all, the events from before stay loaded.

## Load order

The server reads the files in a fixed order:

1. The files in `DefaultEvents/`.
2. The files directly in `news/`.
3. Every other folder, sorted by name.

Within a folder, files are sorted by name. Upper and lower case don't matter.

The order decides two things:

- **Two events with the same `id`:** the one loaded later wins. Because `DefaultEvents/` loads first, your own copy of a shipped event always wins over the shipped one. The reload report still lists the duplicate as an error, naming both files.
- **Scheduler values:** each file can set some scheduler values. For each value, the file loaded last wins. See [scheduler.json](#schedulerjson) below.

## Changing a shipped event

You have two ways. Pick one per event:

- **Edit the file in `DefaultEvents/` directly.** The mod never overwrites a file that exists, so your changes are kept through updates. This is the simplest way.
- **Copy the event into your own folder** and edit the copy. Then delete the original file from `DefaultEvents/`. If you keep both, your copy still wins, but the reload report shows a duplicate-id error every time.

!!! warning "Deleting a shipped event doesn't remove it"
    If you delete a file from `DefaultEvents/` and no other file has that event's `id`, the mod writes the file again on the next reload. To switch a shipped event off, disable it instead: use the **All events** tab of the News plugin window, or run `/stockmarket news disable <eventId>`.

### How new shipped events arrive

When you update the mod, you get its new events automatically. On every reload, the mod checks each shipped event. If no file anywhere in `news/` defines its `id`, the mod writes it to `DefaultEvents/<id>.json`. It never changes a file that exists.

This top-up only runs while the `DefaultEvents/` folder exists. If you want to run your server only with your own events, delete the whole `DefaultEvents/` folder. Keep at least one `.json` file somewhere in `news/`, though: if the folder has no `.json` file at all, the mod treats it as a first start and writes all shipped events again.

## scheduler.json

`scheduler.json` sets how often random news happen and how strong they are. The mod writes it on the first start with these values:

```json title="config/StockMarket/news/scheduler.json"
{
  "scheduler": {
    "minSecondsBetweenEvents": 7200,
    "maxSecondsBetweenEvents": 16200,
    "maxActiveEventsGlobal": 3,
    "maxActiveEventsPerMarket": 1,
    "historyMaxEntries": 1000,
    "impactDurationMultiplier": 3.0,
    "impactStrengthMultiplier": 0.5
  }
}
```

With these values, a random event starts every 2 to 4.5 hours, which is about 6 news a day. Each event lasts three times as long as its file says and moves the price half as far. The [Event file reference](event-reference.md) explains every value.

Every reload starts from the built-in values and then applies the `scheduler` block of each file in load order. So a `scheduler` block in your own file overrides `scheduler.json` for the values it sets.

!!! tip
    To try out different values while the server runs, use `/stockmarket news scheduler set <key> <value>` or the **Scheduler** tab of the News plugin window. These changes stay until you reset them, even through a reload. See [News commands](commands.md).

## Pictures

Event pictures go in the `pictures/` folder. An event names its picture with the `picture` field, for example `"picture": "diamond_rush.png"`: just the file name, never a path.

A picture must be a PNG file of at most 128 KiB, between 16 and 512 pixels per side. Square pictures work best. You can use colour: the game turns every picture into the black-on-paper newspaper look.

Each shipped event comes with its own picture. Like the events, missing shipped pictures are written again on every reload, and a picture file that exists is never overwritten. To use your own art, replace the file and keep its name. All details are on the [News pictures](pictures.md) page.

## Updating from an older version

Before version 2.2, all shipped events were in one file, `news/default_events.json`. On the first start with the new version, the mod converts that file once:

1. It first applies this version's changes to the values you never edited. The scheduler moves to the new, less frequent timing. If the old luxury tax event is unchanged, it gets its new rule: it fires only once until it is repealed.
2. Every event in the file becomes its own file in `DefaultEvents/`, named after the event's `id`. This includes events you edited and events you added yourself. Your changes are kept.
3. The `scheduler` block becomes `scheduler.json`.
4. The old file is renamed to `default_events.json.migrated`. The mod never reads it again. Keep it as a backup, and delete it once you're happy with the result.

Some special cases:

- **`DefaultEvents/` already exists:** the folder wins. The old file is only renamed, not converted. The server log says so.
- **`scheduler.json` already exists:** it is kept. The old `scheduler` block stays only in the backup file.
- **The old file isn't valid JSON:** it is not converted and keeps its name. It loads like any other news file, so the reload report shows its errors. Fix it, and the next start converts it.

Check the server log after the first start. It lists how many event files were written.

## Related pages

- [Event file reference](event-reference.md): every field of an event.
- [Writing your first event](tutorial.md): a step-by-step tutorial.
- [News commands](commands.md): reload, trigger, stop and the scheduler commands.
- [News plugin](../plugins/news.md): per-market news settings.
