# Materials tags — mob-drop & gathering materials (poultry was the example)

Scope, per Audrey 2026-11-17: **every material, not just poultry**. Poultry was
one example. This note covers the first materials sweep: poultry, mob-drop fine
crafting materials, and a gathering-material gap check. It replaces the
poultry-only framing of the original task.

Date: 2026-11-17. Totals after this sweep (validated):
- `data/tags.json`: **310 tagged entries / 2,390 phrases** (was 298 / 2,257
  before this sweep — +12 entries, +133 phrases; 18 entries touched:
  12 new, 6 updated)
- `tools/apply_tags.py`: pass — "tagged 310 entries in data/pois.json
  (2390 tag phrases)"
- `tools/test_search.py`: **149/149 pass** (test file is a fixed case list;
  new tags were spot-checked separately — see below)

Do NOT rebuild the DLL from this note alone — the v1.8.1 UI-polish build is
in progress separately; these tags are data ready to merge into it.

## 1. How "search for a material / mob" works here

There is **no official GW2 API dataset for mobs or their spawn points**
(`GET /v2/npcs` → 404, `GET /v2/vendors` → 503, checked 2026-11-16).
The only viable source is the GW2 Wiki, plus farm guides. The wiki's
pattern, verified on the pages below, is:

- A **material page** (e.g. Slab of Poultry Meat, Vial of Potent Blood)
  lists 30–80 mobs that drop it, with locations given as a region
  ("Tyria", "Shiverpeak Mountains") or an area ("The Bloodfields") —
  **not a waypoint**.
- A **mob page** (e.g. Golden Moa, Skelk Scavenger) lists areas by map —
  again, **not a waypoint**.
- A **farm guide** (Almarsguides, Hero of the People collection guide)
  sometimes names an exact waypoint — those are the only
  high-confidence links.

So a tag is only added where one of these holds:
(a) a guide/wiki note names the waypoint explicitly, or
(b) a mob's wiki location is a named area whose waypoint/POI of the
same name exists in `data/pois.json` in the same map
(e.g. Skelk Scavenger → The Bloodfields → Bloodfields Waypoint).
Area-level matches are flagged medium confidence in the tag note.
Nothing was invented: no waypoint, chat code, or spawn was guessed.

## 2. Poultry — the original example

"Poultry farming" in GW2 means farming **Slab of Poultry Meat**
(Chef material, WvW feasts, Hungry Cat scavenger hunt). It drops from
moas, raptors, vultures, chickens and other birds — there is no
"poultry node" and no chicken farm you harvest. The two real farms:

| Spot | Waypoint | Chat link | Source |
|---|---|---|---|
| Crimson Moa, NE of Village of Butcher's Block, Diessa Plateau | Bloodcliff Waypoint | `[&BMQDAAA=]` | Wiki, Slab of Poultry Meat, Notes: "hunt Crimson Moa just north-east of the Village of Butcher's Block around Bloodcliff Waypoint — there are packs that re-spawn quickly there." |
| Aggressive Vultures around the Amnoon bazaar, Crystal Oasis | Amnoon Waypoint | `[&BLsKAAA=]` | Wiki, Slab list: Veteran Aggressive Vulture in Free City of Amnoon; Dragon Owl Gaming (2026-07-10) poultry-meat route, Amnoon rooftops/bazaar, ~17 slabs/hour solo |
| Golden Moa, Queensdale | Crossing Waypoint | `[&BPIAAAA=]` | GW2 forum (2015): "Go to Crossing Waypoint in Queensdale. There are a ton of Moa's there."; Hero of the People guide: Golden Moa west of Crossing |
| Golden Moa / Skelk Scavenger, The Bloodfields | Bloodfields Waypoint | `[&BAIEAAA=]` | Wiki, The Bloodfields foe list; wiki, Skelk Scavenger location = The Bloodfields only |

Also tagged: Fallen Angels Garrison Waypoint `[&BFEBAAA=]`
(Fields of Ruin) for "chicken / angry chicken" — wiki Chicken:
farm chickens in the Stronghold of Ebonhawke, SW city; attacking them
spawns Angry Chickens (skyscale Egg of Fear infusion spot).
**Caveat, in the tag note:** this is a chicken *location*, not a
poultry-meat farm. Bloodcliff / Amnoon are the poultry farms.

