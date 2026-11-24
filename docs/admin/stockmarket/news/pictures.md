---
title: "News pictures"
description: "Adding pictures to events: file rules, the newsprint look, default pictures and syncing."
---

# News pictures

Every news event can have a picture. It shows next to the story in the newspaper, in the **Active** tab of the News plugin window and in the event details. All shipped events come with their own picture.

## Adding a picture

1. Put a PNG file into `config/StockMarket/news/pictures/` on the server. Files in subfolders are ignored.
2. Name it in the event with the `picture` field:

    ```json
    {
      "picture": "wheat_shortage.png"
    }
    ```

3. Run `/stockmarket news reload`.

The `picture` value is only the file name, never a path. It must end in `.png`, can't start with a dot and can't contain `/`, `\`, `:` or `..`. A wrong name is dropped with an error in the reload report, and the event loads without a picture. If the file doesn't exist, the report warns you, and the event also loads without a picture.

## File rules

| Rule | Limit |
|---|---|
| Format | PNG. The server checks the file content, not just the name. |
| File size | At most 128 KiB. |
| Width and height | Each between 16 and 512 pixels. |

A file that breaks a rule is listed as an error in the reload report and isn't used. The other pictures still load.

## How pictures look

You can use colour. The game turns every picture into grey ink on newspaper, so all pictures look like they were printed in the same paper.

Square pictures work best. The newspaper and the event details show the picture in a square box and cut off what sticks out on the sides, so keep the important part in the middle. The **Active** tab shows the whole picture, scaled down to fit.

## The shipped pictures

The mod writes one picture per shipped event into `pictures/`, named after the event, for example `diamond_rush.png`. Like the [shipped events](config-files.md#how-new-shipped-events-arrive), they top themselves up:

- On every reload, a missing shipped picture is written again.
- A picture file that exists is never overwritten.

So:

- **To use your own art,** replace the file and keep its name.
- **To show a shipped event without a picture,** remove the `picture` field from its event file. Deleting the PNG doesn't help, it comes back on the next reload.

## Changing a picture

After you change or replace a file, run `/stockmarket news reload`. New news use the new picture.

News that are already published keep the picture they came out with. The server copies each picture into the world when the news is published, so old newspaper entries never change, even if you delete the file later. Copies that no news in the history uses any more are deleted by themselves.

## How players get the pictures

Players don't need to install anything. The game downloads each picture from the server when it needs it. On a network, the slaves pass these downloads on to the master, which keeps all pictures. See [Master and slave servers](../../multi-server.md).

## Related pages

- [News config files](config-files.md): the news folder.
- [Event file reference](event-reference.md): the `picture` field and the other fields.
- [Market news](../../../stockmarket/newspaper.md): what players see.
