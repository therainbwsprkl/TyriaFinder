# Dataset coverage — `data/pois.json` (Tyria Finder v1.11.0; dataset unchanged from v1.7)

Tags in v1.11.0: **335 entries / 2,761 phrases** (unchanged from v1.10.4 — v1.11.0 is a publish-identity build only: FIND signature + GitHub update provider, no dataset changes) — v1.10.4 removed the "daily activity" umbrella tags (see below); v1.10.1 was a layout/UI fix, v1.10.2 a performance fix + no Map Bonus prices, v1.10.3 removed the v1.10 user-custom tags — no dataset changes in those versions (was 336 / 2,773 in v1.9–v1.10.3). User-custom tags (v1.10, removed in v1.10.3) were never in this dataset (see `docs/user-tags.md`). (was 298 / 2,257 in v1.8.1) — materials/mob tags (docs/mob-and-poultry-tags.md), map-bonus entry waypoints and rift entry waypoints, guild-mission + mount-race tags (docs/guild-missions-mount-races.md), and daily-activity tags (docs/daily-activities.md) — **v1.10.4: the "daily activity" umbrella tags are removed** (the four individual activity name tags stay; the Lionbridge entry is gone as a tagged entry) — (all verified in this dataset, no chat code invented).

Generated 2026-11-16 from the official Guild Wars 2 API (no API key needed):
- `https://api.guildwars2.com/v2/maps?ids=all` — 1,086 map entries
- `https://api.guildwars2.com/v2/continents/1/floors/*` (127 floors) and
  `https://api.guildwars2.com/v2/continents/2/floors/*` (56 floors) — 183 floor
  files, 8.2 MB raw, fetched 2026-11-16

Build script: `tools/build_dataset.py` (re-runnable; raw API cache is not
committed — re-fetch to regenerate).

## Totals

| Type in dataset | Count |
|---|---|
| Waypoint (`waypoint`) | 983 |
| Point of Interest (`landmark` in the API) | 2,237 |
| Vista (`vista`) | 553 |
| **Total** | **3,773** |

- Maps covered (at least one entry): **169**
- Chat links are taken **verbatim** from the API (`chat_link` field), not
  re-encoded by us. Spot-checked against known codes from in-game use:
  Jaka Itzel Waypoint → `[&BOAHAAA=]`, Caledon Haven Waypoint →
  `[&BDwBAAA=]`, Rosko's Campsite Waypoint → `[&BNgAAAA=]`,
  Junction Camp Waypoint → `[&BLAAAAA=]` — all four match exactly.
- Deduplication: the same POI appears on several floors of the same
  continent (floors are zoom / sub-level variants). Entries are deduped by
  POI id; raw POI rows before dedup were 15,926.

## Coverage — what is missing, honestly

**No real open-world map is missing by name.** Of the 123 maps whose
`/v2/maps` type is `Public`, 95 are present by name. The 28 absent by name
are, on inspection, *not* playable open-world maps:

- **Duplicate / instance versions of a real map** (the real map is present
  under its plain name): `Dragon's Stand (Heart of Thorns)` (real map:
  `Dragon's Stand`, id 1041), `Bloodtide Coast (Public)`, `Brisban
  Wildlands (Public)`, `Caledon Forest (Public)`, `Fields of Ruin
  (Public)`, `Fireheart Rise (Public)`, `Gendarran Fields (Public)`,
  `Lake Doric (Public)`, `Metrica Province (Public)`, `Snowden Drifts
  (Public)`, `Thunderhead Peaks (Public)`, `The Battle For Lion's Arch
  (Public)`.
- **Strike / boss / story instances** with no map POIs: `Dragon Arena
  (Public)`, `Dragonstorm (Public)`, `Boneskinner (Public)`, `Celestial
  Challenge`, `Cold War (Public)`, `Fraenir of Jormag (Public)`,
  `Shiverpeaks Pass (Public)`, `Voice of the Fallen and Claw of the Fallen
  (Public)`, `Whisper of Jormag (Public)`, `Secret Lair of the Snowmen
  (Public)`, `Noble's Folly`.
- **Convergence instances**: `Convergence: Mount Balrior (Public)`,
  `Convergence: Outer Nayos (Public)`, `Convergence: Nexus of Eternity`.
- **Festival / unnamed**: `Stopped Clock Tower`, map id 1150 (empty name).

Expansion-era open-world maps **are** present, including Janthir Syntri,
Lowland Shore, Bava Nisos, Amnytas, Inner Nayos, Seitung Province, New
Kaineng City, The Echovald Wilds, Dragon's End, Sandswept Isles, Domain
of Istan, Jahai Bluffs, Dragonfall, Grothmar Valley, Bjora Marches,
Drizzlewood Coast and Skywatch Archipelago. The earlier worry that the
continents API is incomplete for newer maps did **not** hold up for
open-world maps on this fetch — the gaps are the instance duplicates above.