Chickens themselves drop almost nothing farmable (they are mostly
ambient/non-hostile); "chicken" as a search term now returns the
Ebonhawke farm and the Butcher's Block moa spot, which is the honest
answer to "where are the chickens".

## 3. Mob starter set — what was tagged

18 entries touched. Mob names are tagged as well as material names,
so searching "moa", "skelk", "wolf", "minotaur", "spider", "bandit",
"centaur", "harpy", "jotun", "grawl", "vulture", "chicken" now returns
the waypoint nearest where that mob spawns.

| Waypoint / POI | Map | Chat link | New tags (material + mob) | Source |
|---|---|---|---|---|
| Bloodcliff Waypoint | Diessa Plateau | `[&BMQDAAA=]` | poultry, slab of poultry meat, poultry meat, poultry farm, chicken, crimson moa, moa, moa farm, red meat | Wiki, Slab of Poultry Meat note |
| Amnoon Waypoint | Crystal Oasis | `[&BLsKAAA=]` | poultry, slab of poultry meat, poultry meat, poultry farm, aggressive vulture, vulture, vultures | Wiki, Slab list; Dragon Owl Gaming 2026 |
| Crossing Waypoint | Queensdale | `[&BPIAAAA=]` | golden moa, moa, poultry, slab of poultry meat, poultry meat, egg, red meat, brackish skale, skale, tiny scale, small scale, vial of weak blood, weak blood, bone chip, tiny claw, tiny fang | GW2 forum 2015; Hero of the People guide; wiki Golden Moa drops (Egg, Slab of Poultry Meat, Tiny Claw) |
| Blue Ice Shining Waypoint | Frostgorge Sound | `[&BIUCAAA=]` | skelk, alpine skelk, skelk farm, arctodus, vial of potent blood, potent blood, vial of powerful blood, powerful blood, large fang, vicious fang, large claw, vicious claw | Almarsguides, Frostgorge Skelk & Arctodus (explicit waypoint) |
| Watchful Waypoint | Frostgorge Sound | `[&BH0CAAA=]` | skelk, alpine skelk, vial of potent blood, potent blood, vial of powerful blood, powerful blood, large fang, vicious fang | Almarsguides, secondary skelk camp; closest waypoint Watchful, usually contested — Honor of the Waves / Slough of Despond are fallbacks |
| Breaktooth's Waypoint | Fireheart Rise | `[&BBoCAAA=]` | wolf, wolves, large claw, large fang, vicious claw, vicious fang | Almarsguides, Fireheart Rise Wolf Farming (explicit waypoint) |
| Bloodfields Waypoint | Gendarran Fields | `[&BAIEAAA=]` | golden moa, moa, skelk scavenger, skelk, poultry, slab of poultry meat, vial of thin blood, thin blood, vial of blood, small fang | Wiki, The Bloodfields; wiki, Skelk Scavenger drops (Small Fang, Vial of Blood, Vial of Thin Blood) |
| Northfields Waypoint | Gendarran Fields | `[&BJABAAA=]` | minotaur, minotaurs, vial of thin blood, thin blood, ridgeback skale, skale, small scale, large scale | Almarsguides, Vial of Thin Blood at Minotaurs, Gendarran Fields; Hero guide, Ridgeback Skale north of Northfields |
| Fallen Angels Garrison Waypoint | Fields of Ruin | `[&BFEBAAA=]` | chicken, angry chicken, chickens, poultry | Wiki, Chicken; Cellofrag skyscale guide |
| Arundon Waypoint | Frostgorge Sound | `[&BHgCAAA=]` | minotaur, minotaurs, vial of potent blood, potent blood, large bone, grawl | Almarsguides, Minotaurs in Frostgorge Sound; Hero guide, Minotaurs north of Arundon |
| Sorrow's Embrace Waypoint | Dredgehaunt Cliffs | `[&BD8FAAA=]` | jotun, bone, heavy bone, totem, engraved totem | Almarsguides, Dredgehaunt Cliffs Jotun (Bone & Totems) 45+ |
| Okarinoo Waypoint | Timberline Falls | `[&BEYCAAA=]` | jotun, grawl, heavy bone, engraved totem | Almarsguides, Jotun + Grawl in Timberline Falls (Engraved Totem & Heavy Bones) |
| Behem Waypoint | Blazeridge Steppes | `[&BP0BAAA=]` | canyon spider, spider, spiders, venom sac, scale, smooth scale, large scale | Almarsguides, Blazeridge Scale + Venom Sac Farming; Hero guide, Canyon Spiders east of Behem |
| Vale Waypoint | Queensdale | `[&BPQAAAA=]` | bandit, bandits, vial of weak blood, weak blood, bone chip, tiny claw, rawhide leather, leather | Hero guide, Bandits NE of Vale; Almarsguides, Bandithaunt Caverns, Queensdale |
| Ojon's Lumbermill Waypoint | Queensdale | `[&BPkAAAA=]` | forest spider, spider, spiders, spider leg, venom sac, tiny venom sac | Hero guide, Forest Spiders east of Ojon's |
| Scaver Waypoint | Queensdale | `[&BEUDAAA=]` | tamini, centaur, hoof, vial of weak blood, weak blood, bone chip | Hero guide, Tamini mobs NE of Scaver |
| God's Hand (landmark) | Fireheart Rise | `[&BBMCAAA=]` | harpy, harpies, sharp talon, talon, venom sac | Hero guide, Harpies west of God's Hand POI |
| Noran's Homestead (landmark) | Lake Doric | `[&BKsJAAA=]` | centaur, centaurs, thick leather, thick leather section, leather farm, leather | Lake Doric leather farm: centaur-inhabited NE map, mostly Thick Leather Sections (2022 source). Noran's Homestead is the named POI in that NE area — **medium confidence, area-level**, not a named waypoint in the source. |

