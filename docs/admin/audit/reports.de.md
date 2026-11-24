---
title: "Täglicher Bericht und Berichte"
description: "Der tägliche Audit-Bericht, Berichte auf Abruf mit /banksystem auditreport und die Audit-Log-Dateien."
---

# Täglicher Bericht und Berichte { #daily-digest-and-reports }

BankSystem schreibt einfache Dateien, die du lesen kannst, ohne das Spiel zu starten: ein Log jeder Admin-Aktion und Markierung, eine tägliche Zusammenfassung und Zusammenfassungen auf Abruf. Alle schreibt der Master-Server in

```text
<world>/data/BankSystem/audit/
```

BankSystem löscht diese Dateien nie. Räume sie selbst auf, wenn der Ordner zu groß wird.

## Das Audit-Log { #the-audit-log }

`<yyyy-mm-dd>.log` bekommt eine Zeile pro Ereignis dieses Tages:

- jede Admin-Änderung an einem Konto: Kontostände gesetzt, erhöht oder verringert, Beträge freigegeben, Banken geschlossen, Konten bearbeitet, eingefroren oder aufgetaut;
- Items, die ein Admin zugelassen oder entfernt hat, mit einer zusätzlichen Zeile für jedes Konto, das ein Item verloren hat;
- vergebene oder entzogene BankSystem-Adminrechte sowie Slave-Server, die als vertrauenswürdig eingestuft oder wieder herabgestuft wurden;
- Aktien-Alarme, die mit `/company shares acknowledge` akzeptiert wurden;
- jede [Verdachtsmarkierung](alerts.md).

Jede Zeile enthält die Zeit, was passiert ist, das Konto, das Item und den Betrag und wer es getan hat: Name und UUID eines Spielers, `Console` oder `LuckPerms`, wenn die [LuckPerms-Synchronisation](../permissions.md) ein Admin-Flag geändert hat.

## Der tägliche Bericht { #the-daily-digest }

Beim ersten Server-Tick nach Mitternacht schreibt der Master eine Zusammenfassung des Vortags nach `digest-<yyyy-mm-dd>.md`. Es ist eine Markdown-Datei mit:

- der Geldmenge zu Beginn und am Ende des Tages und der Änderung;
- den Konten, die am meisten Bargeld gewonnen haben;
- jeder Verdachtsmarkierung des Tages;
- der Anzahl der Admin-Aktionen jeder Art und den letzten 20 davon.

Wenn der Server um Mitternacht offline war, schreibt er den Bericht des Vortags beim nächsten Start. Frühere Tage, die er verpasst hat, bekommen keinen Bericht. Ein Bericht, der schon existiert, wird nie neu geschrieben.

| Einstellung | Standard | Was sie bewirkt |
|---|---|---|
| **Täglicher Audit-Bericht** | an | Schreibt den täglichen Bericht. |
| **Bericht: größte Gewinner** | `10` | Wie viele Konten die Liste der Gewinner zeigt, 1 bis 100. |

Beide stehen unter **Verdächtige Aktivität** in den [Mod Settings](../banksystem/settings.md#suspicious-activity).

## Ein Bericht auf Abruf { #a-report-on-demand }

```text
/banksystem auditreport <hours>
```

schreibt dieselbe Zusammenfassung für die letzten 1 bis 720 Stunden nach `digest-<date>_<time>-<hours>h.md` und nennt dir den vollständigen Pfad. Wenn du den Befehl auf einem Slave-Server ausführst, wird der Bericht auf dem Master geschrieben.

Die Bargeldwerte stammen aus dem Kontoverlauf. Für den Bericht muss deshalb **Balance snapshot interval (minutes)** eingeschaltet sein.

## StockMarket { #stockmarket }

StockMarket schreibt seine Alarme ins Server-Log, als Zeilen, die mit `[StockMarket Alert]` beginnen. Der Master speichert außerdem jeden Alarm und den Server, auf dem jede Order platziert wurde, in `<world>/data/StockMarket/Database/stockmarket_diagnostics.db`. Du kannst die Datei mit jedem SQLite-Browser öffnen. Das [Audit Tool](audit-tool.md) liest sie auch.

## Verwandte Seiten { #related-pages }

- [Alarme und Verdachtsmarkierungen](alerts.md): was die Markierungen bedeuten.
- [Im Spiel untersuchen](investigating.md): ein Konto im Audit-Fenster verfolgen.
- [Datendateien und Backups](../backups.md): jede Datendatei beider Mods.