The other 917 of 1,086 `/v2/maps` entries with no dataset entry are
instance / PvP / story / dungeon maps, which have no waypoints/POIs/vistas
in the continents data by design.

## Hero Points — EXCLUDED from v1 (known gap)

Hero Points were in the locked v1 spec, but they **cannot** be built from
the official API, and we did not fake them:

- The continents API's `skill_challenges` entries have **no name and no
  `chat_link`** — only a coordinate and, for most, an id like `"0-224"`;
  275 of the 337 unique skill challenges have no id at all, only a coord.
- Unique skill challenges found: **337** (across 47 maps in the raw data).
- A hero point therefore has nothing searchable by name and nothing to
  copy to the clipboard, which are the two things this addon is for.

The UI still has a Hero filter, but it shows an explicit "not available
from the official API" empty state instead of inventing names.

**v1.1 path (not done):** hero-challenge names live on the GW2 Wiki
(per-map "List of hero challenges" tables, e.g. Queensdale lists
"Defeat Chhk the Windmill King" etc.). That would be a separate,
wiki-sourced dataset that needs its own verification pass — coordinates
matched to the API skill challenges, and a chat link per challenge, which
the wiki does not consistently give. Do not add hero points until that
dataset exists and is checked.

## Also excluded (deliberately)

- `unlock`-type POIs: 23 unique (mastery insights etc.). They are not
  waypoints/POIs/vistas and have no consistent search use here.
- Tasks (hearts), sectors, mastery points: not in scope. Adventures
  WERE in scope from v1.6 (see below); hero points are still excluded.

## Vistas are (almost all) unnamed in the API

- 548 of 553 vistas have `name: null` in the continents API; only 5 have a
  real name (e.g. "Hullgarden Vista", "Mosaic Bower"). Vistas are unnamed
  in-game too — they are just "Vista" markers.
- One waypoint is also unnamed: id 1824, Super Adventure Box, `[&BCAHAAA=]`.
- The addon therefore shows unnamed entries with a synthetic display label
  `Vista — <Map Name>` / `Waypoint — <Map Name>` (derived from the map
  name, not an in-game name). Their `chat_link` is still the real API one,
  so copy-to-clipboard still works. Searching "vista" + a map name will
  find them; searching a vista by a proper name will not, because the API
  gives it none.

## Keyword tags (v1.2–v1.7; unchanged in v1.8)

- 280 of the 3,773 entries carry curated tags (`data/tags.json`, 2,117
  tag phrases), merged into `data/pois.json` by `tools/apply_tags.py`,
  which fails loudly on any chat_link / name / map mismatch. v1.4–v1.7
  additions were merged by `tools/add_v14_tags.py` /
  `tools/add_v16_jps.py` / `tools/add_v16_adventures.py` /
  `tools/add_v16_minidungeons.py` / `tools/add_v16_collections.py` /
  `tools/add_v17_psna.py`,
  which look each (name, map) up in the dataset and fail on a missing
  or ambiguous entry — no chat_link was typed in by hand (two
  entries share a name+map and were tagged by explicit chat_link:
  Shipwreck Peak Waypoint `[&BN4HAAA=]` and Obsidian Sanctum
  Waypoint, one entry per WvW team colour; v1.7 additionally checks
  every expected chat_link against the dataset). The tag list is
  documented in full in `README.md` ("What changed in v1.7").
- v1.4 is multi-spot: a tag phrase is attached to several entries, so
  one search returns all well-known spots. By category (entries, with
  overlaps where one waypoint serves two categories — e.g. Trader's
  Forum is both a JP and a service hub): gathering 63, Event Timers
  metas 17, dungeons 9, raids 2, strikes 3 hubs, jumping
  puzzles 72 (v1.6), services 20, chest runs 3, world bosses 23,
  adventures 66 (v1.6), mini dungeons 23 (v1.6), Dive Master
  collection 36 (v1.6), PSNA 40 (v1.7).
- Gathering tags (63 entries): v1.2 start waypoints from Lady Elyssa's
  Guides README, Gathering section (re-checked 2026-11-16/17), plus
  v1.4 multi-spot expansion. Flax 9 farm spots (GameRant Best Flax
  Farming Locations 2024-11-06, wiki Flax, Metabattle). Rich Mithril 9
  and Rich Orichalcum 15 (wiki vein pages, Almars spawn list,
  Strikingly guide). Quartz 4 (forum quartz guide). Rich Copper 5,
  Silver 5, Gold 4, Iron 7, Platinum 6 — these are labelled map hubs
  (GW2 Life crafting-material lists + wiki vein pages give map lists
  only, no spot waypoint). Elder Wood 6, Hard Wood 5, Soft Wood 5
  (map hubs, wiki tree pages). Seasoned Wood still 2 — no verified
  farm spot beyond the two Lady Elyssa legs. One tagged entry is not
  a waypoint: Spearmarshal's Lament (Rich Orichalcum, Domain of Vabbi)
  is a landmark POI in the API — tagged as-is, not re-labelled.
  v1.3 adds two more as-is landmarks: Chalice of Tears (Ember Bay) and
  Searing Ascent (Draconis Mons), which ARE their jumping puzzles.
