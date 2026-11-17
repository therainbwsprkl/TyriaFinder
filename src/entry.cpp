// Tyria Finder — Raidcore Nexus addon, v1.11.0
// v1.11.0: PUBLISH BUILD — FIND signature (0x46494E44, permanent) +
// GitHub update provider (https://github.com/therainbwsprkl/TyriaFinder).
// This is a NEW addon identity to Nexus vs the v1.10.4 dev build: the
// dev signature is gone, so the old dev DLL must be removed first.
// The signature must NEVER change again after the first published release.
// v1.10.4: DAILY ACTIVITY SECTION REMOVED (Audrey's ask). The whole
// v1.9 section is gone from the UI — no header, text, button, or
// "today's game is one of" line — and the "daily activity" umbrella
// tags were removed from data/tags.json (the Lionbridge entry, whose
// only tags were those, is gone; the four individual activities keep
// their own name tags). Baked tags are now 335 entries / 2,761 phrases.
// v1.10.3: USER TAGS REMOVED (Audrey's ask — felt clunky and
// confusing). The whole v1.10 feature is gone: no Tag button on
// result rows, no add-tag editor, no personal-tags list, no
// per-user tag file loading/saving. Any existing per-user tag
// file on disk is left alone, just unused. Search is back to
// baked tags only (336 entries /
// 2,773 phrases). The v1.10.2 performance work stays: cached
// search, precomputed haystacks, ListClipper — minus the
// user-tags cache key.
// v1.10.2: TYPING-LAG FIX + NO PRICES. Typing lagged because Search()
// ran the full 3,773-entry scan on EVERY ImGui frame (60x/sec), and
// inside it every entry rebuilt its lower-cased haystack and tag
// strings from scratch (thousands of allocations per frame, on the
// game thread) and the result list was re-sorted every frame. Now the
// haystacks/tags are lower-cased ONCE at first search and cached, and
// Search() results are cached — re-run only when the query, the type
// filters, the map, or the (bucketed) player position
// actually change, or the PSNA day rolls over. Rendering also uses
// ImGuiListClipper so only visible result rows build widgets.
// Also: Map Bonus Rewards no longer shows any prices (Audrey's ask) —
// no gold values, no price footer. Rows are "1. Malchor's Leap —
// Shiny Bauble" only; the ranking order is still the 17 Nov 2026
// snapshot order.
// v1.10.1: LAYOUT FIX — search results were pushed off-screen: the
// PSNA / Map Bonus / Rifts sections sat above the
// results, so with a query typed (e.g. "flax", 9 matches found) the
// "Showing 9 of 9" line sat at the very bottom of the 640px window
// and no result row was visible or clickable. Now, while a query is
// non-empty, those three sections are hidden and the
// results render immediately under the search box. With an empty
// search box the info sections show exactly as before. Also removes
// the "Try one of these" clickable example buttons (Audrey's ask).
// v1.10: user-custom tags — REMOVED in v1.10.3 (see header).
// (formerly GW2 Waypoint Search; renamed v1.8, functionality unchanged from v1.7)
// v1.8.1: UI polish only — tags are hidden from the user (search-only, never
// printed on a result line), hero-points text removed from the visible UI,
// raw counts removed, "Daily PSNA" expanded to "Daily Pact Supply Network
// Agents", and a proper empty state with clickable example searches.
// v1.9: Map Bonus Rewards section (8-week baked ranking, Thu 20:00 UTC
// reset, ranking order from the 17 Nov 2026 price snapshot — v1.10.2 shows
// NO prices in the UI) + Rifts section (11-week baked
// rotating cycle, Mon 07:30 UTC reset) under
// the PSNA section; materials / mob tags from
// docs/mob-and-poultry-tags.md (poultry, moas, skelk, etc.), guild
// mission + mount race tags from docs/guild-missions-mount-races.md,
// and daily-activity tags from docs/daily-activities.md merged in
// (336 tagged entries / 2,773 phrases). No search, ranking, or hotkey
// changes. Rifts spawn randomly on each map — the entry waypoint
// is a central hub, NOT a rift spawn point, and the UI says so.
// Copyright (c) 2026 — MIT license. See README.md.
//
// What it does: an in-game ImGui search window. Type a waypoint / POI /
// vista name, click a result (or press Enter) and its GW2 chat link
// ([&...]) is copied to the Windows clipboard, ready to paste in GW2 chat.
// Open it with Alt+Shift+W or by clicking its gold map-pin icon in the
// Nexus QuickAccess bar at the top of the screen.
// What it does NOT do: no teleport, no automation, no personal-waypoint
// pin, no game-memory reads except MumbleLink / Nexus APIs.
//
// v1.4: multi-spot tags. A tag phrase can be attached to several entries,
// so searching a resource/service returns ALL its well-known spots
// (flax: 9 farm spots; rich orichalcum: 15; rich mithril: 9; Mystic
// Forge: 2; trading post: 9; laurel merchants: 11; every crafting
// discipline: 10 city hubs). 140 entries carry curated tags
// (data/tags.json, 769 phrases): gathering + chest runs, world bosses,
// Event Timers metas, dungeons / fractals / strikes / raids, jumping
// puzzles, and city services (bank / trading post / Mystic Forge /
// crafting / laurel merchants). Searching a tag returns those waypoints,
// with the matched tag kept internal for ranking only, never shown in the UI.
// See README.md / data/tags.json for the full list and sources.
// NOTE: a query that is also a map name (e.g. "dragon's stand") returns
// every POI on that map as rank-0 name matches first; the tagged waypoint
// is in that list as a rank-1 tag match. That is the ranking by design.
// Same for a query that is also a POI name ("trading post" landmarks,
// "hard wood" matching Iceshard Trail in Drizzlewood Coast).
//
// Crash note (2026-11-16, Verdant Brink, 0xC0000005 in Gw2-64.exe):
// the faulting address was in Gw2-64.exe, UnhideNPCs was in the stack,
// and this DLL appeared in no stack frame, so this addon is assessed
// UNLIKELY to be the cause. Defensive fix in v1.1 anyway: MumbleLink
// positions are validated as finite before any distance math / sorting,
// because a non-finite position (the crash log reported 0,0,-inf) would
// otherwise feed NaN into std::sort's comparator. See README.md.
//
// v1.5: the v2.0 zoomable tile map was REMOVED at Audrey's request —
// it made the whole addon slow. This build is search-only again, same
// search/tags as v1.4. The map code is archived, not deleted, in
// archive/map_view-v2.0/ (src/map_view.h/.cpp, tools/test_tiles.py).
// No tile downloads, no WinHTTP, no Alt+Shift+M.
//
// v1.7: Pact Supply Network Agents (PSNA) — daily rotation, search-only,
// still no map. The 7-day weekday table is baked in (see kPsnaLinks
// below); the current PSNA day is computed at runtime from the system
// UTC time, locations changing at 08:00 UTC, NOT at the 00:00 UTC daily
// reset. "daily psna" / "psna today" / "today psna" returns ONLY today's
// 6 agents, ranked first, labelled "Daily Pact Supply — <Weekday>: <Agent>".
// Plain "psna" / "pact supply" lists ALL 40 PSNA locations (42 agent-day
// slots; Camp Resolve Waypoint and Fort Trinity Waypoint each repeat on
// two days). "psna monday" .. "psna sunday" returns that day's 6.
// 40 entries carry PSNA tags (data/tags.json, tools/add_v17_psna.py);
// 20 of the 42 published codes are landmark POIs, tagged as-is — the
// agent's spot, not a waypoint — never substituted. Recipes are random
// per vendor per day and are NOT in the addon. Also new: a "Copy daily
// list" button copies today's 6 chat links as one space-separated line
// (71 characters — fits GW2 chat's 199-character line limit), with a
// "Copied daily list!" confirmation. No other "daily" tags exist in the
// dataset, so the daily list is the PSNA set only. See README.md /
// data/COVERAGE.md.
//
// Dataset: src/pois_data.h, generated from data/pois.json (official GW2 API,
// 2026-11-16). See data/COVERAGE.md — notably Hero Points are NOT in the
// dataset because the official API gives them no name and no chat link.

