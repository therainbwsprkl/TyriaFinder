> **REMOVED in v1.10.3 (2026-11-17, Audrey's request — the feature felt clunky and confusing).**
>
> The whole user-custom-tags feature is gone from the addon: no Tag button on result rows, no add-tag editor, no My tags list, no per-user tag file loading/saving, no user-tag merge in Search(). Search is back to baked tags only (336 entries / 2,773 phrases). An existing per-user tag file on disk is left alone, just unused — delete it by hand if you want it gone. The rest of this note is the historical design record of v1.10, kept for reference only.
>
# User-custom tags — Tyria Finder v1.10

Any user can add their own search keywords to any waypoint / POI / vista,
in-game. This note is the design record; the user-facing version is in
`README.md` ("What changed in v1.10").

## Storage

- File: **`TyriaFinder_user_tags.txt`**, next to the DLL in
  `<Guild Wars 2>\addons\`. Created on first save; a missing file just
  means no user tags yet.
- Format: plain text, one tag per line — chat link, a tab, then the tag
  phrase, e.g. `[&BOAHAAA=]\tmy farm spot`. Two comment lines at the top
  explain the format. Human-readable and hand-editable; restart GW2
  after hand-editing (the file is loaded once, at startup).
- The file is **never** baked into the DLL and **never** overwrites
  `data/tags.json`. Tags are **never sent anywhere** — the addon makes
  no network calls at all.
- A tag is only a search phrase. It cannot change a place's name, map,
  or chat code, and it cannot create a new waypoint. Tags for a chat
  link that is not in the dataset are silently dropped on load.

## Validation (C++ `NormalizeUserTag`, mirrored in `tools/test_search.py`)

Trim, collapse internal whitespace, lowercase; 1–40 characters; must
contain at least one letter or number; no tab / line break / `|` (those
would break the file format). No duplicates, case-insensitive, against
the baked tags for that place or the user's own tags for it. At most
20 tags per place. Invalid input shows a short reason in the editor.

## Search

User tags merge with baked tags at **rank 1** in `Search()` — same
whole-word / substring token rule as baked tags (`TokenMatchesTagPhrase`),
same ranking (name match first, then tag match, then same-map / nearest /
alphabetical). They stay **hidden from result lines** (v1.8.1 rule):
a result line never prints any tag, baked or user.

## UI

- **Tag button:** a small `Tag` button at the right of every result row.
  Clicking it opens the add-tag editor above the results (it does not
  copy the link — clicking the row itself still copies).
- **Editor:** "Add a tag — <place>", a text field (`e.g. my farm spot`),
  **Add tag** (or Enter) and **Done**. Shows the place's existing user
  tags with a Remove button each, plus a short feedback line
  ("Added …" / refusal reason, shown ~5 s) and a note that tags are
  only on this computer.
- **My tags:** a collapsing header below the Daily Activity section
  listing every tagged place alphabetically by display name, each with
  its tags and a Remove button per tag. Hidden entirely when the user
  has no tags yet.
- Saves happen **immediately** on add / remove (file rewritten, tags
  sorted per place). If the save fails, the in-memory change is rolled
  back and the editor says the addons folder may not be writable.

## Implementation notes

- File I/O is plain C (`fopen` / `fgets` / `fputs`), not `<fstream>`:
  `<fstream>` pulled ~0.6 MB of static libstdc++ into the DLL
  (.text 0xac440 → 0x1452f8, DLL 1.9 MB → 3.5 MB in the first v1.10
  build). With C I/O the DLL is back to 1,952,840 bytes.
- The DLL directory is found from `GetModuleFileNameA(hSelf, …)` at
  load time; the path is stored in `g_userTagsPath`.
- `FindMatchingUserTag()` is called only after the baked-tag lookup
  misses, so baked tags keep their existing behaviour exactly.
- What cannot be tested on the Linux build machine: the actual file
  I/O under Windows and the ImGui flow. What is tested:
  `tools/test_search.py` (192 cases) mirrors the merge and the
  validation exactly, including a negative case ("banana" finds
  nothing without the user tag). The in-game flow is Audrey's test
  in README.md ("How to test — v1.10", step 6b).