- Jumping puzzles, v1.6 (72 entries): the wiki "Jumping puzzle" list
  (68 JPs) was fetched 2026-11-17 and every entry's nearest-waypoint
  column checked against `data/pois.json`. 67 of 68 covered; only
  Mistwrought Vault is missing (Green/Blue World Citadel Waypoint
  not in the API dataset; Alpine Borderlands absent). Where the wiki
  and the v1.3 Dulfy source disagree on the nearest waypoint, BOTH
  are tagged (see README.md "What changed in v1.6" for the list).
- Adventures, v1.6 (66 entries, 93 taggable pairs of 123): HoT 15/15
  verified (GuildJen, wiki Getting there, AyinMaiden, Dulfy,
  ProjektDyad); PoF/LWS4/IBS 34/39 (22 verified, 12 medium-
  confidence — area-listing or guide route-grouping, flagged in the
  tag notes — 5 unverified, not tagged); EoD/SotO/Janthir/VoE/
  festivals/Other 44/69 (30 verified cleanly, 14 caveated/derived —
  flagged — 11 in instance maps with no usable waypoint, 14
  unverified, not tagged). Sources: wiki adventure pages and the
  Adventures navbox (the wiki "Adventure" index page returns HTTP
  403 and was not retried; individual adventure pages open fine),
  GuildJen map guides, ProjektDyad, MetaBattle, Dulfy, AyinMaiden,
  Tekkit, forums. Repeating adventures are tagged per map; ambiguous
  ones are tagged both ways (see README.md).
- Mini dungeons, v1.6 (23 entries, 20 of 22): wiki "Jumping puzzle"
  table nearest-waypoint column, Dulfy Reborn, GuildJen, ProjektDyad
  (End of Dragons Mini Dungeons, 2025-02-10), AyinMaiden, TheGamer,
  .ru wiki mirror (the English wiki returns HTTP 403 via
  browser.open and was not retried). Not tagged: Trial of the Elders
  and From Ruins to Riches (entrance known, no source names a
  waypoint — the nearest-waypoint guesses for them are inferences
  only, so they stay out). Vexa's Lab is single-source (GuildJen
  Mawdrey guide) and disagrees with the v1.3 JP tag (Keeper's
  Waypoint vs Pig Iron Waypoint) — both are in the results, flagged.
- Collections, v1.6 — Dive Master only (36 of 38): the only
  collection set that is a complete closed list with every objective
  a fixed physical location. Rejected for this build: Central Tyria
  Mastery Insights (9, too small — best Phase 2/fallback); all-
  expansion Mastery Insights (100+, too large); legendary
  collections (mixed types — events, vendor purchases, crafting,
  drops — most objectives have no waypoint); Janthir/SotO
  collections (mixed types, time-gates). Source: Dulfy Dive Master
  guide, cross-checked against the wiki Diving Goggles page (38
  locations, not 37 — Dulfy's intro says 37 but its numbered list
  runs 1–38). Not tagged: the 2 Hidden Garden goggles (no single
  nearest waypoint) and the 3 non-counting goggles.
- Region search, v1.6: the search haystack is now "<display name>
  <map name> <region>" (see `src/entry.cpp`), so a region/map name
  returns all its entries; the results cap was raised 100 → 250.
  "castora" → 205 results (5 maps, 14 waypoints, 168 POIs, 23
  vistas); "eternity's garden" → 50 (4 waypoints); "creeping
  crevasse" → Shipwreck Peak Waypoint only (a Verdant Brink
  mastery-insight area, not a JP or a POI in the dataset); "janthir"
  → 190; "heart of maguuma" → 204. **This corrects the v1.3 note
  below that Castora maps have no waypoints — they have 14.** Regions
  in the dataset: Ascalon, Cantha, Castora, Crystal Desert, Fractals
  of the Mists, Heart of Maguuma, Horn of Maguuma, Janthir, Kryta,
  Mad King's Realm, Maguuma Wastes, Player vs. Player, Ring of Fire,
  Ruins of Orr, Shiverpeak Mountains, Steamspur Mountains, Super
  Adventure Box, Tarnished Coast, World vs. World, plus one
  empty-string region. No region in the dataset is empty: every
  region has at least its maps' POIs/vistas.