#include <windows.h> // lowercase: MinGW cross-compile on Linux is case-sensitive

#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstring>
#include <ctime>
#include <string>
#include <vector>
#include <cstdio>
#include <map>

#include "nexus/Nexus.h"
#include "mumble/Mumble.h"
#include "imgui/imgui.h"

#include "pois_data.h"
#include "icon_data.h" // embedded QuickAccess icon PNGs (no external files)

// ---------------------------------------------------------------------------
// Nexus plumbing (follows RaidcoreGG/Nexus-Template-cpp, MIT)
// ---------------------------------------------------------------------------

void AddonLoad(AddonAPI_t* aApi);
void AddonUnload();
void AddonRender();
void OnToggleKeybind(const char* aIdentifier, bool aIsRelease);
void AddonOptions()
{
    ImGui::Separator();
    ImGui::Text("Tyria Finder  v1.11.0");
    ImGui::TextWrapped("Find anything in Tyria and copy its chat link. Search with Alt+Shift+W or the gold map-pin icon in the Nexus QuickAccess bar.");
    ImGui::TextWrapped("Try \"flax\", \"tequatl\", \"daily psna\", \"poultry\", \"rift\", \"guild rush\", or \"crab toss\". Click a result to copy its chat link, then paste it in GW2 chat.");
    ImGui::TextWrapped("Map Bonus Rewards and Rifts sections use baked weekly tables — the Map Bonus ranking order is the 17 Nov 2026 snapshot order, with no prices shown. Check /wiki Weekly Rift Hunting in-game for live rift values.");
}

AddonDefinition_t AddonDef  = {};
HMODULE           hSelf     = nullptr;
AddonAPI_t*       APIDefs   = nullptr;
NexusLinkData_t*  NexusLink = nullptr;
Mumble::Data*     MumbleLink = nullptr;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID /*lpReserved*/)
{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) { hSelf = hModule; }
    return TRUE;
}

extern "C" __declspec(dllexport) AddonDefinition_t* GetAddonDef()
{
    // Published signature: "FIND" — 0x46494E44 ('F'=0x46, 'I'=0x49,
    // 'N'=0x4E, 'D'=0x44, big-endian, as in THPS 0x54485053 / HELP
    // 0x48454C50). PERMANENT: this is the addon's identity to Nexus
    // and must never change after the first published release.
    AddonDef.Signature  = 0x46494E44;
    AddonDef.APIVersion = NEXUS_API_VERSION;
    AddonDef.Name       = "Tyria Finder";
    AddonDef.Version.Major = 1;
    AddonDef.Version.Minor = 11;
    AddonDef.Version.Build = 0;
    AddonDef.Version.Revision = 0;
    AddonDef.Author      = "Audrey";
    AddonDef.Description = "Find anything in Tyria and copy its chat link: search waypoints, POIs, vistas, jumping puzzles, adventures, mini dungeons, collections, daily Pact Supply Network Agents, world bosses, metas, gathering spots, services and regions by name or keyword.";
    AddonDef.Load        = AddonLoad;
    AddonDef.Unload      = AddonUnload;
    AddonDef.Flags       = AF_None;
    AddonDef.Provider    = UP_GitHub; // updates via GitHub releases
    AddonDef.UpdateLink  = "https://github.com/therainbwsprkl/TyriaFinder";
    return &AddonDef;
}

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

static bool g_visible        = false;
static bool g_quickAccessAdded = false;
static bool IsFiniteFloat(float v) { return std::isfinite(v); }
static bool g_filterWaypoint = true;
static bool g_filterPoi      = true;
static bool g_filterVista    = true;
static char g_query[128]     = {};
static bool g_focusSearch    = false; // focus the search box when the window opens
static char g_queryLower[128] = {};
static int  g_lastCopiedId   = -1;
static char g_lastCopiedLink[32] = {};
static double g_lastCopiedAt = -1000.0;
static double g_dailyCopiedAt = -1000.0; // "Copy daily list" feedback timer
static char g_dailyCopiedList[128] = {}; // last daily list copied (for feedback)

static std::string ToLower(const std::string& s)
{
    std::string out = s;
    for (char& c : out) { c = (char)std::tolower((unsigned char)c); }
    return out;
}

// Copy plain text to the Windows clipboard. Returns true on success.
static bool CopyToClipboard(const char* text)
{
    if (!text || !*text) { return false; }
    if (!OpenClipboard(nullptr)) { return false; }
    bool ok = false;
    EmptyClipboard();
    const size_t len = std::strlen(text) + 1;
    HGLOBAL h = GlobalAlloc(GMEM_MOVEABLE, len);
    if (h)
    {
        void* p = GlobalLock(h);
        if (p)
        {
            std::memcpy(p, text, len);
            GlobalUnlock(h);
            ok = SetClipboardData(CF_TEXT, h) != nullptr;
        }
        if (!ok) { GlobalFree(h); }
        // On success Windows owns the handle; do not free it.
    }
    CloseClipboard();
    return ok;
}

static void CopyResult(const PoiEntry* poi)
{
    if (!poi) { return; }
    if (CopyToClipboard(poi->chat_link))
    {
        g_lastCopiedId = poi->id;
        std::strncpy(g_lastCopiedLink, poi->chat_link, sizeof(g_lastCopiedLink) - 1);
        g_lastCopiedLink[sizeof(g_lastCopiedLink) - 1] = '\0';
        g_lastCopiedAt = ImGui::GetTime();
    }
}

// ---------------------------------------------------------------------------
// PSNA (Pact Supply Network Agents) — v1.7 daily rotation
// ---------------------------------------------------------------------------
// 6 agents, one per region, on a FIXED 7-day weekday cycle. Sources:
// GW2 Wiki "Pact Supply Network Agent" table 2025-07-27..2025-08-03,
// Doncpauli PSNA page (fetched live 2026-11-17), gw2timer-sourced gist
// — all three agree on the weekday mapping. 4 gist codes were REJECTED
// after checking data/pois.json (see tools/add_v17_psna.py): the table
// below uses the Doncpauli codes, every one verified in the dataset.
// Agent order in each row: Verma, Derwena, Fox, Mehem, Yana, Katelyn.
// 20 of the 42 codes are landmark POIs, not waypoints — tagged as-is.
// Locations change at 08:00 UTC, NOT at the 00:00 UTC daily reset.
// Recipes are random per vendor per day and are NOT in this addon.
// No network fetch: the table is baked in and the day is computed from
// the system UTC clock (std::gmtime), so it works offline.
static const char* kPsnaWeekdayNames[7] = {
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
};
static const char* kPsnaAgentNames[6] = {
    "Verma Giftrender", "Lady Derwena", "The Fox",
    "Mehem the Traveled", "Specialist Yana", "Despina Katelyn"
};
static const char* kPsnaAgentRegions[6] = {
    "Ascalon", "Kryta", "Maguuma Jungle",
    "Maguuma Wastes", "Ruins of Orr", "Shiverpeaks"
};
static const char* kPsnaLinks[7][6] = {
    // Monday
    { "[&BA8CAAA=]", "[&BKYBAAA=]", "[&BEwDAAA=]", "[&BIcHAAA=]", "[&BNIEAAA=]", "[&BIMCAAA=]" },
    // Tuesday
    { "[&BIMBAAA=]", "[&BBkAAAA=]", "[&BEgAAAA=]", "[&BH8HAAA=]", "[&BKgCAAA=]", "[&BGQCAAA=]" },
    // Wednesday
    { "[&BPEBAAA=]", "[&BKYAAAA=]", "[&BMIBAAA=]", "[&BH4HAAA=]", "[&BP0CAAA=]", "[&BDgDAAA=]" },
    // Thursday
    { "[&BOcBAAA=]", "[&BIMAAAA=]", "[&BF0AAAA=]", "[&BKsHAAA=]", "[&BO4CAAA=]", "[&BF0GAAA=]" },
    // Friday
    { "[&BNMAAAA=]", "[&BNUGAAA=]", "[&BMwCAAA=]", "[&BJQHAAA=]", "[&BJsCAAA=]", "[&BHsBAAA=]" },
    // Saturday
    { "[&BBABAAA=]", "[&BJIBAAA=]", "[&BLkCAAA=]", "[&BH8HAAA=]", "[&BBEDAAA=]", "[&BEICAAA=]" },
    // Sunday
    { "[&BCECAAA=]", "[&BC0AAAA=]", "[&BDoBAAA=]", "[&BIkHAAA=]", "[&BO4CAAA=]", "[&BIUCAAA=]" },
};

