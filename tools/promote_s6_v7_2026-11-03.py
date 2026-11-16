"""2026-11-03: put Scene 6 v7 (the map diffuses to alpha; render_s6.py --v6 --v7-alpha) into the show under the SAME names.

  4K native render (--scale 2.0, ProRes 4444 + alpha)  -> 01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_<WALL>_wars.mov
  1080 render (--scale 1.0)                            -> 3_HD_1080_fallback/1_PLAY_THESE_IN_ORDER/ + 03_CLEAN_MASTERS_no_edge/S6_<WALL>_wars_CLEAN.mov
  the v6.2 files of those places                       -> 04_WORKING_FILES/superseded/S6_v6.2/<name>_v6.2_<4K|1080>.mov
Gate: every file probes right (size, 3,960 frames, alpha, sound). Every move/copy is sha256-verified. Nothing deleted.
  python promote_s6_v7_2026-11-03.py [--dry]
"""
import hashlib, json, os, shutil, subprocess, sys

M = 'D:/SOTR/SOTR_MEDIA'
F = M + '/01_FINAL_FOR_SHOW'
PLAY, HD, CLEAN = F + '/1_PLAY_THESE_IN_ORDER', F + '/3_HD_1080_fallback/1_PLAY_THESE_IN_ORDER', M + '/03_CLEAN_MASTERS_no_edge'
W = M + '/04_WORKING_FILES/S6_v7_map_option'
SUP = M + '/04_WORKING_FILES/superseded/S6_v6.2'
WALLS = {'LEFT': 1440, 'CENTRE': 1800, 'RIGHT': 1440}
DRY = '--dry' in sys.argv


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,pix_fmt,width,height,nb_frames', '-of', 'json', p]))
    v = [s for s in j['streams'] if s['codec_type'] == 'video'][0]
    return int(v['width']), int(v['height']), int(v['nb_frames']), 'a' in v['pix_fmt'][:4], any(s['codec_type'] == 'audio' for s in j['streams'])


def move(src, dst):
    print('move', src, '->', dst)
    if DRY:
        return
    h = sha(src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    assert not os.path.exists(dst), dst
    shutil.move(src, dst)
    assert sha(dst) == h
    return h


def copy(src, dst):
    print('copy', src, '->', dst)
    if DRY:
        return
    h = sha(src)
    assert not os.path.exists(dst), dst
    shutil.copyfile(src, dst + '._tmp_')
    assert sha(dst + '._tmp_') == h
    os.rename(dst + '._tmp_', dst)


bad = []
for n, w in WALLS.items():
    for d, mult in (('_tmp_4K_alpha_native', 2), ('_tmp_4K_alpha', 1)):
        p = f'{W}/{d}/S6_{n}.mov'
        got = probe(p) if os.path.exists(p) else None
        if got != (w * mult, 1080 * mult, 3960, True, True):
            bad.append((p, got))
if bad:
    sys.exit('GATE FAILED: %s' % bad)
for n in WALLS:
    name = f'S6_{n}_wars'
    move(f'{PLAY}/{name}.mov', f'{SUP}/{name}_v6.2_4K.mov')
    move(f'{HD}/{name}.mov', f'{SUP}/{name}_v6.2_1080.mov')
    move(f'{CLEAN}/{name}_CLEAN.mov', f'{SUP}/{name}_CLEAN_v6.2_1080.mov')
    shutil.copyfile(f'{W}/_tmp_4K_alpha/S6_{n}.mov', f'{W}/{name}_1080_alpha.mov') if not DRY else None
    move(f'{W}/_tmp_4K_alpha_native/S6_{n}.mov', f'{PLAY}/{name}.mov')
    copy(f'{W}/_tmp_4K_alpha/S6_{n}.mov', f'{HD}/{name}.mov')
    copy(f'{W}/_tmp_4K_alpha/S6_{n}.mov', f'{CLEAN}/{name}_CLEAN.mov')
print('DONE')
