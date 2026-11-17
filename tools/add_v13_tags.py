#!/usr/bin/env python3
"""v1.3 tag additions: merge into data/tags.json, validating every
(name, map) against data/pois.json (chat_link is looked up, not guessed).
Run: python3 tools/add_v13_tags.py
Then: python3 tools/apply_tags.py && python3 tools/generate_pois_header.py
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pois = json.load(open(os.path.join(BASE, "data", "pois.json")))["entries"]
by_nm = {}
for e in pois:
    by_nm.setdefault((e.get("name"), e["map_name"]), []).append(e)

# (name, map, [tags], note or "")
ADD = [
 # --- 1. Event Timers metas (Cellofrag timer index, wiki v5.4 data; per-event guides) ---
 ("Pact Base Camp Waypoint", "Dragon's Stand",
  ["dragon's stand", "against the mouth of mordremoth", "mouth of mordremoth", "mordremoth", "meta event"],
  "Dragon's Stand meta staging: Preparation @ [&BBAIAAA=] (InGameTimer)."),
 ("Camp Resolve Waypoint", "The Silverwastes",
  ["silverwastes", "riba", "mordrem vinewrath", "vinewrath", "meta event"],
  "RIBA cycle: Camp Resolve is the primary waypoint (Hardstuck RIBA guide; GuildWarsHub)."),
 ("Jaka Itzel Waypoint", "Verdant Brink",
  ["verdant brink night", "night bosses", "verdant brink", "meta event"],
  "Verdant Brink night meta (5 night bosses, map-wide); Jaka Itzel is the central hub waypoint."),
 ("Provern Shore Waypoint", "Gendarran Fields",
  ["ley-line anomaly", "ley-line anomaly gendarran", "anomaly", "meta event"],
  "Ley-Line Anomaly (Gendarran Fields rotation): timer code [&BOQAAAA=] IS Provern Shore Waypoint."),
 ("Prosperity Waypoint", "Dry Top",
  ["dry top", "sandstorm", "crash site", "meta event"],
  "Dry Top meta (Crash Site / sandstorm cycle); Prosperity is the central Dry Top waypoint."),
 ("Doric's Landing Waypoint", "Lake Doric",
  ["lake doric", "queenslayer", "meta event"],
  "Lake Doric meta; Doric's Landing is the map's main entry waypoint."),
 ("Amnoon Waypoint", "Crystal Oasis",
  ["casino blitz", "pinata", "casino", "meta event"],
  "Casino Blitz / pinata meta takes place in Amnoon."),
 ("Champion's Dawn Waypoint", "Domain of Istan",
  ["palawadan", "istan", "meta event"],
  "Palawadan meta (Domain of Istan); Champion's Dawn is the Istan entry waypoint."),
 ("Harvest Complex Waypoint", "Dragon's End",
  ["dragon's end", "battle for the jade sea", "soo-won", "soo won", "meta event"],
  "Battle for the Jade Sea (Soo-Won) staging at Harvest Complex, Dragon's End."),
 ("Bastion of the Celestial Waypoint", "Amnytas",
  ["defense of amnytas", "amnytas", "meta event"],
  "Defense of Amnytas meta, Amnytas."),
 ("Astral Ward Encampment Waypoint", "Skywatch Archipelago",
  ["skywatch", "wizard's court", "meta event"],
  "Skywatch Archipelago meta (Defend the Wizard's Court); Astral Ward Encampment is the hub waypoint."),
 ("Mantle's Arrival Waypoint", "Bava Nisos",
  ["a titanic voyage", "titanic voyage", "bava nisos", "meta event"],
  "A Titanic Voyage meta, Bava Nisos; Mantle's Arrival is the Bava entry waypoint."),
 ("Stricken Plains Waypoint", "Janthir Syntri",
  ["of mists and monsters", "janthir syntri", "meta event"],
  "Of Mists and Monsters meta, Janthir Syntri; Stricken Plains is the main camp waypoint."),
 ("Eye of the North Waypoint", "Eye of the North",
  ["dragonstorm", "twisted marionette", "battle for lion's arch", "tower of nightmares", "public instance", "meta event"],
  "Eye of the North public instances (Dragonstorm, Twisted Marionette, Battle for Lion's Arch, Tower of Nightmares) all start from the Eye of the North."),
 ("Tower Courtyard Waypoint", "The Wizard's Tower",
  ["convergence", "outer nayos convergence", "mount balrior convergence", "nexus of eternity convergence", "meta event"],
  "Public Convergences are entered from the Wizard's Tower (Tower Courtyard)."),
 ("Lutgardis Plaza Waypoint", "New Kaineng City",
  ["kaineng blackout", "blackout", "meta event"],
  "Kaineng Blackout meta, New Kaineng City; Lutgardis Plaza is the central Kaineng hub waypoint."),
 ("Village Waypoint", "Seitung Province",
  ["aetherblade assault", "seitung", "meta event"],
  "Aetherblade Assault meta, Seitung Province; Village is the Seitung hub waypoint."),
 # --- 2. Dungeons / fractals / strikes / raids ---
 ("Ascalonian Catacombs Waypoint", "Plains of Ashford",
  ["ascalonian catacombs", "dungeon", "ac"], "Dungeon entrance waypoint."),
 ("Beetletun Waypoint", "Queensdale",
  ["caudecus's manor", "caudecus manor", "dungeon", "cm"],
  "Caudecus's Manor entrance is south of Beetletun; code [&BPoAAAA=] per GW2 F2P dungeon list."),
 ("Twilight Arbor Waypoint", "Caledon Forest",
  ["twilight arbor dungeon", "dungeon", "ta"], "Dungeon entrance waypoint (also Great Jungle Wurm, already tagged)."),
 ("Tribulation Waypoint", "Dredgehaunt Cliffs",
  ["sorrow's embrace", "dungeon", "se"], "Sorrow's Embrace entrance waypoint."),
 ("The Citadel of Flame Waypoint", "Fireheart Rise",
  ["citadel of flame dungeon", "dungeon", "cof"], "Dungeon entrance waypoint (also Rich Mithril, already tagged)."),
 ("Honor of the Waves Waypoint", "Frostgorge Sound",
  ["honor of the waves", "dungeon", "hotw"], "Dungeon entrance waypoint."),
 ("Crucible of Eternity Waypoint", "Mount Maelstrom",
  ["crucible of eternity", "dungeon", "coe"], "Dungeon entrance waypoint."),
 ("Arah Waypoint", "Cursed Shore",
  ["ruined city of arah", "arah", "dungeon"], "Dungeon entrance waypoint."),
 ("Fort Marriner Waypoint", "Lion's Arch",
  ["fractals", "fractals of the mists", "mistlock observatory", "dungeon transport", "dungeon", "lfg"],
  "Fractals of the Mists portal is south of Fort Marriner; the dungeon-transport NPC is also there."),
 ("Bloodcoast Ward Waypoint", "Lion's Arch",
  ["raid", "raids", "lion's arch aerodrome", "aerodrome", "spirit vale", "salvation pass",
   "stronghold of the faithful", "hall of chains", "mythwright gambit", "key of ahdashim",
   "mount balrior raid", "raid wing"],
  "Lion's Arch Aerodrome (raid lobby, portals to all wings) is west of Bloodcoast Ward Waypoint."),
 ("Depths of the Maw Waypoint", "Bloodstone Fen",
  ["bastion of the penitent", "raid"],
  "Bastion of the Penitent open-world portal is just west of Depths of the Maw Waypoint (wiki)."),
 ("Eye of the North Waypoint", "Eye of the North",
  ["strike", "strikes", "icebrood saga strike", "shiverpeaks pass strike", "fraenir of jormag",
   "boneskinner", "whisper of jormag", "cold war strike", "forging steel", "strike mission"],
  "Icebrood Saga strikes are entered from the Eye of the North strike portal."),
 ("Arborstone Waypoint", "Arborstone",
  ["strike", "strikes", "end of dragons strike", "aetherblade hideout strike",
   "xunlai jade junkyard", "kaineng overlook", "harvest temple", "old lion's court strike", "strike mission"],
  "End of Dragons strikes are entered from Arborstone (The Ready Room / scrying stones)."),
 ("Tower Courtyard Waypoint", "The Wizard's Tower",
  ["strike", "strikes", "secrets of the obscure strike", "cosmic observatory", "temple of febe", "strike mission"],
  "Secrets of the Obscure strikes are entered from the Wizard's Tower."),
 # --- 3. Gathering / chest runs (Lady Elyssa README, Chest Run section) ---
 ("Akk Wilds Waypoint", "Metrica Province",
  ["chest run", "empyreal fragments", "gathering"],
  "Lady Elyssa Chest Run: Empyreal Fragments starts at Akk Wilds Waypoint."),
 ("Wanderer's Waypoint", "Auric Basin",
  ["heart of thorns chests", "chest run", "aurillium", "gathering"],
  "Lady Elyssa Chest Run: Auric Basin chests start at Wanderer's Waypoint."),
 ("Order of Whispers Camp Waypoint", "Tangled Depths",
  ["heart of thorns chests", "chest run", "ley-line crystals", "gathering"],
  "Lady Elyssa Chest Run: Tangled Depths chests start at Order of Whispers Camp Waypoint."),
 # --- 4. Jumping puzzles (Dulfy JP guide locations; nearest waypoint by location) ---
 ("Loreclaw Waypoint", "Plains of Ashford",
  ["loreclaw expanse", "jumping puzzle", "jp"], "JP is at Loreclaw Expanse, SE Ashford (Dulfy)."),
 ("Breached Wall Waypoint", "Diessa Plateau",
  ["crimson plateau", "wall breach blitz", "jumping puzzle", "jp"],
  "Both JPs are at/around the Breached Wall, south Diessa (Dulfy)."),
 ("Blasted Moors Waypoint", "Diessa Plateau",
  ["grendich gamble", "jumping puzzle", "jp"], "JP in the Blasted Moors, middle of Diessa (Dulfy)."),
 ("Behem Waypoint", "Blazeridge Steppes",
  ["behem gauntlet", "jumping puzzle", "jp"], "JP at the east end, Behem Gauntlet (Dulfy)."),
 ("Terra Carorunda Waypoint", "Blazeridge Steppes",
  ["craze's folly", "jumping puzzle", "jp"], "JP in Terra Carorunda, NE Blazeridge (Dulfy)."),
 ("Old Piken Ruins Waypoint", "Iron Marches",
  ["chaos crystal cavern", "jumping puzzle", "jp"], "JP at Old Piken Ruins, SW Iron Marches (Dulfy)."),
 ("Pig Iron Waypoint", "Fireheart Rise",
  ["pig iron quarry", "jumping puzzle", "jp"], "JP at Pig Iron Mine, SE Fireheart Rise (Dulfy)."),
 ("Keeper's Waypoint", "Fireheart Rise",
  ["vexa's lab", "jumping puzzle", "jp"], "JP east of Keeper's Sanctum, Fireheart Rise (Dulfy)."),
 ("Cereboth Waypoint", "Kessex Hills",
  ["collapsed observatory", "jumping puzzle", "jp"], "JP in Cereboth Canyon, south Kessex Hills (Dulfy)."),
 ("Broadhollow Waypoint", "Gendarran Fields",
  ["not so secret", "jumping puzzle", "jp"], "JP at Broadhollow Waypoint (Dulfy)."),
 ("Sorrowful Waypoint", "Bloodtide Coast",
  ["professor portmatt's lab", "portmatt's lab", "jumping puzzle", "jp"],
  "JP near Sorrowful Sound, west Bloodtide Coast (Dulfy)."),
 ("Spiral Waypoint", "Caledon Forest",
  ["morgan's leap", "dark reverie", "jumping puzzle", "jp"],
  "Both JPs are at Morgan's Spiral, SE Caledon Forest (Dulfy)."),
 ("Astorea Waypoint", "Caledon Forest",
  ["spekk's laboratory", "spekk's lab", "jumping puzzle", "jp"],
  "JP at Sandycove Beach, west Caledon Forest (Dulfy); Astorea is the west-coast waypoint."),
 ("Sleive's Waypoint", "Caledon Forest",
  ["spelunker's delve", "jumping puzzle", "jp"], "JP at Sleive's Inlet, SE Caledon Forest (Dulfy)."),
 ("Cuatl Waypoint", "Metrica Province",
  ["goemm's lab", "jumping puzzle", "jp"], "JP south of Cuatl Waypoint, east Metrica Province (Dulfy)."),
 ("Govoran Waypoint", "Mount Maelstrom",
  ["conundrum cubed", "hidden garden", "jumping puzzle", "jp"],
  "Conundrum Cubed is NW of Govoran's Waypoint; Hidden Garden has an access point there (Dulfy)."),
 ("Osenfold Waypoint", "Wayfarer Foothills",
  ["shaman's rookery", "jumping puzzle", "jp"], "JP at Osenfold Shear, west Wayfarer Foothills (Dulfy)."),
 ("False Lake Waypoint", "Lornar's Pass",
  ["griffonrook run", "jumping puzzle", "jp"], "JP near False Lake, west Lornar's Pass (Dulfy)."),
 ("Tribulation Waypoint", "Dredgehaunt Cliffs",
  ["tribulation rift scaffolding", "tribulation caverns", "jumping puzzle", "jp"],
  "Both JPs are at Tribulation, SW Dredgehaunt Cliffs (Dulfy)."),
 ("Okarinoo Waypoint", "Timberline Falls",
  ["coddler's cove", "jumping puzzle", "jp"], "JP at Okarinoo Waypoint, SE Timberline Falls (Dulfy)."),
 ("Foundation 86 Waypoint", "Timberline Falls",
  ["only zuhl", "jumping puzzle", "jp"], "JP at Foundation 86, NE Timberline Falls (Dulfy)."),
 ("Ice Floe Waypoint", "Frostgorge Sound",
  ["shattered ice ruins", "jumping puzzle", "jp"], "JP at Shattered Ice Floe, north Frostgorge Sound (Dulfy)."),
 ("Valley of Lyss Waypoint", "Malchor's Leap",
  ["antre of adjournment", "scavenger's chasm", "jumping puzzle", "jp"],
  "Both JPs are east of Valley of Lyss, south Malchor's Leap (Dulfy)."),
 ("Trader's Forum Waypoint", "Lion's Arch",
  ["troll's end", "jumping puzzle", "jp"], "JP at Trader's Forum, Lion's Arch (Dulfy)."),
 ("Farshore Waypoint", "Lion's Arch",
  ["urmaug's secret", "jumping puzzle", "jp"], "JP in the NE corner of Lion's Arch (Dulfy); Farshore is the NE waypoint."),
 ("Chalice of Tears", "Ember Bay",
  ["chalice of tears", "jumping puzzle", "jp"],
  "This IS the JP location (landmark POI in the API) — tagged as-is, like Spearmarshal's Lament in v1.2."),
 ("Searing Ascent", "Draconis Mons",
  ["searing ascent", "jumping puzzle", "jp"],
  "This IS the JP location (landmark POI in the API) — tagged as-is."),
 # --- 5. Services (GuildWarsHub bank/TP ranking; forum guides) ---
 ("Trader's Forum Waypoint", "Lion's Arch",
  ["bank", "trading post", "mystic forge", "crafting", "crafting station", "laurel vendor", "services",
   "armorsmith", "weaponsmith", "huntsman", "artificer", "leatherworker", "tailor", "jeweler", "chef"],
  "Lion's Arch services: Trader's Forum puts you beside the bank and Mystic Forge, crafting nearby, TP via the jump pad (GuildWarsHub). All 8 standard crafting disciplines are in Lion's Arch Canal Ward."),
 ("Accountancy Waypoint", "Rata Sum",
  ["bank", "trading post", "crafting", "crafting station", "services"],
  "Rata Sum services: Accountancy Waypoint is ranked 1st for bank/TP distance (GuildWarsHub)."),
 ("Ministers Waypoint", "Divinity's Reach",
  ["bank", "trading post", "crafting", "crafting station", "services"],
  "Divinity's Reach services: Ministers Waypoint is right beside the bank (GuildWarsHub)."),
 ("Upper Commons Waypoint", "The Grove",
  ["bank", "trading post", "crafting", "crafting station", "services"],
  "The Grove services are at the Upper Commons."),
 ("Trade Commons Waypoint", "Hoelbrak",
  ["bank", "trading post", "crafting", "crafting station", "services"],
  "Hoelbrak services are at the Trade Commons."),
 ("Claypool Waypoint", "Queensdale",
  ["crafting", "crafting station", "bank", "trading post", "services"],
  "Claypool (Queensdale) has a full set of crafting stations plus bank and trading post nearby."),
]

tags_path = os.path.join(BASE, "data", "tags.json")
data = json.load(open(tags_path))
existing = {t["chat_link"]: t for t in data["tags"]}
added_entries = 0
added_phrases = 0
for name, map_name, tags, note in ADD:
    hits = by_nm.get((name, map_name))
    if not hits:
        sys.exit(f"NOT IN DATASET: {name} / {map_name}")
    if len(hits) > 1:
        sys.exit(f"AMBIGUOUS: {name} / {map_name} -> {[h['chat_link'] for h in hits]}")
    link = hits[0]["chat_link"]
    if link in existing:
        t = existing[link]
        for tag in tags:
            if tag not in t["tags"]:
                t["tags"].append(tag); added_phrases += 1
        if note and "note" not in t:
            t["note"] = note
    else:
        entry = {"chat_link": link, "map": map_name, "name": name, "tags": list(tags)}
        if note:
            entry["note"] = note
        data["tags"].append(entry)
        existing[link] = entry
        added_entries += 1
        added_phrases += len(tags)
data["generated"] = "2026-11-17"
data["source"] = (data.get("source", "") +
 " v1.3: Event Timers metas via Cellofrag timer index (wiki v5.4 data, fetched 2026-11-17) + per-event guides; "
 "dungeons via GW2 F2P dungeon list (waypoint codes) + wiki Raid/Strike pages; JPs via Dulfy JP guide locations; "
 "services via GuildWarsHub bank/TP ranking + forum guides; chest runs via Lady Elyssa README Chest Run section. "
 "Wiki Event Timers page itself still returns HTTP 403 (2026-11-17) — see README 'Not yet added'.")
json.dump(data, open(tags_path, "w"), indent=1)
print(f"v1.3: {added_entries} new tagged entries, {added_phrases} new tag phrases; "
      f"total {len(data['tags'])} entries, {sum(len(t['tags']) for t in data['tags'])} phrases")