// PSNA weekday index, 0 = Monday .. 6 = Sunday, for a UTC time.
// Locations change at 08:00 UTC: before that hour the PREVIOUS day's
// locations still apply. E.g. Mon 19:00 PST (= Tue 03:00 UTC) is still
// Monday's set; Tue 01:00 PST (= Tue 09:00 UTC) is Tuesday's set.
static int PsnaWeekdayIndex(std::time_t t)
{
    const std::tm* tmv = std::gmtime(&t);
    if (!tmv) { return 0; }
    int idx = (tmv->tm_wday + 6) % 7; // tm_wday: 0 = Sunday -> Monday = 0
    if (tmv->tm_hour < 8) { idx = (idx + 6) % 7; } // before 08:00 UTC: yesterday
    return idx;
}

static const PoiEntry* FindByChatLink(const char* link)
{
    if (!link) { return nullptr; }
    for (int i = 0; i < kPoiCount; ++i)
    {
        if (std::strcmp(kPois[i].chat_link, link) == 0) { return &kPois[i]; }
    }
    return nullptr;
}

// Today's 6 PSNA chat links as one space-separated line, in agent order
// (Verma, Derwena, Fox, Mehem, Yana, Katelyn). 6 x 11 chars + 5 spaces
// = 71 characters — fits GW2 chat's 199-character line limit
// (GW2 Wiki "Chat panel") in a single paste, no splitting needed.
// No other "daily" tags exist in the dataset, so the daily list is the
// PSNA set only.
static std::string BuildDailyListString(int weekdayIdx)
{
    std::string s;
    for (int i = 0; i < 6; ++i)
    {
        if (i > 0) { s += " "; }
        s += kPsnaLinks[weekdayIdx][i];
    }
    return s;
}

// ---------------------------------------------------------------------------
// Map Bonus Rewards — v1.9, baked 8-week ranking
// ---------------------------------------------------------------------------
// Central Tyria maps have a FIXED 8-week reward-track cycle, changing
// every Thursday at 20:00 UTC. The tracks never change, but the "best"
// ranking depends on live Trading Post prices, so the ranking below is
// a SNAPSHOT computed 17 Nov 2026 from the GW2 Wiki's full 40-reward
// tables (Template:Map bonus reward data) and live
// /v2/commerce/prices, net of the 15% TP tax (vendor value used for
// vendor-only items like Shiny Bauble, 0 for account-bound items like
// Obsidian Shard). Cross-checks: Week 4 top 3 and Week 8 #1 match
// GW TODOBOX (gw-todo.vercel.app/weekly) at the same date — but TODOBOX
// only ranks 5 maps, while this ranking covers ALL 21 Central Tyria
// maps, so Weeks 1–7 differ from TODOBOX where an untracked map (e.g.
// Mount Maelstrom, Timberline Falls) beats one of its five. Values are
// shown truncated to silver in the UI; the full values are in
// docs/map-bonus-rewards.md. Re-check weekly; the UI date-stamps the
// snapshot and points at /wiki mbrp for live values.
// Week number: anchor Thu 24 Jul 2025 20:00 UTC = Week 8 (wiki page,
// July 2025; verified against TODOBOX "Week 4" on 17 Nov 2026).
// Entry waypoints are central hubs for the map (suggested entry points),
// NOT wiki-published starts — every one verified in data/pois.json.
// Headline reward = the single item contributing the most value that
// week (not always the 44x common reward — e.g. Timberline Falls Week 4
// is 30x Shiny Bauble, not its leather common).
struct MapBonusRow { const char* map; const char* reward; const char* link; };  // v1.10.2: no price/value field — prices are not shown in the addon
static const MapBonusRow kMapBonus[8][5] = {
    // Week 1
    { { "Mount Maelstrom", "Shiny Bauble", "[&BM0CAAA=]" },
      { "Malchor's Leap", "Elaborate Totem", "[&BKYCAAA=]" },
      { "Straits of Devastation", "Vial of Powerful Blood", "[&BO4CAAA=]" },
      { "Southsun Cove", "Ancient Bone", "[&BNUGAAA=]" },
      { "Diessa Plateau", "Shiny Bauble", "[&BMQDAAA=]" } },
    // Week 2
    { { "Frostgorge Sound", "Vial of Powerful Blood", "[&BHoCAAA=]" },
      { "Straits of Devastation", "Shiny Bauble", "[&BO4CAAA=]" },
      { "Kessex Hills", "Shiny Bauble", "[&BBIAAAA=]" },
      { "Blazeridge Steppes", "Shiny Bauble", "[&BE4DAAA=]" },
      { "Southsun Cove", "Vicious Fang", "[&BNUGAAA=]" } },
    // Week 3
    { { "Bloodtide Coast", "Shiny Bauble", "[&BKoBAAA=]" },
      { "Frostgorge Sound", "Shiny Bauble", "[&BHoCAAA=]" },
      { "Brisban Wildlands", "Shiny Bauble", "[&BGMAAAA=]" },
      { "Straits of Devastation", "Vicious Claw", "[&BO4CAAA=]" },
      { "Malchor's Leap", "Vial of Powerful Blood", "[&BKYCAAA=]" } },
    // Week 4 (current at build, 17 Nov 2026)
    { { "Malchor's Leap", "Shiny Bauble", "[&BKYCAAA=]" },
      { "Frostgorge Sound", "Vicious Claw", "[&BHoCAAA=]" },
      { "Southsun Cove", "Armored Scale", "[&BNUGAAA=]" },
      { "Mount Maelstrom", "Ancient Bone", "[&BM0CAAA=]" },
      { "Timberline Falls", "Shiny Bauble", "[&BFACAAA=]" } },
    // Week 5
    { { "Cursed Shore", "Shiny Bauble", "[&BBkDAAA=]" },
      { "Iron Marches", "Shiny Bauble", "[&BOwBAAA=]" },
      { "Lornar's Pass", "Shiny Bauble", "[&BOkAAAA=]" },
      { "Fireheart Rise", "Elaborate Totem", "[&BEAFAAA=]" },
      { "Frostgorge Sound", "Powerful Venom Sac", "[&BHoCAAA=]" } },
    // Week 6
    { { "Southsun Cove", "Shiny Bauble", "[&BNUGAAA=]" },
      { "Fields of Ruin", "Shiny Bauble", "[&BNgAAAA=]" },
      { "Cursed Shore", "Vicious Claw", "[&BBkDAAA=]" },
      { "Straits of Devastation", "Vicious Fang", "[&BO4CAAA=]" },
      { "Mount Maelstrom", "Elaborate Totem", "[&BM0CAAA=]" } },
    // Week 7
    { { "Southsun Cove", "Vicious Claw", "[&BNUGAAA=]" },
      { "Fireheart Rise", "Vial of Powerful Blood", "[&BEAFAAA=]" },
      { "Mount Maelstrom", "Armored Scale", "[&BM0CAAA=]" },
      { "Cursed Shore", "Powerful Venom Sac", "[&BBkDAAA=]" },
      { "Frostgorge Sound", "Vicious Fang", "[&BHoCAAA=]" } },
    // Week 8
    { { "Fireheart Rise", "Shiny Bauble", "[&BEAFAAA=]" },
      { "Harathi Hinterlands", "Shiny Bauble", "[&BLAAAAA=]" },
      { "Cursed Shore", "Ancient Bone", "[&BBkDAAA=]" },
      { "Frostgorge Sound", "Elaborate Totem", "[&BHoCAAA=]" },
      { "Straits of Devastation", "Armored Scale", "[&BO4CAAA=]" } },
};

