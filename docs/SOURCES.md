# SOURCES — where the source material lives

None of this is in git. The script is copyrighted, and media is never committed. All of it
is on Homie's Mac at **`/Users/homie/Documents/SOTR/`**, on the Windows PC at
**`C:\Users\Homie\Documents\SOTR\`**, and mirrored on the external drive at
**`G:\SOTR\HF\SOTR\`** (2026-09-22, 210 MB, verified identical file count). Copy the
folder to the other machine by hand (or the drive), keeping the same layout.

| File / folder | What it is | Used for |
|---|---|---|
| `2026 RMIT Dev 'Secret of the Raft' Workhop Draft V1.pdf` | The workshop script, 24 pp. © Louise Howlett / ReAction Theatre | Canon. `BIBLE.md` summarises it |
| `2026 Secret of the Raft - Propsed Work Schedule V1.pdf` | Draft schedule, weeks 1–13 (30/08 → 22/11) | Scope: Scene 9 items marked "Homie?" |
| `SOTR_RMIT26_Plan_DRAFT_v0.2.pdf` | Black Box set, overview and plan (12.09.26) | `STAGE.md` geometry |
| `INSPO/2026 Visual References - SOTR.pdf` | 13-page mood deck across all scenes | Look references |
| `INSPO/Sc 9/` | 2 salon interiors, 16 photos from the 2022 dev showing, `Dev Showing.mp4` (7:15) | Salon refs; how Scene 9 was staged in 2022 |
| `INSPO/Sc 7/` | Dev-showing photos and `Dev showing.mp4` (3:44) | Not ours (Sahaj). Shows how projection sat behind the actors |
| `INSPO/Sc 1–6, 8, 10/` | Empty | — |
| `2022 Presentation 2 ReAction CCC/` | 11 slides plus the .pptx. Includes 3D renders of the projection box. **Slide 9 = Homie's 2022 Géricault studio concept**, the only prior Scene 9 visual work | Staging intent; studio layout and fragment dissolve |
| `vlcsnap-2026-09-21-*.png` (5) | UE5/Unity stills: alpine farmhouse (Scene 4), burning battlefield (Scenes 3/5/6) | Hyper-real benchmark only. **Not Scene 9** |

Generated plates and loops go to a working folder outside the repo. Pick one location,
note it here, and log every file to `REGISTER.md`.

**Working folder (decided 2026-09-21):** `C:\Users\Homie\Documents\SOTR_MEDIA\`
on the Windows PC, mirrored on the external drive at **`G:\SOTR\HF\SOTR_MEDIA\`**
(2026-09-22, verified identical). Outside the repo, beside the source folder. Subfolders
and the file naming rule are in its own `README.txt`; every file in it must have a row in
`REGISTER.md`. It travels between machines by SSD or OneDrive, like the source folder —
git carries only text.

## External drive mirror (`G:\SOTR\HF\`) — set up 2026-09-22

A full secondary copy for working from the MacBook, alongside Homie's other SOTR
production folders already on that drive (`Final Show`, `Misc Assets`, `Unreal Engine
Project files`, and an existing empty `HF work` folder — not the same as this `HF`).

```
G:\SOTR\HF\
├── SOTR_GENpipeline\   a real `git clone` of the GitHub repo (not a file copy — pushes
│                       and pulls normally, origin already set)
├── SOTR_MEDIA\         full copy of the working folder, verified identical
└── SOTR\               full copy of the source folder, verified identical file count
```

**This is a one-time snapshot, not a live sync.** `SOTR_GENpipeline` on the drive will
drift from `git pull`/`push` like any other clone (that's normal and fine — it's git).
`SOTR_MEDIA` and `SOTR`, though, do **not** auto-update — if either changes on this PC,
the drive's copy goes stale until someone copies again by hand. Treat the drive as a
snapshot to carry to the Mac, not a mirror that stays current on its own.

## Homie's earlier Unreal Engine renders (Scenes 2-5), found 2026-09-28

`F:\OrCha Drive\SOR Show Final\SOR SHOW\SOR Renders\` (127 GB, reference only, never modified). Four
angles each, because that show projected Front / Left / Right / Bottom (floor). 1920x1080 per angle,
DXV 3 (Resolume) .mov + h264 .mp4.

| Folder | What | Used for |
|---|---|---|
| `New Renders/Camps/`, `Camps/Exports/` | The red dusk battlefield with tents (Scenes 3/5), 432 s. `*_CannonballExplosion.mov` (qtrle ARGB, 7.4 s): Scene 5's ending, flash then black smoke and embers | **Scene 6 starts from this smoke** |
| `New Renders/Alps/`, `Flat renders/`, `Alps/` | Scene 4, the alpine farmhouse | — |
| `sz/` | The sea: the Medusa, day into night, and the intro title | Scenes 2/7/8 reference |
| `Transitions/` | Licensed stock ink-bloom mattes (Envato-style) + AE project | Scene 6's ink language (Homie's licence) |
| `Presentation/2022 SHOWING POWERPOINT CCC` | 20-slide development history (2016-2022) | Background |

## Scene 6 public-domain sources (downloaded 2026-09-28, Homie's go-ahead)

In `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/S6_public_domain/`, 17 images from Wikimedia Commons (BnF
Gallica, Paris Musées, the Met). **`_manifest.json` beside them has each file's Commons page, licence
(Public domain or CC0), date, artist and sha256.** Large originals were fetched at 5000 px wide max.

| Group | Files | Dates |
|---|---|---|
| The five battles + Waterloo | Austerlitz and Iéna (Duplessi-Bertaux engravings), Eylau, Friedland, Wagram (period estampes), Mont-Saint-Jean 1815, Jazet's battlefield 1816 | 1805-1816 |
| Goya, *Disasters of War* | pl. 15 executions, pl. 18 death, pl. 30 ravages, pl. 50 famine; pl. 41, 44, 45 fleeing (Met, CC0) | 1810-12 |
| The continent's outline | Natural Earth 1:50m Admin 0 countries (GeoJSON, public domain), fitted to Bellin's map on seven capes (`render_s6.py`) | modern data, shape only |
| Maps | Delisle, West Africa (1707); Bellin, Africa and the mouth of the Senegal (1740s). BnF stamps to be cropped | 1707-1749 |
| The Medusa | Baugean's frigate (the same image as the client's reference deck p. 8). The 1818 raft plan and raft revolt are **later than 1816**: kept for Scenes 8-9 reference, not for Scene 6 | c. 1816 / 1818 |

Fonts in `tools/fonts/` (in git, SIL Open Font License, licences beside them): GFS Didot, Pinyon Script.
