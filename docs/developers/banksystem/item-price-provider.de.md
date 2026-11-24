---
title: "Item-Preisanbieter"
description: "Item-Preise liefern, damit das Gesamtvermögen aufgezeichnet wird."
---

# Item-Preisanbieter { #item-price-provider }

BankSystem zeichnet den Verlauf des Kontostands jedes Bankkontos auf. Wenn eine Mod BankSystem sagt, was Items wert sind, zeichnet BankSystem auch das **Gesamtvermögen** jedes Kontos auf: Geld plus den Wert aller Items, reservierte eingeschlossen. Spieler sehen es als goldene Linie **Total Wealth** im [Kontostandsverlauf](../../banksystem/bank-terminal.md#balance-history). StockMarket liefert diese Preise aus seinen Märkten.

Ohne Preise gibt es keine Vermögenslinie. Sonst ändert sich nichts.

## Die API { #the-api }

Alle vier Methoden liegen auf `BankSystemAPI`:

| Methode | Was sie tut |
|---|---|
| `setItemPriceProvider(ItemPriceProvider)` | Setzt die Preisabfrage. `null` entfernt sie. |
| `setPriceCurrencyItem(short)` | Setzt das Item, in dem die Preise angegeben sind, als seine Short-ID. |
| `getItemPriceProvider()` | Die aktuelle Preisabfrage oder `null`. |
| `getPriceCurrencyItem()` | Das aktuelle Währungs-Item oder `0`. |

Es gibt nur einen Anbieter. Setzt du einen neuen, ersetzt er den alten.

```java
@FunctionalInterface
public interface ItemPriceProvider {
    long getItemPrice(short itemId);
}
```

`getItemPrice` bekommt die Short-ID eines Items und gibt den Preis **eines Items** in Roh-Geldeinheiten (100 = 1.00) zurück, oder `0`, wenn das Item keinen Preis hat. Für Eisen im Wert von 2.50 gibt sie `250` zurück. BankSystem ruft sie nur auf dem Master auf, auf dem Server-Thread, bei jedem Schnappschuss einmal pro Konto und Item; halte sie also schnell und blockiere nicht. Auf einem Slave hat das Setzen eines Anbieters keine Wirkung.

## Registrieren { #registering }

```java
BankSystemAPI api = BankSystemMod.getAPI();
api.getEvents().getBanksystemSetupCompleteSignal().addListener(() -> {
    api.setItemPriceProvider(itemId -> {
        Market market = findMarket(itemId);       // your lookup by BankSystem short id
        return market == null ? 0 : market.getPriceRaw();
    });
    api.setPriceCurrencyItem(MoneyItem.getItemID().getShort());
});
```

Registriere den Anbieter, nachdem BankSystem mit dem Einrichten fertig ist, zum Beispiel in `getBanksystemSetupCompleteSignal()`. **Du musst den Anbieter und das Währungs-Item setzen.** Ohne Währungs-Item (`0`) zeichnet BankSystem kein Vermögen auf.

Zum Beenden ruf `api.setItemPriceProvider(null)` auf.

## Wie das Vermögen berechnet wird { #how-wealth-is-worked-out }

Bei jedem Kontostand-Schnappschuss, für jedes Konto:

```text
for each bank in the account:
    total = free balance + locked balance
    if the item is money, or the currency item:
        wealth = wealth + total                                    (face value)
    else if price > 0:
        wealth = wealth + total × price / raw units per item
```

- **Geld-Items zählen immer als Bargeld** zum Nennwert, egal welches Währungs-Item du setzt.
- **Roh-Einheiten pro Item** sind `100` bei einer normalen Bank. Bei einem Slot, der an eine [Währungs-Mod](currency-integration.md) gebunden ist, ist es der Wert einer Münze dieser Mod in Roh-Einheiten.
- Items mit Preis `0` tragen nichts bei.

Wie oft Schnappschüsse entstehen, legt **Balance snapshot interval (minutes)** in den [Mod Settings](../../admin/banksystem/settings.md#utilities) fest, standardmäßig 1 Minute. Ein Eintrag wird nur geschrieben, wenn sich der Wert geändert hat oder wenn **Balance snapshot heartbeat (minutes)** abgelaufen ist. Die Vermögenseinträge werden mit der Item-ID `32767` (`BalanceHistoryRecord.WEALTH_ITEM_ID`) gespeichert.

!!! note "Deine Preise fließen in eine Verdachtsprüfung ein"
    Die Vermögenslinie wird auch für die Markierung `WEALTH_JUMP` genutzt: Wächst das Vermögen eines Kontos in kurzer Zeit stark, bekommen Admins einen Alarm. Ein plötzlicher Preissprung in deiner Mod kann sie auslösen. Ohne Anbieter wird diese Markierung nie gesetzt. Siehe [Transaktionsbuch](transaction-ledger.md#suspicion-flags).

## Item-IDs { #item-ids }

BankSystem gibt jedem Item eine `short`-ID. So ordnest du deine eigenen Items diesen IDs zu:

```java
// From an ItemStack (master only; registers the item if it's new)
short id = ItemID.getOrRegisterFromItemStackServerSide_direct(stack).getShort();

// From a known short id
ItemStack stack = new ItemID(id).getStack(); // a copy, or ItemStack.EMPTY if unknown; never null
```

`ItemID` liegt in `net.kroia.banksystem.util`.

## Verwandte Seiten { #related-pages }

- [BankSystem-API](api.md): Rohbeträge und der Einstiegspunkt.
- [Events und Signale](events.md): das oben verwendete Setup-Signal.
- [So arbeiten die beiden Mods zusammen](../../together.md#your-total-wealth-uses-market-prices): was Spieler sehen.