// Central Tyria Map Bonus week, 1–8, for a UTC time. Tracks change
// Thursday 20:00 UTC: before that hour on a Thursday it is still the
// old week. Anchor: Thu 24 Jul 2025 20:00 UTC (epoch 1753387200) = Week 8.
static int MapBonusWeekIndex(std::time_t t)
{
    const std::time_t anchor = 1753387200; // Thu 2025-07-24 20:00 UTC
    if (t < anchor) { return 8; }
    const long weeks = (long)((t - anchor) / (7 * 24 * 3600));
    return (int)(((8 - 1 + weeks) % 8) + 1);
}

// ---------------------------------------------------------------------------
// Rifts — v1.9, baked 11-week rotating cycle
// ---------------------------------------------------------------------------
// Rift Hunting (Secrets of the Obscure). 11 maps ALWAYS have rifts
// (Kryptis: Skywatch Archipelago, Amnytas, Inner Nayos; Titanspawn:
// Lowland Shore, Janthir Syntri, Mistburned Barrens, Bava Nisos;
// Castora: Shipwreck Strand, Starlit Weald, Eternity's Garden,
// Leyspring Hollows) plus 3 more Kryptis maps each week on a FIXED,
// published 11-week cycle (GW2 Wiki Template:Weekly_Rift_Hunting).
// Formula: index = 1 + floor((now - anchor) / 7 days) mod 11, anchor
// Mon 2023-11-06 07:30 UTC (epoch 1699255800, = 2023-11-05 23:30
// America/Los_Angeles). Rotation changes Monday 07:30 UTC.
// Current week at build (Mon 16 Nov 2026): Set 5 — Iron Marches,
// Verdant Brink, Bitterfrost Frontier. Computed, not fetched live —
// verify with /wiki Weekly Rift Hunting in game; if ArenaNet changes
// the cycle the baked table goes stale, same caveat as PSNA.
// HONESTY: rifts spawn RANDOMLY on a map, one per tier, and move when
// closed. There is NO published rift start waypoint. Every waypoint
// below is a central / main-entry hub for its map, verified in
// data/pois.json — the UI must say to use your Scan for Rift keybind once there.
struct RiftRow { const char* map; const char* type; const char* link; };
static const RiftRow kRiftAlways[11] = {
    { "Skywatch Archipelago", "Kryptis", "[&BA4OAAA=]" },
    { "Amnytas", "Kryptis", "[&BDQOAAA=]" },
    { "Inner Nayos", "Kryptis", "[&BGYOAAA=]" },
    { "Lowland Shore", "Titanspawn", "[&BK4OAAA=]" },
    { "Janthir Syntri", "Titanspawn", "[&BCoPAAA=]" },
    { "Mistburned Barrens", "Titanspawn", "[&BFAPAAA=]" },
    { "Bava Nisos", "Titanspawn", "[&BGEPAAA=]" },
    { "Shipwreck Strand", "Castora", "[&BMwPAAA=]" },
    { "Starlit Weald", "Castora", "[&BMAPAAA=]" },
    { "Eternity's Garden", "Castora", "[&BPwPAAA=]" },
    { "Leyspring Hollows", "Castora", "[&BDYQAAA=]" },
};
static const RiftRow kRiftRotating[11][3] = {
    { { "Straits of Devastation", "Kryptis", "[&BO4CAAA=]" },
      { "Elon Riverlands", "Kryptis", "[&BFMKAAA=]" },
      { "Domain of Istan", "Kryptis", "[&BBoLAAA=]" } },
    { { "Sparkfly Fen", "Kryptis", "[&BMkBAAA=]" },
      { "Tangled Depths", "Kryptis", "[&BPUHAAA=]" },
      { "Sandswept Isles", "Kryptis", "[&BEMLAAA=]" } },
    { { "Bloodtide Coast", "Kryptis", "[&BKoBAAA=]" },
      { "Lake Doric", "Kryptis", "[&BK0JAAA=]" },
      { "Domain of Vabbi", "Kryptis", "[&BA8KAAA=]" } },
    { { "Frostgorge Sound", "Kryptis", "[&BHoCAAA=]" },
      { "Ember Bay", "Kryptis", "[&BHgJAAA=]" },
      { "Seitung Province", "Kryptis", "[&BJ4MAAA=]" } },
    { { "Iron Marches", "Kryptis", "[&BOkBAAA=]" },
      { "Verdant Brink", "Kryptis", "[&BOAHAAA=]" },
      { "Bitterfrost Frontier", "Kryptis", "[&BIEJAAA=]" } },
    { { "Mount Maelstrom", "Kryptis", "[&BM0CAAA=]" },
      { "Jahai Bluffs", "Kryptis", "[&BH4LAAA=]" },
      { "New Kaineng City", "Kryptis", "[&BCANAAA=]" } },
    { { "Malchor's Leap", "Kryptis", "[&BKYCAAA=]" },
      { "Bloodstone Fen", "Kryptis", "[&BEEJAAA=]" },
      { "Desert Highlands", "Kryptis", "[&BJEKAAA=]" } },
    { { "Fireheart Rise", "Kryptis", "[&BEAFAAA=]" },
      { "Dry Top", "Kryptis", "[&BHoHAAA=]" },
      { "Auric Basin", "Kryptis", "[&BAIIAAA=]" } },
    { { "Cursed Shore", "Kryptis", "[&BBkDAAA=]" },
      { "Southsun Cove", "Kryptis", "[&BNUGAAA=]" },
      { "Crystal Oasis", "Kryptis", "[&BLsKAAA=]" } },
    { { "Mount Maelstrom", "Kryptis", "[&BM0CAAA=]" },
      { "Lake Doric", "Kryptis", "[&BK0JAAA=]" },
      { "Domain of Vabbi", "Kryptis", "[&BA8KAAA=]" } },
    { { "Timberline Falls", "Kryptis", "[&BFACAAA=]" },
      { "Thunderhead Peaks", "Kryptis", "[&BLsLAAA=]" },
      { "The Echovald Wilds", "Kryptis", "[&BMcMAAA=]" } },
};

