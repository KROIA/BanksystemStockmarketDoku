---
title: "Discord-Feed"
description: "Handel, Bankereignisse und Alarme an Discord-Webhooks senden."
---

# Discord-Feed { #discord-feed }

Beide Mods können in Discord-Kanäle posten: Einzahlungen, Überweisungen, Handel, Änderungen durch Admins und Alarme. Sie verwenden Discord-Webhooks, also brauchst du keinen Bot. Der Feed ist standardmäßig aus.

<figure markdown="span">
  ![Fünf Nachrichten des Discord-Feeds von einem Webhook namens Economy Feed: ein Marktkauf (64 Diamanten), ein Marktverkauf (128 Weizen), ein Marktalarm (ein Handelsgewinn über der Schwelle), eine Bankeinzahlung (256 Eisenbarren) und eine Dividende (750.00 an 3 Aktionäre)](../assets/images/shared/discord-feed.png){ .own-size width="589" }
</figure>

Nur der Master-Server postet, also erscheint jedes Ereignis genau einmal. Slaves senden nichts.

## Einrichten { #setting-it-up }

1. **Erstelle einen Webhook** in Discord: Kanaleinstellungen → **Integrationen** → **Webhooks** → **Neuer Webhook** → **Webhook-URL kopieren**. Ein Webhook pro Kanal.
2. **Starte den Server einmal.** Er legt den Ordner `config/modutilities/discord/` mit `webhooks.json`, `banksystem.json` und `stockmarket.json` an.
3. **Trage deine Webhooks** in `webhooks.json` ein, jeden unter einem Namen deiner Wahl:

    ```json
    {
      "webhooks": {
        "bank": "https://discord.com/api/webhooks/<id>/<token>",
        "admins": "https://discord.com/api/webhooks/<id>/<token>"
      }
    }
    ```

    Nur URLs von Discord-Webhooks werden angenommen. Andere Einträge werden mit einer Warnung im Log übersprungen.

4. **Wähle die Nachrichten** in `banksystem.json` und `stockmarket.json`. Jeder Nachrichtentyp ist anfangs aus. Schalte die gewünschten ein und liste die Namen der Webhooks auf, an die sie gehen:

    ```json
    {
      "language": "en_us",
      "types": {
        "bank-deposit":   { "enabled": true, "webhooks": ["bank"],   "minAmount": 1000 },
        "bank-suspicion": { "enabled": true, "webhooks": ["admins"], "minAmount": 0 }
      }
    }
    ```

    `minAmount` überspringt kleinere Ereignisse: bei Geld in Dollar, sonst die Anzahl der Items. `language` legt die Sprache der Nachrichten fest: `en_us`, `de_de`, `de_ch` oder `zh_cn`.

5. **Schalte den Feed ein** in den Mod-Einstellungen jeder Mod: **Discord-Feed** für BankSystem, **Discord-Feed (Trades und Warnungen)** für StockMarket. Kein Neustart nötig.
6. **Lade die Dateien** mit `/banksystem discord reload`, oder starte den Server neu.

!!! warning "Halte die Webhook-URLs geheim"
    Wer eine Webhook-URL hat, kann in deinen Kanal posten. Gib `webhooks.json` nicht weiter und füge die URLs nirgends ein. Die Mods zeigen sie nie im Spiel oder im Log.

## Befehle { #commands }

| Befehl | Was er tut |
|---|---|
| `/banksystem discord status` | Listet die Webhooks auf (gültig oder nicht) und, für beide Mods, welche Nachrichtentypen an sind, ihren `minAmount` und ihre Webhooks. |
| `/banksystem discord reload` | Liest alle Dateien in `config/modutilities/discord/` neu ein. |

`/stockmarket discord` und `/modutilities discord` tun dasselbe. Alle drei brauchen Operator-Level 3 oder die Berechtigung `modutilities.command.discord`, siehe [Admins und Berechtigungen](permissions.md). Auf einem Slave meldet der Status-Befehl zuerst, dass der Master postet. Die Zeilen darunter zeigen die eigenen Webhooks, die Warteschlange und die Nachrichtentypen des Slaves, nicht die des Masters.

## Nachrichten von BankSystem { #banksystem-messages }

