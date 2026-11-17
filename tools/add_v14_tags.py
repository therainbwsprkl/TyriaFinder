#!/usr/bin/env python3
"""v1.4 tag additions: multi-spot tags. Merge into data/tags.json,
validating every (name, map) against data/pois.json (chat_link looked up,
not guessed). Same merge pattern as add_v13_tags.py.
Run: python3 tools/add_v14_tags.py
Then: python3 tools/apply_tags.py && python3 tools/generate_pois_header.py
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pois = json.load(open(os.path.join(BASE, "data", "pois.json")))["entries"]
by_nm = {}
for e in pois:
    by_nm.setdefault((e.get("name"), e["map_name"]), []).append(e)

DISC = ["armorsmith", "weaponsmith", "huntsman", "artificer",
        "leatherworker", "tailor", "jeweler", "chef"]

# (name, map, [tags], note or "")
ADD = [
 # --- 1. Flax: ALL well-known farm spots (GameRant Best Flax Farming
 #     Locations 2024-11-06; GW2 wiki Flax page; Metabattle flax guide) ---
 # Jaka Itzel already tagged in v1.2.
 ("Ogre Camp Waypoint", "Tangled Depths",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax farm: 8 nodes at The Great Tree, up the rocky arch where tropical birds nest (GameRant; wiki Flax)."),
 ("Ground Zero Waypoint", "Bloodstone Fen",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax farm: 8 nodes in the Fragmented Wastes, 5 just over the waypoint (GameRant; wiki Flax)."),
 ("Soulkeeper's Airship Waypoint", "Bloodstone Fen",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax farm: same Fragmented Wastes cluster as Ground Zero, reachable from the airship (GameRant; wiki Flax)."),
 ("Heathen's Hold Waypoint", "Draconis Mons",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax farm: ring of 10 nodes in the Druid's Grotto, Savage Rise (GameRant; wiki Flax)."),
 ("Yatendi Village Waypoint", "Jahai Bluffs",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax farm: 8 nodes at the Jungle Anomaly, top platform of Wyvern Roost (GameRant; wiki Flax)."),
 ("Eastwatch Waypoint", "Auric Basin",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax around Eastwatch Waypoint, Auric Basin (farming guide; wiki Flax lists flax at Eastwatch Bluff)."),
 ("Westwatch Waypoint", "Auric Basin",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax around Westwatch Waypoint, Auric Basin (farming guide; wiki Flax lists flax at Westwatch Patch)."),
 ("Allied Encampment Waypoint", "Domain of Kourna",
  ["flax", "flax farm", "flax seeds", "gathering"],
  "Flax farm: ~4 nodes at Palawa's Benevolence, north of Allied Encampment, Arkjok Farmlands (Metabattle; wiki Flax)."),
 # --- 2. Rich Mithril: guaranteed-rich-vein waypoints (wiki Rich Mithril
 #     Vein; GW2 Life Rich Mithril maps) ---
 # Citadel of Flame already tagged in v1.2.
 ("Verdance Waypoint", "Cursed Shore",
  ["rich mithril", "mithril", "gathering"],
  "Rich Mithril Vein east of Verdance Waypoint, Cursed Shore (wiki Rich Mithril Vein)."),
 ("Shipwreck Rock Waypoint", "Cursed Shore",
  ["rich mithril", "mithril", "gathering"],
  "Guaranteed Rich Mithril Vein west of Shipwreck Rock Waypoint, Mausollus Sea (wiki Rich Mithril Vein)."),
 ("Meddler's Waypoint", "Cursed Shore",
  ["rich mithril", "mithril", "gathering"],
  "Rich Mithril Vein west of Meddler's Waypoint, Cursed Shore (wiki Rich Mithril Vein)."),
 ("Doric's Waypoint", "Malchor's Leap",
  ["rich mithril", "mithril", "gathering"],
  "Rich Mithril Vein NE of Doric's Waypoint, Karst Plains (wiki Rich Mithril Vein)."),
 ("Valley of Lyss Waypoint", "Malchor's Leap",
  ["rich mithril", "mithril", "gathering"],
  "Rich Mithril Vein east of Valley of Lyss Waypoint, Malchor's Leap (wiki Rich Mithril Vein)."),
 ("Slough of Despond Waypoint", "Frostgorge Sound",
  ["rich mithril", "mithril", "gathering"],
  "Rich Mithril Vein south of Slough of Despond Waypoint, Iron Horse Mines tunnel, Frostgorge Sound (wiki Rich Mithril Vein)."),
 ("Path of Starry Skies Waypoint", "Frostgorge Sound",
  ["rich mithril", "mithril", "gathering"],
  "Rich Mithril Vein SW of Path of Starry Skies Waypoint, Snow Climb, Frostgorge Sound (wiki Rich Mithril Vein)."),
 ("Pearl Islet Waypoint", "Southsun Cove",
  ["rich mithril", "mithril", "gathering"],
  "Map hub for Rich Mithril Vein on Southsun Cove (GW2 Life: Rich Mithril Vein maps include Southsun Cove; Dappled Shores area)."),
 # --- 3. Rich Orichalcum: named waypoints (Almars Orichalcum Spawn
 #     Locations; wiki Rich Orichalcum Vein; Strikingly gathering guide) ---
 # Spearmarshal's Lament + Lair of the Forgotten already tagged in v1.2.
 ("Drakkar Waypoint", "Frostgorge Sound",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node right next to Drakkar Waypoint, Frostgorge Sound (Almars spawn list)."),
 ("Earthshake Waypoint", "Frostgorge Sound",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node right by Earthshake Waypoint, Frostgorge Sound (Almars spawn list)."),
 ("Dimotiki Waypoint", "Frostgorge Sound",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node SE of Dimotiki Waypoint, Frostgorge Sound (Almars spawn list)."),
 ("Pagga's Waypoint", "Malchor's Leap",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum nodes above and west of Pagga's Waypoint, Malchor's Leap (Almars spawn list)."),
 ("Doric's Waypoint", "Malchor's Leap",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node near Doric's Waypoint, Malchor's Leap (Almars spawn list)."),
 ("Blighted Arch Waypoint", "Malchor's Leap",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node at Blighted Arch, Malchor's Leap (Almars spawn list)."),
 ("Murmur Waypoint", "Malchor's Leap",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node west of Murmur Waypoint, Malchor's Leap (Almars spawn list)."),
 ("Anchorage Waypoint", "Cursed Shore",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum nodes SE of and by Anchorage Waypoint, Cursed Shore (Almars spawn list)."),
 ("Meddler's Waypoint", "Cursed Shore",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node west of Meddler's Waypoint, Cursed Shore (Almars spawn list)."),
 ("Gavbeorn's Waypoint", "Cursed Shore",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node SE of Gavbeorn's Waypoint, Cursed Shore (Almars spawn list)."),
 ("Pursuit Pass Waypoint", "Cursed Shore",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Rich Orichalcum node by Pursuit Pass Waypoint, Cursed Shore (Almars spawn list)."),
 ("Red Leaf Retreat Waypoint", "Lake Doric",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Guaranteed Rich Orichalcum at Lakeside Bazaar mastery point, fastest from Red Leaf Retreat walking east (Strikingly gathering guide)."),
 ("Lakeside Bazaar Waypoint", "Lake Doric",
  ["rich orichalcum", "orichalcum", "gathering"],
  "Guaranteed Rich Orichalcum at the Lakeside Bazaar mastery point, Lake Doric (Strikingly gathering guide)."),
 # --- 4. Quartz: Dry Top nodes beyond Prosperity (forum quartz guide) ---
 # Prosperity + Destiny's Gorge already tagged in v1.2.
 ("Repair Station Waypoint", "Dry Top",
  ["quartz", "quartz crystal", "gathering"],
  "Quartz Crystal nodes at Crash Site 1, reachable from Repair Station Waypoint, Dry Top (forum quartz guide)."),
 ("Vine Bridge Waypoint", "Dry Top",
  ["quartz", "quartz crystal", "gathering"],
  "Rich Quartz Crystal node in Cragrock Palace, reachable from Vine Bridge Waypoint, Dry Top (forum quartz guide)."),
 # --- 5. Rich Copper / Silver / Gold / Iron / Platinum: one map-hub
 #     waypoint per map the vein spawns on (GW2 Life crafting-material
 #     lists; wiki vein pages). Labelled map hubs, not single farm spots. ---
 ("Ashford Waypoint", "Plains of Ashford",
  ["rich copper", "copper", "gathering"],
  "Map hub: Rich Copper Vein spawns in Plains of Ashford (GW2 Life; wiki Rich Copper Vein)."),
 ("Claypool Waypoint", "Queensdale",
  ["rich copper", "copper", "gathering"],
  "Map hub: Rich Copper Vein spawns in Queensdale (GW2 Life; wiki Rich Copper Vein)."),
 ("Desider Atum Waypoint", "Metrica Province",
  ["rich copper", "copper", "gathering"],
  "Map hub: Rich Copper Vein spawns in Metrica Province (GW2 Life; wiki Rich Copper Vein)."),
 ("Crossroads Haven Waypoint", "Wayfarer Foothills",
  ["rich copper", "copper", "gathering"],
  "Map hub: Rich Copper Vein spawns in Wayfarer Foothills (GW2 Life; wiki Rich Copper Vein)."),
 ("Cereboth Waypoint", "Kessex Hills",
  ["rich silver", "silver", "rich iron", "iron", "soft wood", "gathering"],
  "Map hub: Rich Silver Vein, Rich Iron Vein and Soft Wood all spawn in Kessex Hills (GW2 Life; wiki vein pages)."),
 ("Provern Shore Waypoint", "Gendarran Fields",
  ["rich silver", "silver", "soft wood", "gathering"],
  "Map hub: Rich Silver Vein and Soft Wood spawn in Gendarran Fields (GW2 Life; wiki vein pages)."),
 ("Gallowfields Waypoint", "Brisban Wildlands",
  ["rich silver", "silver", "rich iron", "iron", "soft wood", "gathering"],
  "Map hub: Rich Silver Vein, Rich Iron Vein and Soft Wood all spawn in Brisban Wildlands (GW2 Life; wiki vein pages)."),
 ("Durmand Priory Waypoint", "Lornar's Pass",
  ["rich silver", "silver", "rich iron", "iron", "gathering"],
  "Map hub: Rich Silver Vein and Rich Iron Vein spawn in Lornar's Pass (GW2 Life; wiki vein pages)."),
 ("Forlorn Gate Waypoint", "Fields of Ruin",
  ["rich gold", "gold", "gathering"],
  "Map hub: Rich Gold Vein spawns in Fields of Ruin (GW2 Life; wiki Rich Gold Vein)."),
 ("Lowland Burns Waypoint", "Blazeridge Steppes",
  ["rich gold", "gold", "rich iron", "iron", "gathering"],
  "Map hub: Rich Gold Vein and Rich Iron Vein spawn in Blazeridge Steppes (GW2 Life; wiki vein pages)."),
 ("Graupel Waypoint", "Dredgehaunt Cliffs",
  ["rich gold", "gold", "rich iron", "iron", "gathering"],
  "Map hub: Rich Gold Vein and Rich Iron Vein spawn in Dredgehaunt Cliffs (GW2 Life; wiki vein pages)."),
 ("Junction Camp Waypoint", "Harathi Hinterlands",
  ["rich iron", "iron", "gathering"],
  "Map hub: Rich Iron Vein spawns in Harathi Hinterlands (GW2 Life; wiki Rich Iron Vein)."),
 ("Firthside Vigil Waypoint", "Bloodtide Coast",
  ["rich platinum", "platinum", "gathering"],
  "Map hub: Rich Platinum Vein spawns in Bloodtide Coast (GW2 Life; wiki Rich Platinum Vein)."),
 ("Bulwark Waypoint", "Iron Marches",
  ["rich platinum", "platinum", "hard wood", "gathering"],
  "Map hub: Rich Platinum Vein and Hard Wood spawn in Iron Marches (GW2 Life; wiki vein pages)."),
 ("Gentle River Waypoint", "Timberline Falls",
  ["rich platinum", "platinum", "gathering"],
  "Map hub: Rich Platinum Vein spawns in Timberline Falls (GW2 Life; wiki Rich Platinum Vein)."),
 ("The Citadel of Flame Waypoint", "Fireheart Rise",
  ["rich platinum", "platinum", "hard wood", "gathering"],
  "Map hub: Rich Platinum Vein and Hard Wood spawn in Fireheart Rise (GW2 Life; wiki vein pages)."),
 ("Ashen Waypoint", "Mount Maelstrom",
  ["rich platinum", "platinum", "gathering"],
  "Map hub: Rich Platinum Vein spawns in Mount Maelstrom (GW2 Life; wiki Rich Platinum Vein)."),
 # --- 6. Wood: extra map hubs (wiki tree pages; GW2 Life) ---
 # Elder Wood: Waywarde / Pagga's / Camp Reclamation already tagged in v1.2.
 ("Earthshake Waypoint", "Frostgorge Sound",
  ["elder wood", "gathering"],
  "Map hub: Elder Wood (Cypress Sapling) spawns in Frostgorge Sound (wiki Elder Wood Log)."),
 ("Anchorage Waypoint", "Cursed Shore",
  ["elder wood", "gathering"],
  "Map hub: Elder Wood (Cypress Sapling) spawns in Cursed Shore (wiki Elder Wood Log)."),
 ("Pearl Islet Waypoint", "Southsun Cove",
  ["elder wood", "gathering"],
  "Map hub: Elder Wood (Cypress Sapling) spawns in Southsun Cove (wiki Elder Wood Log)."),
 # Seasoned Wood: NOT expanded — no verified single farm spot beyond the
 # two Lady Elyssa legs (Graupel, Wynchona Rally Point); see README.
 # --- 7. Services, multi-spot ---
 # Mystic Forge: Lion's Arch (Trader's Forum, v1.3) + Heart of the Mists.
 ("PvP Lobby Waypoint", "Heart of the Mists",
  ["mystic forge", "services"],
  "Mystic Forge in the Heart of the Mists lobby (everylastrecipe Mystic Forge guide; forum)."),
 # New full-service hubs (Allakhazam Crafting wiki: masters + stations +
 # trading post + merchants at each; GuildWarsHub bank/TP ranking).
 ("Factorium Waypoint", "Black Citadel",
  ["bank", "guild bank", "trading post", "crafting", "crafting station",
   "services", "merchant", "merchants"] + DISC,
  "Black Citadel services: Canton Factorium has all 8 crafting disciplines, bank, trading post and merchants (Allakhazam Crafting wiki)."),
 ("Ashford Waypoint", "Plains of Ashford",
  ["bank", "guild bank", "trading post", "crafting", "crafting station",
   "services", "merchant", "merchants", "rich copper", "copper", "gathering"] + DISC,
  "Plains of Ashford services: Ashford Forum has all 8 crafting disciplines, bank, trading post and merchants (Allakhazam Crafting wiki). Also a Rich Copper map hub."),
 ("Mabon Waypoint", "Caledon Forest",
  ["crafting", "crafting station", "services", "merchant", "merchants"] + DISC,
  "Caledon Forest services: Mabon Market has crafting masters/stations and merchants (Allakhazam Crafting wiki; no trading post/bank verified there)."),
 ("Desider Atum Waypoint", "Metrica Province",
  ["crafting", "crafting station", "services", "merchant", "merchants",
   "rich copper", "copper", "gathering"] + DISC,
  "Metrica Province services: Desider Atum has crafting masters/stations and merchants (Allakhazam Crafting wiki). Also a Rich Copper map hub."),
 ("Smokestead Waypoint", "Plains of Ashford",
  ["trading post", "merchant", "merchants", "services"],
  "Village of Smokestead, Plains of Ashford, has a trading post and merchants (Allakhazam Crafting wiki)."),
 # Existing hubs gain all 8 disciplines + merchant + guild bank.
 ("Accountancy Waypoint", "Rata Sum",
  ["merchant", "merchants", "guild bank"] + DISC,
  "Rata Sum services: all 8 disciplines are at the Interdisciplinary Accessium / Accountancy area (Allakhazam Crafting wiki)."),
 ("Ministers Waypoint", "Divinity's Reach",
  ["merchant", "merchants", "guild bank"] + DISC,
  "Divinity's Reach services: all 8 disciplines are at the District Promenade (Allakhazam Crafting wiki)."),
 ("Upper Commons Waypoint", "The Grove",
  ["merchant", "merchants", "guild bank"] + DISC,
  "The Grove services: all 8 disciplines are at Maker's Terrace (Allakhazam Crafting wiki)."),
 ("Trade Commons Waypoint", "Hoelbrak",
  ["merchant", "merchants", "guild bank"] + DISC,
  "Hoelbrak services: all 8 disciplines are at the Trade Commons (Allakhazam Crafting wiki)."),
 ("Claypool Waypoint", "Queensdale",
  ["merchant", "merchants", "guild bank"] + DISC,
  "Claypool has a full set of crafting stations (v1.3); all 8 disciplines are there."),
 ("Trader's Forum Waypoint", "Lion's Arch",
  ["merchant", "merchants", "guild bank", "laurel merchant", "laurel"],
  "Lion's Arch Trader's Forum: also has merchants, guild bank, and a laurel merchant nearby."),
 # Laurel merchants: ALL verified locations (wiki Laurel Merchant page).
 ("Arborstone Waypoint", "Arborstone",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant in Arborstone (wiki Laurel Merchant)."),
 ("Memorial Waypoint", "Black Citadel",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant in the Memorial Quadrant, Black Citadel (wiki Laurel Merchant)."),
 ("Amnoon Waypoint", "Crystal Oasis",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant in the Free City of Amnoon, Crystal Oasis (wiki Laurel Merchant)."),
 ("Balthazar Waypoint", "Divinity's Reach",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant at the Plaza of Balthazar, Divinity's Reach (wiki Laurel Merchant)."),
 ("Snowblind Waypoint", "Gendarran Fields",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant at Havoc's Heir, Snowblind Peaks, Gendarran Fields (wiki Laurel Merchant)."),
 ("Fort Marriner Waypoint", "Lion's Arch",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant at Fort Marriner, Lion's Arch (wiki Laurel Merchant)."),
 ("Bloodcoast Ward Waypoint", "Lion's Arch",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant at the Lion's Arch Aerodrome, west of Bloodcoast Ward (wiki Laurel Merchant)."),
 ("Accountancy Waypoint", "Rata Sum",
  ["laurel merchant", "laurel vendor", "laurel"],
  "Laurel Merchant in Creator's Commons, Rata Sum (wiki Laurel Merchant)."),
 ("Upper Commons Waypoint", "The Grove",
  ["laurel merchant", "laurel vendor", "laurel"],
  "Laurel Merchant in the Garden of Dusk, The Grove (wiki Laurel Merchant; Upper Commons is the Grove hub)."),
 ("Great Lodge Waypoint", "Hoelbrak",
  ["laurel merchant", "laurel vendor", "laurel", "services"],
  "Laurel Merchant at The Great Lodge, Hoelbrak (wiki Laurel Merchant)."),
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
 " v1.4: multi-spot tags — flax via GameRant Best Flax Farming Locations "
 "(2024-11-06) + wiki Flax + Metabattle; rich mithril/orichalcum via wiki vein "
 "pages + Almars spawn list + Strikingly guide; quartz via forum quartz guide; "
 "copper/silver/gold/iron/platinum/wood map hubs via GW2 Life crafting-material "
 "lists + wiki vein/tree pages; services via Allakhazam Crafting wiki + wiki "
 "Laurel Merchant page + everylastrecipe Mystic Forge guide.")
json.dump(data, open(tags_path, "w"), indent=1)
print(f"v1.4: {added_entries} new tagged entries, {added_phrases} new tag phrases; "
      f"total {len(data['tags'])} entries, {sum(len(t['tags']) for t in data['tags'])} phrases")