// Weekly Rift Hunting set, 1–11, for a UTC time. Rotation changes
// Monday 07:30 UTC (weekly reset). Anchor: Mon 2023-11-06 07:30 UTC.
static int RiftSetIndex(std::time_t t)
{
    const std::time_t anchor = 1699255800; // Mon 2023-11-06 07:30 UTC
    if (t < anchor) { return 1; }
    const long weeks = (long)((t - anchor) / (7 * 24 * 3600));
    return (int)(1 + (weeks % 11));
}

// ---------------------------------------------------------------------------
// Search
// ---------------------------------------------------------------------------

struct SearchResult
{
    const PoiEntry* poi;
    bool  sameMap;
    float dist; // continent units from player, only meaningful if sameMap
    int   rank; // 0 = name/map match, 1 = keyword/tag match (name first)
    std::string matchedTag; // the tag phrase that matched, rank 1 only
    std::string psnaLabel; // v1.7: "Daily Pact Supply — Monday: Verma Giftrender (Ascalon)" etc., PSNA-day results only
};

// A query token matches a haystack ("<display> <map>") if it is a
// substring (tokens of 3+ letters) or a whole word in it. The whole-word
// rule matters for 1-2 letter aliases: "tt" must find the Triple Trouble
// tag, not all 173 entries whose name or map contains "tt" (e.g. every
// "Battlegrounds" map). Same rule as for tag phrases, below.
static bool TokenMatchesHay(const std::string& hay, const std::string& token)
{
    if (token.size() >= 3) { return hay.find(token) != std::string::npos; }
    std::string word;
    for (size_t i = 0; i <= hay.size(); ++i)
    {
        const char c = (i < hay.size()) ? hay[i] : ' ';
        if (c == ' ' || c == '\t')
        {
            if (!word.empty() && word == token) { return true; }
            word.clear();
        }
        else { word += c; }
    }
    return false;
}

// A query token matches a tag phrase if it is a whole word in the phrase,
// or (for tokens of 3+ letters) a substring of it. The whole-word rule
// matters for short aliases: "tt" must match the tag "tt" for Triple
// Trouble, but must NOT match "battle in tarir" just because "battle"
// contains "tt".
static bool TokenMatchesTagPhrase(const std::string& phrase, const std::string& token)
{
    std::string word;
    for (size_t i = 0; i <= phrase.size(); ++i)
    {
        const char c = (i < phrase.size()) ? phrase[i] : ' ';
        if (c == ' ' || c == '\t')
        {
            if (!word.empty() && word == token) { return true; }
            word.clear();
        }
        else { word += c; }
    }
    if (token.size() >= 3 && phrase.find(token) != std::string::npos) { return true; }
    return false;
}

// Returns the first tag phrase (tags are '|' separated) that every token
// matches, or "" if none does. Takes the tags ALREADY lower-cased —
// v1.10.2: the lower-cased haystacks/tags are precomputed once (see
// EnsureSearchPrecomputed) instead of ToLower()ing all 3,773 entries
// on every frame, which was the typing lag.
static std::string FindMatchingTagLower(const std::string& all, const std::vector<std::string>& tokens)
{
    if (all.empty()) { return ""; }
    size_t start = 0;
    while (start <= all.size())
    {
        const size_t sep = all.find('|', start);
        const std::string phrase = all.substr(start, sep == std::string::npos ? std::string::npos : sep - start);
        bool ok = !phrase.empty();
        for (const std::string& t : tokens)
        {
            if (!TokenMatchesTagPhrase(phrase, t)) { ok = false; break; }
        }
        if (ok) { return phrase; }
        if (sep == std::string::npos) { break; }
        start = sep + 1;
    }
    return "";
}

// Lower-cased "<display> <map> <region>" haystacks and '|' tag strings,
// built ONCE (v1.10.2). Before this, Search() rebuilt all 3,773 of
// them with ToLower() — thousands of std::string allocations — on
// every ImGui frame, which is what made typing stutter.
static std::vector<std::string> g_hayLower;
static std::vector<std::string> g_tagsLower;
static void EnsureSearchPrecomputed()
{
    if (!g_hayLower.empty()) { return; }
    g_hayLower.reserve(kPoiCount);
    g_tagsLower.reserve(kPoiCount);
    for (int i = 0; i < kPoiCount; ++i)
    {
        g_hayLower.push_back(ToLower(std::string(kPois[i].display) + " " + kPois[i].map_name + " " + kPois[i].region));
        g_tagsLower.push_back(kPois[i].tags ? ToLower(kPois[i].tags) : std::string());
    }
}

