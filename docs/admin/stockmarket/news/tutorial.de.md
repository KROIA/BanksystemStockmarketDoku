---
title: "Dein erstes Ereignis schreiben"
description: "Anleitung Schritt für Schritt, vom einfachsten Ereignis bis zu Ketten und Tests."
---

# Dein erstes Ereignis schreiben { #writing-your-first-event }

In dieser Anleitung schreibst du ein News-Ereignis über einen Weizenmangel, testest es und machst daraus dann eine kleine Geschichte mit einem Folgeereignis. Du brauchst das StockMarket-Admin-Flag und einen Markt für Weizen, der das NewsPlugin abonniert hat. Alle Felder sind in der [Referenz der Ereignisdatei](event-reference.md) erklärt.

## 1. Die Datei anlegen { #1-create-the-file }

Lege in `config/StockMarket/news/` einen Ordner für deine eigenen Ereignisse an, zum Beispiel `MyServer/`. Lege diese Datei hinein:

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

Dieses Ereignis hebt den Weizenpreis um bis zu 30 % an und lässt ihn dann abklingen, mit dem Zeitablauf eines `shock`. `adminOnly` verhindert, dass es zufällig feuert, solange du es testest.

## 2. Die Datei laden { #2-load-it }

Führe aus:

```text
/stockmarket news reload
```

Der Chat zeigt einen Bericht. Wenn er ein Problem mit `wheat_shortage.json` meldet, behebe es und lade erneut. Die meisten Probleme sind Tippfehler: ein fehlendes Komma, ein fehlendes Anführungszeichen oder ein falsch geschriebener Feldname, den der Bericht als *unknown field* anzeigt.

## 3. Das Ereignis testen { #3-test-it }

Starte das Ereignis:

```text
/stockmarket news trigger wheat_shortage
```

