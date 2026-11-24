---
title: "Default events"
description: "The list of shipped news events with their headlines and affected markets."
---

# Default events

StockMarket ships 73 news events. On the first start they are written to `config/StockMarket/news/DefaultEvents/`, one file per event, each with a picture in `pictures/`. Every event has its texts in English, German and Simplified Chinese. To change or switch off one of them, see [Changing a shipped event](config-files.md#changing-a-shipped-event).

## Reading the tables

The events are grouped by their `category`. For each event:

- **Headline:** the English headline.
- **ID:** the event's `id`, for the commands and your own chains and requirements.
- **Markets:** the items it moves. `#` marks a tag, `*` a pattern, see [Markets](event-reference.md#markets). A number after `×` is the `weightFactor`. A negative one moves that market the other way.
- **Effect:** the peak as written in the file, and the event type: `shock` (fast up, slow fade), `trend` (slow up and down) or `crash` (fast move, long recovery). *permanent* means the change stays. *story* means the event has several steps, with the names of its variants.

The peaks are the values in the files. The shipped [scheduler.json](config-files.md#schedulerjson) halves every effect and makes every event three times as long, so a `+40%` event moves the price by about 20% in play.

Notes under the effect mean:

- *admin only:* never fires at random, only by `trigger`.
- *requirements:* only fires when earlier events allow it, see [Requirements](advanced-events.md#requirements).
- *chain:* can start a follow-up event.
- *weight 0:* only starts as a follow-up or by `trigger`.
- *news before / after the price moves:* the event has an announce delay.

## The events

### Commodities (26)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Diamond rush in the northern mountains! | `diamond_rush` | `diamond`, `diamond_block`, `#c:ores` ×0.3, `emerald` ×−0.4 | −35% trend<br>news before the price moves |
| Mine collapse halts iron production! | `iron_supply_disruption` | `iron_ingot`, `iron_block`, `raw_iron` ×0.8 | +45% shock |
| Leaked: expedition secures massive ancient debris hoard | `netherite_insider_leak` | `netherite_ingot`, `netherite_scrap` ×0.8, `ancient_debris` ×0.8 | −30% shock<br>news after the price moves |
| Harvest festival drives up grain demand! | `wheat_harvest_festival` | `wheat`, `bread` ×0.6 | +22% trend |
| Bee colonies boom - honey floods the market | `honey_bumper_season` | `honey_bottle`, `honeycomb` ×0.8, `sweet_berries` ×0.5 | −22% trend |
| Massive copper seam opened in coastal cliffs! | `copper_seam_discovery` | `copper_ingot`, `copper_block`, `raw_copper` ×0.8 | −25%, permanent |
| Nether quartz glut buries the market! | `nether_quartz_glut` | `quartz`, `quartz_block` ×0.8 | −28% trend |
| Colossal geode cracked open - amethyst everywhere! | `amethyst_geode_discovery` | `amethyst_shard` | −30%, permanent |
| Glowstone farms flood the market with light! | `glowstone_farm_boom` | `glowstone_dust`, `glowstone` ×0.8 | −25% trend |
| Ocean monument stripped bare - prismarine floods in! | `prismarine_monument_raid` | `prismarine_shard`, `prismarine_crystals` ×0.9, `prismarine` ×0.6 | −35% shock |
| Dripstone the new fashion in grand halls! | `dripstone_cavern_rush` | `dripstone_block`, `pointed_dripstone` ×0.7 | +28% trend |
| Bumper summer floods the market with melons | `melon_summer_glut` | `melon_slice`, `melon` ×0.7 | −22% trend |
| Southern trade route opens the cocoa floodgates | `cocoa_trade_route_opens` | `cocoa_beans` | −28% trend |
| Foraging craze sends mushroom prices soaring | `mushroom_foraging_craze` | `red_mushroom`, `brown_mushroom`, `mushroom_stew` ×0.6, `bread` ×−0.2 | +24% trend |
| Brewers empty the nether wart stocks! | `netherwart_brewing_shortage` | `nether_wart`, `sugar` ×−0.2, `glowstone_dust` ×−0.15 | +42% shock |
| Record beetroot harvest weighs on prices | `beetroot_harvest_surplus` | `beetroot`, `beetroot_soup` ×0.6 | −20% trend |
| Spring shearing floods the wool market | `spring_shearing_glut` | `string` ×0.5, `#minecraft:wool`, `leather` ×−0.3 | −24% trend |
| Great salmon run fills the nets | `salmon_spawning_run` | `salmon`, `cooked_salmon` ×0.6 | −25% trend |
| Alchemists' guild empties the blaze-rod stalls! | `blaze_rod_brewing_rush` | `blaze_rod`, `blaze_powder` ×0.7 | +32% trend |
| Expedition fever drives ender-pearl demand sky-high | `ender_pearl_expedition_boom` | `ender_pearl`, `ender_eye` ×0.6 | +28% trend |
| Apothecaries bid up ghast tears for healing tonics! | `ghast_tear_apothecary_craze` | `ghast_tear` | +40% shock |
| End raids stall - shulker shells scarce for good | `shulker_shell_shortage` | `shulker_shell` | +30%, permanent |
| Outer islands yield a chorus-fruit glut | `chorus_fruit_bumper_harvest` | `chorus_fruit`, `popped_chorus_fruit` ×0.7 | −25% trend |
| Fire-resistance brewing drives magma-cream demand | `magma_cream_alchemy_demand` | `magma_cream` | +26% trend |
| Rush to repair elytra empties membrane stocks | `phantom_membrane_repair_run` | `phantom_membrane` | +30% trend |
| Triumphant End expedition floods the market with relics! | `end_expedition_returns` | `elytra`, `dragon_breath` ×0.6 | −40% crash<br>requirements |

### Markets (3)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Ore bubble bursts - mining stocks in free fall! | `ore_market_crash` | `*_ore`, `raw_*` ×0.7 | −50% crash |
| Black-dye trade collapses as fashion turns pale | `ink_dye_market_crash` | `ink_sac`, `black_dye` ×0.8, `white_dye` ×−0.3 | −40% crash |
| Margin calls wipe out overleveraged traders in a cascade! | `margin_call_crash` | `diamond`, `emerald` ×0.8, `gold_ingot` ×0.6 | −45% crash<br>requirements; weight 0 |

### Politics (7)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Trade council adopts the gold standard! | `gold_reserve_standard` | `gold_ingot` | +25%, permanent<br>requirements; chain → `gold_rush_rumor` |
| Trade council abandons the gold standard! | `end_of_gold_standard` | `gold_ingot` | −20%, permanent<br>requirements |
| Trade council signs sweeping import tariff treaty | `import_tariff_treaty` | `iron_ingot`, `gold_ingot` ×0.8 | +18%, permanent<br>requirements |
| The mint recoins the realm's currency! | `mint_recoinage_reform` | `gold_ingot`, `iron_ingot` ×0.6 | +28%, permanent<br>requirements |
| Trade council embargoes all foreign metals! | `metals_export_embargo` | `iron_ingot`, `copper_ingot` ×0.8, `gold_ingot` ×0.6 | +24%, permanent |
| Council levies steep luxury tax on gems and gold | `luxury_goods_tax` | `diamond`, `emerald` ×0.8, `gold_ingot` ×0.6 | −20%, permanent<br>requirements |
| Council scraps the luxury tax on gems and gold | `luxury_tax_repealed` | `diamond`, `emerald` ×0.8, `gold_ingot` ×0.6 | +22%, permanent<br>requirements; undoes `luxury_goods_tax` |

### Rumors (3)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Rumors of a massive gold strike sweep the trading floor! | `gold_rush_rumor` | `gold_ingot` | story: `pump_and_dump` or `fizzle` |
| Speculators pile into amethyst on wild rumors! | `amethyst_speculation` | `amethyst_shard` | story: `pump_and_dump` or `fizzle` |
| Speculative mania grips the trading floor! | `speculation_mania` | `diamond`, `emerald` ×0.8, `gold_ingot` ×0.6 | story: `euphoria` or `cooler_heads`<br>chain → `margin_call_crash` |

### Crime (4)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Counterfeit emeralds flood the market! | `emerald_counterfeit_scandal` | `emerald`, `emerald_block` | −40% crash<br>admin only |
| Cartel corners quartz supply - prices squeezed! | `quartz_cartel_squeeze` | `quartz` | +45% shock<br>admin only |
| Counterfeit gold coin floods the market - trust collapses! | `counterfeit_coin_scandal` | `gold_ingot` | −42% crash<br>admin only |
| Daring vault heist empties the gem exchange! | `gemstone_heist` | `diamond`, `emerald` ×0.8 | +40% shock<br>news after the price moves |

### Technology (2)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Engineering breakthrough doubles redstone efficiency! | `redstone_breakthrough` | `redstone` | +30% trend<br>news before the price moves |
| Enchanting craze sends lapis demand soaring! | `lapis_enchanting_craze` | `lapis_lazuli`, `lapis_block` ×0.8 | +30% trend<br>news before the price moves |

### Economy (5)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Construction boom drives lumber demand to record highs | `lumber_construction_boom` | `#minecraft:logs`, `*_planks` ×0.6, `stone` ×−0.15 | +35% trend |
| Deep quarry opens - deepslate cheap for good | `deepslate_quarry_expansion` | `cobbled_deepslate`, `deepslate` ×0.8 | −20%, permanent |
| New river plantations turn sugar cane cheap for good | `sugarcane_plantation_boom` | `sugar_cane`, `sugar` ×0.8, `paper` ×0.4 | −25%, permanent |
| New tanneries drive a run on leather | `leather_tannery_boom` | `leather`, `#minecraft:wool` ×−0.25 | +30% trend |
| Royal treasury floods the market with fresh coin | `treasury_stimulus_windfall` | `diamond`, `gold_ingot` ×0.8, `emerald` ×0.8, `iron_ingot` ×0.6 | +30% trend<br>news before the price moves |

### Disaster (8)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Locust swarm ravages farmland - staple crops in short supply! | `crop_pest_outbreak` | `wheat`, `potato` ×0.9, `carrot` ×0.9, `bread` ×0.5 | +38% shock |
| Volcano erupts - villages fortify against ashfall! | `volcanic_eruption` | `obsidian`, `basalt` ×0.8, `blackstone` ×0.7 | +48% shock<br>admin only |
| Wildfires sweep the taiga - lumber prices spike! | `great_forest_fire` | `#minecraft:logs`, `*_planks` ×0.6 | story: `wildfire`<br>chain → `great_forest_fire_recovery` |
| Blight returns to the potato fields! | `potato_blight_return` | `potato`, `baked_potato` ×0.6 | +40% shock |
| Great drought scorches the croplands! | `great_drought` | `wheat`, `potato` ×0.9, `carrot` ×0.9, `beetroot` ×0.8 | +40% shock<br>chain → `grain_relief_convoy` |
| Cattle plague fells the herds - meat and hides grow scarce! | `cattle_plague_outbreak` | `beef`, `milk_bucket` ×0.7, `leather` ×0.5 | +42% shock<br>admin only |
| Overfishing collapses the cod grounds for good | `cod_overfishing_crisis` | `cod`, `cooked_cod` ×0.6 | +30%, permanent |
| Henhouse fire wipes out laying flocks - eggs vanish! | `henhouse_fire_egg_shortage` | `egg` | +40% shock<br>news after the price moves |

### Labor (2)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Coal miners walk out - furnaces run cold! | `coal_miners_strike` | `#minecraft:coals` | +36% shock |
| Dockworkers walk out - harbor cranes fall silent! | `dockworkers_strike` | `iron_ingot`, `copper_ingot` ×0.8, `#minecraft:planks` ×0.4 | +40% shock |

### Recovery (2)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Disaster relief planks flood the lumber market | `great_forest_fire_recovery` | `#minecraft:logs`, `*_planks` ×0.6 | −18% trend<br>requirements |
| Relief caravans pour grain into the stricken markets | `grain_relief_convoy` | `wheat`, `potato` ×0.9, `carrot` ×0.9, `beetroot` ×0.8 | −20% trend<br>requirements; weight 0 |

### Cultural (8)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Winter solstice gifting season lifts sweets and textiles | `winter_solstice_gifting` | `cake`, `cookie` ×0.8, `#minecraft:wool` ×0.5 | +28% trend<br>chain → `post_solstice_slump` |
| After the solstice: gift-market demand collapses | `post_solstice_slump` | `cake`, `cookie` ×0.8, `#minecraft:wool` ×0.5 | −28% crash |
| Tuff-and-calcite facades sweep the townhouses | `tuff_facade_fashion` | `tuff`, `calcite` ×0.8, `cobblestone` ×−0.15 | +30% trend |
| Autumn festival lifts the pumpkin trade! | `pumpkin_autumn_festival` | `pumpkin`, `pumpkin_pie` ×0.7, `carved_pumpkin` ×0.5, `cake` ×−0.15 | +25% trend |
| Aquarium fad grips the wealthy | `tropical_fish_aquarium_fad` | `tropical_fish` | +32% trend |
| Winter craze for rabbit stew empties the warrens | `rabbit_stew_winter_craze` | `rabbit`, `cooked_rabbit` ×0.7, `rabbit_hide` ×0.4, `mutton` ×−0.25 | +30% trend |
| Respawn anchors become the must-have - crying obsidian soars | `crying_obsidian_anchor_fad` | `crying_obsidian`, `*_bed` ×−0.15 | +28% trend |
| Court adopts royal purple - dye prices soar! | `royal_purple_fashion` | `purple_dye`, `magenta_dye` ×0.7, `pink_dye` ×0.5 | +30% trend |

### Conflict (3)

| Headline | ID | Markets | Effect |
|---|---|---|---|
| Kingdoms race to build redstone defenses | `redstone_arms_race` | `redstone`, `iron_ingot` ×0.5 | story: `escalation` or `brief_scare` |
| Archery muster empties the fletchers' feather stores | `fletcher_feather_demand` | `feather` | +28% trend |
| Warlord posts a bounty on wither skulls! | `wither_skull_bounty` | `wither_skeleton_skull`, `soul_sand` ×0.4 | +45% shock<br>admin only |

## Storylines

Some events belong together:

| Story | Events |
|---|---|
| Gold standard | `gold_reserve_standard` raises gold for good and can start `gold_rush_rumor`. At least 3 hours later, `end_of_gold_standard` can lower it again. Each happens once per world. |
| Luxury tax | `luxury_goods_tax` lowers gems and gold for good. At least two days later, `luxury_tax_repealed` takes the change back exactly. Then the tax can come again. |
| Forest fire | `great_forest_fire` drives lumber up in five steps. When it ends, there is a 70% chance that `great_forest_fire_recovery` makes lumber cheap. |
| Drought | `great_drought` drives crops up. When it ends, there is a 70% chance that `grain_relief_convoy` brings prices down. |
| Winter solstice | `winter_solstice_gifting` lifts sweets and wool. When it ends, there is a 60% chance that `post_solstice_slump` drops the same markets. |
| Speculation | `speculation_mania` pumps gems and gold. When it ends, there is a 60% chance that `margin_call_crash` follows. |

The `requires` and `chains` of each event are in its file. How they work is on [Advanced events](advanced-events.md).

## Events that never fire at random

Six events are admin only: `emerald_counterfeit_scandal`, `volcanic_eruption`, `quartz_cartel_squeeze`, `cattle_plague_outbreak`, `wither_skull_bounty` and `counterfeit_coin_scandal`. They are strong events for server stories. Start them with `/stockmarket news trigger <eventId>`, or set `adminOnly` to `false` in their file to let them fire at random.

## Related pages

- [Event file reference](event-reference.md): what each field means.
- [Advanced events](advanced-events.md): sequences, requirements and chains.
- [News commands](commands.md): trigger, enable and disable events.
- [News config files](config-files.md): where the files are and how they update.
