---
title: "Admins und Berechtigungen"
description: "Der Admin-Modus von StockMarket und BankSystem, Operator-Level sowie die LuckPerms-Nodes und Optionen zur Synchronisierung."
---

# Admins und Berechtigungen { #admins-and-permissions }

Jede Mod hat ihr eigenes **Admin-Flag**, getrennt vom Operator-Status in Minecraft. Das Flag entscheidet, wer die Admin-Bildschirme öffnen und die Daten anderer Spieler bearbeiten kann. Operator-Level und Berechtigungs-Nodes entscheiden, wer das Flag vergeben darf.

## Jemanden zum Admin machen { #making-someone-admin }

| Befehl | Was er tut |
|---|---|
| `/banksystem op [player]` | Gibt dem Spieler oder dir das Admin-Flag von BankSystem. |
| `/banksystem deop [player]` | Nimmt es wieder weg. |
| `/stockmarket op [player]` | Gibt das Admin-Flag von StockMarket. |
| `/stockmarket deop [player]` | Nimmt es wieder weg. |

Diese Befehle brauchen Operator-Level 2 oder den passenden Berechtigungs-Node unten. Gib sie im Spiel ein: Die Befehle von BankSystem funktionieren nicht in der Serverkonsole. Sie funktionieren nur auf dem Master-Server eines [Netzwerks](multi-server.md). Die Flags werden dort gespeichert, also gelten sie auf jedem Server.

Ein Operator ohne das Flag ist kein Admin: Er kann sich das Flag selbst geben, aber bis dahin kann er weder die Konten anderer Spieler noch die Marktverwaltung öffnen.

## Was jedes Flag erlaubt { #what-each-flag-allows }

**Admins von BankSystem** können:

- die bankfähigen Items auswählen und, mit Operator-Level 2, die [Mod-Einstellungen](banksystem/settings.md) ändern;
- jedes Konto öffnen, bearbeiten und einfrieren;
- jedes Unternehmen verwalten;
- den Audit-Bildschirm, die Kontostandverläufe und die Berichte verwenden;
- die [Chat-Alarme](audit/alerts.md) erhalten.

**Admins von StockMarket** können:

- im Verwaltungsbildschirm (`/stockmarket manage`) Märkte anlegen, ändern und entfernen;
- Voreinstellungen verwenden, Märkte öffnen und schließen und die Admin-Befehle für News ausführen;
- die [Mod-Einstellungen](stockmarket/mod-settings.md) von StockMarket ändern.

Die meisten Admin-Befehle beider Mods sind für jeden Spieler sichtbar, laufen aber nur für einen Spieler mit dem Flag. Alle anderen bekommen eine Meldung „nur für Admins“.

## Ohne Berechtigungs-Mod { #without-a-permission-mod }

Jeder Berechtigungs-Node fällt auf ein Operator-Level zurück:

- Befehle, die das Flag setzen, Daten sichern oder Servern vertrauen, brauchen **Operator-Level 2**.
- Befehle, die nur das Admin-Flag brauchen, lassen jeden Spieler durch, und das Flag entscheidet.
- Die Konsole und Befehlsblöcke verwenden immer Operator-Level 2.

## Berechtigungs-Nodes { #permission-nodes }

Mit LuckPerms (oder einer anderen Berechtigungs-Mod) kannst du jeden Node pro Spieler oder Gruppe erlauben oder verweigern. Nodes werden nur für Spieler auf dem Server geprüft, der die Prüfung ausführt.

### BankSystem { #banksystem }

| Node | Erlaubt |
|---|---|
| `banksystem.admin.command.op` | `/banksystem op` und `deop` |
| `banksystem.admin.adminmode` | Das Admin-Flag eines Spielers ändern, wenn eine andere Mod das auf einem Slave-Server verlangt. `/banksystem op` verwendet diesen Node nicht. |
| `banksystem.admin.command.trust` | `/banksystem trust` und `untrust` |
| `banksystem.admin.command.backup` | `/banksystem backup …` |
| `banksystem.admin.command.symbols` | `/banksystem symbols …` (braucht auch das Admin-Flag) |
| `banksystem.admin.command.restorebinding` | `/banksystem restorebinding` (braucht auch das Admin-Flag) |
| `banksystem.admin.software` | Die Banking Software an einem anderen Spieler verwenden. Braucht auch das Admin-Flag und den Kreativmodus. |
| `banksystem.admin` | Das Admin-Flag selbst, solange die LuckPerms-Synchronisierung an ist (siehe unten) |

