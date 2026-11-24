---
title: "API für Unternehmen, Auszahlungen und Dividenden"
description: "Auszahlungen planen, Dividenden zahlen und das Aktien-Design aus einer anderen Mod lesen."
---

# API für Unternehmen, Auszahlungen und Dividenden { #companies-payouts-and-dividends-api }

Ein Unternehmen in BankSystem besitzt ein Bankkonto und gibt Aktien aus. Spieler richten [Auszahlungen und Dividenden](../../banksystem/payouts.md) im Unternehmensfenster ein. Deine Mod kann dasselbe über zwei Interfaces tun, die nur auf dem Master laufen, und auf dem Client das Aktiensymbol eines Unternehmens zeichnen:

| Interface | Von | Läuft auf |
|---|---|---|
| `IPayoutManager` | `api.getPayoutManager()` | Master |
| `IDividendPayer` | `api.getDividendPayer()` | Master |
| `IBankSystemVisualLookup` | `api.getVisualLookup()` | Client |
| `IShareIconRenderer` | `api.getShareIconRenderer()` | Client |

Die API hat keinen Aufruf, der Unternehmen auflistet. Jedes Unternehmen hat eine Nummer, die das Unternehmensfenster als **Firmen-ID** zeigt (siehe [Ein Unternehmen gründen und führen](../../banksystem/companies.md#overview)). Alle Methoden unten nehmen diese Nummer als `companyId`.

## Auszahlungen { #payouts }

Ein Auszahlungsplan zahlt in festen Abständen einen Betrag vom Unternehmenskonto aus.

```java
IPayoutManager payouts = api.getPayoutManager();
```

Auf einem Slave gibt jede Änderung `NOT_MASTER` zurück und jeder Lesezugriff eine leere Liste oder ein Future mit einer leeren Liste oder `0`. Es gibt keine asynchrone Variante: Ruf es aus Code auf, der auf dem Master läuft.

### Einen Plan anlegen { #creating-a-schedule }

```java
CreateOutcome created = payouts.createSchedule(
        companyId,
        workerUuid,                        // target player
        2500L,                             // raw amount: 25.00
        20L * 60 * 20,                     // interval in ticks: 20 minutes
        PayoutExecutor.getLastObservedTick(), // now, on the payout clock
        managerUuid,                       // who created it, or null
        PayoutSchedule.NO_TARGET_ACCOUNT,  // -1 = the target's personal account
        "Worker", "",                      // names shown in the screen
        PayoutSchedule.Mode.FIXED_PAYOUT,
        PayoutSchedule.MONEY_CURRENCY);    // 0 = money
if (created.result() == IPayoutManager.OpResult.OK) {
    long scheduleId = created.scheduleId();
}
```

| Parameter | Bedeutung |
|---|---|
| `target` | Der Spieler, der die Auszahlung bekommt. Pflicht für `FIXED_PAYOUT`. Setz ihn auch für `ONE_TIME`: Ein `ONE_TIME` ohne Ziel wird nicht abgelehnt, aber jede Ausführung schlägt fehl und wird jede Sekunde wiederholt. Darf für `DIVIDEND` `null` sein. |
| `amount` | Rohbetrag pro Ausführung (100 = 1.00), größer als `0`. |
| `intervalTicks` | Ticks zwischen den Ausführungen, mindestens `20` (eine Sekunde). |
| `nowTick` | Der aktuelle Tick der Auszahlungsuhr: Übergib `PayoutExecutor.getLastObservedTick()` (in `net.kroia.banksystem.banking.company`). Die erste Ausführung kommt `intervalTicks` danach. Übergib nicht `server.getTickCount()`: Die Pläne laufen auf einem eigenen Zähler von BankSystem, der davon abweichen kann. |
| `createdBy` | Wer den Plan angelegt hat, oder `null`. |
| `targetAccountNr` | Ein bestimmtes Konto des Ziels oder `-1` (`NO_TARGET_ACCOUNT`) für sein persönliches Konto. Für ein bestimmtes Konto braucht das Ziel darauf das Recht zum Einzahlen. |
| `targetPlayerName`, `targetAccountName` | Namen, die das Unternehmensfenster zeigt, solange sich der Spieler oder das Konto nicht nachschlagen lässt. |
| `mode` | Siehe unten. |
| `currencyItem` | Short-ID des ausgezahlten Items; `0` (`MONEY_CURRENCY`) = Geld. Das Unternehmenskonto braucht eine Bank für dieses Item. |

Die Kurzform `createSchedule(companyId, target, amount, intervalTicks, nowTick, createdBy)` legt eine `FIXED_PAYOUT` in Geld an das persönliche Konto des Ziels an.

| `PayoutSchedule.Mode` | Was eine Ausführung tut |
|---|---|
| `FIXED_PAYOUT` | Zahlt `amount` an das Ziel. Der Standard. |
| `DIVIDEND` | Verteilt `amount` als Gesamtbetrag auf alle Aktionäre, nach den Aktien, die sie in diesem Moment halten. |
| `ONE_TIME` | Zahlt `amount` einmal an das Ziel und entfernt sich dann selbst. Eine fehlgeschlagene Ausführung wird eine Sekunde später wiederholt. |

Auszahlungen werden einmal pro Sekunde geprüft. Nach einem Serverneustart beginnt jeder Plan ab diesem Moment ein volles Intervall.

### Pläne ändern und entfernen { #changing-and-removing-schedules }

| Methode | Rückgabewert | Was sie tut |
|---|---|---|
| `updateSchedule(companyId, scheduleId, newAmount, newIntervalTicks)` | `OpResult` | Ändert Betrag und Intervall. Es gelten dieselben Grenzen wie beim Anlegen. |
| `updateScheduleEx(companyId, scheduleId, newAmount, newIntervalTicks, nowTick, newTarget, newTargetAccountNr, newTargetPlayerName, newTargetAccountName, newMode, newCurrencyItem)` | `OpResult` | Ändert alles. |
| `pauseSchedule(companyId, scheduleId, boolean paused)` | `OpResult` | Pausiert den Plan oder setzt ihn fort. Ein pausierter Plan läuft nicht und sammelt keine verpassten Ausführungen an. |
| `deleteSchedule(companyId, scheduleId)` | `OpResult` | Entfernt den Plan. |
| `listSchedulesFor(companyId)` | `List<PayoutSchedule>` | Ein Schnappschuss der Pläne des Unternehmens. |
| `getHistory(scheduleId, limit)` | `CompletableFuture<List<PayoutHistoryRecord>>` | Die letzten Ausführungen, die neueste zuerst. |
| `getTotalPaidForSchedule(scheduleId)` | `CompletableFuture<Long>` | Die Rohsumme aller erfolgreichen Ausführungen. |

`OpResult`: `OK`, `COMPANY_MISSING`, `SCHEDULE_MISSING`, `INVALID_INPUT` (Betrag `0` oder weniger, Intervall unter 20 Ticks oder eine `FIXED_PAYOUT` ohne Ziel) oder `NOT_MASTER`.

`PayoutSchedule` (in `net.kroia.banksystem.banking.company`) hat Getter für jedes Feld: `getScheduleId()`, `getTargetUUID()`, `getAmount()`, `getIntervalTicks()`, `getNextRunTick()`, `isPaused()`, `getMode()`, `getCurrencyItem()`, `getTargetAccountNr()`, `getMissedAmount()` und `getMissedCount()` (fehlgeschlagene Ausführungen, die noch nicht nachgezahlt sind), `isPausedByCurrencyBan()` (pausiert, weil ein Admin sein Item verboten hat; erlaubt er das Item wieder, läuft der Plan weiter) und weitere.

### Ergebnisse einer Ausführung { #results-of-a-run }

Jede Ausführung schreibt einen `PayoutHistoryRecord` und löst [`getPayoutExecutedEvent()`](events.md#payouts-and-dividends) mit dem Status aus, auch wenn sie fehlschlägt. Eine erfolgreiche Ausführung schreibt ein Paar `PAYOUT`-Einträge (bei Dividendenplänen `DIVIDEND`) mit der Firmen-ID ins Transaktionsbuch. Die Status stehen unter [Events und Signale](events.md#payouts-and-dividends).

## Eine Dividende zahlen { #paying-a-dividend }

`IDividendPayer` zahlt sofort eine Dividende, wie **Dividende auszahlen** im Unternehmensfenster.

```java
PayDividendResult result = api.getDividendPayer().payDividend(
        companyId,
        50L,                             // raw amount per share: 0.50
        false,                           // includeCompanyAccount, see below
        playerUuid,                      // who paid it, or null
        PayoutSchedule.MONEY_CURRENCY);  // 0 = money, or the short id of an item
if (result.success()) {
    long total = result.totalPaid();     // raw
    int holders = result.holderCount();
}
```

Die Regeln:

- **Alles oder nichts, vorab geprüft.** Kann der freie Kontostand des Unternehmens nicht jeden Aktionär voll bezahlen, bekommt niemand etwas, und nichts ändert sich. Schlägt nach dieser Prüfung trotzdem eine einzelne Überweisung fehl (selten), wird dieser Aktionär übersprungen, und die anderen werden bezahlt. `totalPaid()` und `holderCount()` zeigen, was wirklich gezahlt wurde.
- **Nur ganze Aktien in Bankkonten zählen**, freie und reservierte, von jedem Aktien-Item des Unternehmens. Jeder Aktionär bekommt seine Anzahl ganzer Aktien × `amountPerShare`; wer weniger als eine Aktie hält, bekommt nichts.
- **Das Unternehmen zahlt nie an sich selbst.** Sein eigenes Konto wird immer ausgelassen; `includeCompanyAccount` hat keine Wirkung.
- **Nur der freie Kontostand des Unternehmens zahlt.** Reserviertes Geld zählt nicht.
- **`actor` wird nicht geprüft.** Er wird in die `DIVIDEND`-Einträge im Transaktionsbuch geschrieben. Löst ein Spieler die Dividende in deiner Mod aus, prüfe seine Rechte am Unternehmen selbst.

Eine erfolgreiche Dividende löst [`getDividendPaidEvent()`](events.md#payouts-and-dividends) aus.

| `PayDividendResult.Reason` | Bedeutung |
|---|---|
| `OK` | Gezahlt. |
| `NOT_MASTER` | Auf einem Slave aufgerufen. |
| `COMPANY_MISSING` | Es gibt kein Unternehmen mit dieser ID. |
| `INVALID_INPUT` | `amountPerShare` ist `0` oder weniger, oder die Summe ist zu groß. |
| `NO_SHARES` | Niemand sonst hält Aktien in einem Bankkonto. |
| `INSUFFICIENT_FUNDS` | Der freie Kontostand deckt die Summe nicht. Bei Geld auch, wenn das Unternehmenskonto keine Geld-Bank hat. |
| `CURRENCY_ITEM_MISSING` | Das Unternehmenskonto hat keine Bank für das Item, oder `currencyItem` ist `Company.CURRENCY_UNSET` (keine Währung gesetzt). |
| `ACCOUNT_FROZEN` | Das Unternehmenskonto ist eingefroren. |
| `SHARES_UNDER_REVIEW` | In Bankkonten liegen mehr Aktien, als das Unternehmen geprägt hat. Dividenden ruhen, bis ein Admin das bestätigt, siehe [Integrität der Aktien](../../admin/banksystem/companies.md#share-integrity). |
| `INTERNAL` | Etwas anderes ist schiefgegangen; sieh im Server-Log nach. |
| `NO_PERMISSION` | Wird von `payDividend` nicht zurückgegeben. |

## Aktien-Design auf dem Client { #share-visuals-on-the-client }

Jedes Unternehmen gestaltet seine Aktie: ein Hintergrund- und ein Vordergrundsymbol, jeweils mit einer Farbe (siehe [Die Aktie gestalten](../../banksystem/shares.md#designing-the-share)). Mit zwei Client-Interfaces kann deine Mod sie anzeigen.

### Das Design lesen { #reading-the-visuals }

```java
ShareVisuals v = api.getVisualLookup().getShareVisuals(itemId);
if (v != null) {
    Component name = v.displayName();
    long issued = v.totalSharesIssued();
}
```

Ruf es auf dem Client-Thread auf. Es blockiert nie. Es gibt `null` zurück, wenn das Item keine Unternehmensaktie ist oder wenn das Design diesen Client noch nicht erreicht hat. In diesem Fall fragt es beim Server an, und du bekommst es bei einem späteren Aufruf; frag also im nächsten Frame erneut. Auf einem dedizierten Server gibt es immer `null` zurück.

| `ShareVisuals` | Bedeutung |
|---|---|
| `bgSymbolId()`, `bgTint()` | ID des Hintergrundsymbols und seine ARGB-Farbe. Die ID ist leer, wenn nichts gesetzt ist. |
| `fgSymbolId()`, `fgTint()` | ID des Vordergrundsymbols und seine ARGB-Farbe. |
| `displayName()` | Der Unternehmensname; leer, wenn nicht gesetzt. |
| `description()` | Die Unternehmensbeschreibung; leer, wenn nicht gesetzt. |
| `totalSharesIssued()` | Die Aktien, die gerade ausgegeben sind. |
| `maxSupply()` | Das Aktienlimit, das bei der Gründung des Unternehmens festgelegt wurde; `0` = kein Limit. |

### Das Symbol zeichnen { #drawing-the-icon }

```java
IShareIconRenderer renderer = api.getShareIconRenderer();
if (renderer != null) renderer.renderInto(guiGraphics, x, y, 16, 16, itemId);
else guiGraphics.renderItem(stack, x, y); // fall back to the normal item icon
```

`renderInto(gfx, x, y, w, h, itemId)` zeichnet das farbige Aktiensymbol in ein beliebiges Rechteck auf dem Bildschirm. Ruf es auf dem Render-Thread auf. Ist das Item keine Unternehmensaktie, zeichnet es nichts. Ist das Design noch nicht da, zeichnet es einen Platzhalter, bis es ankommt; ruf es also weiter in jedem Frame auf. `getShareIconRenderer()` gibt auf einem dedizierten Server `null` zurück, ebenso solange noch kein Renderer bereit ist.

## Verwandte Seiten { #related-pages }

- [Events und Signale](events.md): die Events für Auszahlungen und Dividenden.
- [BankSystem-API](api.md): Konten und Banken eines Unternehmens.
- [Auszahlungen und Dividenden](../../banksystem/payouts.md): dieselben Funktionen für Spieler.
- [Transaktionsbuch](transaction-ledger.md): die `PAYOUT`- und `DIVIDEND`-Einträge.
