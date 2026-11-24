---
title: "News-Konfigurationsdateien"
description: "Wo die News-Ereignisdateien liegen, in welcher Reihenfolge der Server sie lädt und wie mitgelieferte Ereignisse und alte Installationen aktualisiert werden."
---

# News-Konfigurationsdateien { #news-config-files }

Alle News-Ereignisse sind einfache JSON-Dateien in einem Ordner. Du fügst News hinzu, indem du eine Datei hineinlegst, und du änderst ein mitgeliefertes Ereignis, indem du seine Datei bearbeitest. Diese Seite erklärt den Ordner: was wohin gehört, was der Server lädt und was passiert, wenn du die Mod aktualisierst.

Was *in* eine Ereignisdatei gehört, steht auf der Seite [Referenz der Ereignisdatei](event-reference.md). Wenn du noch nie ein Ereignis geschrieben hast, beginne mit der [Anleitung](tutorial.md).

## Wo der Ordner liegt { #where-the-folder-is }

Der News-Ordner liegt im `config`-Ordner des Spiels, nicht im Weltordner:

| Einrichtung | Ordner |
|---|---|
| Dedizierter Server | `<server folder>/config/StockMarket/news/` |
| Einzelspieler | `<game folder>/config/StockMarket/news/` |

!!! note "Master- und Slave-Server"
    News laufen nur auf dem Master-Server. Er wählt die Ereignisse aus, bewegt die Preise und schickt die Schlagzeilen an die Slaves. Bearbeite die News-Dateien auf dem Master. Siehe [Master- und Slave-Server](../../multi-server.md).

## Was im Ordner liegt { #whats-in-the-folder }

Beim ersten Start legt die Mod den Ordner an und füllt ihn. Ein typischer Ordner sieht so aus:

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

## Welche Dateien geladen werden { #which-files-are-loaded }

Der Server lädt jede `.json`-Datei:

- direkt in `news/` und
- in jedem Ordner **eine Ebene** unter `news/`, zum Beispiel `news/MyServer/`.

Er überspringt:

- Ordner, die zwei oder mehr Ebenen tief liegen, zum Beispiel `news/MyServer/old/`. Verschiebe eine Datei dorthin, um sie abzuschalten, ohne sie zu löschen.
- Dateien und Ordner, deren Name mit einem Punkt beginnt.
- Dateien, die nicht auf `.json` enden, zum Beispiel `.bak`-Kopien oder `default_events.json.migrated`.

Datei- und Ordnernamen spielen keine Rolle. Ordne deine Ereignisse, wie du willst, zum Beispiel einen Ordner pro Thema oder pro Ereignispaket.

Eine Datei enthält entweder ein Ereignis (wie die Dateien in `DefaultEvents/`) oder mehrere Ereignisse in einer `events`-Liste. Alle Dateien werden zu einem gemeinsamen Vorrat an Ereignissen zusammengeführt. Beide Formate stehen in der [Referenz der Ereignisdatei](event-reference.md).

!!! tip "Änderungen ohne Neustart übernehmen"
    Nachdem du eine Datei hinzugefügt oder geändert hast, führe `/stockmarket news reload` aus. Der Befehl gibt einen Bericht über jedes gefundene Problem aus, nach Datei gruppiert. Eine kaputte Datei bringt den Server nie zum Absturz: Der Server überspringt, was er nicht lesen kann, und lädt den Rest. Findet ein Neuladen überhaupt kein gültiges Ereignis, bleiben die vorherigen Ereignisse geladen.

## Ladereihenfolge { #load-order }

Der Server liest die Dateien in einer festen Reihenfolge:

1. Die Dateien in `DefaultEvents/`.
2. Die Dateien direkt in `news/`.
3. Alle anderen Ordner, nach Namen sortiert.

Innerhalb eines Ordners werden die Dateien nach Namen sortiert. Groß- und Kleinschreibung spielen keine Rolle.

Die Reihenfolge entscheidet über zwei Dinge:

