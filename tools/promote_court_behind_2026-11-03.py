"""2026-11-03: promote the 'judge behind the parchment' court (S9 b3/b5/b7 + 4 strikes) into 01_FINAL_FOR_SHOW under the SAME names.
Old 4K / 1080 / CLEAN court files -> 04_WORKING_FILES/superseded/S9_court_pre_behind_paper/. New files copied in and sha256-verified."""
import hashlib, os, shutil
M = 'C:/Users/Homie/Documents/SOTR_MEDIA'
W = M + '/04_WORKING_FILES/S9_court_behind_paper/final_1080'
S = M + '/04_WORKING_FILES/superseded/S9_court_pre_behind_paper'
SHOW = M + '/01_FINAL_FOR_SHOW'
PLAY = ['S9_b3_CENTRE_court', 'S9_b5_CENTRE_court', 'S9_b7_CENTRE_court']
BACK = ['S9_b3_CENTRE_court_strike-size1', 'S9_b5_CENTRE_court_strike-size2', 'S9_b5_CENTRE_court_strike-size3', 'S9_b7_CENTRE_court_strike-size4']
CLEAN = [p + '_CLEAN' for p in PLAY]
P, B, H = '1_PLAY_THESE_IN_ORDER', '2_BACKUP_LOOPS_for_operator', '3_HD_1080_fallback'
jobs = []  # (new, dest, supersede_tag)
for n in PLAY: jobs += [(f'{W}/4k/{n}.mov', f'{SHOW}/{P}/{n}.mov', '4K_play'), (f'{W}/muxed/{n}.mov', f'{SHOW}/{H}/{P}/{n}.mov', '1080_play')]
for n in BACK: jobs += [(f'{W}/4k/{n}.mov', f'{SHOW}/{B}/{n}.mov', '4K_backup'), (f'{W}/muxed/{n}.mov', f'{SHOW}/{H}/{B}/{n}.mov', '1080_backup')]
for n in CLEAN: jobs += [(f'{W}/cleanmux/{n}.mov', f'{M}/03_CLEAN_MASTERS_no_edge/{n}.mov', 'clean')]
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
for new, dest, tag in jobs:
    assert os.path.exists(new) and os.path.exists(dest), (new, dest)
    d = f'{S}/{tag}'; os.makedirs(d, exist_ok=True)
    old = f'{d}/{os.path.basename(dest)}'
    assert not os.path.exists(old), old
    os.rename(dest, old)
    shutil.copyfile(new, dest)
    assert sha(new) == sha(dest), dest
    print('OK', dest, flush=True)
