---
title: "News-Bilder"
description: "Bilder zu Ereignissen hinzufügen: Regeln für die Dateien, der Zeitungsdruck-Look, mitgelieferte Bilder und die Synchronisierung."
---

# News-Bilder { #news-pictures }

Jedes News-Ereignis kann ein Bild haben. Es erscheint neben der Meldung in der Zeitung, im Tab **Aktiv** des Fensters des News-Plugins und in den Details des Ereignisses. Alle mitgelieferten Ereignisse bringen ihr eigenes Bild mit.

## Ein Bild hinzufügen { #adding-a-picture }

1. Lege eine PNG-Datei auf dem Server in `config/StockMarket/news/pictures/`. Dateien in Unterordnern werden ignoriert.
2. Nenne sie im Ereignis im Feld `picture`:

    ```json
    {
      "picture": "wheat_shortage.png"
    }
    ```

3. Führe `/stockmarket news reload` aus.

Der Wert von `picture` ist nur der Dateiname, nie ein Pfad. Er muss auf `.png` enden, darf nicht mit einem Punkt beginnen und darf weder `/`, `\`, `:` noch `..` enthalten. Ein falscher Name wird mit einem Fehler im Bericht beim Neuladen verworfen, und das Ereignis lädt ohne Bild. Existiert die Datei nicht, warnt dich der Bericht, und das Ereignis lädt ebenfalls ohne Bild.

## Regeln für die Dateien { #file-rules }

| Regel | Grenze |
|---|---|
| Format | PNG. Der Server prüft den Inhalt der Datei, nicht nur den Namen. |
| Dateigröße | Höchstens 128 KiB. |
| Breite und Höhe | Jeweils zwischen 16 und 512 Pixeln. |

Eine Datei, die gegen eine Regel verstößt, wird als Fehler im Bericht beim Neuladen aufgeführt und nicht verwendet. Die anderen Bilder laden trotzdem.

## Wie Bilder aussehen { #how-pictures-look }

Du kannst Farbe verwenden. Das Spiel macht aus jedem Bild graue Druckfarbe auf Zeitungspapier, sodass alle Bilder aussehen, als wären sie in derselben Zeitung gedruckt.

Quadratische Bilder wirken am besten. Die Zeitung und die Details des Ereignisses zeigen das Bild in einem quadratischen Rahmen und schneiden ab, was an den Seiten übersteht. Halte das Wichtige also in der Mitte. Der Tab **Aktiv** zeigt das ganze Bild, passend verkleinert.

## Die mitgelieferten Bilder { #the-shipped-pictures }

Die Mod schreibt ein Bild pro mitgeliefertem Ereignis nach `pictures/`, benannt nach dem Ereignis, zum Beispiel `diamond_rush.png`. Wie die [mitgelieferten Ereignisse](config-files.md#how-new-shipped-events-arrive) füllen sie sich selbst auf:

- Bei jedem Neuladen wird ein fehlendes mitgeliefertes Bild wieder geschrieben.
- Eine vorhandene Bilddatei wird nie überschrieben.

Daher gilt:

- **Um deine eigenen Bilder zu verwenden,** ersetze die Datei und behalte ihren Namen.
- **Um ein mitgeliefertes Ereignis ohne Bild zu zeigen,** entferne das Feld `picture` aus seiner Ereignisdatei. Das PNG zu löschen hilft nicht, es kommt beim nächsten Neuladen zurück.

## Ein Bild ändern { #changing-a-picture }

Nachdem du eine Datei geändert oder ersetzt hast, führe `/stockmarket news reload` aus. Neue News nutzen das neue Bild.

News, die schon veröffentlicht sind, behalten das Bild, mit dem sie erschienen sind. Der Server kopiert jedes Bild in die Welt, wenn die News veröffentlicht wird. Alte Einträge in der Zeitung ändern sich also nie, auch wenn du die Datei später löschst. Kopien, die keine News im Verlauf mehr nutzt, werden von selbst gelöscht.

## Wie die Spieler die Bilder bekommen { #how-players-get-the-pictures }

Die Spieler müssen nichts installieren. Das Spiel lädt jedes Bild vom Server herunter, wenn es gebraucht wird. In einem Netzwerk reichen die Slaves diese Downloads an den Master weiter, der alle Bilder hat. Siehe [Master- und Slave-Server](../../multi-server.md).

## Verwandte Seiten { #related-pages }

- [News-Konfigurationsdateien](config-files.md): der News-Ordner.
- [Referenz der Ereignisdatei](event-reference.md): das Feld `picture` und die anderen Felder.
- [Markt-News](../../../stockmarket/newspaper.md): was die Spieler sehen.