// The real scan. Search() below wraps this with a cache, so it only
// runs when something actually changed — never once per frame.
static std::vector<SearchResult> SearchCompute(const std::string& queryLower)
{
    EnsureSearchPrecomputed();
    std::vector<SearchResult> out;
    if (queryLower.empty()) { return out; }

    // Split the query into tokens; every token must appear in
    // "<display name> <map name>" (rank 0) or in one tag phrase (rank 1).
    std::vector<std::string> tokens;
    {
        std::string cur;
        for (char c : queryLower)
        {
            if (c == ' ' || c == '\t') { if (!cur.empty()) { tokens.push_back(cur); cur.clear(); } }
            else { cur += c; }
        }
        if (!cur.empty()) { tokens.push_back(cur); }
    }

    // v1.7 PSNA-day queries are intercepted here, BEFORE the normal
    // name/tag search, so they return exactly one day's 6 agents in
    // agent order (Verma, Derwena, Fox, Mehem, Yana, Katelyn) with a
    // "Daily Pact Supply — <Weekday>" label — never the whole 40-entry set.
    // A named weekday wins over "daily"/"today" if both are present.
    // Type filters are intentionally ignored here: 20 of the 42 PSNA
    // codes are POIs, and the day's set must always be exactly 6.
    // Plain "psna" / "pact supply" (no day word) falls through to the
    // normal tag search below and returns all 40 PSNA locations.
    {
        const auto hasToken = [&tokens](const char* t)
        {
            for (const std::string& tok : tokens) { if (tok == t) { return true; } }
            return false;
        };
        const bool isPsna = hasToken("psna")
            || (hasToken("pact") && hasToken("supply"));
        int weekdayTok = -1;
        if (isPsna)
        {
            static const char* kDays[7] = {
                "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday"
            };
            for (int d = 0; d < 7; ++d)
            {
                if (hasToken(kDays[d])) { weekdayTok = d; break; }
            }
        }
        const bool isDaily = isPsna && (hasToken("daily") || hasToken("today"));
        if (isPsna && (isDaily || weekdayTok >= 0))
        {
            const int day = (weekdayTok >= 0)
                ? weekdayTok : PsnaWeekdayIndex(std::time(nullptr));
            const bool daily = (weekdayTok < 0);
            for (int i = 0; i < 6; ++i)
            {
                const PoiEntry* p = FindByChatLink(kPsnaLinks[day][i]);
                if (!p) { continue; } // all 42 verified in dataset; skip, don't invent
                SearchResult r;
                r.poi = p;
                r.rank = 0;
                r.sameMap = false;
                r.dist = 0.0f;
                r.matchedTag = "";
                char buf[160];
                std::snprintf(buf, sizeof(buf), "%s — %s: %s (%s)",
                    daily ? "Daily Pact Supply" : "Pact Supply",
                    kPsnaWeekdayNames[day], kPsnaAgentNames[i], kPsnaAgentRegions[i]);
                r.psnaLabel = buf;
                out.push_back(r);
            }
            return out; // exactly today's / that weekday's 6, in table order
        }
    }

    uint32_t curMap = 0;
    float px = 0.0f, py = 0.0f;
    bool havePos = false;
    if (MumbleLink)
    {
        curMap  = MumbleLink->Context.MapID;
        px      = MumbleLink->Context.Compass.PlayerPosition.X;
        py      = MumbleLink->Context.Compass.PlayerPosition.Y;
        // Crash guard (2026-11-16 crash log reported a player position of
        // 0,0,-inf): a non-finite position must never reach the distance
        // math or the sort comparator below. Fall back to alphabetical.
        havePos = (curMap != 0) && IsFiniteFloat(px) && IsFiniteFloat(py);
    }

    for (int i = 0; i < kPoiCount; ++i)
    {
        const PoiEntry& e = kPois[i];
        if (e.type == POI_WAYPOINT && !g_filterWaypoint) { continue; }
        if (e.type == POI_LANDMARK && !g_filterPoi)      { continue; }
        if (e.type == POI_VISTA    && !g_filterVista)    { continue; }

        // v1.6: the haystack is "<display> <map> <region>" — region names
        // are first-class search terms. "Castora" is a region, not a map
        // (5 maps: Starlit Weald, Eternity's Garden, Shipwreck Strand,
        // Leyspring Hollows, Comosus Isle — 205 entries), so it returned
        // nothing before this fix. Same for "Janthir", "Heart of Maguuma",
        // "Horn of Maguuma", etc.
        const std::string& hay = g_hayLower[i];
        bool nameMatch = true;
        for (const std::string& t : tokens)
        {
            if (!TokenMatchesHay(hay, t)) { nameMatch = false; break; }
        }
        std::string matchedTag;
        if (!nameMatch)
        {
            matchedTag = FindMatchingTagLower(g_tagsLower[i], tokens);
            if (matchedTag.empty()) { continue; }
        }

        SearchResult r;
        r.poi     = &e;
        r.rank    = nameMatch ? 0 : 1;
        r.matchedTag = matchedTag;
        r.sameMap = havePos && (uint32_t)e.map_id == curMap
                    && IsFiniteFloat(e.x) && IsFiniteFloat(e.y);
        if (r.sameMap)
        {
            const float d = std::sqrt((e.x - px) * (e.x - px) + (e.y - py) * (e.y - py));
            r.dist = IsFiniteFloat(d) ? d : 0.0f;
            if (!IsFiniteFloat(r.dist)) { r.sameMap = false; r.dist = 0.0f; }
        }
        else
        {
            r.dist = 0.0f;
        }
        out.push_back(r);
    }

    std::sort(out.begin(), out.end(), [](const SearchResult& a, const SearchResult& b)
    {
        // Exact name matches first, then tag matches; within each rank,
        // same-map first, then nearest, then alphabetical (as before).
        if (a.rank != b.rank) { return a.rank < b.rank; }
        if (a.sameMap != b.sameMap) { return a.sameMap > b.sameMap; }
        // Defensive: a non-finite distance sorts last, never as NaN, so
        // the comparator keeps a strict weak ordering even on bad input.
        const float da = IsFiniteFloat(a.dist) ? a.dist : 1e30f;
        const float db = IsFiniteFloat(b.dist) ? b.dist : 1e30f;
        if (a.sameMap && b.sameMap && da != db) { return da < db; }
        const int cmp = std::strcmp(a.poi->display, b.poi->display);
        if (cmp != 0) { return cmp < 0; }
        return std::strcmp(a.poi->map_name, b.poi->map_name) < 0;
    });
    return out;
}

// Cached search (v1.10.2 — the typing-lag fix). AddonRender used to
// call Search() on EVERY frame, so every keystroke — and every idle
// frame — re-scanned all 3,773 entries, re-sorted, and re-allocated.
// Now the result list is computed once and reused until the query,
// the type filters, the current map, the (bucketed)
// player position, or the PSNA day actually changes. Typing a
// character re-runs the scan exactly once for that keystroke; holding
// still costs nothing. Same-map ordering stays live because the
// player position is part of the key, bucketed to 500 continent
// units so small movements don't thrash the cache.
static const std::vector<SearchResult>& Search(const std::string& queryLower)
{
    static const std::vector<SearchResult> s_empty;
    static std::vector<SearchResult> s_cached;
    static std::string s_cachedQuery;
    static bool s_cachedFilters[3] = { true, true, true };
    static int s_cachedPsnaDay = -2;
    static uint32_t s_cachedMap = 0;
    static int s_cachedPosX = 0, s_cachedPosY = 0;
    static bool s_haveCache = false;

    if (queryLower.empty()) { return s_empty; }

    // Cheap key components: current map + bucketed player position
    // (same-map / nearest sorting depends on these), and the PSNA day
    // (only matters for psna queries — skip the gmtime call otherwise).
    uint32_t curMap = 0;
    int posX = 0, posY = 0;
    if (MumbleLink && MumbleLink->Context.MapID != 0
        && IsFiniteFloat(MumbleLink->Context.Compass.PlayerPosition.X)
        && IsFiniteFloat(MumbleLink->Context.Compass.PlayerPosition.Y))
    {
        curMap = MumbleLink->Context.MapID;
        posX = (int)(MumbleLink->Context.Compass.PlayerPosition.X / 500.0f);
        posY = (int)(MumbleLink->Context.Compass.PlayerPosition.Y / 500.0f);
    }
    int psnaDay = -1;
    if (queryLower.find("psna") != std::string::npos
        || queryLower.find("pact") != std::string::npos)
    {
        psnaDay = PsnaWeekdayIndex(std::time(nullptr));
    }

    if (s_haveCache
        && queryLower == s_cachedQuery
        && g_filterWaypoint == s_cachedFilters[0]
        && g_filterPoi == s_cachedFilters[1]
        && g_filterVista == s_cachedFilters[2]
        && psnaDay == s_cachedPsnaDay
        && curMap == s_cachedMap
        && posX == s_cachedPosX && posY == s_cachedPosY)
    {
        return s_cached;
    }

    s_cached = SearchCompute(queryLower);
    s_cachedQuery = queryLower;
    s_cachedFilters[0] = g_filterWaypoint;
    s_cachedFilters[1] = g_filterPoi;
    s_cachedFilters[2] = g_filterVista;
    s_cachedPsnaDay = psnaDay;
    s_cachedMap = curMap;
    s_cachedPosX = posX;
    s_cachedPosY = posY;
    s_haveCache = true;
    return s_cached;
}

static const char* TypeLabel(int type)
{
    switch (type)
    {
        case POI_WAYPOINT: return "Waypoint";
        case POI_LANDMARK: return "POI";
        case POI_VISTA:    return "Vista";
        default:           return "?";
    }
}

// ---------------------------------------------------------------------------
// Load / unload
// ---------------------------------------------------------------------------

