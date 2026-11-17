# Castora waypoints + full JP / adventure / mini-dungeon sweep

Date: 2026-11-17. Task: Audrey — "Castora DOES have waypoints and such, use the wiki to find their names if you have to, there are four castora maps" — then "there are adventures and mini dungeons and jumping puzzles in castora too. make sure you do a full sweep for every expansion".

**Do NOT rebuild the DLL from this note alone** — a separate UI polish build (hide tags, remove hero points) was in progress. The tags below are merged into `data/tags.json` and validated by `tools/apply_tags.py`; the DLL rebuild picks them up.

## 1. Castora — Audrey was right, it is FOUR maps

Wiki: https://wiki.guildwars2.com/wiki/Castora — "Explorable zones: Shipwreck Strand, Starlit Weald, Eternity's Garden, Leyspring Hollows". Also: https://wiki.guildwars2.com/wiki/Guild_Wars_2:_Visions_of_Eternity — "Four zones, 2 upon launch and 2 with seasonal updates". Tyria Pulse (2026-10-23/24, https://tyriapulse.vercel.app/articles/gw2-janthir-wilds-castora): "Castora: four maps".

### Reconciling "14 across the 5 maps"
The earlier note counted **5 maps** because the API dataset has a 5th Castora map: **Comosus Isle** (homestead instance, 5 entries, 1 waypoint). So: **4 explorable maps + 1 homestead = 5 API maps, 14 waypoints total.** Audrey's "four" is correct for explorable maps.

### Waypoints in `data/pois.json` — all 14 present, none missing
| Map | Entries | Waypoints |
|---|---|---|
| Shipwreck Strand | 50 | Dark Leviathan `[&BJwPAAA=]`, Hullgarden Pier `[&BMwPAAA=]`, Pub Canach `[&BJEPAAA=]` |
| Starlit Weald | 51 | Foothold Bivouac `[&BMAPAAA=]`, Hunter's Camp `[&BIoPAAA=]`, Priory Expedition `[&BJ4PAAA=]` |
| Eternity's Garden | 50 | Deepwood Outpost `[&BOQPAAA=]`, Pilgrim's Rest `[&BPwPAAA=]`, Sanctum Exterior `[&BPAPAAA=]`, Temple of Abnegation `[&BPoPAAA=]` |
| Leyspring Hollows | 49 | Doyen's Adytum `[&BB8QAAA=]`, Hall of Assemblage `[&BDYQAAA=]`, Sealed Vestibule `[&BBYQAAA=]` |
| Comosus Isle (homestead) | 5 | Homestead Waypoint `[&BI8PAAA=]` |
| **Total** | **205** | **14** |

No Castora waypoint/POI/vista was missing from the dataset. Searching `"castora"` already returned 205 results before this work (region is in the search haystack, `tools/test_search.py` case `("castora", 205)`), and still does.

