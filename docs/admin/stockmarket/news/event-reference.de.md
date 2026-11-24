---
title: "Referenz der Ereignisdatei"
description: "Jedes Feld einer News-Ereignisdatei: Schlagzeile, Text, Preiswirkung, Märkte, Ankündigungsverzögerung und Prüfung."
---

# Referenz der Ereignisdatei { #event-file-reference }

Diese Seite listet jedes Feld auf, das ein News-Ereignis haben kann. Wo die Dateien hingehören und in welcher Reihenfolge sie geladen werden, steht unter [News-Konfigurationsdateien](config-files.md). Für einen sanften Einstieg folge [Dein erstes Ereignis schreiben](tutorial.md).

## Dateiformate { #file-formats }

Eine Datei enthält entweder **ein Ereignis** oder **eine Liste von Ereignissen**.

Ein Ereignis pro Datei, wie die Dateien in `DefaultEvents/`:

```json title="config/StockMarket/news/MyServer/iron_shortage.json"
{
  "id": "iron_shortage",
  "headline": "Iron runs short!",
  "text": "The smelters can't keep up with demand.",
  "impact": { "type": "shock", "peakFactor": 0.3 },
  "markets": [ { "item": "minecraft:iron_ingot" } ]
}
```

Mehrere Ereignisse in einer Datei, mit einem optionalen `scheduler`-Block:

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

Eine Datei mit einer `id` auf oberster Ebene und ohne `events` oder `scheduler` wird als ein Ereignis gelesen. Alles andere muss eine `events`-Liste haben.

## Felder eines Ereignisses { #event-fields }