void AddonLoad(AddonAPI_t* aApi)
{
    if (!aApi) { return; }
    APIDefs = aApi;

    if (!APIDefs->ImguiContext)
    {
        APIDefs->Log(LOGL_WARNING, "Tyria Finder",
            "Tyria Finder: no ImGui context from Nexus, not loading UI.");
        return;
    }
    ImGui::SetCurrentContext((ImGuiContext*)APIDefs->ImguiContext);
    ImGui::SetAllocatorFunctions(
        (void* (*)(size_t, void*))APIDefs->ImguiMalloc,
        (void (*)(void*, void*))APIDefs->ImguiFree);

    NexusLink  = (NexusLinkData_t*)APIDefs->DataLink_Get("DL_NEXUS_LINK");
    MumbleLink = (Mumble::Data*)APIDefs->DataLink_Get("DL_MUMBLE_LINK");

    APIDefs->GUI_Register(RT_Render, AddonRender);
    APIDefs->GUI_Register(RT_OptionsRender, AddonOptions);
    APIDefs->GUI_RegisterCloseOnEscape("Tyria Finder", &g_visible);

    // Configurable in Nexus > Options > Keybinds. Default Alt+Shift+W.
    APIDefs->InputBinds_RegisterWithString(
        "KB_TYRIA_FINDER_TOGGLE", OnToggleKeybind, "ALT+SHIFT+W");

    // QuickAccess icon in the Nexus bar at the top of the screen.
    // Nexus API v6 (third_party/nexus/Nexus.h): QuickAccess_Add takes
    // (identifier, texture, hover texture, keybind, tooltip); clicking
    // the icon invokes the keybind, so it toggles exactly like Alt+Shift+W.
    // Textures are created first from the embedded PNGs in icon_data.h.
    {
        Texture_t* tex = APIDefs->Textures_GetOrCreateFromMemory(
            "TEX_TYRIA_FINDER", (void*)kIconPng, kIconPng_SIZE);
        Texture_t* texHover = APIDefs->Textures_GetOrCreateFromMemory(
            "TEX_TYRIA_FINDER_HOVER", (void*)kIconHoverPng, kIconHoverPng_SIZE);
        if (tex && texHover)
        {
            APIDefs->QuickAccess_Add("QA_TYRIA_FINDER",
                "TEX_TYRIA_FINDER", "TEX_TYRIA_FINDER_HOVER",
                "KB_TYRIA_FINDER_TOGGLE",
                "Tyria Finder - click to find anything in Tyria");
            g_quickAccessAdded = true;
        }
        else
        {
            APIDefs->Log(LOGL_WARNING, "Tyria Finder",
                "Tyria Finder: QuickAccess icon texture failed to load, "
                "hotkey Alt+Shift+W still works.");
        }
    }

    {
        char loadMsg[256];
        std::snprintf(loadMsg, sizeof(loadMsg),
            "Tyria Finder v1.11.0 loaded. ImGui %s. "
            "Alt+Shift+W search.",
            ImGui::GetVersion());
        APIDefs->Log(LOGL_INFO, "Tyria Finder", loadMsg);
    }
}

void AddonUnload()
{
    if (!APIDefs) { return; }
    // Remove the QuickAccess icon first, while the keybind it invokes
    // still exists, then deregister everything else.
    if (g_quickAccessAdded)
    {
        APIDefs->QuickAccess_Remove("QA_TYRIA_FINDER");
        g_quickAccessAdded = false;
    }
    APIDefs->InputBinds_Deregister("KB_TYRIA_FINDER_TOGGLE");
    APIDefs->GUI_DeregisterCloseOnEscape("Tyria Finder");
    APIDefs->GUI_Deregister(AddonRender);
    APIDefs->GUI_Deregister(AddonOptions);
    APIDefs = nullptr;
}

void OnToggleKeybind(const char* /*aIdentifier*/, bool aIsRelease)
{
    if (!aIsRelease)
    {
        g_visible = !g_visible;
        if (g_visible) { g_focusSearch = true; }
    }
}

// ---------------------------------------------------------------------------
// Render
// ---------------------------------------------------------------------------

