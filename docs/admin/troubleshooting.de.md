---
title: "Fehlerbehebung"
description: "Häufige Serverprobleme mit beiden Mods: eine Welt, die nicht lädt, fehlende Items, nicht vertrauenswürdige Slaves und Bildschirme, die sich nicht öffnen."
---

# Fehlerbehebung { #troubleshooting }

Wenn etwas schiefgeht, schau zuerst ins Server-Log (`logs/latest.log`). Beide Mods beginnen ihre Meldungen mit `[BankSystem]` oder `[StockMarket]`.

## Die Welt lädt nicht { #the-world-doesnt-load }

Beide Mods prüfen ihre Daten, bevor eine Welt lädt. Wenn etwas nicht stimmt, halten sie die Welt an, statt das Geld deiner Spieler zu riskieren. Es wird nichts verändert. Im Einzelspieler erklärt ein Bildschirm mit dem Titel *BankSystem hat diese Welt nicht geladen* oder *StockMarket hat diese Welt nicht geladen* den Grund. Auf einem Server steht der Grund im Log.

| Grund | Was du tust |
|---|---|
| *Gespeicherte Bank-Items gehören zu Mods, die nicht installiert sind* | Du hast eine Mod entfernt, deren Items in der Bank lagen. Installiere die Mod wieder. Oder entferne die Items: Im Einzelspieler klickst du auf **Fehlende Items entfernen und laden**; auf einem Server schaltest du **Items fehlender Mods entfernen (einmalig)** in `settings.json` ein und startest neu. Das Entfernen löscht diese Bestände aus jedem Konto, nachdem die Daten von BankSystem gesichert wurden. |
| *Diese unterschiedlichen Items würden zum selben Item werden* | Eine geänderte Mod oder eine geänderte [Komponentenliste](banksystem/bankable-items.md#changing-the-lists-on-a-world-in-use) würde Items zusammenführen, die jetzt verschieden sind. Mach die Änderung rückgängig oder bestätige das Zusammenführen: **Zusammenführen bestätigen und laden** im Einzelspieler, **Confirm pending item merge (one-shot)** in `settings.json` auf einem Server. Beim Bestätigen werden ihre Bestände addiert. |
| Eine ausstehende Weltreparatur im Log | Die Item-Liste wurde von einer sehr alten Version von BankSystem beschädigt. Sichere die Welt, schalte **Confirm pending world repair (one-shot)** in `settings.json` ein und starte neu. |
| *Diese Welt wurde von einer neueren Version gespeichert* | Die Welt wurde vorher mit einer neueren Version der Mod geöffnet. Aktualisiere die Mod oder stelle ein Backup von vorher wieder her. |
| *Die Aktualisierung der Daten dieser Welt auf die neue Version ist fehlgeschlagen* | Lies den Grund im Log und behebe ihn. Öffne die Welt dann erneut, um die Aktualisierung fortzusetzen. Oder stelle das Backup-Zip wieder her, das die Meldung nennt. Siehe [Installation und Updates](install.md#updating). |

Die einmaligen Einstellungen schalten sich nach einem Start selbst aus. Bearbeite `settings.json` nur, während der Server gestoppt ist, siehe [Mod-Einstellungen](banksystem/settings.md#the-settings-file).

## Spieler können ein Item nicht in die Bank legen { #players-cant-put-an-item-into-the-bank }

| Ursache | Lösung |
|---|---|
| Das Item ist nicht zugelassen. | Lass es in den [Bank Einstellungen](banksystem/bankable-items.md) zu. |
| Das Item ist beschädigt oder verzaubert. | Solche Items können nicht eingezahlt werden. Der Spieler muss es reparieren oder die Verzauberung entfernen. |
| Das Item ist umbenannt oder trägt andere zusätzliche Daten. | Es ist ein anderes Item als das einfache. Lass genau dieses Item mit `/banksystem allowItemInHand` zu. |
| *Der Zustand von … verhindert das Einlagern in der Bank* | Ein Item mit [Einzahlungsbedingung](banksystem/bankable-items.md#items-whose-data-changes), zum Beispiel altes Essen aus TerraFirmaCraft, ist nicht frisch genug. |
| Das Konto ist eingefroren. | Hebe das Einfrieren auf, siehe [Konten verwalten](banksystem/accounts.md#freezing-an-account). |
| Der Spieler ist auf einem nicht vertrauenswürdigen Slave. | Siehe unten. |

## Probleme auf einem Slave-Server { #problems-on-a-slave-server }

| Problem | Lösung |
|---|---|
| Spieler sehen *Dieser Server ist vom Master nicht vertrauenswürdig eingestuft* und können nur schauen | Führe `/banksystem trust <slave id>` auf dem Master aus. |
| Platzhalter und Bank Anzeigen sind auf einem Server leer | Dieser Slave ist nicht vertrauenswürdig. |
| *Request to the master server failed or timed out* | Der Master war langsam, startete gerade neu oder war nicht erreichbar. Prüfe das Ergebnis, bevor du es erneut versuchst, damit nichts zweimal passiert. |
| Der Slave kann sich nicht verbinden | Prüfe `masterHost`, `masterTcpPort` und `sharedSecret` und ob der Port offen ist. Siehe [Master- und Slave-Server](multi-server.md#troubleshooting). |

## Bildschirme und Befehle { #screens-and-commands }

| Problem | Lösung |
|---|---|
| Ein Admin-Befehl antwortet „nur für Admins“ | Du brauchst das Admin-Flag der Mod: `/banksystem op` oder `/stockmarket op`. Operator zu sein reicht nicht. Siehe [Admins und Berechtigungen](permissions.md). |
| Ein Befehl erscheint nach einer Änderung der Berechtigungen nicht | Tritt dem Server neu bei. |
| Der Knopf **Mod Settings** bzw. **Mod-Einstellungen** fehlt | Er erscheint nur auf dem Master-Server und nur für Spieler mit Operator-Level 2. |
| `/banksystem op`, `deop`, `trust` oder `untrust` schlägt in der Serverkonsole fehl | Diese Befehle brauchen einen Spieler. Gib sie im Spiel ein. |
| Der Betrag eines Spielers bleibt reserviert | Lies [Reservierte Beträge](banksystem/accounts.md#locked-amounts), bevor du ihn freigibst. |

## Verwandte Seiten { #related-pages }

- [Datendateien und Backups](backups.md): ein Backup wiederherstellen.
- [Master- und Slave-Server](multi-server.md): Netzwerkprobleme.
- [Bankfähige Items](banksystem/bankable-items.md): welche Items die Bank annimmt.
