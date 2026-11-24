---
title: "News-Befehle"
description: "Die Admin-Befehle unter /stockmarket news und ihre Knöpfe im Verwaltungsfenster."
---

# News-Befehle { #news-commands }

Alle News-Befehle beginnen mit `/stockmarket news`. Die meisten haben einen Knopf im [Fenster des News-Plugins](index.md#the-news-plugin-window), du kannst dasselbe also auch mit der Maus erledigen.

`/stockmarket news` ohne weitere Angaben öffnet die Zeitung. Das darf jeder Spieler, siehe [Markt-News](../../../stockmarket/newspaper.md). Alle anderen Befehle sind für Admins.

## Wer sie nutzen darf { #who-can-use-them }

Du brauchst das StockMarket-Admin-Flag, das du mit `/stockmarket op` bekommst. Mit einer Berechtigungs-Mod brauchst du außerdem den Node `stockmarket.admin.command.news`. Auch die Konsole kann die Befehle nutzen. Siehe [Admins und Berechtigungen](../../permissions.md).

In einem Netzwerk funktionieren die Befehle auf jedem Server: Ein Slave reicht sie an den Master weiter, auf dem die News laufen. Die Tab-Vervollständigung der Ereignisnamen funktioniert nur auf dem Master.

Die Ausgabe der Befehle ist immer auf Englisch.

## Alle Befehle { #all-commands }

| Befehl | Was er tut | Im Fenster |
|---|---|---|
| `/stockmarket news reload` | Liest alle News-Dateien neu ein und gibt den Bericht aus. | **Neu laden** |
| `/stockmarket news list` | Listet alle geladenen Ereignisse mit ihren Markierungen und alle laufenden Ereignisse mit Phase, restlicher Zeit und Wirkung pro Markt. | Tabs **Alle Ereignisse** und **Aktiv** |
| `/stockmarket news info <eventId>` | Zeigt alles über ein Ereignis: Texte, Märkte, Zeitablauf, Abklingzeit und ob es aktiviert ist oder läuft. | Auf das Ereignis klicken |
| `/stockmarket news trigger <eventId> [market]` | Startet das Ereignis jetzt. | **Auslösen** |
| `/stockmarket news stop <eventId>` | Stoppt ein laufendes Ereignis sofort. | **Stopp** |
| `/stockmarket news stop all` | Stoppt alle laufenden Ereignisse. | **Alle stoppen** |
| `/stockmarket news skipphase <eventId>` | Lässt ein laufendes Ereignis zu seiner nächsten Phase oder seinem nächsten Schritt springen. | **Nächste Phase** |
| `/stockmarket news enable <eventId>` | Schaltet ein Ereignis wieder ein. | Checkbox in **Alle Ereignisse** |
| `/stockmarket news disable <eventId>` | Schaltet ein Ereignis aus. | Checkbox in **Alle Ereignisse** |
| `/stockmarket news resetcooldown <eventId>` | Beendet die Abklingzeit des Ereignisses, sodass es sofort wieder gewählt werden kann. | **CD-Reset** |
| `/stockmarket news scheduler show` | Zeigt die Werte des Planers und die nächsten geplanten Ereignisse. | Tab **Planer** |
| `/stockmarket news scheduler set <key> <value>` | Überschreibt einen Wert des Planers. | **Übernehmen** in **Planer** |
| `/stockmarket news scheduler reset [key]` | Entfernt eine Überschreibung oder alle. | **Auf Datei zurücksetzen** (alle) |
| `/stockmarket news registry list` | Zeigt das Ereignisregister der Welt. | |
| `/stockmarket news registry clear <eventId>` | Löscht den Auslöseeintrag eines Ereignisses. | |
| `/stockmarket news registry clear key <key>` | Löscht einen deiner eigenen Werte im Register. | |
| `/stockmarket news registry clear all` | Löscht das ganze Register. | |

## Auslösen { #trigger }

`trigger` startet ein Ereignis sofort und ignoriert dabei sein Gewicht, seine Abklingzeit, `adminOnly`, seine Bedingungen und die Grenzen für aktive Ereignisse. Es verweigert trotzdem, wenn:

- das Ereignis deaktiviert ist oder schon läuft,
- das NewsPlugin ausgeschaltet ist,
- das Ereignis auf keinen abonnierten Markt mit eingeschaltetem **News aktiviert** passt.

Mit `[market]` bewegt das Ereignis nur diesen einen Markt. Schreibe die Item-ID des Markts in Anführungszeichen, zum Beispiel `"minecraft:wheat"`. Die Tab-Vervollständigung schlägt die Namen vor. Teilen sich mehrere Märkte eine Item-ID, zum Beispiel verzauberte Bücher, schlägt sie auch deren Nummern vor.

Das Auslösen startet die Abklingzeit des Ereignisses wie gewohnt. Die Schlagzeile folgt der Ankündigungsverzögerung des Ereignisses. Im Fenster fragt **Auslösen** zuerst nach, wenn die Abklingzeit noch läuft oder die Bedingungen nicht erfüllt sind.

## Stoppen und Phase überspringen { #stop-and-skip-phase }

Diese beiden Befehle beenden ein Ereignis auf verschiedene Weise:

- **`stop`** bricht das Ereignis ab. Seine Wirkung wird sofort entfernt, in jeder Phase, und seine volle Abklingzeit beginnt von vorn. Ein dauerhaftes Ereignis wird abgebrochen, bevor es seine Änderung schreibt, es bleibt also nichts. Ketten, die auf das Ende des Ereignisses warten, starten nicht.
- **`skipphase`** bringt das Ereignis voran: von **Ausstehend** zum Anstieg, dann zur Haltephase, zur Rückbildung und zum Ende, oder zum nächsten Schritt einer Sequenz. Überspringst du die letzte Phase, endet das Ereignis normal: Ein dauerhaftes Ereignis schreibt seine Änderung, und Ketten zum Ende können starten.

Um ein ganzes Ereignis schnell zu testen, löse es aus und nutze `skipphase`, bis es endet.

## Aktivieren und deaktivieren { #enable-and-disable }

Ein deaktiviertes Ereignis feuert nie: nicht zufällig, nicht durch eine Kette und nicht durch `trigger`. Es erscheint als **[deaktiviert]** im Tab **Alle Ereignisse**. Das Deaktivieren stoppt kein laufendes Ereignis; dafür nutzt du `stop`.

Der Ein/Aus-Zustand wird mit der Welt gespeichert und übersteht Neuladen und Neustarts. So schaltest du ein mitgeliefertes Ereignis ab, denn eine gelöschte mitgelieferte Datei kommt zurück, siehe [Ein mitgeliefertes Ereignis ändern](config-files.md#changing-a-shipped-event).

## Planer { #scheduler }

`scheduler set` ändert einen Wert, während der Server läuft, ohne dass du eine Datei bearbeitest. Diese Schlüssel lassen sich setzen:

| Schlüssel | Was er tut |
|---|---|
| `minSecondsBetweenEvents` | Kürzeste Wartezeit zwischen zwei zufälligen Ereignissen. |
| `maxSecondsBetweenEvents` | Längste Wartezeit. |
| `maxActiveEventsGlobal` | Wie viele Ereignisse gleichzeitig laufen dürfen. |
| `maxActiveEventsPerMarket` | Wie viele Ereignisse gleichzeitig einen Markt bewegen dürfen. |

Der Wert muss eine ganze Zahl von mindestens 1 sein, und die kürzeste Wartezeit darf nicht länger als die längste sein. Überschreibungen werden mit der Welt gespeichert: Sie bleiben über Neuladen und Neustarts hinweg, bis du sie zurücksetzt. `scheduler show` und der Tab **Planer** markieren sie als überschrieben.

Die anderen Werte des Planers, etwa die Multiplikatoren, lassen sich nur in den Dateien ändern, siehe [Planerwerte](event-reference.md#scheduler-values).

## Register { #registry }

Das [Ereignisregister der Welt](advanced-events.md#the-world-event-registry) merkt sich, welche Ereignisse gefeuert haben, und enthält die Werte, die Ereignisse mit `records` schreiben. Bedingungen lesen es.

- `registry list` zeigt jeden Auslöseeintrag (wie oft, erstes und letztes Mal, Spieltag) und jeden Wert.
- `registry clear <eventId>` löscht einen Auslöseeintrag. Das Ereignis gilt dann als nie gefeuert, ein einmaliges Ereignis kann also erneut passieren.
- `registry clear key <key>` löscht einen Wert.
- `registry clear all` löscht alles.

## Andere Admins sehen, was du tust { #other-admins-see-what-you-do }

Jeder Befehl, der etwas ändert, wird im Chat den anderen StockMarket-Admins gemeldet, die online sind: Auslösen, Stoppen, übersprungene Phasen, Aktivieren und Deaktivieren, zurückgesetzte Abklingzeiten, Änderungen am Planer, Löschungen im Register und Neuladen. So kann niemand heimlich News starten und damit handeln.

## Verwandte Seiten { #related-pages }

- [News-System](index.md): das Fenster des News-Plugins.
- [Dein erstes Ereignis schreiben](tutorial.md): ein Ereignis Schritt für Schritt testen.
- [Fortgeschrittene Ereignisse](advanced-events.md): Bedingungen und das Register.
- [Admins und Berechtigungen](../../permissions.md): das Admin-Flag und die Berechtigungs-Nodes.