### StockMarket { #stockmarket }

| Node | Erlaubt |
|---|---|
| `stockmarket.admin.command.op` | `/stockmarket op` und `deop` |
| `stockmarket.admin.command.manage` | `/stockmarket manage` (braucht auch das Admin-Flag) |
| `stockmarket.admin.command.preset` | `/stockmarket preset …` (braucht auch das Admin-Flag) |
| `stockmarket.admin.command.news` | Die Admin-Befehle für News (braucht auch das Admin-Flag) |
| `stockmarket.admin.command.market` | `/stockmarket open`, `close` und `<market> remove` (braucht auch das Admin-Flag) |
| `stockmarket.admin.command.backup` | `/stockmarket backup …` |
| `stockmarket.admin.notify` | [Alarme](audit/alerts.md) von StockMarket im Chat, Hinweise, wenn ein anderer Admin Einstellungen ändert, und `/stockmarket alerts` |
| `stockmarket.admin` | Das Admin-Flag selbst, solange die LuckPerms-Synchronisierung an ist (siehe unten) |

Nodes mit dem Hinweis „(braucht auch das Admin-Flag)“ stehen standardmäßig jedem Spieler offen. Du kannst sie nur verwenden, um einen Befehl wegzunehmen: Setze den Node auf `false`, um den Befehl auszublenden, sogar für einen Admin. `banksystem.admin.software` ist anders: Ohne Berechtigungs-Mod braucht er Operator-Level 2.

Die Discord-Befehle beider Mods verwenden den Node `modutilities.command.discord`, der ohne Berechtigungs-Mod Operator-Level 3 braucht.

So gibst du einer Gruppe alle Admin-Rechte beider Mods:

```text
/lp group admin permission set banksystem.admin.* true
/lp group admin permission set stockmarket.admin.* true
```

Ein Spieler, dessen Nodes sich geändert haben, muss eventuell neu beitreten, bevor Befehle erscheinen oder verschwinden.

## Das Admin-Flag mit LuckPerms synchronisieren { #syncing-the-admin-flag-with-luckperms }

Schalte **Admin-Flag mit LuckPerms synchronisieren** in der Gruppe Integrationen der Mod-Einstellungen jeder Mod ein ([BankSystem](banksystem/settings.md#integrations), [StockMarket](stockmarket/mod-settings.md)). Dann werden das Admin-Flag und der Node `banksystem.admin` (bzw. `stockmarket.admin`) in beide Richtungen gleich gehalten:

- `/banksystem op <player>` setzt den Node auch in LuckPerms, sogar für Spieler, die offline sind. `deop` entfernt den eigenen Node des Spielers.
- Wenn du den Node in LuckPerms erteilst oder entfernst, auch über eine Gruppe, ändert sich das Flag sofort.
- Eine Gruppe hat Vorrang: Wenn eine Gruppe den Node noch erteilt, bleibt der Spieler nach `deop` Admin, und der Befehl sagt dir das.
- Wenn du die Synchronisierung zum ersten Mal einschaltest, bekommt jeder bestehende Admin einmal den Node. Es wird nichts entfernt.

!!! note "Die Wildcard enthält das Flag nicht"
    `banksystem.admin.*` erteilt nicht `banksystem.admin` selbst. Erteile diesen Node einzeln, um eine Gruppe zum Admin zu machen.

In einem Netzwerk schaltest du die Synchronisierung auf dem Master ein. Slave-Server geben Änderungen in LuckPerms nur dann an den Master weiter, wenn der Master ihnen [vertraut](multi-server.md#trusted-slaves). Für BankSystem braucht außerdem jeder Slave die Synchronisierung in seiner eigenen Datei: Stoppe den Slave und setze `SYNC_ADMIN_FLAG_WITH_PERMISSION` in seiner `settings.json` auf `true`. Der Bildschirm Mod Settings kann die Datei eines Slaves nicht ändern. Die Synchronisierung von StockMarket braucht einen Neustart des Masters, nachdem du sie eingeschaltet hast.

## Verwandte Seiten { #related-pages }

- [Admin-Befehle](commands.md): jeder Befehl und der Node, den er braucht.
- [Master- und Slave-Server](multi-server.md): Slave-Servern vertrauen.
- [Installation und Updates](install.md): LuckPerms-Versionen, die funktionieren.
