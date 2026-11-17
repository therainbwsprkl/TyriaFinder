#!/usr/bin/env python3
"""v1.6 tag additions, part 4: ALL mini dungeons.
Merge into data/tags.json, validating every (name, map) against
data/pois.json (chat_link looked up, not guessed). Same merge pattern
as add_v16_jps.py: phrases are UNIONED onto already-tagged entries —
most mini dungeons overlap jumping puzzles already tagged, so this
adds "mini dungeon" phrases to those entries rather than new ones.

Source: mini-dungeon researcher (2026-11-17), wiki "Jumping puzzle"
table nearest-waypoint column (search snippets — the wiki itself
returns HTTP 403 via browser.open and was not retried), Dulfy Reborn,
GuildJen, ProjektDyad, AyinMaiden, TheGamer, .ru wiki mirror.
22 mini dungeons in scope; 20 verified, 2 NOT tagged (see header of
the COVERAGE.md unverified list):
- Trial of the Elders (Dragon's End): entrance confirmed at Sanctuary
  of Ione POI [&BEgNAAA=], but no source names a nearest waypoint.
  Speakers Waypoint [&BDsNAAA=] is an inference only — NOT tagged.
- From Ruins to Riches (Leysprint Hollows, Castora): entrance at
  Sealed Vault POI [&BCoQAAA=]; no source names a nearest waypoint.
  Sealed Vestibule Waypoint [&BBYQAAA=] is untied to the entrance —
  NOT tagged.
Classification note: Hexfoundry Unhinged, King Jalis's Refuge,
Soaring Copse, Orb Cavern, Coleopteran Cavern, Inquest Cache are
jumping puzzles, NOT mini dungeons (already JP-tagged where
applicable). "Grounded" (Cursed Shore) and "Melandru's Refuge"
(Lake Doric) are not English-wiki mini dungeons. No mini dungeons
were found in HoT, PoF, Ember Bay, Draconis Mons, or Janthir Wilds.
The wiki Category:Mini-dungeons was reported as 23 pages (article +
22 entries) in a Nov 2025 crawl; 22 verified here — 1–2 pre-VoE
entries may be unidentified or the count includes a redirect.
Pig Iron Quarry: wiki nearest is Severed Breach Waypoint; Pig Iron
Waypoint is a swim-in alternative (already JP-tagged to both) — the
mini-dungeon phrases go on Severed Breach only.
Vexa's Lab: single source (GuildJen Mawdrey guide) — flagged.
Hidden Garden: four access waypoints, same as the JP tags (any
keeper's portal works; nearest depends on which keeper event is up).
Run: python3 tools/add_v16_minidungeons.py
Then: python3 tools/apply_tags.py && python3 tools/generate_pois_header.py
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tags_path = os.path.join(BASE, "data", "tags.json")
pois = json.load(open(os.path.join(BASE, "data", "pois.json")))["entries"]
by_nm = {}
for e in pois:
    by_nm.setdefault((e.get("name"), e["map_name"]), []).append(e)

doc = json.load(open(tags_path))
tags = doc["tags"]
by_link_tags = {t["chat_link"]: t for t in tags}

def add(name, map_name, phrases, note):
    matches = by_nm.get((name, map_name))
    if not matches:
        sys.exit(f"v1.6 md: waypoint not in dataset: {name} / {map_name}")
    if len(matches) > 1:
        sys.exit(f"v1.6 md: ambiguous (name, map): {name} / {map_name}")
    e = matches[0]
    t = by_link_tags.get(e["chat_link"])
    if t is None:
        t = {"chat_link": e["chat_link"], "map": e["map_name"],
             "name": e["name"], "tags": [], "note": note}
        tags.append(t)
        by_link_tags[e["chat_link"]] = t
    for p in phrases:
        if p not in t["tags"]:
            t["tags"].append(p)
    if note and note not in t.get("note", ""):
        t["note"] = (t.get("note", "") + " " + note).strip()

def md_tags(name, expansion, map_name):
    return [name, "mini dungeon", "mini-dungeon",
            expansion + " mini dungeon", name + " " + map_name.lower()]

ADD = [
 ("Ojon's Lumbermill Waypoint", "Queensdale",
  md_tags("bad neighborhood", "core", "Queensdale"),
  "Bad Neighborhood mini dungeon (Dulfy Reborn: go to Ojon's Lumbermill Waypoint, SE of Divinity's Reach; alt approach from Shaemoor Waypoint)."),
 ("Tenaebron Waypoint", "Fields of Ruin",
  md_tags("branded mine", "core", "Fields of Ruin"),
  "Branded Mine mini dungeon (wiki Jumping puzzle table; alt: Helliot Mine Waypoint, head north). Also a jumping puzzle."),
 ("Old Piken Ruins Waypoint", "Iron Marches",
  md_tags("chaos crystal cavern", "core", "Iron Marches"),
  "Chaos Crystal Cavern mini dungeon (wiki: west of Old Piken Ruins Waypoint; Dulfy: SW corner, Old Piken Ruins Waypoint). Also a jumping puzzle."),
 ("Okarinoo Waypoint", "Timberline Falls",
  md_tags("coddler's cove", "core", "Timberline Falls"),
  "Coddler's Cove mini dungeon (wiki: entrance inside Mellagan's Grotto, directly south of the Okarinoo point of interest). Also a jumping puzzle."),
 ("Terra Carorunda Waypoint", "Blazeridge Steppes",
  md_tags("craze's folly", "core", "Blazeridge Steppes"),
  "Craze's Folly mini dungeon (wiki: northeast of Terra Carorunda Waypoint; GuildJen + Coine agree). Also a jumping puzzle."),
 ("Font of Rhand Waypoint", "Diessa Plateau",
  md_tags("flame temple tombs", "core", "Diessa Plateau"),
  "Flame Temple Tombs mini dungeon (TheGamer Mawdrey guide: Font of Rhand Waypoint [&BNwAAAA=]; .ru mirror locations infobox. Note: the portal opens only after the Flame Legion Battles meta event)."),
 ("Wyrmblood Waypoint", "Dredgehaunt Cliffs",
  md_tags("forsaken fortune", "core", "Dredgehaunt Cliffs"),
  "Forsaken Fortune mini dungeon (wiki Getting there; Dulfy: entrance just west of Wyrmblood Waypoint, across the icy bridge). A dungeon/JP hybrid — Explorer achievement, not the JP achievement."),
 ("Cuatl Waypoint", "Metrica Province",
  md_tags("goemm's lab", "core", "Metrica Province"),
  "Goemm's Lab mini dungeon (wiki; Dulfy: puzzle entrance just south of Cuatl Waypoint). Also a jumping puzzle."),
 ("Loreclaw Waypoint", "Plains of Ashford",
  md_tags("loreclaw expanse", "core", "Plains of Ashford"),
  "Loreclaw Expanse mini dungeon (wiki; Dulfy: Loreclaw Expanse waypoint in the SE corner of Plains of Ashford). Also a jumping puzzle."),
 ("Severed Breach Waypoint", "Fireheart Rise",
  md_tags("pig iron quarry", "core", "Fireheart Rise"),
  "Pig Iron Quarry mini dungeon (wiki: northeast of Severed Breach Waypoint, on top of the island; alt: swim from Pig Iron Waypoint). Also a jumping puzzle."),
 ("Gleaner's Cove Waypoint", "Caledon Forest",
  md_tags("spekks's laboratory", "core", "Caledon Forest"),
  "Spekks's Laboratory mini dungeon (wiki Jumping puzzle table). Also a jumping puzzle."),
 ("Falias Thorp Waypoint", "Caledon Forest",
  md_tags("tears of itlaocol", "core", "Caledon Forest"),
  "Tears of Itlaocol mini dungeon (.ru mirror: soloable mini-dungeon in Caledon Forest, south of Falias Thorp Waypoint)."),
 ("Pig Iron Waypoint", "Fireheart Rise",
  md_tags("vexa's lab", "core", "Fireheart Rise"),
  "Vexa's Lab mini dungeon (GuildJen Mawdrey guide only — single source: go to Pig Iron Waypoint [&BBcCAAA=] and head north to the entrance). Also a jumping puzzle."),
 ("Breached Wall Waypoint", "Diessa Plateau",
  md_tags("wall breach blitz", "core", "Diessa Plateau"),
  "Wall Breach Blitz mini dungeon (wiki: southwest of Breached Wall Waypoint). Also a jumping puzzle."),
 ("Red Leaf Retreat Waypoint", "Lake Doric",
  md_tags("noran's safe room", "living world", "Lake Doric"),
  "Noran's Safe Room mini dungeon (GuildJen Head of the Snake guide: buy 'Key to Noran's Secret Chest' from the heart NPC at Red Leaf Retreat Waypoint [&BK8JAAA=]; entrance in the basement of Noran's house, Harvest Cascades. Corroborated by AyinMaiden)."),
 ("Village Waypoint", "Seitung Province",
  md_tags("spirit vestibule", "eod", "Seitung Province"),
  "Spirit Vestibule mini dungeon (ProjektDyad, End of Dragons Mini Dungeons: 'The closest Waypoint is Village Waypoint — [&BJ4MAAA=]')."),
 ("Mori Village Waypoint", "The Echovald Wilds",
  md_tags("valdhertz crypts", "eod", "The Echovald Wilds"),
  "Valdhertz Crypts mini dungeon (ProjektDyad: entrance in Quarry Forelands north of Mori Village Waypoint — [&BMcMAAA=]. Requires the hidden 'Cryptseeker' achievement to enter — click the Ancient Lantern at the gate)."),
 ("Jade Gate Waypoint", "The Echovald Wilds",
  md_tags("vasburg armory", "eod", "The Echovald Wilds"),
  "Vasburg Armory mini dungeon (ProjektDyad: start at Jade Gate Waypoint — [&BPkMAAA=] and go southwest to Teleri Village — [&BCkNAAA=], then north into the cave)."),
 ("Pub Canach Waypoint", "Shipwreck Strand",
  md_tags("'booter's path", "voe", "Shipwreck Strand"),
  "'Booter's Path mini dungeon (wiki: from Pub Canach Waypoint, travel north and west to the Twisting Hollows; the entrance is on the northern side of the Hollows). In both the wiki Mini-dungeons and Jumping puzzles categories."),
 ("Criterion Waypoint", "Mount Maelstrom",
  md_tags("hidden garden", "core", "Mount Maelstrom"),
  "Hidden Garden mini dungeon — access via Criterion Waypoint (one of four access waypoints: Criterion, Avernan, Oxbow Isle, Irwin Isle; any keeper's portal works, nearest depends on which keeper event is up). Also a jumping puzzle."),
 ("Avernan Waypoint", "Mount Maelstrom",
  md_tags("hidden garden", "core", "Mount Maelstrom"),
  "Hidden Garden mini dungeon — access via Avernan Waypoint (one of four access waypoints). Also a jumping puzzle."),
 ("Oxbow Isle Waypoint", "Mount Maelstrom",
  md_tags("hidden garden", "core", "Mount Maelstrom"),
  "Hidden Garden mini dungeon — access via Oxbow Isle Waypoint (one of four access waypoints). Also a jumping puzzle."),
 ("Irwin Isle Waypoint", "Mount Maelstrom",
  md_tags("hidden garden", "core", "Mount Maelstrom"),
  "Hidden Garden mini dungeon — access via Irwin Isle Waypoint (one of four access waypoints). Also a jumping puzzle."),
]

for name, map_name, phrases, note in ADD:
    add(name, map_name, phrases, note)

json.dump(doc, open(tags_path, "w"), indent=1)
print(f"v1.6 md: {len(tags)} tagged entries, "
      f"{sum(len(t['tags']) for t in tags)} tag phrases")