- **Zwei Ereignisse mit derselben `id`:** Das später geladene gewinnt. Weil `DefaultEvents/` zuerst lädt, gewinnt deine eigene Kopie eines mitgelieferten Ereignisses immer gegen das mitgelieferte. Der Bericht beim Neuladen führt das Duplikat trotzdem als Fehler auf und nennt beide Dateien.
- **Planerwerte:** Jede Datei kann einige Werte des Planers setzen. Für jeden Wert gilt die zuletzt geladene Datei. Siehe [scheduler.json](#schedulerjson) unten.

## Ein mitgeliefertes Ereignis ändern { #changing-a-shipped-event }

Du hast zwei Möglichkeiten. Wähle pro Ereignis eine davon:

- **Bearbeite die Datei in `DefaultEvents/` direkt.** Die Mod überschreibt nie eine vorhandene Datei, deine Änderungen bleiben also über Updates hinweg erhalten. Das ist der einfachste Weg.
- **Kopiere das Ereignis in deinen eigenen Ordner** und bearbeite die Kopie. Lösche dann die Originaldatei aus `DefaultEvents/`. Behältst du beide, gewinnt deine Kopie trotzdem, aber der Bericht beim Neuladen zeigt jedes Mal einen Fehler wegen doppelter ID.

!!! warning "Löschen entfernt ein mitgeliefertes Ereignis nicht"
    Wenn du eine Datei aus `DefaultEvents/` löschst und keine andere Datei die `id` dieses Ereignisses hat, schreibt die Mod die Datei beim nächsten Neuladen wieder. Um ein mitgeliefertes Ereignis abzuschalten, deaktiviere es stattdessen: im Tab **Alle Ereignisse** des Fensters des News-Plugins oder mit `/stockmarket news disable <eventId>`.

### Wie neue mitgelieferte Ereignisse ankommen { #how-new-shipped-events-arrive }

Wenn du die Mod aktualisierst, bekommst du ihre neuen Ereignisse automatisch. Bei jedem Neuladen prüft die Mod jedes mitgelieferte Ereignis. Definiert keine Datei irgendwo in `news/` seine `id`, schreibt die Mod es nach `DefaultEvents/<id>.json`. Eine vorhandene Datei ändert sie nie.

Dieses Auffüllen läuft nur, solange der Ordner `DefaultEvents/` existiert. Wenn du deinen Server nur mit deinen eigenen Ereignissen betreiben willst, lösche den ganzen Ordner `DefaultEvents/`. Behalte aber mindestens eine `.json`-Datei irgendwo in `news/`: Enthält der Ordner gar keine `.json`-Datei, behandelt die Mod das als ersten Start und schreibt alle mitgelieferten Ereignisse erneut.

## scheduler.json { #schedulerjson }

`scheduler.json` legt fest, wie oft zufällige News kommen und wie stark sie sind. Die Mod schreibt die Datei beim ersten Start mit diesen Werten:

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

Mit diesen Werten startet alle 2 bis 4.5 Stunden ein zufälliges Ereignis, also etwa 6 News pro Tag. Jedes Ereignis dauert dreimal so lang, wie seine Datei sagt, und bewegt den Preis halb so weit. Die [Referenz der Ereignisdatei](event-reference.md) erklärt jeden Wert.

Jedes Neuladen beginnt mit den eingebauten Werten und wendet dann den `scheduler`-Block jeder Datei in der Ladereihenfolge an. Ein `scheduler`-Block in deiner eigenen Datei überschreibt also `scheduler.json` für die Werte, die er setzt.

!!! tip
    Um andere Werte auszuprobieren, während der Server läuft, nutze `/stockmarket news scheduler set <key> <value>` oder den Tab **Planer** des Fensters des News-Plugins. Diese Änderungen bleiben, bis du sie zurücksetzt, auch über ein Neuladen hinweg. Siehe [News-Befehle](commands.md).

## Bilder { #pictures }

Die Bilder der Ereignisse gehören in den Ordner `pictures/`. Ein Ereignis nennt sein Bild im Feld `picture`, zum Beispiel `"picture": "diamond_rush.png"`: nur den Dateinamen, nie einen Pfad.

Ein Bild muss eine PNG-Datei mit höchstens 128 KiB und 16 bis 512 Pixeln pro Seite sein. Quadratische Bilder wirken am besten. Du kannst Farbe verwenden: Das Spiel bringt jedes Bild in den Zeitungslook mit Schwarz auf Papier.

Jedes mitgelieferte Ereignis bringt sein eigenes Bild mit. Wie bei den Ereignissen werden fehlende mitgelieferte Bilder bei jedem Neuladen wieder geschrieben, und eine vorhandene Bilddatei wird nie überschrieben. Um deine eigenen Bilder zu verwenden, ersetze die Datei und behalte ihren Namen. Alle Details stehen auf der Seite [News-Bilder](pictures.md).

## Update von einer älteren Version { #updating-from-an-older-version }

Vor Version 2.2 lagen alle mitgelieferten Ereignisse in einer Datei, `news/default_events.json`. Beim ersten Start mit der neuen Version wandelt die Mod diese Datei einmal um:

1. Zuerst wendet sie die Änderungen dieser Version auf die Werte an, die du nie bearbeitet hast. Der Planer wechselt zum neuen, selteneren Zeitablauf. Ist das alte Ereignis zur Luxussteuer unverändert, bekommt es seine neue Regel: Es feuert nur einmal, bis es abgeschafft wird.
2. Jedes Ereignis in der Datei wird zu einer eigenen Datei in `DefaultEvents/`, benannt nach der `id` des Ereignisses. Das gilt auch für Ereignisse, die du bearbeitet oder selbst hinzugefügt hast. Deine Änderungen bleiben erhalten.
3. Der `scheduler`-Block wird zu `scheduler.json`.
4. Die alte Datei wird in `default_events.json.migrated` umbenannt. Die Mod liest sie nie wieder. Behalte sie als Backup und lösche sie, sobald du mit dem Ergebnis zufrieden bist.

Einige Sonderfälle:

- **`DefaultEvents/` existiert bereits:** Der Ordner gewinnt. Die alte Datei wird nur umbenannt, nicht umgewandelt. Das Server-Log meldet das.
- **`scheduler.json` existiert bereits:** Die Datei bleibt erhalten. Der alte `scheduler`-Block bleibt nur in der Backup-Datei.
- **Die alte Datei ist kein gültiges JSON:** Sie wird nicht umgewandelt und behält ihren Namen. Sie lädt wie jede andere News-Datei, der Bericht beim Neuladen zeigt also ihre Fehler. Behebe sie, dann wandelt der nächste Start sie um.

Prüfe nach dem ersten Start das Server-Log. Es nennt, wie viele Ereignisdateien geschrieben wurden.

## Verwandte Seiten { #related-pages }

- [Referenz der Ereignisdatei](event-reference.md): jedes Feld eines Ereignisses.
- [Dein erstes Ereignis schreiben](tutorial.md): eine Anleitung Schritt für Schritt.
- [News-Befehle](commands.md): reload, trigger, stop und die Befehle für den Planer.
- [News-Plugin](../plugins/news.md): News-Einstellungen pro Markt.
