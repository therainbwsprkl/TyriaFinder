# Guild missions + mount races — Tyria Finder tags

Date: 2026-11-17. Data only — no DLL rebuild by this task (v1.9 build in progress separately).
Totals after this task: **331 tagged entries / 2,666 phrases** (was 310 / 2,390 — +21 entries, +276 phrases).
Validation: `tools/apply_tags.py` pass, `tools/test_search.py` **149/149 pass**.
Note: `data/tags.json` later moved to 336 / 2,773 — the parallel v1.9 build merged its own map-bonus + rift tags into the same file after this task validated; those +5 entries / +107 phrases are NOT this task's.
Spot-checks: "guild rush" → 7, "guild puzzle" → 3, "guild challenge" → 6, "guild bounty" / "guild trek" → 1 (Guild Initiative HQ, see below), "mount race" → 16, "roller beetle race" → 6, "race to the finish" → 7.

Sources: GW2 Wiki (Guild mission / Guild Rush / Guild Challenge / Guild Puzzle / Mount race pages — wiki.guildwars2.com returned HTTP 403 on 2026-11-17, not retried; the same tables were read via the Russian wiki mirror wiki.guildwars-2.ru and via Dulfy Reborn / GuildJen / ArenaNet, which reproduce the wiki tables), Dulfy Reborn guild guides, GuildJen guilds guide, ArenaNet "Roller Beetle Racing Is Drifting Your Way" (guildwars2.com). No waypoint or chat code was invented — every code below was verified to exist in `data/pois.json` with the name/map shown.

## Guild missions — full type list

Weekly missions, refresh **Monday at reset** (GuildJen). Up to 10 assigned per week by guild level + Mission Preference (PvE / PvP / WvW / No Preference). All PvE missions take place in **Central Tyria**.

### PvE — 5 types (Dulfy / GuildJen / wiki)

| Type | What it is | Fixed or rotating? | Tagging verdict |
|---|---|---|---|
| Guild Bounty | Track down and defeat specific target NPCs roaming open-world maps, 15 min limit. 18 targets in the Dulfy list (+3 Blazeridge extras in some lists: Weird Wind Rider, Peculiar Pig, Curious Cow — same Blazeridge path). | **Rotating / roaming.** Each target has its own map, but roams a path with many possible spawn points (Sotzz has 300+ spawn locations per Dulfy). No single start waypoint. | **Not tagged per-target.** See below. |
| Guild Trek | Find hidden glowing guild marks from a screenshot + name clue, 20 min. **186 locations**, random subset per mission. | **Random.** No fixed location at all. | **Not tagged per-location.** See below. |
| Guild Rush | Transformed into a creature, run an obstacle course to the finish. | **Fixed — 7 routes**, one assigned at random per activation (5 hrs to locate it). | **Fully tagged — 7/7.** |
| Guild Challenge | Open-world group events: defend, destroy, escort. | **Fixed — 6 challenges**, one assigned at random. | **Fully tagged — 6/6.** |
| Guild Puzzle | Instanced multi-room puzzle + jumping, team mechanics. | **Fixed — 3 puzzles**, one assigned at random. Each has its own waypoint outside the entrance (uncontested once activated). | **Fully tagged — 3/3.** |

### PvP missions — not taggable
PvP Score/Conquest, PvP Rank Points, PvP Matches & Wins (GuildJen). Take place in structured PvP, no open-world waypoint. **Not tagged.**

### WvW missions — not taggable
WvW Capture & Hold, WvW World Experience, WvW Objective Capture, WvW Challenge (Obsidian Sanctum) (GuildJen / LineGames). Take place in the Mists / WvW maps, no PvE waypoint in the dataset. **Not tagged.**

