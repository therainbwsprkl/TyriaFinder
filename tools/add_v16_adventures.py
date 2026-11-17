#!/usr/bin/env python3
"""v1.6 tag additions, part 2: ALL adventures (wiki Adventures navbox).
Merge into data/tags.json, validating every (name, map) against
data/pois.json (chat_link looked up, not guessed). Same merge pattern as
add_v16_jps.py: phrases are UNIONED onto already-tagged entries.

Sources (three research passes, 2026-11-17):
- HoT (15/15 verified): GuildJen Verdant Brink / Auric Basin guides,
  GW2 wiki "Getting there" (Flying Circus, Haywire Punch-o-Matic
  Battle, The Ley-Line Run), AyinMaiden, Dulfy, ProjektDyad.
- PoF / LWS4 / IBS (34 taggable of 39): wiki adventure + map pages,
  Dulfy, GuildJen, AyinMaiden, Granny's guides, Japanese Fandom wiki.
  22 verified, 12 medium-confidence (area-listing / route-grouping,
  flagged ⚠️ in the note) — included, flagged, not guessed.
- EoD / SotO / Janthir / VoE / festivals / Other (44 taggable of 69):
  wiki, GuildJen, ProjektDyad, MetaBattle, Tekkit, forums. 30 verified
  cleanly, 14 with a caveat / derived (flagged ⚠️) — included, flagged.
  11 festival adventures are in instance maps with NO usable waypoint
  (7 Super Adventure Box, 4 Halloween) — NOT tagged. 14 unverified —
  NOT tagged (see README / data/COVERAGE.md unverified list).

Ambiguities (both waypoints tagged, multi-spot model):
- On Wings of Gold: Northwatch (GuildJen, detailed) vs Forgotten City
  (ProjektDyad). Haywire Punch-o-Matic Battle: Ley-Line Confluence
  (wiki no-mastery route) vs Rata Novus (wiki "easiest way"). The
  Ley-Line Run: Ley-Line Confluence (wiki first route) vs Ogre Camp
  (Nuhoch Wallow route). Shooting Gallery: Faren's Flyer (primary)
  vs Shrouded Ruins (alternate path).
- Repeating adventures (Griffon Expert/Master, Jade Bot Rally, Swift
  Skiffs, Siege Stampede, Skyscale Target Practice, Warclaw Run) are
  tagged PER MAP, each with its own start waypoint, plus a
  "<name> <map>" phrase so "griffon expert crystal oasis" works.
- Spelling: the adventure is "The Floor Is Lava" (no question mark).
  "Castoran King Crab" is also listed by the wiki as "King Crab of
  Castora" — both phrases tagged.
- Roller Beetle Time Trials (7): derived 1:1 — the wiki "Roller Beetle
  Racing Week" page lists exactly 7 waypoints for the 7 tracks and
  MetaBattle lists each track's area/map; each waypoint is in a
  distinct map matching its track. Flagged as derived in the note.
- "Alliance Staging Ground" is the dataset's exact name field for
  the Mistburned Barrens waypoint [&BFAPAAA=] (no "Waypoint" suffix
  in the API) — the tag entry uses the dataset name, as apply_tags.py
  requires.
Run: python3 tools/add_v16_adventures.py
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
        sys.exit(f"v1.6 adv: waypoint not in dataset: {name} / {map_name}")
    if len(matches) > 1:
        sys.exit(f"v1.6 adv: ambiguous (name, map): {name} / {map_name}")
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
    e = {x["chat_link"]: x for x in pois}.get(chat_link)
    if e is None:
        sys.exit(f"v1.6 adv: chat_link not in dataset: {chat_link}")
    t = by_link_tags.get(chat_link)
    if t is None:
        t = {"chat_link": e["chat_link"], "map": e["map_name"],
             "name": e["name"], "tags": [], "note": note}
        tags.append(t)
        by_link_tags[chat_link] = t
    for p in phrases:
        if p not in t["tags"]:
            t["tags"].append(p)
    if note and note not in t.get("note", ""):
        t["note"] = (t.get("note", "") + " " + note).strip()

ADV = "adventure"
def adv_tags(name, expansion, map_name, extra=()):
    return [name, ADV, expansion + " adventure",
            name + " " + map_name.lower()] + list(extra)

# (waypoint name, map, [phrases], note)
ADD = [
 # --- Heart of Thorns ---
 ("Mellaggan's Valor Waypoint", "Verdant Brink",
  adv_tags("flying circus", "hot", "Verdant Brink"),
  "Flying Circus adventure (wiki Getting there: from Mellaggan's Valor Waypoint, head north-west, Bouncing Mushroom up to Uprooted Paradise)."),
 ("Shrouded Ruins Waypoint", "Verdant Brink",
  adv_tags("salvage pit", "hot", "Verdant Brink") +
  adv_tags("shooting gallery", "hot", "Verdant Brink"),
  "Salvage Pit adventure (GuildJen: start at Shrouded Ruins, head east). Also Shooting Gallery alternate path (GuildJen; primary is Faren's Flyer)."),
 ("Faren's Flyer Waypoint", "Verdant Brink",
  adv_tags("shooting gallery", "hot", "Verdant Brink"),
  "Shooting Gallery adventure (GuildJen: head straight east from Faren's Flyer Waypoint)."),
 ("Southwatch Waypoint", "Auric Basin",
  adv_tags("a fungus among us", "hot", "Auric Basin"),
  "A Fungus Among Us adventure (GuildJen: start at Southwatch Waypoint, head west toward Griffonfall)."),
 ("Forgotten City Waypoint", "Auric Basin",
  adv_tags("fallen masks", "hot", "Auric Basin") +
  adv_tags("sanctum scramble", "hot", "Auric Basin") +
  adv_tags("on wings of gold", "hot", "Auric Basin"),
  "Fallen Masks + Sanctum Scramble adventures (GuildJen). Also On Wings of Gold alternate route (ProjektDyad: northeast from Forgotten City; GuildJen primary is Northwatch)."),
 ("Northwatch Waypoint", "Auric Basin",
  adv_tags("on wings of gold", "hot", "Auric Basin"),
  "On Wings of Gold adventure (GuildJen: start at Northwatch Waypoint, through the Northgate, east along the uppermost balcony)."),
 ("Wanderer's Waypoint", "Auric Basin",
  adv_tags("the floor is lava", "hot", "Auric Basin", ["floor is lava"]),
  "The Floor Is Lava adventure (GuildJen: start at Wanderer's Waypoint on the surface level). Spelled without a question mark per the wiki."),
 ("Teku Nuhoch Waypoint", "Tangled Depths",
  adv_tags("beetle feast", "hot", "Tangled Depths"),
  "Beetle Feast adventure (AyinMaiden: Teku Nuhoch Waypoint, circle up to Nuhoch Village; Dulfy)."),
 ("SCAR Camp Waypoint", "Tangled Depths",
  adv_tags("drone race", "hot", "Tangled Depths") +
  adv_tags("scrap rifle field test", "hot", "Tangled Depths"),
  "Drone Race + Scrap Rifle Field Test adventures (Japanese Fandom wiki SCAR Bivouac area; AyinMaiden: port to SCAR Camp, follow the path northeast)."),
 ("Ley-Line Confluence Waypoint", "Tangled Depths",
  adv_tags("haywire punch-o-matic battle", "hot", "Tangled Depths") +
  adv_tags("the ley-line run", "hot", "Tangled Depths", ["ley-line run"]),
  "Haywire Punch-o-Matic Battle + The Ley-Line Run adventures (wiki Getting there: Ley-Line Confluence is the no-mastery / first-listed route)."),
 ("Rata Novus Waypoint", "Tangled Depths",
  adv_tags("haywire punch-o-matic battle", "hot", "Tangled Depths"),
  "Haywire Punch-o-Matic Battle adventure, alternate route (wiki Getting there: Rata Novus Waypoint with Nuhoch Wallows, 'the easiest way')."),
 ("Ogre Camp Waypoint", "Tangled Depths",
  adv_tags("the ley-line run", "hot", "Tangled Depths", ["ley-line run"]),
  "The Ley-Line Run adventure, alternate route (wiki: Ogre Camp Waypoint via a Nuhoch Wallow)."),
 # --- Path of Fire ---
 ("Amnoon Waypoint", "Crystal Oasis",
  adv_tags("refugee supply run", "pof", "Crystal Oasis") +
  adv_tags("griffon master", "pof", "Crystal Oasis"),
  "Refugee Supply Run adventure (wiki: Free City of Amnoon area; start at the refugee camp in Amnoon — medium confidence, area listing). Griffon Master, Crystal Oasis (wiki: from Amnoon Waypoint, outside the Tomb of the Abandoned)."),
 ("Temple of Kormir Waypoint", "Crystal Oasis",
  adv_tags("griffon expert", "pof", "Crystal Oasis"),
  "Griffon Expert, Crystal Oasis (wiki Getting there: from Temple of Kormir Waypoint go east, Springer; Dulfy)."),
 ("Highjump Ranch Waypoint", "Desert Highlands",
  adv_tags("griffon expert", "pof", "Desert Highlands"),
  "Griffon Expert, Desert Highlands (wiki 'Highlands Griffon Expert' Getting there, Windshear Scarps)."),
 ("Derelict Delve Waypoint", "Desert Highlands",
  adv_tags("griffon master", "pof", "Desert Highlands"),
  "Griffon Master, Desert Highlands (wiki 'Highlands Griffon Master' Getting there, Fortune's Vale)."),
 ("Skimmer Ranch Waypoint", "Elon Riverlands",
  adv_tags("skimshallow cove supply run", "pof", "Elon Riverlands") +
  adv_tags("griffon expert", "pof", "Elon Riverlands"),
  "Skimshallow Cove Supply Run (wiki: started by Nura on Skimmer Ranch, southwest of the waypoint) + Griffon Expert, Elon Riverlands (wiki 'Riverlands Griffon Expert' Getting there, Vulture Drifts)."),
 ("Olishar's Oasis Camp Waypoint", "Elon Riverlands",
  adv_tags("griffon master", "pof", "Elon Riverlands"),
  "Griffon Master, Elon Riverlands (wiki 'Riverlands Griffon Master' Getting there, Shoals of Sovereignty)."),
 ("The Scourgeway Waypoint", "The Desolation",
  adv_tags("shadows intel", "pof", "The Desolation") +
  adv_tags("griffon expert", "pof", "The Desolation") +
  adv_tags("griffon master", "pof", "The Desolation"),
  "Shadows Intel + Griffon Expert + Griffon Master, The Desolation (Japanese Fandom wiki, The Scourgeway area page — medium confidence, area listing; Dulfy jackal-portal note for the Master course)."),
 ("Seborhin Waypoint", "Domain of Vabbi",
  adv_tags("garden wine and cheese run", "pof", "Domain of Vabbi"),
  "Garden Wine and Cheese Run (wiki map table: Garden of Seborhin area — medium confidence, area listing)."),
 ("Necropolis Waypoint", "Domain of Vabbi",
  adv_tags("necropolis embalming supply run", "pof", "Domain of Vabbi"),
  "Necropolis Embalming Supply Run (wiki map table: The Necropolis area; started by the Managing Embalmer — medium confidence, area listing)."),
 ("Vehjin Palace Waypoint", "Domain of Vabbi",
  adv_tags("vehjin noble necessities run", "pof", "Domain of Vabbi"),
  "Vehjin Noble Necessities Run (wiki: speak to the Overwhelmed Volunteer Steward near Vehjin Palace Waypoint)."),
 ("Vehtendi Academy Waypoint", "Domain of Vabbi",
  adv_tags("vehtendi school supply run", "pof", "Domain of Vabbi") +
  adv_tags("griffon expert", "pof", "Domain of Vabbi"),
  "Vehtendi School Supply Run (wiki map table: Vehtendi Academy area; Academy Provisioner — medium confidence) + Griffon Expert, Vabbi (wiki 'Vabbian Griffon Expert' Getting there, Kodash Bazaar)."),
 ("Market Ruins Waypoint", "Domain of Vabbi",
  adv_tags("griffon master", "pof", "Domain of Vabbi"),
  "Griffon Master, Vabbi (wiki 'Vabbian Griffon Master' Getting there: Skimmer to King Joko's Sky Garden, Kodash Bazaar)."),
 ("Guild Bluff Waypoint", "Lion's Arch",
  adv_tags("advanced skimmer course", "pof", "Lion's Arch"),
  "Advanced Skimmer Course (wiki: south of Guild Initiative Headquarters; GuildJen/AyinMaiden: south of Guild Bluff Waypoint, talk with Sibaha — medium confidence)."),
 # --- Living World Season 4 ---
 ("Astralarium Waypoint", "Domain of Istan",
  adv_tags("ancient weapons", "living world", "Domain of Istan") +
  adv_tags("griffon master", "living world", "Domain of Istan"),
  "Ancient Weapons (wiki: speak to Quartermaster Soanso near Astralarium Waypoint; head southeast) + Griffon Master, Istan (wiki Astralarium area page — medium confidence)."),
 ("Champion's Dawn Waypoint", "Domain of Istan",
  adv_tags("griffon expert", "living world", "Domain of Istan"),
  "Griffon Expert, Istan (AyinMaiden 'Lost to Time' route: right by the Istan Griffon Expert adventure, reached from Champion's Dawn heading east — medium confidence)."),
 ("Atholma Waypoint", "Sandswept Isles",
  adv_tags("crystal corral", "living world", "Sandswept Isles"),
  "Crystal Corral (wiki: head south from Atholma Waypoint; start: Veteran Defector Gliffu, Damos Isle)."),
 ("Anniogel Encampment Waypoint", "Sandswept Isles",
  adv_tags("griffon expert", "living world", "Sandswept Isles"),
  "Griffon Expert, Sandswept Isles (wiki 'Sandswept Isles Griffon Expert' Getting there, Eastern Complex)."),
 ("Allied Encampment Waypoint", "Domain of Kourna",
  adv_tags("roller beetle training", "living world", "Domain of Kourna") +
  adv_tags("griffon expert", "living world", "Domain of Kourna"),
  "Roller Beetle Training (wiki: run north from Allied Encampment Waypoint) + Griffon Expert, Kourna (wiki Getting there, Yohlon Bluffs)."),
 ("Apizmic Grounds Waypoint", "Domain of Kourna",
  adv_tags("griffon master", "living world", "Domain of Kourna"),
  "Griffon Master, Kourna (wiki Getting there, Dabiji Hollows)."),
 ("Revolution's Heart Waypoint", "Thunderhead Peaks",
  adv_tags("ice floe magnet run", "living world", "Thunderhead Peaks") +
  adv_tags("thunderhead keep volatile delivery", "living world", "Thunderhead Peaks"),
  "Ice Floe Magnet Run (AyinMaiden groups it under Revolution's Heart Waypoint — medium confidence; Observation Deck Waypoint at Thunderhead Keep is an uncompared alternative) + Thunderhead Keep Volatile Delivery (wiki: started by Olmakhan Windcaller at Refiner's Joy, south of Revolution's Heart Waypoint)."),
 # --- The Icebrood Saga ---
 ("Wardowns Waypoint", "Grothmar Valley",
  adv_tags("grothmar crater circuit", "icebrood saga", "Grothmar Valley"),
  "Grothmar Crater Circuit (GuildJen Bound by Blood: from Wardowns Waypoint, head to Blood Stand Stage; Time Trial NPC by the water's edge)."),
 ("Dalada Forest Waypoint", "Grothmar Valley",
  adv_tags("grothmar grand tour", "icebrood saga", "Grothmar Valley") +
  adv_tags("grothmar valley skyscale trial", "icebrood saga", "Grothmar Valley"),
  "Grothmar Grand Tour (GuildJen: Time Trial in Dalada Forest) + Grothmar Valley Skyscale Trial (wiki: run south-east from Dalada Forest Waypoint to the Priory Research Station)."),
 ("Forward Camp Waypoint", "Drizzlewood Coast",
  adv_tags("arena of the wolverine", "icebrood saga", "Drizzlewood Coast") +
  adv_tags("flight of the eagle spirit", "icebrood saga", "Drizzlewood Coast") +
  adv_tags("the ox's yoke", "icebrood saga", "Drizzlewood Coast"),
  "Arena of the Wolverine (Drizzlewood has only two waypoints; arena at Archstone Coast, northern half — medium confidence) + Flight of the Eagle Spirit (wiki: run north-east from Forward Camp to Frostvein Dominion Camp) + The Ox's Yoke (wiki: shrine at Sentinel Bay, east of Forward Camp)."),
 # --- End of Dragons ---
 ("Garden Heights Waypoint", "New Kaineng City",
  adv_tags("jade bot rally", "eod", "New Kaineng City"),
  "Jade Bot Rally, New Kaineng City (wiki Jade Bot Rally—Kaineng: 'right next to the Garden Heights Waypoint')."),
 ("Mori Village Waypoint", "The Echovald Wilds",
  adv_tags("jade bot rally", "eod", "The Echovald Wilds"),
  "Jade Bot Rally, Echovald (wiki Jade Bot Rally—Echovald: 'west to the Mori Village (Mori Village Waypoint)')."),
 ("Luxon Terminus Waypoint", "Gyala Delve",
  adv_tags("jade bot rally", "eod", "Gyala Delve"),
  "Jade Bot Rally, Gyala Delve (wiki Jade Bot Rally—Gyala Delve: 'right next to the Luxon Terminus Waypoint')."),
 ("Jadepillar Point Waypoint", "Gyala Delve",
  adv_tags("silent sands", "eod", "Gyala Delve"),
  "Silent Sands (wiki: zip line at top of Fossilized Overlook, south of Jadepillar Point Waypoint)."),
 # --- Secrets of the Obscure ---
 ("Beacon of Ages Waypoint", "Skywatch Archipelago",
  adv_tags("skyscale target practice", "soto", "Skywatch Archipelago"),
  "Skyscale Target Practice, Skywatch Archipelago (GuildJen: west of Beacon of Ages Waypoint, talk with Astral Ride Master Kensuke)."),
 ("Forward Bivouac Waypoint", "Inner Nayos",
  adv_tags("free kryptis essence", "soto", "Inner Nayos") +
  adv_tags("reuniting lost kryptis", "soto", "Inner Nayos"),
  "Free Kryptis Essence (wiki + GuildJen: east of Forward Bivouac Waypoint) + Reuniting Lost Kryptis (wiki: from Forward Bivouac Waypoint, move south to the Isolated Grasslands)."),
 ("Tower Courtyard Waypoint", "The Wizard's Tower",
  adv_tags("fly by night", "soto", "The Wizard's Tower") +
  adv_tags("skyscale target practice", "soto", "The Wizard's Tower"),
  "Fly by Night (GuildJen places it at the top of The Wizard's Court, directly above Tower Courtyard Waypoint — caveated, no source states it outright) + Skyscale Target Practice, Wizard's Tower (GuildJen: outside the tower, east of Tower Courtyard Waypoint)."),
 # --- Janthir Wilds ---
 ("Harvest Shore Waypoint", "Lowland Shore",
  adv_tags("harvest shore salmon run", "janthir", "Lowland Shore"),
  "Harvest Shore Salmon Run (forum + GuildJen: 'Start next to Harvest Shore Waypoint')."),
 ("Harvest Den Waypoint", "Lowland Shore",
  adv_tags("hide-and-seek challenge", "janthir", "Lowland Shore"),
  "Hide-and-Seek Challenge (wiki Harvest Den page lists the adventure + Harvest Den Waypoint; GuildJen: west of Denning Forge)."),
 ("Astral Ward Moon Camp Waypoint", "Lowland Shore",
  adv_tags("moon camp covert salmon run", "janthir", "Lowland Shore") +
  adv_tags("raven scouting", "janthir", "Lowland Shore"),
  "Moon Camp Covert Salmon Run (GuildJen: 'Start below the Astral Ward Moon Camp Waypoint') + Raven Scouting (GuildJen: 'Start north of Astral Ward Moon Camp Waypoint')."),
 ("Journeykin Outpost Waypoint", "Lowland Shore",
  adv_tags("warclaw run", "janthir", "Lowland Shore"),
  "Warclaw Run, Lowland Shore (GuildJen: 'Start the adventure east of Journeykin Outpost Waypoint')."),
 ("Stricken Plains Waypoint", "Janthir Syntri",
  adv_tags("swift skiffs", "janthir", "Janthir Syntri"),
  "Swift Skiffs, Janthir Syntri (GuildJen calls it 'River Mapping Adventure north of Stricken Plains Waypoint' — caveated: confirm this is the Swift Skiffs adventure before relying on it)."),
 ("Festering Basin Waypoint", "Janthir Syntri",
  adv_tags("save woodland creatures", "janthir", "Janthir Syntri"),
  "Save Woodland Creatures (GuildJen: south of Festering Basin Waypoint)."),
 ("Sanguine Crater Waypoint", "Janthir Syntri",
  adv_tags("the view from the top", "janthir", "Janthir Syntri"),
  "The View from the Top (wiki: 'Found just north of Sanguine Crater Waypoint')."),
 ("Forager's Hunt Waypoint", "Janthir Syntri",
  adv_tags("warclaw run", "janthir", "Janthir Syntri"),
  "Warclaw Run, Janthir Syntri (GuildJen + Ayinmaiden: south / southwest of Forager's Hunt Waypoint)."),
 ("Alliance Staging Ground", "Mistburned Barrens",
  adv_tags("hazardous research", "janthir", "Mistburned Barrens") +
  adv_tags("search-and-rescue challenge", "janthir", "Mistburned Barrens"),
  "Hazardous Research + Search-and-Rescue Challenge (GuildJen routes via Alliance Staging Ground Waypoint; forum confirms players waypoint back there from the Garden of the Unseen / Hidden Sacrarium — caveated: nearest waypoint to the adventure NPC itself is not separately confirmed. Dataset name is 'Alliance Staging Ground', no 'Waypoint' suffix.)"),
 # --- Visions of Eternity ---
 ("Dark Leviathan Waypoint", "Shipwreck Strand",
  adv_tags("castoran king crab", "voe", "Shipwreck Strand", ["king crab of castora"]) +
  adv_tags("glimmering arches grand prix", "voe", "Shipwreck Strand"),
  "Castoran King Crab (ProjektDyad: event spawns south of Dark Leviathan Waypoint; wiki also calls it 'King Crab of Castora') + Glimmering Arches Grand Prix (ProjektDyad: head straight west of Dark Leviathan Waypoint, talk with Castaway Caldus)."),
 ("Hullgarden Pier Waypoint", "Shipwreck Strand",
  adv_tags("flying fireworks", "voe", "Shipwreck Strand"),
  "Flying Fireworks (wiki: head west from Hullgarden Pier Waypoint, then use a skyscale to ascend the cliff; talk to Astral Ward Illuminate Lightburn)."),
 ("Pub Canach Waypoint", "Shipwreck Strand",
  adv_tags("skimmer-net scramble", "voe", "Shipwreck Strand"),
  "Skimmer-Net Scramble (ProjektDyad: southeast from Pub Canach Waypoint, speak with Castaway Kae; GuildJen: at Jetsam Point)."),
 ("Hunter's Camp Waypoint", "Starlit Weald",
  adv_tags("old magic", "voe", "Starlit Weald") +
  adv_tags("ley-line rider", "voe", "Starlit Weald"),
  "Old Magic (ProjektDyad: Lost Basilica, southwest from Hunter's Camp Waypoint) + Ley-Line Rider (ProjektDyad: head northwest of Hunter's Camp Waypoint, speak with Specialist Nobu)."),
 # --- Festivals ---
 ("Crown Pavilion Waypoint", "Divinity's Reach",
  adv_tags("firecracker lighting", "festival", "Divinity's Reach") +
  adv_tags("firecracker lighting 2", "festival", "Divinity's Reach") +
  adv_tags("racing in the new year", "festival", "Divinity's Reach") +
  adv_tags("pavilion pursuit", "festival", "Divinity's Reach") +
  adv_tags("snowfall sprint", "festival", "Divinity's Reach"),
  "Firecracker Lighting + Firecracker Lighting 2 (Lunar New Year, Crown Pavilion; ProjektDyad + wiki) + Racing in the New Year (ProjektDyad: race spawns southwest from Crown Pavilion Waypoint — caveated, describes the race event) + Pavilion Pursuit (Festival of the Four Winds, wiki table: Time Trial NPC in the centre of the Crown Pavilion near the waypoint — caveated, table cell had a template error) + Snowfall Sprint (Wintersday, ProjektDyad: race starts northwest of Crown Pavilion Waypoint)."),
 ("Bazaar Docks Waypoint", "Labyrinthine Cliffs",
  adv_tags("crystal collection", "festival", "Labyrinthine Cliffs") +
  adv_tags("flying dolyak", "festival", "Labyrinthine Cliffs") +
  adv_tags("labyrinthine skiffs", "festival", "Labyrinthine Cliffs") +
  adv_tags("skimmer slalom", "festival", "Labyrinthine Cliffs"),
  "Crystal Collection + Flying Dolyak + Labyrinthine Skiffs (Festival of the Four Winds, wiki activities table 'Closest waypoint' column) + Skimmer Slalom (same table column lists Bazaar Docks; the adventure page's Getting there mentions Sky Docks — table column taken as the direct statement, flagged for a second look)."),
 ("Sky Docks Waypoint", "Labyrinthine Cliffs",
  adv_tags("griffon expert", "festival", "Labyrinthine Cliffs") +
  adv_tags("griffon master", "festival", "Labyrinthine Cliffs"),
  "Griffon Expert + Griffon Master, Labyrinthine Cliffs (Festival of the Four Winds, wiki table: Expert starts on the Phoenix Dawn airship south of the waypoint; Master starts on the stone pillar northwest of Sky Docks Waypoint)."),
 # --- Other: Roller Beetle Time Trials (derived 1:1, see header) ---
 ("Nageling Waypoint", "Diessa Plateau",
  adv_tags("ghostfire run", "roller beetle", "Diessa Plateau"),
  "Ghostfire Run, Roller Beetle Time Trial (MetaBattle: track at Noxin Dells, Diessa Plateau; Nageling is the Diessa waypoint in the wiki's Racing Week list — derived)."),
 ("Avernan Waypoint", "Mount Maelstrom",
  adv_tags("infernal leap", "roller beetle", "Mount Maelstrom"),
  "Infernal Leap, Roller Beetle Time Trial (MetaBattle: track at The Stychs, Mount Maelstrom; Avernan is the Mount Maelstrom waypoint in the wiki's list — derived)."),
 ("Torstvedt Homestead Waypoint", "Snowden Drifts",
  adv_tags("jormag's fang", "roller beetle", "Snowden Drifts"),
  "Jormag's Fang, Roller Beetle Time Trial (MetaBattle: track at Valslake, Snowden Drifts; Torstvedt Homestead is the Snowden waypoint in the wiki's list — derived)."),
 ("Provern Shore Waypoint", "Gendarran Fields",
  adv_tags("lakeside loop", "roller beetle", "Gendarran Fields"),
  "Lakeside Loop, Roller Beetle Time Trial (MetaBattle: track AT Provern Shore — direct name match)."),
 ("Gallowfields Waypoint", "Brisban Wildlands",
  adv_tags("tropic valley raceway", "roller beetle", "Brisban Wildlands"),
  "Tropic Valley Raceway, Roller Beetle Time Trial (MetaBattle: track at The Gallowfields — direct name match)."),
 ("Pearl Islet Waypoint", "Southsun Cove",
  adv_tags("shoreside sprint", "roller beetle", "Southsun Cove"),
  "Shoreside Sprint, Roller Beetle Time Trial (new Southsun course; Evon Gnashblade letter: talk to Sareb in Southsun Cove; Pearl Islet is the Southsun waypoint in the wiki's list — derived)."),
 ("Overlake Haven Waypoint", "Kessex Hills",
  adv_tags("kessex corner", "roller beetle", "Kessex Hills"),
  "Kessex Corner, Roller Beetle Time Trial (MetaBattle: track at Giant's Passage, Kessex Hills; Overlake Haven is the Kessex waypoint in the wiki's list — derived)."),
]

for name, map_name, phrases, note in ADD:
    add(name, map_name, phrases, note)

# Shipwreck Peak Waypoint: two dataset entries share name+map (map 1052
# is open-world Verdant Brink, [&BN4HAAA=]); tag that one by chat_link.
add_by_link("[&BN4HAAA=]",
            adv_tags("bugs in the branches", "hot", "Verdant Brink") +
            adv_tags("tendril torchers", "hot", "Verdant Brink"),
            "Bugs in the Branches adventure (GuildJen: head north from Shipwreck Peak Waypoint). Tendril Torchers adventure (GuildJen: head south from Shipwreck Peak Waypoint through the Dry Step Mesas).")

json.dump(doc, open(tags_path, "w"), indent=1)
print(f"v1.6 adv: {len(tags)} tagged entries, "
      f"{sum(len(t['tags']) for t in tags)} tag phrases")