Spot-checks after `apply_tags.py` (searching `data/pois.json`):
- "poultry" → 5 results (Amnoon, Bloodcliff, Fallen Angels, Bloodfields, Crossing)
- "moa" → 4 (Bloodcliff, Bloodfields, Crossing, + Coil Waypoint from the
  earlier Nonmoa Lake dive tag — a false-positive name match, pre-existing)
- "skelk" → 3 (Blue Ice Shining, Watchful, Bloodfields)
- "vicious fang" → 3 (Breaktooth's, Blue Ice Shining, Watchful)
- "thick leather" → 1 (Noran's Homestead)
- "chicken" → 2 (Bloodcliff, Fallen Angels Garrison)
- "minotaur" → 2 (Arundon, Northfields)
- "spider" → 2 (Behem, Ojon's Lumbermill)

### Mob sample — coverage check (20 farm mobs sampled)

19 of 20 sampled mobs had a verifiable nearest waypoint by the rules
above. The sample was deliberately biased toward farm-guide mobs, so
this is **not** a claim about mobs in general.

Verifiable: Golden Moa, Crimson Moa, Aggressive Vulture, Alpine Skelk,
Skelk Scavenger, Arctodus, Fireheart Wolf, Minotaur, Jotun, Grawl,
Canyon Spider, Forest Spider, Harpy, Bandit, Tamini, Brackish Skale,
Ridgeback Skale, Chicken, Lake Doric Centaur (medium).
Not verifiable: **Risen Raptor** — wiki Slab list gives only
"Cursed Shore / Malchor's Leap"; the old Union Waypoint farm
(Almarsguides, nerfed 2013) has no verified current waypoint, so it
was not tagged.

The honest general picture: most of the ~26,500 wiki NPC pages list
only an area, and most material pages list 30–80 droppers across a
whole region. Picking *one* nearest waypoint for an arbitrary mob is
usually unverifiable. A "search any mob" feature that is honest needs
either (a) a curated starter set like this one, expanded mob by mob,
or (b) a new data source (e.g. a community mob-location dataset) —
neither the wiki nor the official API provides a complete one today.

## 4. Gathering materials — gap sweep

Already tagged before this sweep (no change needed): all rich ore
veins (copper, silver, gold, iron, platinum, mithril, orichalcum),
all wood tiers (soft, seasoned, hard, elder — green wood was already
covered by the copper/ore hubs), quartz crystal, rich quartz, flax
(9 spots). Searching "copper", "mithril", "elder wood", "flax",
"quartz" already works.

**Not yet searchable, and not tagged in this sweep — no verified
single farm waypoint found:**
- Cooking plants / vegetables: onion, carrot, potato, lettuce, herb
  seedling, button mushroom, blueberry, strawberry, etc. These grow
  at scattered nodes / vegetable farms across many maps; no published
  single "best" waypoint was verified for any one of them in this
  pass. (Almarsguides lists a Mature Herb farm in Bloodtide Coast
  and a Chilli Pepper farm, but the waypoint for each was not
  verified — do not tag from a video title alone.)
- Dust: Pile of Glittering / Shimmering / Radiant / Luminous /
  Incandescent / Crystalline Dust. Dropped by elementals and from
  loot bags everywhere; no single farm waypoint verified.
- Cloth scraps: Jute / Wool / Cotton / Linen / Silk / Gossamer.
  Salvaged from armour and dropped (as bags) by humanoids; no single
  farm waypoint verified. Bandit spots (Vale / Ojon) are the closest
  existing lead, but "bandits drop cloth" was not verified to a
  specific material tier, so it was not tagged.
- Lodestones (Charged, Onyx, Molten, Corrupted, etc.): event / mob
  specific, no single farm waypoint verified in this pass.
- Snow Truffle, Passion Flower, Omnomberry, etc.: rare node materials,
  no single waypoint verified.

## 5. Mob-drop fine materials — what is now searchable, tier by tier

Fine crafting materials are 8 families × 6 tiers. This sweep covers
them **partially** — one farm waypoint per family where a guide
verified it. A material name that is *not* listed below is not yet
searchable by that exact name (searching the mob or the family word,
e.g. "fang", may still return a spot).

- **Blood:** Vial of Weak Blood (Crossing, Vale, Scaver), Vial of
  Thin Blood (Bloodfields, Northfields), Vial of Blood (Bloodfields),
  Vial of Potent Blood (Blue Ice Shining, Watchful, Arundon),
  Vial of Powerful Blood (Blue Ice Shining, Watchful).
  **Missing:** Vial of Thick Blood (tier 4) — no verified farm spot.
- **Bone:** Bone Chip (Crossing, Vale, Scaver), Bone (Sorrow's
  Embrace, generic "bone"), Heavy Bone (Sorrow's, Okarinoo),
  Large Bone (Arundon). **Missing:** Ancient Bone (tier 6).
- **Claw:** Tiny Claw (Crossing, Vale), Large Claw (Blue Ice,
  Breaktooth's), Vicious Claw (Blue Ice, Breaktooth's).
  **Missing:** Small Claw, Claw, Sharp Claw (tiers 2–4).
- **Fang:** Tiny Fang (Crossing), Small Fang (Bloodfields),
  Large Fang (Blue Ice, Watchful, Breaktooth's), Vicious Fang
  (Blue Ice, Watchful, Breaktooth's). **Missing:** Sharp Fang.
- **Scale:** Tiny Scale, Small Scale (Crossing, Northfields),
  Smooth Scale, Large Scale (Behem, Northfields). **Missing:**
  Scale (tier 3, generic — "scale" does return Behem), Armored
  Scale (tier 6).
- **Totem:** Totem, Engraved Totem (Sorrow's, Okarinoo).
  **Missing:** Tiny / Small / Intricate / Elaborate Totem.
- **Venom Sac:** Venom Sac (Behem, Ojon's, God's Hand), Tiny Venom
  Sac (Ojon's). **Missing:** Small Venom Sac, Full Venom Sac,
  Potent Venom Sac, Powerful Venom Sac.
- **Leather sections:** Rawhide Leather (Vale), Thick Leather
  Section (Noran's Homestead). **Missing as a search term:**
  Thin / Coarse / Rugged / Hardened Leather Section — these come
  from salvaging armour / loot bags, not from a mob farm, so there
  is no honest single waypoint for them.
- **Meat:** Slab of Poultry Meat (5 spots, §2), Slab of Red Meat /
  Cut of Quality Red Meat (Bloodcliff, Crossing — Golden/Crimson
  Moa drops). **Missing:** Slab of Red Meat as a dedicated farm
  (beasts generally; no single spot verified).

## 6. What "every material" realistically means

The game has **150+ crafting materials** (8 fine families × 6 tiers,
6 leather, 6 cloth, ores, wood, plants, dust, lodestones, cooking
ingredients, expansion materials like Mithril, etc.), and **thousands
of mobs**. A complete "search any material → waypoint" and "search
any mob → waypoint" is **not feasible from the wiki alone**, for the
reasons in §1: most entries have no waypoint-level location at all.

Realistic scope, in order:
1. **Done in this sweep:** poultry + a starter mob set (18 waypoints)
   covering the most-searched farm families at tiers 1, 3, 5 and 6.
2. **Next, highest value:** fill the missing tier-4/6 fine materials
   (Vial of Thick Blood, Sharp Fang/Claw, Ancient Bone, Armored
   Scale, Intricate/Elaborate Totem, Potent/Powerful Venom Sac) —
   one verified farm waypoint each, same rules. Expect ~6–10 more
   waypoints.
3. **Then:** cooking plants with a verified vegetable-farm waypoint
   each (only where a guide names one), and dust/cloth only if a
   verifiable farm emerges — otherwise leave them honestly
   unsearchable rather than tagging a guess.
4. **Not feasible without a new data source:** literally every mob
   (26,500+ wiki NPC pages) and literally every material. If Audrey
   wants a specific mob or material next, name it and it can be
   researched and tagged the same way, one at a time.

## Sources

- GW2 Wiki, Slab of Poultry Meat —
  https://wiki.guildwars2.com/wiki/Slab_of_Poultry_Meat
  (drop table; note on Crimson Moa at Bloodcliff Waypoint)
- GW2 Wiki, Chicken — https://wiki.guildwars2.com/wiki/Chicken
  (locations; Ebonhawke farm / Angry Chickens)
- GW2 Wiki, Golden Moa — https://wiki.guildwars2.com/wiki/Golden_Moa
  (locations; drops: Egg, Slab of Poultry Meat, Tiny Claw)
- GW2 Wiki, Skelk Scavenger —
  https://wiki.guildwars2.com/wiki/Skelk_Scavenger
  (location: The Bloodfields only; drops: Small Fang, Vial of Blood,
  Vial of Thin Blood)
- GW2 Wiki, Moa — https://wiki.guildwars2.com/wiki/Moa ;
  Skelk — https://wiki.guildwars2.com/wiki/Skelk
  (family lists; no waypoint-level locations — this is the limit)
- GW2 Wiki, Vial of Potent Blood —
  https://wiki.guildwars2.com/wiki/Vial_of_Potent_Blood
  (drop table: 60+ mobs, locations are regions/areas, not waypoints)
- Almarsguides, Guild Wars 2 Farming Locations —
  https://almarsguides.com/computer/games/guildwars2/farming/
  (index: Weak Blood Queensdale, Thin Blood Minotaurs/Bats Gendarran,
  Jotun Dredgehaunt, Fang Dredgehaunt, Scale/Venom Blazeridge,
  Sharp Fang Iron Marches, Wolves Fireheart, Jotun/Grawl Timberline,
  Minotaurs Frostgorge, Skelk & Arctodus Frostgorge)
- Almarsguides, Frostgorge Skelk & Arctodus —
  https://almarsguides.com/computer/games/guildwars2/farming/locations/skelk.cfm
  (Blue Ice Shining Waypoint; Watchful Waypoint secondary)
- Almarsguides, Fireheart Rise Wolf Farming —
  https://almarsguides.com/computer/games/guildwars2/farming/locations/fireheartrisewolves.cfm
  (Breaktooth's Waypoint)
- Dragon Owl Gaming, GW2 Poultry Meat farm, Crystal Oasis (2026-07-10,
  via Facebook reel) — Aggressive Vultures, Amnoon bazaar, ~17 slabs/hour
- GW2 Forum (archive, 2015), poultry farming thread —
  "Go to Crossing Waypoint in Queensdale. There are a ton of Moa's there."
  (forum-en.gw2archive.eu)
- Hero of the People collection guide (GuildWars2 wiki community guide,
  via cdn-cms.f-static.net) — Golden Moa west of Crossing, Brackish
  Skale south of Crossing, Harpies west of God's Hand, Forest Spiders
  east of Ojon's, Bandits NE of Vale, Tamini NE of Scaver, Minotaurs
  north of Arundon, Canyon Spiders east of Behem, Ridgeback Skale
  north of Northfields, Branded south of Tenaebron
- Allakhazam, Crafting (GW2) —
  https://camelot.allakhazam.com/wiki/Crafting_(GW2)
  (fine-material tier table: Blood/Bone/Claw/Dust/Fang/Scale/Totem/
  Venom, tiers I–VI)
- Lake Doric leather farm (2022 source, via search) — centaur NE Lake
  Doric, mostly Thick Leather Sections
- Dataset: `data/pois.json` (3,773 entries) and `data/tags.json`
  (310 entries after this sweep); validation: `tools/apply_tags.py`,
  `tools/test_search.py` (149/149)