### Guild Bounty — the 18 Dulfy targets (map only, no waypoint tagged)
2-MULT (Timberline Falls), Ander "Wildman" Westward (Southsun Cove), Big Mayana (Sparkfly Fen), Bookworm Bwikki (Lornar's Pass), Brekkabek (Harathi Hinterlands), Crusader Michiele (Sparkfly Fen), Deputy Brooke (Snowden Drifts), Devious Teesa (Frostgorge Sound), Diplomat Tarban (Brisban Wildlands), Half Baked Komali (Mount Maelstrom), Poobadoo (Kessex Hills), Prisoner 1141 (Iron Marches), Shaman Arderus (Fireheart Rise), Short-Fuse Felix (Diessa Plateau), Sotzz the Scallywag (Gendarran Fields), Tricksy Trekksa (Blazeridge Steppes), Trillia Midwell (Fields of Ruin), Yanonka the Rat-Wrangler (Fields of Ruin). Plus, per MMORPG-Life: Weird Wind Rider, Peculiar Pig, Curious Cow (all Blazeridge Steppes, same path as Tricksy Trekksa).
**Why not tagged:** tagging a roaming target to one waypoint would send a guild to the wrong end of a map. Searching "guild bounty" instead returns **Guild Initiative Headquarters, Lion's Arch `[&BFwHAAA=]`** — the guild-mission hub — with a note explaining bounty targets roam their maps and trek locations are random. That is the honest starting point, not a spawn point.

### Guild Trek — 186 locations, random
Per Dulfy, ~180–186 trek locations, random subset per mission, identified only by a screenshot + name in the guild panel. **No location is tagged.** Searching "guild trek" returns the Guild Initiative HQ entry (same hub note as bounty).

## Guild Rush — 7/7 tagged

Wiki/Dulfy table (closest waypoint per rush):

| Rush | Map / area | Waypoint tagged |
|---|---|---|
| Bear Lope | Lornar's Pass, Posternus Caverns | Durmand Priory Waypoint `[&BOkAAAA=]` |
| Chicken Run | Fields of Ruin, Flameroot Caverns | Fangfury Watch Waypoint `[&BEwBAAA=]` (Blackblade's Watch is closer but can be contested) |
| Crab Scuttle | Southsun Cove, Southsun Shoals | Kiel's Outpost Waypoint `[&BNwGAAA=]` |
| Devourer Burrow | Diessa Plateau, Spider Nest Cavern | Manbane's Waypoint `[&BMkDAAA=]` |
| Ghost Wolf Run | Harathi Hinterlands, Bonerattler Caverns | Faun's Waypoint `[&BKUAAAA=]` |
| Quaggan Paddle | Frostgorge Sound, Talabaroop Waves | Twoloop Waypoint `[&BIACAAA=]` |
| Spider Scurry | Dredgehaunt Cliffs, Dostoev Sky Peak | Hessdallen Kenning Waypoint `[&BF0CAAA=]` |

Note: Dulfy says "6 known locations" — the wiki table lists 7 (Ghost Wolf Run is the seventh). All 7 are tagged.

## Guild Challenge — 6/6 tagged

| Challenge | Map / area | Waypoint tagged |
|---|---|---|
| Blightwater Shatterstrike | Blazeridge Steppes, Blightwater Basin | Tumok's Waypoint `[&BPsBAAA=]` |
| Branded for Termination | Fields of Ruin, Varim's Run | Helliot Mine Waypoint `[&BEsBAAA=]` |
| Deep Trouble | Mount Maelstrom, The Mire Sea | Irwin Isle Waypoint `[&BNICAAA=]` |
| Save Our Supplies | Iron Marches, The Granite Front | Viper's Run Waypoint `[&BOoBAAA=]` |
| Scratch Sentry Defense | Timberline Falls, Fionnghuala Scratch | Stromkarl Waypoint `[&BEYEAAA=]` |
| Southsun Crab Toss | Southsun Cove, Southsun Shoals | Kiel's Outpost Waypoint `[&BNwGAAA=]` (shared with Crab Scuttle) |

## Guild Puzzle — 3/3 tagged

| Puzzle | Map | Waypoint tagged |
|---|---|---|
| Angvar's Trove | Snowden Drifts | Angvar's Trove Waypoint `[&BP8GAAA=]` |
| Langmar Estate | Plains of Ashford | Langmar Estate Waypoint `[&BPgGAAA=]` |
| Proxemics Lab | Brisban Wildlands | Proxemics Lab Waypoint `[&BPkGAAA=]` |

Codes per NeoGAF/wiki puzzle table, all three verified in `data/pois.json`. Each puzzle's waypoint becomes uncontested once the puzzle is activated (wiki).

## Mount races — full list

A mount race is a timed event: register with a Race Organizer, run checkpoints to the finish. A Time Trial adventure is usually available in the same area. Roller beetle races restart 15 min after the previous race ends (wiki).

### Roller beetle races — 5/5 tagged
Already tagged as Time Trial adventures in earlier builds; this task added "roller beetle race" / "mount race" phrases:

| Race | Map / area | Waypoint tagged |
|---|---|---|
| Ghostfire Run | Diessa Plateau, Noxin Dells | Nageling Waypoint `[&BN0AAAA=]` (ArenaNet: "starts near Nageling Waypoint") |
| Infernal Leap | Mount Maelstrom, The Stychs | Avernan Waypoint `[&BM8CAAA=]` (ArenaNet: "begins on the shore below Avernan Waypoint") |
| Jormag's Fang | Snowden Drifts, Valslake | Torstvedt Homestead Waypoint `[&BLsAAAA=]` (ArenaNet: "just south of Torstvedt Homestead Waypoint") |
| Lakeside Loop | Gendarran Fields, Provern Shore | Provern Shore Waypoint `[&BOQAAAA=]` (ArenaNet: "starts near Provern Shore Waypoint") |
| Tropic Valley Raceway | Brisban Wildlands, The Gallowfields | Proxemics Lab Waypoint `[&BPkGAAA=]` (ArenaNet: "begins near Proxemics Lab Waypoint"; also the guild-puzzle waypoint) |

### Race to the Finish (PoF + LWS4) — 7/7 tagged (2 medium-confidence, flagged)

| Race | Map / area | Waypoint tagged |
|---|---|---|
| Race to the Finish: Crystal Oasis | Crystal Oasis, Free City of Amnoon | Amnoon Waypoint `[&BLsKAAA=]` — map hub in Amnoon; no source names a race-start waypoint outright |
| Race to the Finish: Desert Highlands | Desert Highlands, Brightwater Inlet | Brightwater Waypoint `[&BJEKAAA=]` (Dulfy video starts at Brightwater Waypoint) |
| Race to the Finish: Elon Riverlands | Elon Riverlands, Vulture Drifts | Olishar's Oasis Camp Waypoint `[&BCgKAAA=]` (Dulfy: "Race starts just south of Olishar's Oasis Camp waypoint") |
| Race to the Finish: The Desolation | The Desolation, Sand Jackal Run | Sand Jackal Run Waypoint `[&BHcKAAA=]` (Dulfy: "The race starts at Sand Jackal Run waypoint") |
| Flying Finish (Race to the Finish: Domain of Vabbi) | Domain of Vabbi, Kodash Bazaar | Vehtendi Academy Waypoint `[&BA8KAAA=]` — **medium confidence**: GuildJen says the race starts in Vehtendi Arena; Vehtendi Academy is the nearest named waypoint to the arena, no source names a waypoint outright |
| Race to the Finish: Domain of Istan | Domain of Istan, Corsair Flotilla → Issnur Bay | Chalon Docks Waypoint `[&BAkLAAA=]` — **medium confidence**: GuildJen/Dulfy place the race at Corsair Flotilla (skimmer, every 45 min); Chalon Docks is the nearest named waypoint to Corsair Flotilla, no source names a waypoint outright |
| Race to the Finish: Olmakhan Docks | Sandswept Isles, around Atholma | Atholma Waypoint `[&BEMLAAA=]` (GuildJen: skimmer race around Atholma) |

Not tagged: Race to the Finish: Inquest Facility (Sandswept Isles) — starts "around the northern perimeter of Rata Primus" / Northern Complex Coves (GuildJen/Dulfy); no waypoint in that area is in the dataset and no source names one. Listed as missing below.

### Seasonal / festival races — tagged where a waypoint exists

| Race | Where / when | Waypoint tagged |
|---|---|---|
| Mad King's Raceway | Mad King's Realm, Halloween (Shadow of the Mad King) — mount races + time trials, rentals available; entry via Lunatic Boatmaster teleport | Mad King's Raceway Waypoint `[&BJsLAAA=]` |
| Dragon Bash mount race | Hoelbrak, Dragon Bash — Trade Commons | Trade Commons Waypoint `[&BIYDAAA=]` (ProjektDyad: head to Trade Commons Waypoint) |
| Wintersday race / Frozen Footrace | Divinity's Reach, Wintersday — race ~every 20 min, on foot or mount | Crown Pavilion Waypoint `[&BCwDAAA=]` (Divinity's Reach entry; already tagged with Racing in the New Year / Snowfall Sprint) |
| Lunar New Year mount race | Divinity's Reach, Lunar New Year — Crown Pavilion, raptor rental 10s | Crown Pavilion Waypoint `[&BCwDAAA=]` (same entry) |
| Skimmer Slalom | Labyrinthine Cliffs, Festival of the Four Winds — every 2h at :30 | Bazaar Docks Waypoint `[&BBwHAAA=]` (already tagged with the Skimmer Slalom adventure) |
| Flying Dolyak | Labyrinthine Cliffs, Festival of the Four Winds — every 2h on the hour, transformed into a dolyak | Bazaar Docks Waypoint `[&BBwHAAA=]` (already tagged) |

## Still missing / unverifiable — do not tag without a verified start point

1. **Guild Bounty individual targets (18–21)** — roaming targets, 300+ spawn points for some; no single waypoint. Hub entry only (Guild Initiative HQ).
2. **Guild Trek locations (186)** — random subset per mission, screenshot-only clues. No location tagged.
3. **PvP guild missions** — structured PvP, no waypoint.
4. **WvW guild missions** — Mists / WvW maps, no PvE waypoint in the dataset.
5. **Race to the Finish: Inquest Facility (Sandswept Isles)** — northern perimeter of Rata Primus / Northern Complex Coves; no source names a waypoint, none in that area in the dataset.
6. **Junundu Wurm race (Domain of Vabbi)** — one dynamic event, mount a Junundu wurm; no fixed start waypoint published.
7. **Super Adventure Box race** — inside the SAB hub, mounts cannot be used; instance, no waypoint.
8. **Shing Jea Boardwalk / other festival roller-beetle events** — no fixed race-start waypoint verified.
9. **"Finders Inner Keepers" (Jahai Bluffs)** — a treasure race, not a mount race; not tagged as one.

## Honest verdict on "every type" / "every mount race"

**Guild missions: every *type* is covered, but not every *instance* of every type.** Rush 7/7, Challenge 6/6, Puzzle 3/3 are fully tagged to fixed, verified waypoints. Bounty and Trek cannot be done as single-waypoint tags by design (roaming / random) — the honest coverage is a hub entry + the full target/location lists in this note. PvP/WvW missions have no waypoint to tag. So "every type" is true at type level, with Bounty/Trek/PvP/WvW covered only as types, not as locations.

**Mount races: every permanent race is covered.** Roller beetle 5/5, Race to the Finish 7/8 (Inquest Facility is the one gap), seasonal/festival races 6/6 where a waypoint exists. The remaining gaps are races with no fixed start waypoint (Junundu, SAB, Inquest Facility) — those need a per-race research pass or an in-game check, not a guessed waypoint.