| Typ | Gepostet, wenn |
|---|---|
| `bank-deposit` | Items oder Geld auf ein Konto gehen: Bank Terminal, Bank Upload Block, Banknoten und Währungsbindungen. |
| `bank-withdraw` | Items oder Geld herauskommen, auch wenn ein geschlossenes Konto ausgezahlt wird. |
| `bank-transfer-in`, `bank-transfer-out` | Ein Konto eine Überweisung empfängt oder sendet. |
| `bank-payout` | Ein Unternehmen seine Mitglieder bezahlt. Gepostet für das empfangende Konto. |
| `bank-dividend` | Ein Unternehmen eine Dividende zahlt. Eine Dividendenausschüttung ist eine Nachricht mit der Summe und der Anzahl der Aktionäre. |
| `bank-share` | Aktien geprägt, eingelöst oder gehandelt werden. |
| `bank-admin` | Ein Admin einen Kontostand ändert, ein Konto freigibt, einfriert, bearbeitet oder schließt oder ein bankfähiges Item entfernt. Das Entfernen eines Items ist eine Nachricht für alle Konten. |
| `bank-suspicion` | Eine [Verdachtsmarkierung](audit/alerts.md) gesetzt wird. |
| `bank-other` | Alles andere, zum Beispiel das Startguthaben. |

Aktiengeschäfte werden hier nicht gepostet. StockMarket postet sie selbst.

## Nachrichten von StockMarket { #stockmarket-messages }

| Typ | Gepostet, wenn |
|---|---|
| `market-buy` | Die Kauforder eines Spielers abgeschlossen ist: ausgeführt oder storniert, nachdem ein Teil davon ausgeführt wurde. Zeigt Item, Menge und Durchschnittspreis. |
| `market-sell` | Dasselbe für Verkaufsorders. |
| `market-exchange` | Die Order [Item gegen Item](../stockmarket/pair-trading.md) eines Spielers abgeschlossen ist. Eine Nachricht pro Order, mit dem, was verkauft wurde, was gekauft wurde, und dem übrigen Geld. |
| `market-alert` | Ein [Handelsalarm](audit/alerts.md#stockmarket-alerts) ausgelöst wird. |

Orders von Bots und Orders ohne Ausführung werden nie gepostet. Beim Handel ist `minAmount` die Anzahl der gehandelten Items. Bei `market-exchange` ist es die Menge, die der Spieler in die Order eingegeben hat.

## Datenschutz { #privacy }

Nachrichten zu Handel und Bank nennen nur den Spieler. Sie lassen die Kontonummer, die UUID des Spielers und das andere Konto einer Überweisung weg.

Zwei Nachrichtentypen sind anders. `bank-suspicion` zeigt das markierte Konto, und `market-alert` nennt den Spieler und seine UUID. Sende sie in einen Kanal, den nur Admins lesen können.

### Mehr Felder anzeigen { #showing-more-fields }

Du kannst ändern, was eine Nachricht zeigt. Gib dem Typ eine eigene `fields`-Liste. Sie ersetzt die Standardfelder vollständig, also liste jedes Feld auf, das du willst:

```json
"bank-transfer-out": {
  "enabled": true, "webhooks": ["bank"], "minAmount": 0,
  "fields": [
    {"name": "Player",       "value": "{player}",        "inline": true},
    {"name": "Account",      "value": "{account}",       "inline": true},
    {"name": "Counterparty", "value": "{other_account}", "inline": true},
    {"name": "Amount",       "value": "{amountText}",    "inline": true},
    {"name": "Time",         "value": "{time}",          "inline": false}
  ]
}
```

Führe danach `/banksystem discord reload` aus. Ein Feld mit leerem Wert wird weggelassen. Ein Typ kann auch einen eigenen `title` und eine eigene `color` haben. Deine eigenen Felder bleiben erhalten, wenn ein Update einer Mod die Standardwerte ändert.

| Nachrichten | Werte, die du verwenden kannst |
|---|---|
| `bank-*` | `{player}`, `{player_uuid}`, `{account}`, `{other_account}`, `{item}`, `{amountText}` (formatiert), `{amount}` (reine Zahl), `{holders}`, `{company}`, `{kind}`, `{note}`, `{time}` |
| `bank-suspicion` | `{account}`, `{flag}`, `{severity}`, `{amountText}`, `{amount}`, `{details}`, `{ref}`, `{time}` |
| `market-buy`, `market-sell` | `{player}`, `{player_uuid}`, `{account}`, `{item}`, `{item_id}`, `{amount}`, `{price}` (Durchschnitt), `{time}` |
| `market-exchange` | `{player}`, `{player_uuid}`, `{account}`, `{sold_item}`, `{sold_item_id}`, `{sold_amount}`, `{sold_price}`, `{bought_item}`, `{bought_item_id}`, `{bought_amount}`, `{bought_price}`, `{leftover}`, `{currency}`, `{amount}`, `{interMarketGroup}`, `{time}` |

## Verwandte Seiten { #related-pages }

- [Alarme und Verdachtsmarkierungen](audit/alerts.md): was die Alarme bedeuten.
- [Platzhalter](placeholders.md): Live-Werte im Spiel anzeigen.
- [Admins und Berechtigungen](permissions.md): wer die Discord-Befehle ausführen darf.