| Feld | Pflicht | Standard | Was es tut |
|---|---|---|---|
| `id` | ja | | Eindeutiger Name des Ereignisses. Befehle, Ketten und Bedingungen nutzen ihn. Nutze Kleinbuchstaben und `_`, zum Beispiel `iron_shortage`. |
| `headline` | ja | | Der Titel in der Zeitung. Ein Text oder ein Text pro Sprache, siehe [unten](#headline-and-text). |
| `text` | ja | | Die Meldung unter der Schlagzeile. Gleiches Format wie `headline`. |
| `impact` | eins von beiden | | Eine einfache Preiswirkung, siehe [Preiswirkung](#impact). |
| `sequences` | eins von beiden | | Eine Geschichte in mehreren Schritten, siehe [Fortgeschrittene Ereignisse](advanced-events.md#sequences). |
| `markets` | ja | | Die Items, die das Ereignis bewegt, siehe [Märkte](#markets). |
| `category` | nein | `general` | Eine Bezeichnung für deinen eigenen Überblick. Sie erscheint in `/stockmarket news info` und ändert sonst nichts. |
| `weight` | nein | `1` | Wie wahrscheinlich das Ereignis gewählt wird, siehe [Gewicht und Abklingzeit](#weight-and-cooldown). |
| `cooldownSeconds` | nein | `0` | Wie lange das Ereignis nach seinem Start nicht erneut feuern kann. |
| `adminOnly` | nein | `false` | `true`: Das Ereignis feuert nur, wenn ein Admin es auslöst. |
| `announceDelayMs` | nein | keine Verzögerung | Veröffentlicht die Schlagzeile, bevor oder nachdem sich der Preis zu bewegen beginnt, siehe [Ankündigungsverzögerung](#announce-delay). |
| `picture` | nein | kein Bild | Der Dateiname eines PNG in `news/pictures/`, siehe [News-Bilder](pictures.md). |
| `requires` | nein | | Bedingungen, die erfüllt sein müssen, bevor das Ereignis feuern kann. Siehe [Fortgeschrittene Ereignisse](advanced-events.md#requirements). |
| `records` | nein | | Werte, die das Ereignis bei seiner Veröffentlichung in das Gedächtnis der Welt schreibt. Siehe [Fortgeschrittene Ereignisse](advanced-events.md#the-world-event-registry). |
| `chains` | nein | | Folgeereignisse. Siehe [Fortgeschrittene Ereignisse](advanced-events.md#chains). |
| `undoes` | nein | | Nimmt die dauerhafte Änderung eines anderen Ereignisses zurück. Siehe [Fortgeschrittene Ereignisse](advanced-events.md#undoing-a-permanent-change). |

Ein Ereignis hat entweder `impact` oder `sequences`, nie beides. Es gibt kein Feld `enabled`: Du schaltest Ereignisse mit `/stockmarket news enable` und `disable` oder im Fenster des News-Plugins ein und aus.

## Schlagzeile und Text { #headline-and-text }

Schreibe einen einfachen Text oder einen Text pro Sprache:

```json
{
  "headline": {
    "en_us": "Iron runs short!",
    "de_de": "Eisen wird knapp!"
  }
}
```

Jeder Spieler sieht den Text in seiner Spielsprache. Fehlt diese, sieht er `en_us`, und fehlt auch das, den ersten Eintrag. Die mitgelieferten Ereignisse haben Englisch, Deutsch und vereinfachtes Chinesisch (`en_us`, `de_de`, `zh_cn`).

Halte Schlagzeilen kurz. Sind Schlagzeile und Text zusammen größer als 32 KB, warnt dich der Bericht beim Neuladen.

## Gewicht und Abklingzeit { #weight-and-cooldown }

Wenn der Timer abläuft, wählt der Server zufällig ein Ereignis aus allen Ereignissen, die gerade feuern können. `weight` legt die Chancen fest: Ein Ereignis mit Gewicht `10` wird zehnmal so oft gewählt wie eines mit Gewicht `1`. Ein Ereignis mit Gewicht `0` wird nie zufällig gewählt. Nur eine Kette oder ein Admin kann es starten.

Ein Ereignis kann nur gewählt werden, wenn:

- es aktiviert ist, nicht `adminOnly` ist und nicht schon läuft,
- seine Abklingzeit vorbei ist,
- seine `requires`-Bedingungen erfüllt sind,
- mindestens einer seiner Märkte das NewsPlugin abonniert hat, **News aktiviert** eingeschaltet hat und unter der Grenze für Ereignisse pro Markt liegt.

`cooldownSeconds` beginnt, wenn das Ereignis startet. Die Zeit zählt nur, solange der Server läuft. Ein Admin kann ein Ereignis auch während seiner Abklingzeit auslösen.

## Ankündigungsverzögerung { #announce-delay }

Ohne `announceDelayMs` erscheint die Schlagzeile genau in dem Moment, in dem sich der Preis zu bewegen beginnt. Mit dem Feld wählt der Server bei jedem Feuern eine zufällige Verzögerung zwischen `min` und `max` Millisekunden:

```json
{
  "announceDelayMs": { "min": 15000, "max": 90000 }
}
```

- **Positive Werte:** Die Schlagzeile kommt zuerst, der Preis folgt später. Schnelle Spieler können reagieren, bevor der Markt es tut.
- **Negative Werte:** Der Preis bewegt sich zuerst, die Schlagzeile folgt. Spieler, die die Charts beobachten, können es bemerken, bevor die News draußen sind, wie bei Insiderhandel.

Im Tab **Aktiv** erscheint ein Ereignis, dessen Preiswirkung noch nicht begonnen hat, als **Ausstehend**, und ein Ereignis, dessen Schlagzeile noch nicht draußen ist, zeigt *Veröffentlichung ausstehend*. Der Bericht beim Neuladen warnt dich, wenn eine negative Verzögerung so lang ist, dass die Wirkung vorbei ist, bevor die Schlagzeile erscheint.

## Preiswirkung { #impact }

`impact` beschreibt eine einfache Wirkung: ansteigen, halten, zurückgehen.

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

| Feld | Pflicht | Was es tut |
|---|---|---|
| `type` | nein | `shock`, `trend` oder `crash`. Legt den Standard-Zeitablauf unten fest. Standard `shock`. |
| `peakFactor` | ja | Die stärkste Wirkung. `0.45` = 45 % über dem normalen Preis, `-0.3` = 30 % darunter. Muss über `-1` liegen. |
| `rampUpSeconds` | nein | Wie lange die Wirkung braucht, um bis zu ihrem Höchstwert zu wachsen. |
| `durationSeconds` | nein | Wie lange die Wirkung auf ihrem Höchstwert bleibt. |
| `reversal` | nein | Wie die Wirkung wieder verschwindet: `ramp` (gerade Linie), `exponential` (erst schnell, dann langsamer) oder `none` (dauerhaft). |
| `reversalSeconds` | nein | Wie lange die Rückbildung dauert. Für `exponential` siehe unten. |
| `noise` | nein | Zufälliges Zittern der Wirkung. `0.05` lässt sie in jedem Tick um bis zu 5 % ihrer Größe springen. Standard `0`. |

Jeder `type` füllt den Zeitablauf aus, den du weglässt:

| Typ | `rampUpSeconds` | `durationSeconds` | `reversal` | `reversalSeconds` |
|---|---|---|---|---|
| `shock` | 5 | 300 | `exponential` | 300 |
| `trend` | 120 | 600 | `ramp` | 600 |
| `crash` | 10 | 120 | `exponential` | 900 |

Bei `exponential` ist `reversalSeconds` die Zeit, in der etwa zwei Drittel der Wirkung abklingen. Das Ereignis endet nach dem Sechsfachen dieser Zeit, wenn fast nichts mehr übrig ist.

Mit `"reversal": "none"` klingt die Wirkung nie ab. Wenn die Haltephase endet, wird die Änderung dauerhaft in den Standardpreis des Markts geschrieben. Ein dauerhaftes Ereignis lässt sich mit [`undoes`](advanced-events.md#undoing-a-permanent-change) zurücknehmen.

Alle Dauern sind in Sekunden Serverlaufzeit angegeben und werden mit dem `impactDurationMultiplier` des Planers gestreckt. Jeder `peakFactor` wird mit `impactStrengthMultiplier` skaliert. Mit der mitgelieferten [scheduler.json](config-files.md#schedulerjson) dauert jedes Ereignis dreimal so lang und bewegt die Preise halb so weit, wie seine Datei sagt.

### Wie die Wirkung berechnet wird { #how-the-effect-is-calculated }

Für jedes laufende Ereignis und jeden seiner Märkte:

```text
factor = 1 + effect × weightFactor × Sensitivity × (1 + wobble)
```

- `effect` ist der aktuelle Wert des Ereignisses: Er wächst bis `peakFactor` und geht wieder zurück.
- `weightFactor` kommt aus dem [Markteintrag](#markets).
- Sensitivity ist die Einstellung **Empfindlichkeit** des Markts im [News-Plugin](../plugins/news.md).
- `wobble` ist eine Zufallszahl zwischen −`noise` und +`noise`.

Bewegen mehrere Ereignisse denselben Markt, werden ihre Faktoren multipliziert. Das Ergebnis wird zwischen 0.1 und 10 gehalten, und der Zielpreis des Markts wird damit multipliziert.

## Märkte { #markets }

`markets` listet die Items auf, die das Ereignis bewegt. Jeder Eintrag hat ein `item` und optional einen `weightFactor`:

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

| Form | Beispiel | Passt auf |
|---|---|---|
| Item-ID | `minecraft:diamond` | Genau dieses Item. Ohne `:` wird `minecraft:` ergänzt. |
| Tag | `#c:ores` | Jedes Item im Tag. |
| Muster | `minecraft:*_ore` | Jedes Item, dessen ID zum Muster passt. `*` steht für beliebigen Text. |
| Item-ID mit `components` | siehe unten | Eine Variante eines Items, zum Beispiel ein bestimmtes verzaubertes Buch. |

`weightFactor` skaliert die Wirkung für diesen Eintrag (Standard `1`). `0.5` ergibt die halbe Wirkung. Ein negativer Wert kehrt sie um: Im Beispiel oben werden Smaragde billiger, wenn Diamanten teurer werden.

Passt ein Item auf mehrere Einträge, zählt der **erste** Eintrag. Setze genaue Items vor Tags und Muster.

Für Items mit zusätzlichen Daten ergänze `components` im selben Format wie in den [Marktvoreinstellungen](../presets.md). Tags und Muster können keine `components` haben.

Das Ereignis bewegt nur Märkte, die existieren, das NewsPlugin abonniert haben und **News aktiviert** eingeschaltet haben. Ein Item aus einer Mod, die nicht installiert ist, erzeugt eine Warnung und wird übersprungen. Ist kein Eintrag nutzbar, kann das Ereignis nie feuern.

## Planerwerte { #scheduler-values }

Diese Werte gehören in `scheduler.json` oder in den `scheduler`-Block einer beliebigen Ereignisdatei. Für jeden Wert gilt die zuletzt geladene Datei. Werte, die du weglässt, behalten ihren eingebauten Standard.

| Wert | Eingebauter Standard | Mitgelieferte `scheduler.json` | Was er tut |
|---|---|---|---|
| `minSecondsBetweenEvents` | 7200 | 7200 | Kürzeste Wartezeit zwischen zwei zufälligen Ereignissen. |
| `maxSecondsBetweenEvents` | 16200 | 16200 | Längste Wartezeit. Die tatsächliche Wartezeit liegt zufällig dazwischen. |
| `maxActiveEventsGlobal` | 3 | 3 | Wie viele Ereignisse gleichzeitig laufen dürfen. |
| `maxActiveEventsPerMarket` | 1 | 1 | Wie viele Ereignisse gleichzeitig einen Markt bewegen dürfen. |
| `historyMaxEntries` | 1000 | 1000 | Wie viele News im Verlauf bleiben. Ältere werden gelöscht. `0` behält keine. |
| `impactDurationMultiplier` | 1.0 | 3.0 | Streckt jede Dauer jedes Ereignisses. |
| `impactStrengthMultiplier` | 1.0 | 0.5 | Skaliert jede Wirkung jedes Ereignisses. |

Die Wartezeiten zählen nur, solange der Server läuft. Die beiden Grenzen gelten nur für zufällige Ereignisse: Auslösen durch Admins und Ketten ignorieren sie.

Ist `minSecondsBetweenEvents` größer als `maxSecondsBetweenEvents`, fallen beide auf die eingebauten Standards zurück. Die Multiplikatoren müssen über `0` liegen. Die ersten vier Werte kannst du überschreiben, während der Server läuft, siehe [News-Befehle](commands.md#scheduler).

## Prüfung { #validation }

Jedes Neuladen prüft alle Dateien und gibt einen Bericht aus, nach Datei gruppiert, Fehler zuerst. Probleme gibt es in zwei Arten:

- **Fehler** überspringen etwas. Eine kaputte Datei wird übersprungen, die anderen Dateien laden trotzdem. Die meisten Fehler in einem Ereignis überspringen dieses Ereignis: eine fehlende `id`, `headline` oder `text`, beide oder keines von `impact` und `sequences`, ein falscher Werttyp oder ein kaputter `requires`-Eintrag. Fehler in `picture`, `records`, `chains` und `undoes` verwerfen nur dieses Feld, und das Ereignis lädt trotzdem.
- **Warnungen** laden das Ereignis trotzdem, sagen dir aber, dass etwas falsch aussieht: ein unbekanntes Feld (oft ein Tippfehler), ein Item, das nicht installiert ist, ein fehlendes Bild oder ein Ereignis, das nie feuern kann, zum Beispiel weil seine `markets`-Liste fehlt oder auf nichts passt.

Dieselbe `id` in zwei Dateien ist ein Fehler: Die später geladene Datei gewinnt, siehe [Ladereihenfolge](config-files.md#load-order).

Findet ein Neuladen überhaupt kein gültiges Ereignis, bleiben die vorherigen Ereignisse geladen. Laufende Ereignisse werden durch ein Neuladen nie verändert: Sie laufen mit den Werten zu Ende, mit denen sie gestartet sind.

## Verwandte Seiten { #related-pages }

- [Dein erstes Ereignis schreiben](tutorial.md): ein Ereignis Schritt für Schritt aufbauen.
- [Fortgeschrittene Ereignisse](advanced-events.md): Sequenzen, Bedingungen und Ketten.
- [Mitgelieferte Ereignisse](default-events.md): 73 funktionierende Beispiele.
- [News-Konfigurationsdateien](config-files.md): wohin die Dateien gehören.