### What was newly tagged — Castora (19 entries, 15 new + 4 extended)
All 14 waypoints now carry `castora` + map name + `voe` / `visions of eternity`. Before this work only 4 Castora entries were tagged at all (Dark Leviathan, Hullgarden Pier, Pub Canach, Hunter's Camp — adventures only).

**Metas (verified staging points, GuildJen + Tyria Pulse):**
- Hammerhart Rumble! (Shipwreck, every 2h from 00:40 UTC) — at Hammerhart Battery POI `[&BHUPAAA=]`; route from Pub Canach Waypoint (Bozofriendly command guide). Tagged: Hammerhart Battery POI + Pub Canach Waypoint.
- Secrets of the Weald (Starlit, every 2h from 01:40 UTC) — at Consecrated Piazza POI `[&BG8PAAA=]`. Tagged: Consecrated Piazza POI.
- Shackles of the Ancients (Eternity's Garden, every 2h from 01:15 UTC) — starts at The Forge POI `[&BP8PAAA=]`. Tagged: The Forge POI.
- Depths of Cruelty (Leyspring, every 3h) — starts at Hall of Assemblage Waypoint `[&BDYQAAA=]` (GuildJen). Tagged there.

**Adventures (10 in Castora, all now tagged):**
- Shipwreck Strand (4): Castoran King Crab / Glimmering Arches Grand Prix → Dark Leviathan; Flying Fireworks → Hullgarden Pier; Skimmer-Net Scramble → Pub Canach.
- Starlit Weald (2): Old Magic / Ley-Line Rider → Hunter's Camp.
- Eternity's Garden (2): Kitshark → Kitshark Den POI `[&BOYPAAA=]`; Skimmer Relic Scour → Sanctum Exterior Waypoint (NW of it, ProjektDyad).
- Leyspring Hollows (2): Aetherlocation Detective → Sealed Vestibule Waypoint (NW of it, ProjektDyad/GuildJen); **Serpent Simulator → Primus Minor POI `[&BCwQAAA=]`** (NE of it, speak with Simulation Engineer Oruum, ProjektDyad — found in the full sweep, not in the first Castora pass).

**Jumping puzzles (Castora, 5 now tagged):**
- 'Booter's Path → Pub Canach (already tagged in v1.6).
- Soaring Copse → Soaring Copse POI `[&BKcPAAA=]` itself.
- Orb Cavern → Inquest Supply Cavern POI `[&BLQPAAA=]` (GuildJen: head to Inquest Supply Cavern and take the underwater path; wiki Orb Cavern: grotto beneath Riddled Cove, descend from underwater at the back of Inquest Supply Cavern).
- Coleopteran Cavern → Doyen's Adytum Waypoint (GuildJen mastery insights; JawseGaming video starts at Doyen's Adytum, SE to Narcisse).
- Inquest Cache → Hall of Assemblage Waypoint (GuildJen: insight above the end of the Inquest Cache JP; Hall of Assemblage is the nearest verified waypoint).
- Temple of Abnegation → Temple of Abnegation Waypoint.

**Mini dungeons (Castora, 2 now tagged):**
- 'Booter's Path → Pub Canach (already tagged in v1.6).
- From Ruins to Riches → Hall of Assemblage Waypoint, **medium confidence, flagged in the tag note**: the mini-dungeon ends at Navarium Core, NW of Hall of Assemblage (GuildJen); the entrance is at Sealed Vault POI and no source names a waypoint for the entrance itself (see README v1.6 note — this tag is tied to the *end* point, not the entrance).
- Temple of Abnegation → Temple of Abnegation Waypoint (chain starts there, GuildJen). **Chamber of Regret is NOT a separate mini dungeon** — it is the third chamber/event inside Temple of Abnegation (ProjektDyad/GuildJen); it is tagged as a phrase on the Temple of Abnegation entry, not as its own entry.

**Not tagged — Castora JP-like names with no verified location:**
Artificer's Rise, Birdie Benefactor, Inquest Hologram, Meandering Magic, Munchin' Moths — these appear in the wiki 'Booter's Path page Castora footer list, and Birdie Benefactor / Inquest Hologram are discussed on the forums as timed JP-like challenges (cuckoo-clock / hologram, fail = can't retry that day). None of them is a POI in `pois.json` and no source names a nearest waypoint for any of them. Do not tag them until a verified start point exists.

## 2. Full sweep — every expansion

Baseline is v1.6 (documented in `data/COVERAGE.md` and `tools/add_v16_*.py`): JPs 67/68 of the wiki list, adventures 93 taggable pairs of 123, mini dungeons 20/22. This sweep re-checked those lists against the wiki + guides, and added only what could be verified in this pass.

### Jumping puzzles
- **Before this sweep:** 72 JP-tagged entries (test count). **After:** 77.
- **New in this sweep (5):** Temple of Abnegation, Coleopteran Cavern, Inquest Cache, Soaring Copse, Orb Cavern — all Castora, all above.
- **Still missing (1): Mistwrought Vault** — wiki JP list: nearest waypoint Green World Citadel Waypoint (also Blue World Citadel Waypoint). Neither waypoint nor the Alpine Borderlands map is in the API dataset at all (`pois.json` has no Alpine Borderlands entries), so there is nothing to tag it to. This is a dataset gap, not a tag gap. Obsidian Sanctum (the other WvW JP) IS tagged.
- Per-expansion JP status after this sweep: Core — complete except Mistwrought Vault (WvW); HoT — complete; PoF/LWS3 — complete (Chalice of Tears, Searing Ascent are tagged as-is landmarks); LWS4/IBS — complete; EoD — complete (incl. Trials of the Tengu); SotO — complete; Janthir Wilds — complete (Treetop Beehive, Vale Brazier, Queen's Confidence, Traversing the Titan); VoE/Castora — complete for the 5 JPs on the map Activities lists + Temple of Abnegation, except the 5 unverified timed-challenge names above.

### Adventures
- **Before this sweep:** 67 adventure-tagged entries (test count; 69 with the SAB name match). **After:** 71 (70 + SAB name match).
- **New in this sweep (4, all Castora):** Skimmer Relic Scour, Aetherlocation Detective, Kitshark, Serpent Simulator.
- **Castora adventures are now 10/10 tagged** (see §1).
- **Still missing (v1.6, unchanged by this sweep):** 11 festival adventures in instance maps with **no usable waypoint** (7 Super Adventure Box, 4 Halloween) — cannot be tagged, by design; and 14 adventures v1.6 recorded as unverified (no source names a nearest waypoint). No new verifiable adventure was found for any other expansion in this sweep — the v1.6 per-expansion counts stand: HoT 15/15, PoF/LWS4/IBS 34/39, EoD/SotO/Janthir/festivals/Other 44/69 (now +4 VoE = 48/69 for that group, all 4 being the Castora ones).
- Note: the "123 adventures" total is the wiki Adventures navbox count from v1.6; it does not cleanly include the newer VoE adventures, so the denominator is stale — the honest statement is "all verifiable open-world adventures are tagged; instance-only and unverified ones are not".

### Mini dungeons
- **Before this sweep:** 23 mini-dungeon-tagged entries (test count; 20 of 22 mini dungeons). **After:** 26 entries — **22 of 22 mini dungeons, i.e. complete.**
- **New in this sweep (3):**
  - From Ruins to Riches → Hall of Assemblage (medium confidence, flagged — see §1).
  - **Trial of the Elders → Sanctuary of Ione POI `[&BEgNAAA=]`, Dragon's End.** This resolves the v1.6 blocker: no source names a *waypoint*, but ProjektDyad (End of Dragons Mini Dungeons, 2025-02-10) and GuildJen both give the entrance as the grate at Sanctuary of Ione POI with its chat code. Tagged to the entrance POI itself, exactly as Hammerhart Battery / Consecrated Piazza / The Forge are tagged for metas. No waypoint was invented.
  - Temple of Abnegation → Temple of Abnegation Waypoint (see §1; Chamber of Regret is inside it).
- **Still missing: none.** The wiki mini-dungeon list is now fully covered. (The README/COVERAGE v1.6 note "Not tagged: Trial of the Elders and From Ruins to Riches" is now out of date — update it at the next build.)

## 3. Totals after this work
- Tagged entries: **280 → 298** (+18 from this task: 15 Castora first pass + 3 full-sweep finds).
- Tag phrases: **2,117 → 2,257** (+140 from this task).
- Test counts updated in `tools/test_search.py` (with reasons in comments): jumping puzzle 72 → 77, adventure 67 → 71, mini dungeon 23 → 26.
- `tools/test_search.py`: **149/149 pass** after the updates. `tools/apply_tags.py`: passes, no name/map mismatches.
- **DLL NOT rebuilt by this task** (per instructions). The new tags were merged into the v1.8.1 build by the parent (see MEMORY.md: v1.8.1 delivered 2026-11-17, sha256 61c1ed36734994657620b73340482c601e0dd712ac6d55d6eb85baba3bb170df).
- **Note on later file state:** after this task's last write, a parallel material-farm tagging task added 12 more entries to `data/tags.json` (poultry/material tags, e.g. Bloodcliff Waypoint, Amnoon Waypoint), bringing the file to **310 entries / 2,390 phrases** at last check. Those 12 are NOT part of this Castora/sweep task; tests still pass 149/149 after the merge.

## 4. Still missing / unverified — do not tag without a verified start point
1. Mistwrought Vault (JP, WvW) — Green/Blue World Citadel Waypoint not in the API dataset; Alpine Borderlands absent entirely.
2. Castora timed JP challenges — Artificer's Rise, Birdie Benefactor, Inquest Hologram, Meandering Magic, Munchin' Moths — no POI in the dataset, no verified nearest waypoint.
3. 11 festival adventures in instance maps (7 SAB, 4 Halloween) — no usable waypoint by design.
4. 14 adventures v1.6 left unverified — no source names a nearest waypoint (see `tools/add_v16_adventures.py` header / README).
5. From Ruins to Riches tag is medium-confidence (end point, not entrance) — flagged in its tag note; if a source ever names the entrance waypoint, retag to that.

## Sources
- GW2 Wiki, Castora: https://wiki.guildwars2.com/wiki/Castora
- GW2 Wiki, Visions of Eternity: https://wiki.guildwars2.com/wiki/Guild_Wars_2:_Visions_of_Eternity
- Tyria Pulse, Janthir Wilds and Castora metas (2026-10-23/24): https://tyriapulse.vercel.app/articles/gw2-janthir-wilds-castora
- GuildJen map achievement guides (Shipwreck Strand, Starlit Weald, Eternity's Garden, Leyspring Hollows): https://guildjen.com/shipwreck-strand-achievements-guide/ etc.
- ProjektDyad mastery guides (Shipwreck Strand, Starlit Weald, Eternity's Garden, Leyspring Hollows; End of Dragons Mini Dungeons 2025-02-10): https://projektdyad.com/guides-list/
- GW2 Wiki, Orb Cavern: https://wiki.guildwars2.com/wiki/Orb_Cavern
- GW2 Wiki, Jumping puzzle list: https://wiki.guildwars2.com/wiki/Jumping_puzzle
- GW2 Wiki, 'Booter's Path: https://wiki.guildwars2.com/wiki/%27Booter%27s_Path
- Wiki map pages returned HTTP 403 via browser.open on 2026-11-17 (same as the earlier Event Timers / Mystic Forge 403s) — map-level lists were verified via search-result extracts and the guide sites above instead. Do not retry those exact fetches.
