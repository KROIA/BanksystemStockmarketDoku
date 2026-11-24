---
title: "Fortgeschrittene Ereignisse"
description: "Sequenzen in mehreren Schritten, Auslösebedingungen, das Ereignisregister der Welt und Ketten von Ereignissen."
---

# Fortgeschrittene Ereignisse { #advanced-events }

Ein einfaches Ereignis steigt an, hält sich und klingt ab. Diese Seite zeigt, wie du längere Geschichten erzählst: Ereignisse in mehreren Schritten, Ereignisse, die von früheren News abhängen, und Ereignisse, die andere Ereignisse starten. Lies zuerst die [Referenz der Ereignisdatei](event-reference.md).

## Sequenzen { #sequences }

Statt `impact` kann ein Ereignis `sequences` haben: eine Liste von Varianten der Geschichte. Jedes Mal, wenn das Ereignis feuert, wählt der Server eine Variante nach ihrem `weight` aus und spielt ihre Schritte nacheinander ab.

Diese gekürzte Fassung des mitgelieferten `gold_rush_rumor` hat zwei Varianten. In zwei von drei Fällen treibt das Gerücht den Preis hoch und lässt ihn dann abstürzen. In einem von drei Fällen verläuft es im Sand:

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

### Felder einer Sequenz { #sequence-fields }

| Feld | Pflicht | Was es tut |
|---|---|---|
| `name` | ja | Name der Variante. Er erscheint in den Details des Ereignisses. |
| `weight` | nein | Wie oft diese Variante im Vergleich zu den anderen gewählt wird. Muss über `0` liegen. Standard `1`. |
| `steps` | ja | Die Schritte, in ihrer Reihenfolge. Mindestens einer. |

### Felder eines Schritts { #step-fields }

| Feld | Pflicht | Was es tut |
|---|---|---|
| `name` | ja | Name des Schritts, eindeutig innerhalb seiner Variante. Ketten können über diesen Namen bei einem Schritt starten. |
| `durationSeconds` | ja | Wie lange der Schritt dauert: eine Zahl oder `{ "min": …, "max": … }` für eine zufällige Länge. |
| `targetFactor` | ja, außer bei `hold` | Wo die Wirkung am Ende des Schritts stehen soll. `0.4` = 40 % über normal, `-0.15` = 15 % darunter. Muss über `-1` liegen. |
| `curve` | nein | Wie die Wirkung dorthin kommt, siehe unten. Standard `linear`. |
| `noise` | nein | Zufälliges Zittern während dieses Schritts, wie bei `impact`. Standard `0`. |
| `markets` | nein | Andere Märkte nur für diesen Schritt, im selben Format wie die `markets` des Ereignisses. Ohne das Feld nutzt der Schritt die Märkte des Ereignisses. |
| `permanent` | nein | `true` beim **letzten** Schritt macht seinen Endwert dauerhaft. Nur beim letzten Schritt erlaubt. |

Jeder Schritt beginnt dort, wo der vorige geendet hat. Der erste Schritt beginnt bei `0`.

| Kurve | Was die Wirkung tut |
|---|---|
| `linear` | Bewegt sich in einer geraden Linie zu `targetFactor`. |
| `instant` | Springt sofort auf `targetFactor` und bleibt dort für den Rest des Schritts. |
| `exponential` | Bewegt sich erst schnell, dann langsamer. Wenn der Schritt endet, ist sie fast angekommen. |
| `hold` | Bleibt, wo sie ist. `targetFactor` wird ignoriert. |

Der letzte Schritt sollte bei `0` enden. Tut er das nicht und ist er nicht `permanent`, springt die Wirkung am Ende der Sequenz auf `0` zurück, und der Bericht beim Neuladen warnt dich.

Ein letzter Schritt mit `permanent` wirkt wie `"reversal": "none"`: Wenn die Sequenz endet, wird sein Endwert dauerhaft in den Standardpreis des Markts geschrieben.

