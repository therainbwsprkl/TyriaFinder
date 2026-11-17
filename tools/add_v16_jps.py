#!/usr/bin/env python3
"""v1.6 tag additions, part 1: ALL jumping puzzles (wiki list) + Creeping
Crevasse mastery insight. Merge into data/tags.json, validating every
(name, map) against data/pois.json (chat_link looked up, not guessed).
Same merge pattern as add_v13_tags.py / add_v14_tags.py, plus:
- if an entry is already tagged, new phrases are UNIONED onto it
- BY_LINK entries are keyed by explicit chat_link (for Obsidian Sanctum:
  three dataset entries share name+map, one per WvW team colour)
Run: python3 tools/add_v16_jps.py
Then: python3 tools/apply_tags.py && python3 tools/generate_pois_header.py

Source: GW2 Wiki "Jumping puzzle" list table (fetched 2026-11-17),
nearest-waypoint column, cross-checked against the dataset (every
waypoint below exists in data/pois.json with the name/map shown).
Discrepancies with the v1.3 Dulfy-sourced tags are kept, not smoothed
over: where wiki and Dulfy name different nearest waypoints, BOTH are
tagged (multi-spot model) and the difference is noted in README.md:
- Pig Iron Quarry: wiki Severed Breach, Dulfy Pig Iron Waypoint
- Spekk's Laboratory / Spelunker's Delve: wiki has Spekk's at
  Gleaner's Cove and Spelunker's at Astorea; v1.3 (Dulfy) had them
  swapped (Spekk's at Astorea). Both waypoints now carry both phrases.
- Shaman's Rookery: wiki Zelechor Hot Springs, Dulfy Osenfold
- Urmaug's Secret / Weyandt's Revenge: wiki has Urmaug's at Guild
  Bluff and Weyandt's at Farshore; v1.3 had Urmaug's at Farshore.
  Farshore now carries both, Guild Bluff carries Urmaug's.
- Tribulation Rift Scaffolding / Caverns: wiki Sorrow's Embrace
  Waypoint, v1.3 Tribulation Waypoint. Both tagged.
- Hidden Garden: wiki lists 4 access waypoints (Criterion, Avernan,
  Oxbow Isle, Irwin Isle); v1.3 tagged Govoran (Conundrum Cubed
  entrance). All 5 now carry "hidden garden".
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tags_path = os.path.join(BASE, "data", "tags.json")
pois = json.load(open(os.path.join(BASE, "data", "pois.json")))["entries"]
by_nm = {}
for e in pois:
    by_nm.setdefault((e.get("name"), e["map_name"]), []).append(e)
by_link = {e["chat_link"]: e for e in pois}

doc = json.load(open(tags_path))
tags = doc["tags"]
by_link_tags = {t["chat_link"]: t for t in tags}

def add(name, map_name, phrases, note):
    matches = by_nm.get((name, map_name))
    if not matches:
        sys.exit(f"v1.6 JP: waypoint not in dataset: {name} / {map_name}")
    if len(matches) > 1:
        sys.exit(f"v1.6 JP: ambiguous (name, map): {name} / {map_name} "
                 f"({len(matches)} entries) — use BY_LINK instead")
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

def add_by_link(chat_link, phrases, note):
    e = by_link.get(chat_link)
    if e is None:
        sys.exit(f"v1.6 JP: chat_link not in dataset: {chat_link}")
    t = by_link_tags.get(chat_link)
    if t is None:
        t = {"chat_link": e["chat_link"], "map": e["map_name"],
             "name": e["name"], "tags": [], "note": note}
        tags.append(t)
        by_link_tags[chat_link] = t
    for p in phrases:
        if p not in t["tags"]:
            t["tags"].append(p)

JP = "jumping puzzle"
# (name, map, [extra phrases beyond name + "jumping puzzle" + "jp"], note)
ADD = [
 # --- Ascalon: new (Loreclaw, Grendich, Wall Breach, Behem, Craze's,
 #     Chaos Crystal already tagged in v1.3) ---
 ("Redreave Mill Waypoint", "Diessa Plateau",
  ["crimson plateau", JP, "jp", "core jumping puzzle"],
  "Crimson Plateau JP (wiki Jumping puzzle list)."),
 ("Tenaebron Waypoint", "Fields of Ruin",
  ["branded mine", JP, "jp", "core jumping puzzle"],
  "Branded Mine JP (wiki Jumping puzzle list)."),
 ("Dalada Forest Waypoint", "Grothmar Valley",
  ["gauntlet of the khan-ur", "khan-ur", JP, "jp", "icebrood saga jumping puzzle"],
  "Gauntlet of the Khan-Ur JP (wiki Jumping puzzle list)."),
 ("Severed Breach Waypoint", "Fireheart Rise",
  ["pig iron quarry", JP, "jp", "core jumping puzzle"],
  "Pig Iron Quarry JP, wiki nearest waypoint (v1.3/Dulfy tagged Pig Iron Waypoint instead — both tagged)."),
 # --- Cantha (End of Dragons) ---
 ("Monastery Waypoint", "Seitung Province",
  ["trials of the tengu", JP, "jp", "cantha jumping puzzle", "eod jumping puzzle"],
  "Trials of the Tengu JP (wiki Jumping puzzle list)."),
 ("Lutgardis Plaza Waypoint", "New Kaineng City",
  ["wind through the walls", JP, "jp", "cantha jumping puzzle", "eod jumping puzzle"],
  "Wind through the Walls JP (wiki Jumping puzzle list)."),
 # --- Crystal Desert ---
 ("Yatendi Village Waypoint", "Jahai Bluffs",
  ["displaced vizier's tower", "vizier's tower", JP, "jp", "living world jumping puzzle"],
  "Displaced Vizier's Tower JP (wiki Jumping puzzle list)."),
 # --- Heart of Maguuma: mastery-insight JPs (wiki lists them as JPs) ---
 ("Pact Encampment Waypoint", "Verdant Brink",
  ["verdant brink insight: canopy over pact encampment", "canopy over pact encampment", JP, "jp", "hot jumping puzzle", "mastery insight"],
  "Verdant Brink Insight: Canopy Over Pact Encampment (wiki Jumping puzzle list; mastery insight)."),
 ("Forgotten City Waypoint", "Auric Basin",
  ["egg bearer", JP, "jp", "hot jumping puzzle", "mastery insight"],
  "Egg Bearer JP in the Inner Chamber of Tarir (wiki Jumping puzzle list; mastery insight)."),
 ("Westwatch Waypoint", "Auric Basin",
  ["highest gear", JP, "jp", "hot jumping puzzle", "mastery insight"],
  "Highest Gear JP, past the Ancient Golem Part hero challenge (wiki Jumping puzzle list; mastery insight)."),
 ("Ogre Camp Waypoint", "Tangled Depths",
  ["disco dancing delver", JP, "jp", "hot jumping puzzle", "mastery insight"],
  "Disco Dancing Delver JP under The Great Tree (wiki Jumping puzzle list; mastery insight)."),
 ("Rata Novus Waypoint", "Tangled Depths",
  ["master mushroom spelunker", JP, "jp", "hot jumping puzzle", "mastery insight"],
  "Master Mushroom Spelunker JP (wiki Jumping puzzle list; mastery insight)."),
 # --- Janthir Wilds ---
 ("Harvest Den Waypoint", "Lowland Shore",
  ["treetop beehive", JP, "jp", "janthir jumping puzzle"],
  "Treetop Beehive JP at Apiary Holt (wiki Jumping puzzle list)."),
 ("Hot Springs Waypoint", "Lowland Shore",
  ["vale brazier", JP, "jp", "janthir jumping puzzle"],
  "Vale Brazier JP at Lamplighter's Perch (wiki Jumping puzzle list)."),
 ("Autumn's Vale Waypoint", "Lowland Shore",
  ["queen's confidence", JP, "jp", "janthir jumping puzzle"],
  "Queen's Confidence JP (wiki Jumping puzzle list)."),
 ("Hidden Nodule Waypoint", "Bava Nisos",
  ["traversing the titan", JP, "jp", "janthir jumping puzzle"],
  "Traversing the Titan JP inside the Hidden Nodule (wiki Jumping puzzle list)."),
 # --- Kryta: new (Troll's End, Not So Secret, Portmatt's already tagged) ---
 ("Fort Marriner Waypoint", "Lion's Arch",
  ["troll's revenge", JP, "jp", "core jumping puzzle"],
  "Troll's Revenge JP (wiki Jumping puzzle list)."),
 ("Guild Bluff Waypoint", "Lion's Arch",
  ["urmaug's secret", JP, "jp", "core jumping puzzle"],
  "Urmaug's Secret JP, wiki nearest waypoint (v1.3/Dulfy tagged Farshore Waypoint instead — both tagged)."),
 ("Farshore Waypoint", "Lion's Arch",
  ["weyandt's revenge", JP, "jp", "core jumping puzzle"],
  "Weyandt's Revenge JP in Sharkmaw Caverns (wiki Jumping puzzle list; v1.3 tagged this waypoint as Urmaug's Secret — it now carries both)."),
 ("Godslost Waypoint", "Queensdale",
  ["demongrub pits", JP, "jp", "core jumping puzzle"],
  "Demongrub Pits JP (wiki Jumping puzzle list)."),
 ("Cornucopian Fields Waypoint", "Gendarran Fields",
  ["swashbuckler's cove", JP, "jp", "core jumping puzzle"],
  "Swashbuckler's Cove JP (wiki Jumping puzzle list)."),
 ("Arcallion Waypoint", "Harathi Hinterlands",
  ["fawcett's bounty", "fawcett's revenge", JP, "jp", "core jumping puzzle"],
  "Fawcett's Bounty JP north of Arca Lake (wiki Jumping puzzle list; falling in a pit near the start gives Fawcett's Revenge)."),
 ("Lion Point Waypoint", "Southsun Cove",
  ["skipping stones", JP, "jp", "core jumping puzzle"],
  "Skipping Stones JP in the cave south of the waypoint (wiki Jumping puzzle list)."),
 ("Pearl Islet Waypoint", "Southsun Cove",
  ["under new management", JP, "jp", "core jumping puzzle"],
  "Under New Management JP east of the waypoint (wiki Jumping puzzle list)."),
 # --- Maguuma Jungle: new (Morgan's Leap, Dark Reverie, Goemm's,
 #     Conundrum Cubed already tagged) ---
 ("Gleaner's Cove Waypoint", "Caledon Forest",
  ["spekk's laboratory", "spekk's lab", JP, "jp", "core jumping puzzle"],
  "Spekk's Laboratory JP, wiki nearest waypoint (v1.3/Dulfy tagged Astorea Waypoint instead — both tagged, both waypoints carry both phrases)."),
 ("Astorea Waypoint", "Caledon Forest",
  ["spelunker's delve", JP, "jp", "core jumping puzzle"],
  "Spelunker's Delve JP, wiki nearest waypoint (v1.3 tagged this waypoint as Spekk's Lab — it now carries both)."),
 ("Criterion Waypoint", "Mount Maelstrom",
  ["hidden garden", JP, "jp", "core jumping puzzle"],
  "Hidden Garden JP, one of 4 access waypoints (wiki Jumping puzzle list; v1.3 tagged Govoran instead)."),
 ("Avernan Waypoint", "Mount Maelstrom",
  ["hidden garden", JP, "jp", "core jumping puzzle"],
  "Hidden Garden JP, one of 4 access waypoints (wiki Jumping puzzle list)."),
 ("Oxbow Isle Waypoint", "Mount Maelstrom",
  ["hidden garden", JP, "jp", "core jumping puzzle"],
  "Hidden Garden JP, one of 4 access waypoints (wiki Jumping puzzle list)."),
 ("Irwin Isle Waypoint", "Mount Maelstrom",
  ["hidden garden", JP, "jp", "core jumping puzzle"],
  "Hidden Garden JP, one of 4 access waypoints (wiki Jumping puzzle list)."),
 ("Darkweather Waypoint", "Sparkfly Fen",
  ["hexfoundry unhinged", JP, "jp", "core jumping puzzle"],
  "Hexfoundry Unhinged JP (wiki Jumping puzzle list)."),
 ("Ocean's Gullet Waypoint", "Sparkfly Fen",
  ["verarium delves", JP, "jp", "core jumping puzzle"],
  "Verarium Delves JP (wiki Jumping puzzle list)."),
 # --- Maguuma Wastes ---
 ("Prosperity Waypoint", "Dry Top",
  ["prospect valley crash site", JP, "jp", "living world jumping puzzle"],
  "Prospect Valley Crash Site JP at Crash Site (wiki Jumping puzzle list)."),
 ("Drydock Grotto Waypoint", "The Silverwastes",
  ["retrospective runaround", JP, "jp", "living world jumping puzzle"],
  "Retrospective Runaround JP at SS Topsy-Turvy (wiki Jumping puzzle list)."),
 # --- Ring of Fire ---
 ("Castaway Circus Waypoint", "Ember Bay",
  ["skip up the volcano", "chalice of tears", JP, "jp", "living world jumping puzzle"],
  "Skip up the Volcano JP, also known as Chalice of Tears (wiki Jumping puzzle list; the Chalice of Tears landmark is tagged as-is too)."),
 ("Heathen's Hold Waypoint", "Draconis Mons",
  ["searing ascent", JP, "jp", "living world jumping puzzle"],
  "Searing Ascent JP at the Searing Ascent POI (wiki Jumping puzzle list; the Searing Ascent landmark is tagged as-is too)."),
 # --- Ruins of Orr: new (Antre, Scavenger's already tagged) ---
 ("Lone Post Waypoint", "Straits of Devastation",
  ["vizier's tower", JP, "jp", "core jumping puzzle"],
  "Vizier's Tower JP on the island east of the waypoint (wiki Jumping puzzle list)."),
 ("Shipwreck Rock Waypoint", "Cursed Shore",
  ["buried archives", JP, "jp", "core jumping puzzle"],
  "Buried Archives JP (wiki Jumping puzzle list)."),
 ("Camp Reclamation Waypoint", "Siren's Landing",
  ["abaddon's ascent", "abaddon ascent", JP, "jp", "living world jumping puzzle"],
  "Abaddon's Ascent JP (wiki Jumping puzzle list)."),
 # --- Shiverpeak Mountains: new (Shaman's Rookery, Griffonrook,
 #     Tribulation Rift/Caverns, Coddler's, Only Zuhl, Shattered Ice
 #     already tagged) ---
 ("Zelechor Hot Springs Waypoint", "Wayfarer Foothills",
  ["shaman's rookery", JP, "jp", "core jumping puzzle"],
  "Shaman's Rookery JP, wiki nearest waypoint (v1.3/Dulfy tagged Osenfold Waypoint instead — both tagged)."),
 ("Snowhawk Landing Waypoint", "Snowden Drifts",
  ["king jalis's refuge", "king jalis refuge", JP, "jp", "core jumping puzzle"],
  "King Jalis's Refuge JP (wiki Jumping puzzle list)."),
 ("Sorrow's Embrace Waypoint", "Dredgehaunt Cliffs",
  ["tribulation rift scaffolding", "tribulation caverns", JP, "jp", "core jumping puzzle"],
  "Tribulation Rift Scaffolding + Tribulation Caverns JPs, wiki nearest waypoint (v1.3 tagged Tribulation Waypoint instead — both tagged)."),
 # --- The Mists ---
 ("Lounge Atrium Waypoint", "Armistice Bastion",
  ["armistice bastion", JP, "jp", "wvw jumping puzzle"],
  "Armistice Bastion JP north of the waypoint (wiki Jumping puzzle list)."),
 ("Fort Marriner Waypoint", "Lion's Arch",
  ["mistlock mountaineer", JP, "jp", "fractal jumping puzzle"],
  "Mistlock Mountaineer JP in the Mistlock Observatory (wiki Jumping puzzle list; reached from Lion's Arch)."),
 # --- Festivals ---
 ("Crown Pavilion Waypoint", "Divinity's Reach",
  ["winter wonderland", JP, "jp", "festival jumping puzzle", "wintersday jumping puzzle"],
  "Winter Wonderland JP, Wintersday only, via Crown Pavilion Waypoint (wiki Jumping puzzle list)."),
 ("Trader's Forum Waypoint", "Lion's Arch",
  ["mad king's clock tower", "stopped clock tower", JP, "jp", "festival jumping puzzle", "halloween jumping puzzle"],
  "Mad King's Clock Tower + Stopped Clock Tower JPs, Halloween only (wiki Jumping puzzle list)."),
 # --- Creeping Crevasse: NOT a JP and NOT a POI in the dataset — it is
 #     a Verdant Brink mastery-insight area, reached from Shipwreck Peak.
 #     Tag that waypoint so the search still finds the way there.
 #     (by chat_link: two dataset entries share the name, map 1052 is
 #     the open-world Verdant Brink one, [&BN4HAAA=].) ---
]

for name, map_name, phrases, note in ADD:
    add(name, map_name, phrases, note)

# Obsidian Sanctum: three dataset entries share name+map (one per WvW
# team colour, [&BAIHAAA=] / [&BAMHAAA=] / [&BAQHAAA=]); tag all three.
for link in ("[&BAIHAAA=]", "[&BAMHAAA=]", "[&BAQHAAA=]"):
    add_by_link(link, ["obsidian sanctum", JP, "jp", "wvw jumping puzzle"],
                "Obsidian Sanctum JP, accessed from the three keeps in Eternal Battlegrounds (wiki Jumping puzzle list).")

# Creeping Crevasse mastery insight -> Shipwreck Peak Waypoint (open-world
# Verdant Brink, map 1052), by chat_link (see note above).
add_by_link("[&BN4HAAA=]",
            ["creeping crevasse", "creeping crevasse insight", "verdant brink insight", "mastery insight"],
            "Creeping Crevasse mastery insight (Verdant Brink Insight: Creeping Crevasse) — glide west from Shipwreck Peak Waypoint (Dulfy mastery-insight guide; TheGamer). No POI by this name exists in the API dataset, so the waypoint is tagged instead.")

json.dump(doc, open(tags_path, "w"), indent=1)
print(f"v1.6 JP: {len(tags)} tagged entries, "
      f"{sum(len(t['tags']) for t in tags)} tag phrases")
