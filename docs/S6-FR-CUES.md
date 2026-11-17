# Scene 6, French cut: word-level cue map and the retime (TMAP), 2026-11-17

Source: `G:\SOTR\Meeting notes\Nov 2026\Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` (121.25 s).
Transcribed with faster-whisper medium, fr, word timestamps. Raw output: `words.txt` / `words.json` in
`C:\Users\Homie\AppData\Local\Temp\claude\1a87b61f2be73074\a669ac62-a83c-484c-aa60-f60b13915ad0\scratchpad\`
(scratch, may be cleared; this table is the record).

## Found
- The first word is at **15.94 s** (not 0). Before it there's only sound.
- **The track still has three English lines:** "You're leaving France?" (88.84), "Where are you going?" (97.50),
  "Away from here." (99.96-102.32; "Away" scored 0.04, so it may be French, "Loin d'ici"; check by ear). For Homie.
- After 102.3 s there's no voice: 19 s for the map, liquefy and dissolve.

## Cue table (old v14 timeline -> the French track)

| Line (on the track) | new s | old s (v14) | speed (old s per new s) |
|---|---|---|---|
| (smoke, the march) | 0.00 | 0.0 | |
| Après vingt-trois années de guerre | 15.94 | 18.0 | 1.13 |
| J'ai appris à être forte... comme les hommes | 19.26 | 23.5 | 1.66 |
| Pour nos braves, nos glorieux soldats | 24.84 | 32.0 | 1.52 |
| Nous avons connu la victoire | 29.84 | 38.0 | 1.20 |
| Austerlitz | 33.04 | 41.0 | 0.94 |
| Wagram | 34.28 | 43.5 | 2.02 |
| Iéna | 35.92 | 46.0 | 1.52 |
| Eylau | 37.50 | 50.0 | 2.53 |
| Friedland | 38.74 | 52.5 | 2.02 |
| Nous avons cru à la victoire | 40.32 | 57.0 | 2.85 |
| Et puis il y a eu la famine | 43.90 | 59.5 | 0.70 |
| Les exécutions | 46.80 | 63.0 | 1.21 |
| La mort | 48.64 | 67.0 | 2.17 |
| Et malgré tout, nous avons parlé | 51.42 | 79.0 | 4.3 (Goya fades, colour walls come in) |
| de liberté | 52.86 | 82.4 | 2.4 |
| d'égalité | 54.20 | 84.4 | 1.5 |
| de fraternité | 55.80 | 86.4 | 1.25 |
| Il fallait continuer à se battre pour Napoléon | 58.10 | 96.0 | 4.2 (Louise: shorter L/É/F hold) |
| jusqu'à Waterloo | 62.50 | 101.0 | 1.14 |
| là où Napoléon est vaincu | 64.68 | 105.0 | 1.83 |
| Humilié, exilé... je ne reconnais plus mon pays | 68.92 | 110.0 | 1.18 |
| La France est divisée | 75.28 | 121.0 | 1.73 |
| Monarchistes | 78.80 | 124.0 | 0.85 |
| Napoléonistes | 80.08 | 126.0 | 1.56 |
| La France est dangereuse pour moi | 81.84 | 128.0 | 1.14 |
| (the flags start burning) | 83.90 | 130.5 | 1.21 |
| Alors, je pars (85.98) / burn ends | 88.60 | 137.5 | 1.49 |
| [EN] You're leaving France? (88.84) / Oui, je dois partir... loin de tout ça | 90.74 | 141.0 | 1.64 |
| [EN] Where are you going? | 97.50 | 145.0 | 0.59 |
| Loin. | 99.28 | 147.0 | 0.89 |
| (the map, at real speed) | 112.78 | 160.5 | 1.00 |
| (ink dissolve, 7.5 s, then clear) | 120.25 | 165.0 | 0.60 |
| (end, clear) | 121.25 | 165.0 | |

The LIBERTÉ / ÉGALITÉ / FRATERNITÉ words show from 52.9 to about 62 s, about 9 s (it was 17.6 s).
The fastest stretches are the five battles (2-2.9x, each picture about 2.5 s) and 67-79 old (the Goya death fades in 2.9 s).

## How the retime is built (`render_s6.py --retime-fr`, not written yet)
- TMAP = the knots above (new -> old, piecewise linear). Every scripted cue reads t_old = TMAP(t_new).
- Physical motion at real speed: the loop textures (GenFlag.frame ~1041, GenSmoke.draw ~1183, Smoke.draw ~1651, the
  sin(t*..) wobbles) read phys = t_new + (t_passed - t_old_now), which keeps the +3/+7 flag offsets. dt = 1/FPS real.
- The ink dissolve gets its own real-time length (7.5 s), then 1 s fully clear.
- Off by default: v14 renders bit-identically without it.
- Review render at scale 0.5 (`--final`, picture only, no scratch mux) into
  `D:/SOTR/SOTR_MEDIA/04_WORKING_FILES/S6_french_review/`, then the composite `06_S6_wars_FRENCH_review.mp4` with Darrin's
  wav as the sound and these French lines as the captions (the three English lines tagged [EN]).