Die Dauern werden einmal ausgewürfelt, wenn das Ereignis startet. Sie werden mit `impactDurationMultiplier` gestreckt, und jeder `targetFactor` wird mit `impactStrengthMultiplier` skaliert, siehe [Planerwerte](event-reference.md#scheduler-values).

!!! tip "Schrittnamen einfacher Ereignisse"
    Ein `impact`-Ereignis verhält sich wie eine Variante mit den Schritten `ramp`, `hold` und `reversal`. Ein dauerhaftes hat `ramp`, `hold` und `permanent`. Diese Namen kannst du in Ketten nutzen.

## Das Ereignisregister der Welt { #the-world-event-registry }

Der Server führt ein Gedächtnis darüber, was in der Welt passiert ist. Er speichert es mit der Welt und behält es über Neustarts und Neuladen hinweg. Es enthält zwei Dinge:

- **Auslöseeinträge.** Für jedes Ereignis: wie oft es gefeuert hat, wann es zum ersten und zum letzten Mal gefeuert hat, und an welchem Spieltag. Ein Ereignis gilt als gefeuert, wenn seine Schlagzeile veröffentlicht ist.
- **Deine eigenen Werte.** Paare aus Schlüssel und Wert, die Ereignisse mit `records` schreiben.

`records` schreibt Werte, wenn die Schlagzeile des Ereignisses veröffentlicht wird:

```json
{
  "records": {
    "era": "gold_standard",
    "luxury_tax": "active"
  }
}
```

Werte sind immer Text, aber Text wie `"3"` lässt sich als Zahl vergleichen. Ein späteres Schreiben auf denselben Schlüssel ersetzt den Wert. Das Register enthält höchstens 256 Schlüssel, und Schlüssel und Werte dürfen höchstens 256 Zeichen lang sein. Der Bericht beim Neuladen warnt dich, wenn `records` diese Grenzen überschreitet.

Was gespeichert ist, siehst du mit `/stockmarket news registry list`. Mit den `registry clear`-Befehlen kannst du Einträge löschen, siehe [News-Befehle](commands.md#registry).

## Bedingungen { #requirements }

`requires` ist eine Liste von Bedingungen. Das Ereignis kann nur feuern, wenn **alle** erfüllt sind:

```json
{
  "requires": [
    { "type": "firedBefore", "eventId": "luxury_goods_tax", "minSecondsAgo": 172800 },
    { "type": "keyEquals", "key": "luxury_tax", "value": "active" }
  ]
}
```

| Typ | Felder | Erfüllt, wenn |
|---|---|---|
| `firedBefore` | `eventId`, `minTimes` (Standard 1), `minSecondsAgo`, `maxSecondsAgo` | Das Ereignis hat mindestens `minTimes`-mal gefeuert. Mit `minSecondsAgo` oder `maxSecondsAgo` muss sein letztes Feuern mindestens oder höchstens so lange her sein. Ein Ereignis, das nie gefeuert hat, erfüllt dies nie, auch nicht mit `minTimes` 0. |
| `notFired` | `eventId` | Das Ereignis hat nie gefeuert. Nutze die eigene `id` des Ereignisses für ein einmaliges Ereignis. |
| `notFiredWithin` | `eventId`, `seconds` | Das Ereignis hat nie gefeuert, oder sein letztes Feuern ist mehr als `seconds` her. |
| `countAtLeast` | `eventId`, `count` | Das Ereignis hat mindestens `count`-mal gefeuert. |
| `countAtMost` | `eventId`, `count` | Das Ereignis hat höchstens `count`-mal gefeuert. |
| `keyEquals` | `key`, `value` | Der Schlüssel hat genau diesen Wert. |
| `keyNotEquals` | `key`, `value` | Der Schlüssel hat einen anderen Wert oder existiert nicht. |
| `keyExists` | `key` | Der Schlüssel existiert. |
| `keyAbsent` | `key` | Der Schlüssel existiert nicht. |
| `keyAtLeast` | `key`, `value` (Zahl) | Der Schlüssel enthält eine Zahl von mindestens `value`. |
| `keyAtMost` | `key`, `value` (Zahl) | Der Schlüssel enthält eine Zahl von höchstens `value`. |

Die Zeiten in Bedingungen sind echte Zeit: Sie zählen weiter, während der Server aus ist. Abklingzeiten tun das nicht, sie zählen nur, solange der Server läuft.

Ein unbekannter `type` oder ein fehlendes Feld ist ein Fehler, und das ganze Ereignis wird übersprungen. Eine Bedingung, die sich nicht prüfen lässt, darf ein Ereignis nie durchlassen.

Der Server prüft die Bedingungen, wenn er ein Ereignis plant, und noch einmal, wenn das Ereignis fällig ist. Eine Kette prüft sie erneut, wenn ihre Verzögerung vorbei ist. Auslösen durch einen Admin ignoriert sie, aber das Fenster des News-Plugins fragt zuerst nach, wenn sie nicht erfüllt sind.

## Eine dauerhafte Änderung zurücknehmen { #undoing-a-permanent-change }

`undoes` nimmt die dauerhafte Änderung eines anderen Ereignisses zurück. Die Luxussteuer senkt die Preise von Edelsteinen dauerhaft, und ihre Abschaffung bringt sie zurück:

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

Während es läuft, bewegt das Ereignis die Preise wie jedes andere Ereignis. Wenn es endet, wendet es nicht seine eigene dauerhafte Änderung an. Stattdessen fügt es genau das wieder hinzu, was `luxury_goods_tax` auf jedem Markt geändert hat. Ein Markt, den die Steuer nie geändert hat, bleibt, wie er ist. Das zurücknehmende Ereignis muss selbst dauerhaft sein, sonst hat es an seinem Ende nichts anzuwenden.

## Ketten { #chains }

`chains` startet Folgeereignisse. Auf einen Waldbrand kann billiges Holz folgen, auf einen Spekulationsrausch ein Crash:

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

| Feld | Pflicht | Was es tut |
|---|---|---|
| `eventId` | ja | Das Ereignis, das starten soll. |
| `on` | ja | Wann: `publish` (wenn die Schlagzeile erscheint), `step` (wenn ein Schritt beginnt) oder `completion` (wenn das Ereignis endet). |
| `step` | bei `on: step` | Der Name des Schritts. Der Bericht beim Neuladen warnt dich, wenn keine Variante einen Schritt mit diesem Namen hat. |
| `chance` | nein | Wie wahrscheinlich das Folgeereignis ist, von `0` bis `1`. Standard `1`. |
| `delaySeconds` | nein | Wartezeit, bevor das Folgeereignis startet: eine Zahl oder `{ "min": …, "max": … }`. Standard `0`. Sie zählt nur, solange der Server läuft. |
| `sameMarkets` | nein | `true`: Das Folgeereignis bewegt die Märkte des ersten Ereignisses statt seiner eigenen. Standard `false`. |

Wenn der Moment kommt, würfelt der Server die Wahrscheinlichkeit einmal aus. Gewinnt der Wurf, wartet das Folgeereignis seine Verzögerung ab und startet dann. Wartende Folgeereignisse überstehen Neustarts.

Ein Folgeereignis ignoriert die Abklingzeit und beide Grenzen für aktive Ereignisse. Seine eigene Abklingzeit beginnt wie gewohnt. Wenn es fällig ist, wird es übersprungen, wenn:

- es deaktiviert ist oder schon läuft,
- seine Bedingungen nicht erfüllt sind,
- es auf keinen Markt passt.

Eine Kette kann kein `adminOnly`-Ereignis starten: Das ist ein Fehler, und die Kette wird verworfen. `completion`-Ketten feuern nicht, wenn ein Admin das Ereignis stoppt. Sie feuern aber, wenn **Nächste Phase** die letzte Phase überspringt.

**Schleifenschutz.** Eine Kette kann höchstens 4 Folgeereignisse hintereinander haben, und ein Ereignis kann nicht zweimal in derselben Kette vorkommen. A → B → A passiert also nie. Eine Kette von einem Ereignis zu sich selbst mit `chance` 1 und ohne `notFired`-Bedingung erzeugt eine Warnung.

!!! tip "Ereignisse, die nur Ketten starten sollen"
    Gib einem Folgeereignis `"weight": 0`. Es wird nie zufällig gewählt, nur von seiner Kette oder von einem Admin. Die mitgelieferten `margin_call_crash` und `grain_relief_convoy` funktionieren so.

## Beispiel: der Handlungsstrang Goldstandard { #example-the-gold-standard-storyline }

Die mitgelieferten Politik-Ereignisse erzählen mithilfe des Registers eine Geschichte:

1. **`gold_reserve_standard`** hebt Gold dauerhaft an. Es setzt `notFired` auf sich selbst voraus, passiert also einmal pro Welt. Es speichert `era` = `gold_standard`. Wenn sein Schritt `hold` beginnt, startet es mit 50 % Wahrscheinlichkeit 5 bis 15 Minuten später `gold_rush_rumor`.
2. **`end_of_gold_standard`** senkt Gold dauerhaft. Es setzt voraus, dass der Goldstandard vor mindestens 3 Stunden gefeuert hat, dass `era` noch `gold_standard` ist und dass es selbst nie gefeuert hat. Es speichert `era` = `fiat`.

Die Luxussteuer funktioniert genauso, kann sich aber wiederholen: `luxury_goods_tax` setzt voraus, dass `luxury_tax` nicht `active` ist, und setzt den Wert auf `active`. `luxury_tax_repealed` setzt `active` und mindestens zwei Tage seit der Steuer voraus, setzt `repealed` und nimmt die Steuer zurück. Danach kann die Steuer erneut kommen.

## Verwandte Seiten { #related-pages }

- [Referenz der Ereignisdatei](event-reference.md): alle Grundfelder.
- [Dein erstes Ereignis schreiben](tutorial.md): ein Beispiel für eine Kette, Schritt für Schritt.
- [Mitgelieferte Ereignisse](default-events.md): jeder mitgelieferte Handlungsstrang.
- [News-Befehle](commands.md): auslösen, Phasen überspringen und das Register.