void AddonRender()
{
    if (!APIDefs) { return; }
    if (NexusLink && !NexusLink->IsGameplay) { return; }
    if (!g_visible) { return; }

    // Style first, before Begin, so window padding actually applies
    // (pushing it after Begin left the first row clipped at the edge).
    ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(14, 12));
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, ImVec2(8, 6));
    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(8, 6));
    ImGui::SetNextWindowSize(ImVec2(640, 640), ImGuiCond_FirstUseEver);
    if (!ImGui::Begin("Tyria Finder", &g_visible))
    {
        ImGui::PopStyleVar(3);
        ImGui::End();
        return;
    }

    // One short line — the detail lives in the empty state below.
    ImGui::TextDisabled("Search a place, resource, boss, event, or region — click a result to copy its chat link.");

    if (g_focusSearch) { ImGui::SetKeyboardFocusHere(); g_focusSearch = false; }
    ImGui::SetNextItemWidth(-70.0f);
    const bool enterPressed = ImGui::InputTextWithHint(
        "##Search", "Search Tyria...", g_query, sizeof(g_query), ImGuiInputTextFlags_EnterReturnsTrue);
    ImGui::SameLine();
    if (ImGui::Button("Clear")) { g_query[0] = '\0'; }

    // Lower-cased copy, recomputed only when the query text actually
    // changed (v1.10.2 — was a ToLower allocation every frame).
    {
        static char s_prevQuery[128] = {};
        if (std::strcmp(s_prevQuery, g_query) != 0)
        {
            std::strncpy(g_queryLower, ToLower(g_query).c_str(), sizeof(g_queryLower) - 1);
            g_queryLower[sizeof(g_queryLower) - 1] = '\0';
            std::strncpy(s_prevQuery, g_query, sizeof(s_prevQuery) - 1);
            s_prevQuery[sizeof(s_prevQuery) - 1] = '\0';
        }
    }

    ImGui::Checkbox("Waypoints", &g_filterWaypoint); ImGui::SameLine();
    ImGui::Checkbox("POIs", &g_filterPoi);           ImGui::SameLine();
    ImGui::Checkbox("Vistas", &g_filterVista);

    // v1.10.1 layout rule: while the user is searching, the info
    // sections below stay hidden so the result list renders immediately
    // under the search box, inside the window, clickable. With an empty
    // search box they show exactly as before.
    const bool searching = g_queryLower[0] != '\0';
    const std::time_t now = std::time(nullptr); // v1.10.2: one clock read per frame for PSNA / Map Bonus / Rifts

    // Daily Pact Supply Network Agents — visible when the search box is
    // empty (v1.10.1: hidden while searching, so results are not pushed
    // off-screen). "Copy daily list" copies today's 6 chat links as one
    // space-separated line, ready to paste in GW2 chat. It does not
    // touch the single-result copy below.
    if (!searching)
    {
        const int psnaDay = PsnaWeekdayIndex(now);
        ImGui::Separator();
        ImGui::TextColored(ImVec4(0.91f, 0.79f, 0.48f, 1.0f),
            "Daily Pact Supply Network Agents — %s",
            kPsnaWeekdayNames[psnaDay]);
        ImGui::TextDisabled("Locations change at 08:00 UTC / 00:00 PST.");
        if (ImGui::Button("Copy daily list"))
        {
            const std::string list = BuildDailyListString(psnaDay);
            if (CopyToClipboard(list.c_str()))
            {
                std::strncpy(g_dailyCopiedList, list.c_str(), sizeof(g_dailyCopiedList) - 1);
                g_dailyCopiedList[sizeof(g_dailyCopiedList) - 1] = '\0';
                g_dailyCopiedAt = ImGui::GetTime();
            }
        }
        ImGui::SameLine();
        if (g_dailyCopiedAt >= 0.0 && (ImGui::GetTime() - g_dailyCopiedAt) < 5.0)
        {
            ImGui::TextColored(ImVec4(0.3f, 1.0f, 0.3f, 1.0f), "Copied daily list!");
        }
        else
        {
            ImGui::TextDisabled("Today's 6 agents, ready to paste.");
        }
        ImGui::Separator();
    }

    // Map Bonus Rewards — v1.9, directly under the PSNA section, same
    // gold header style. Click a row to copy its entry waypoint code.
    // v1.10.2: NO prices shown — row is "1. Malchor's Leap — Shiny
    // Bauble" only. The ranking order is the 17 Nov 2026 snapshot
    // order. Hidden while searching (v1.10.1).
    if (!searching)
    {
        const int mbWeek = MapBonusWeekIndex(now);
        ImGui::TextColored(ImVec4(0.91f, 0.79f, 0.48f, 1.0f),
            "Map Bonus Rewards — Week %d", mbWeek);
        ImGui::TextDisabled("Best Central Tyria maps this week · resets Thu 20:00 UTC.");
        for (int i = 0; i < 5; ++i)
        {
            const MapBonusRow& row = kMapBonus[mbWeek - 1][i];
            char label[192];
            std::snprintf(label, sizeof(label), "%d. %s  —  %s",
                i + 1, row.map, row.reward);
            if (ImGui::Selectable(label))
            {
                if (CopyToClipboard(row.link))
                {
                    g_lastCopiedId = -2;
                    std::strncpy(g_lastCopiedLink, row.link, sizeof(g_lastCopiedLink) - 1);
                    g_lastCopiedLink[sizeof(g_lastCopiedLink) - 1] = '\0';
                    g_lastCopiedAt = ImGui::GetTime();
                }
            }
            if (ImGui::IsItemHovered())
            {
                ImGui::SetTooltip("Click to copy %s", row.link);
            }
        }
        ImGui::Separator();
    }

    // Rifts This Week — v1.9, third in the stack. Hidden while searching
    // (v1.10.1). Rotating 3 always visible; the 11 always-available maps
    // under a collapsing header so the window stays manageable. Click a
    // row to copy its entry waypoint code only (no "copy all" — 14 codes
    // would exceed the 199-char chat limit). The note is the honesty
    // flag: rifts spawn randomly, so the waypoint is an entry hub, not a
    // rift location.
    if (!searching)
    {
        const int riftSet = RiftSetIndex(now);
        ImGui::TextColored(ImVec4(0.91f, 0.79f, 0.48f, 1.0f),
            "Rifts This Week");
        ImGui::TextDisabled("Resets Monday 07:30 UTC. Rifts spawn randomly on each map — use your Scan for Rift keybind once you're there.");
        ImGui::TextDisabled("Rotating this week — Kryptis:");
        for (int i = 0; i < 3; ++i)
        {
            const RiftRow& row = kRiftRotating[riftSet - 1][i];
            char label[192];
            std::snprintf(label, sizeof(label), "%s  —  %s", row.map, row.type);
            if (ImGui::Selectable(label))
            {
                if (CopyToClipboard(row.link))
                {
                    g_lastCopiedId = -2;
                    std::strncpy(g_lastCopiedLink, row.link, sizeof(g_lastCopiedLink) - 1);
                    g_lastCopiedLink[sizeof(g_lastCopiedLink) - 1] = '\0';
                    g_lastCopiedAt = ImGui::GetTime();
                }
            }
            if (ImGui::IsItemHovered())
            {
                ImGui::SetTooltip("Click to copy %s", row.link);
            }
        }
        if (ImGui::CollapsingHeader("Always available (11 maps)"))
        {
            const char* group = nullptr;
            for (int i = 0; i < 11; ++i)
            {
                const RiftRow& row = kRiftAlways[i];
                if (!group || std::strcmp(group, row.type) != 0)
                {
                    group = row.type;
                    ImGui::TextDisabled("%s:", group);
                }
                char label[192];
                std::snprintf(label, sizeof(label), "%s  —  %s", row.map, row.type);
                if (ImGui::Selectable(label))
                {
                    if (CopyToClipboard(row.link))
                    {
                        g_lastCopiedId = -2;
                        std::strncpy(g_lastCopiedLink, row.link, sizeof(g_lastCopiedLink) - 1);
                        g_lastCopiedLink[sizeof(g_lastCopiedLink) - 1] = '\0';
                        g_lastCopiedAt = ImGui::GetTime();
                    }
                }
                if (ImGui::IsItemHovered())
                {
                    ImGui::SetTooltip("Click to copy %s", row.link);
                }
            }
        }
        ImGui::Separator();
    }

    // Daily Activity — REMOVED in v1.10.4 (Audrey's ask). The whole
    // v1.9 static section is gone: no header, no text, no button, no
    // "today's game is one of" line. The four individual activities
    // (Crab Toss, Keg Brawl, Sanctum Sprint, Southsun Survival) are
    // still searchable by name to their own waypoints; only the
    // "daily activity" umbrella tags / Edinna routing were removed
    // (see docs/daily-activities.md).

    const std::vector<SearchResult>& results = Search(g_queryLower); // v1.10.2: reference to the cached list — no per-frame copy
    if (enterPressed && !results.empty()) { CopyResult(results[0].poi); }

    // "Copied!" feedback, visible for a few seconds after a copy.
    // g_lastCopiedId is a POI id for search results, or -2 for a
    // Map Bonus / Rifts row copy (no result to highlight).
    if (g_lastCopiedId != -1 && (ImGui::GetTime() - g_lastCopiedAt) < 5.0)
    {
        ImGui::TextColored(ImVec4(0.3f, 1.0f, 0.3f, 1.0f),
            "Copied! %s", g_lastCopiedLink);
    }

    if (g_queryLower[0] == '\0')
    {
        // Empty state (v1.10.1): static hint only — the clickable
        // "Try one of these" example buttons were removed at Audrey's
        // request. The daily info sections below fill the rest of the
        // window when the search box is empty.
        ImGui::TextDisabled("Type anything — a waypoint, POI, vista, adventure, mini dungeon, or region.");
        ImGui::TextDisabled("Find waypoints, POIs, and vistas — plus jumping puzzles, adventures, mini dungeons, collections, bosses, metas, and gathering spots.");
    }
    else if (results.empty())
    {
        ImGui::TextDisabled("No matches. Check the type filters, or try a shorter / different spelling.");
    }
    else
    {
        const size_t shown = results.size() > 250 ? 250 : results.size();
        ImGui::TextDisabled("Showing %zu of %zu matches%s",
            shown, results.size(),
            (MumbleLink && MumbleLink->Context.MapID != 0)
                ? " - same-map results first" : "");
        ImGui::BeginChild("TyriaFinderResults", ImVec2(0, 0), true);
        // v1.10.2: ListClipper — only the rows actually on screen
        // build Selectable/Button widgets each frame (was all 250).
        ImGuiListClipper clipper;
        clipper.Begin((int)shown);
        while (clipper.Step())
        {
        for (int ii = clipper.DisplayStart; ii < clipper.DisplayEnd; ++ii)
        {
            size_t i = (size_t)ii;
        {
            const PoiEntry* p = results[i].poi;
            // Clean line only: Name — Type · Map (Region). Keyword tags
            // still drive the search, but are never printed here.
            char label[320];
            std::snprintf(label, sizeof(label), "%s  —  %s  ·  %s (%s)%s",
                p->display, TypeLabel(p->type), p->map_name, p->region,
                results[i].sameMap ? "  [here]" : "");
            // PSNA-day results carry their day/agent label.
            if (!results[i].psnaLabel.empty())
            {
                std::strncat(label, "  -- ", sizeof(label) - std::strlen(label) - 1);
                std::strncat(label, results[i].psnaLabel.c_str(), sizeof(label) - std::strlen(label) - 1);
            }
            // Clicking the row copies its chat link.
            if (ImGui::Selectable(label, g_lastCopiedId == p->id))
            {
                CopyResult(p);
            }
            if (ImGui::IsItemHovered())
            {
                ImGui::SetTooltip("Click to copy %s", p->chat_link);
            }
        } // row block
        } // for ii in clipper range
        } // while clipper.Step()
        ImGui::EndChild();
    }

    ImGui::PopStyleVar(3);
    ImGui::End();
}