Die Schlagzeile wird an alle Spieler veröffentlicht, und das Ereignis erscheint im Tab **Aktiv** des [Fensters des News-Plugins](index.md#the-news-plugin-window), mit seiner Phase und seiner Wirkung auf Weizen. So testest du schneller:

- `/stockmarket news skipphase wheat_shortage` springt zur nächsten Phase.
- `/stockmarket news stop wheat_shortage` beendet es sofort und entfernt seine Wirkung.

Du kannst das Ereignis erneut auslösen, sobald es nicht mehr läuft, auch während seiner Abklingzeit.

!!! tip "Auf einem Markt testen"
    Gib einen Markt an, um das Ereignis auf ihn zu beschränken: `/stockmarket news trigger wheat_shortage "minecraft:wheat"`. Die Tab-Vervollständigung schlägt die Marktnamen vor.

## 4. Mehr Märkte bewegen { #4-move-more-markets }

Brot wird auch teurer, aber weniger. Und bei teurem Weizen kaufen die Leute stattdessen mehr Kartoffeln. Ersetze `markets` durch:

```json
{
  "markets": [
    { "item": "minecraft:wheat" },
    { "item": "minecraft:bread", "weightFactor": 0.6 },
    { "item": "minecraft:potato", "weightFactor": 0.3 }
  ]
}
```

`weightFactor` skaliert die Wirkung: Brot steigt um bis zu 18 %, Kartoffeln um bis zu 9 %. Ein negativer `weightFactor` bewegt einen Markt in die andere Richtung.

## 5. Weitere Sprachen hinzufügen { #5-add-other-languages }

Schreibe `headline` und `text` einmal pro Sprache. Die Spieler sehen ihre Spielsprache, oder Englisch, wenn sie fehlt:

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

## 6. Ein Bild hinzufügen { #6-add-a-picture }

Lege ein PNG mit höchstens 128 KiB und 16 bis 512 Pixeln pro Seite in `config/StockMarket/news/pictures/`, zum Beispiel `wheat_shortage.png`. Ergänze dann:

```json
{
  "picture": "wheat_shortage.png"
}
```

Quadratische Bilder wirken am besten. Siehe [News-Bilder](pictures.md).

## 7. Zuerst die News veröffentlichen { #7-publish-the-news-first }

Gib den Spielern einen Vorsprung: Die Schlagzeile erscheint, und der Preis beginnt erst 30 bis 90 Sekunden später, sich zu bewegen.

```json
{
  "announceDelayMs": { "min": 30000, "max": 90000 }
}
```

Negative Werte bewirken das Gegenteil: Der Preis bewegt sich zuerst, und die News folgen.

## 8. Eine Geschichte in Schritten erzählen { #8-tell-a-story-in-steps }

Ersetze `impact` durch `sequences`. Jetzt baut sich der Mangel langsam auf, erreicht seinen Höhepunkt, lässt etwas nach und klingt dann ab:

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

Der letzte Schritt endet bei `0`, also kehrt der Preis zum Normalwert zurück. Siehe [Sequenzen](advanced-events.md#sequences).

## 9. Ein Folgeereignis hinzufügen { #9-add-a-follow-up }

Nach dem Mangel säen die Bauern extra viel Weizen, und der Preis sinkt eine Zeit lang. Schreibe eine zweite Datei:

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

`weight` `0` bedeutet, dass es nie zufällig feuert. Die Bedingung sorgt dafür, dass es nur auf einen echten Mangel folgt. Lass es jetzt vom Mangel starten. Ergänze in `wheat_shortage.json`:

```json
{
  "chains": [
    { "eventId": "wheat_recovery", "on": "completion", "chance": 0.8, "delaySeconds": { "min": 600, "max": 1200 } }
  ]
}
```

Wenn der Mangel normal endet, startet die Erholung mit 80 % Wahrscheinlichkeit 10 bis 20 Minuten später. Siehe [Ketten](advanced-events.md#chains).

Um die Kette zu testen, löse `wheat_shortage` aus und nutze `skipphase`, bis es endet. Ein gestopptes Ereignis startet seine Kette nicht.

## 10. Live gehen { #10-go-live }

Entferne `"adminOnly": true` aus `wheat_shortage.json` (oder setze es auf `false`). Ergänze ein `weight` und ein `cooldownSeconds`, die dazu passen, wie oft du die News haben willst, zum Beispiel:

```json
{
  "weight": 5,
  "cooldownSeconds": 14400
}
```

Lade neu. Ab jetzt kann das Ereignis zufällig kommen. Prüfe es jederzeit mit `/stockmarket news info wheat_shortage`.

## Das vollständige Ereignis { #the-full-event }

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

## Häufige Fehler { #common-mistakes }

| Was du siehst | Warum | Lösung |
|---|---|---|
| *invalid JSON syntax* im Bericht | Ein Komma, ein Anführungszeichen oder eine Klammer stimmt nicht. | Prüfe die Datei mit einem JSON-Validator. |
| *unknown field* | Ein Feldname ist falsch geschrieben, zum Beispiel `peakfactor`. | Nutze genau die Schreibweise aus der Referenz. |
| Das Ereignis feuert nie | `weight` ist `0`, es ist `adminOnly` oder deaktiviert, seine Bedingungen sind nicht erfüllt, oder kein Markt passt. | Führe `/stockmarket news info <eventId>` aus. |
| *matches no subscribed (news-enabled) market* beim Auslösen | Für das Item gibt es keinen Markt, der Markt hat das NewsPlugin nicht abonniert, oder **News aktiviert** ist aus. | Prüfe den Markt in den Einstellungen des [News-Plugins](../plugins/news.md). |
| Der Preis springt am Ende zurück | Der letzte Schritt endet nicht bei `0`. | Lass den letzten Schritt mit `"targetFactor": 0.0` enden, oder markiere ihn als `permanent`. |
| Die Wirkung ist schwächer und länger als geschrieben | Die mitgelieferte `scheduler.json` halbiert die Stärke und verdreifacht die Dauer. | Das ist so gewollt. Ändere bei Bedarf die Multiplikatoren in [scheduler.json](config-files.md#schedulerjson). |
| Das Bild fehlt | Die Datei liegt nicht in `pictures/`, ist zu groß, oder der Name passt nicht. | Prüfe den Bericht nach dem Neuladen. |

## Ereignisse weitergeben { #sharing-events }

Ein Ereignis besteht nur aus seiner JSON-Datei und seinem Bild. Um ein Ereignis an einen anderen Server weiterzugeben, kopiere beide in dessen Ordner `news/` und `news/pictures/` und lade neu. Items aus Mods, die dieser Server nicht hat, werden mit einer Warnung übersprungen.

## Verwandte Seiten { #related-pages }

- [Referenz der Ereignisdatei](event-reference.md): jedes Feld.
- [Fortgeschrittene Ereignisse](advanced-events.md): Sequenzen, Bedingungen und Ketten im Detail.
- [News-Befehle](commands.md): alle Testbefehle.
- [Mitgelieferte Ereignisse](default-events.md): weitere Beispiele zum Kopieren.