- Services tags (20 entries): bank / guild bank 8 hubs, trading post
  9, Mystic Forge 2 (Trader's Forum + PvP Lobby, Heart of the Mists),
  all 8 crafting disciplines at 10 city hubs, merchant(s) 11 hubs,
  laurel merchant 11 locations (wiki Laurel Merchant page). Sources:
  Allakhazam Crafting wiki, GuildWarsHub bank/TP ranking,
  everylastrecipe Mystic Forge guide. NOT added: Divinity's Reach
  Mystic Forge (Duke's Garrison — nearest waypoint unverified; wiki
  Mystic Forge page HTTP 403 on 2026-11-17), Ember Bay / Verdant
  Brink laurel merchants (no verified nearest waypoint), Ebonhawke
  services (no waypoint in the dataset), Scribe / Handiworker.
- World boss / timed event tags (23 entries): the wiki World boss page
  (schedule + boss list, fetched 2026-11-16/17) plus per-boss guides.
  Disputed waypoints are recorded in README.md, not smoothed over:
  Fire Elemental (Muridian vs Survivor's Encampment), Modniir Ulgoth
  (Cloven Hoof vs Junction Camp), Great Jungle Wurm (Twilight Arbor vs
  Falias Thorp), Shadow Behemoth (two waypoints, both tagged), Karka
  Queen (Pearl Islet vs Camp Karka), Drakkar (waypoint code `[&BDkMAAA=]`
  vs the POI code `[&BEUMAAA=]` cited by one guide).
- v1.3 meta sources: Cellofrag timer index reproducing the wiki Event
  Timers schedule (v5.4, retrieved 2026-11-17) + per-event guides.
  The wiki Event Timers page itself still returned HTTP 403 on
  2026-11-17 and was not retried in this build. Ley-Line Anomaly is
  tagged only for Gendarran Fields (timer code `[&BOQAAAA=]` verified
  as Provern Shore Waypoint); Timberline Falls / Iron Marches rotations
  were not verified. Visions of Eternity metas were not added — **the
  v1.3 reason given here was wrong and is corrected in v1.6:** Castora
  maps DO have waypoints in the API dataset (14 across the 5 maps).
  The metas are still unadded because no single verified staging
  waypoint was pinned down for any of them.
- PSNA, v1.7 (40 entries, 42 agent-day slots): Pact Supply Network
  Agents — 6 karma merchants (Pact Commander mastery Supply Line
  Management tier 3, HoT required), one per region, on a fixed 7-day
  weekday cycle, locations changing at 08:00 UTC (not the 00:00 UTC
  daily reset). Weekday table from Doncpauli (fetched live 2026-11-17),
  cross-checked against the GW2 Wiki PSNA table (2025-07-27 to
  2025-08-03) and a gw2timer-sourced gist — all three agree on the
  weekday mapping. All 42 Doncpauli codes exist in the dataset with the
  expected name/map; 22 are waypoints, 20 are landmark POIs, tagged
  as-is (the published code is the agent's spot, never swapped for a
  nearby waypoint). 4 gist codes rejected after dataset lookup (the
  dataset entry is a different place from the expected location):
  Mehem Sunday `[&BIsHAAA=]` (Oasis, not Azarr's Arbor), Fox Thursday
  `[&BE8AAAA=]` (Seraph Protectors, not Wendon Waypoint), Yana Thursday
  `[&BP0DAAA=]` (Armada Harbor, not Fort Trinity), Verma Thursday
  `[&BOQBAAA=]` (Old Piken Ruins, not Scalecatch). The 7-day table is
  baked into `src/entry.cpp` (`kPsnaLinks`) and the current day is
  computed at runtime from the system UTC clock — no network fetch.
  "daily psna" / "psna today" / "today psna" returns only today's 6;
  "psna <weekday>" returns that day's 6; plain "psna" / "pact supply"
  returns all 40 unique locations. The "Copy daily list" button copies
  today's 6 chat links as one 71-character line (GW2 chat limit is 199
  chars/line, GW2 Wiki "Chat panel") — the daily list is PSNA only,
  because no other entry in the dataset carries a "daily" tag. NOT
  added: recipes (random per vendor per day, change 00:00 UTC —
  unpredictable by design).
- Search ranking (see `src/entry.cpp`): rank 0 = every query token
  matches "<display name> <map name> <region>"; rank 1 = every token
  matches one tag phrase. Tokens of 3+ letters match by substring;
  1–2 letter tokens must match a whole word (so "tt" finds Triple
  Trouble, not every "Battlegrounds" map). A query that is also a map
  or region name therefore returns that map's/region's POIs first
  (rank 0) with the tagged waypoint in the list (rank 1); results are
  capped at 250 shown (raised from 100 in v1.6). Verified by the
  149-case replica in `tools/test_search.py` (all pass, 2026-11-17, incl. PSNA day logic + daily-list string).
