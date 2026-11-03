"""2026-11-03: promote the RIGHT gallery v6 (David's Napoleon, bottom frame rebuilt) into the client delivery.

Homie approved the v6 stills and said to finish the files ("final for sure"). Step 1 COPIES the current RIGHT gallery show
files to 04_WORKING_FILES/superseded/S1_gallery/RIGHT_v3_pre_v6/ (sha256-verified, nothing deleted). Step 2 copies the v6
files in under the SAME show names (a .tmp, sha256-verified, then renamed over the old). 3_RIGHT_DAVID_v6 stays the source.

  python tools/promote_gallery_right_v6_2026-11-03.py ROOT SRC_V6_DIR [backup|replace]
  ROOT = the folder holding SOTR_MEDIA (D:/SOTR or G:/SOTR/HF); SRC_V6_DIR holds show_1080/ and loops_4K/.
"""
import hashlib
import os
import shutil
import sys

root, src_root, step = sys.argv[1], sys.argv[2], sys.argv[3]
FINAL = root + '/SOTR_MEDIA/01_FINAL_FOR_SHOW'
SUP = root + '/SOTR_MEDIA/04_WORKING_FILES/superseded/S1_gallery/RIGHT_v3_pre_v6'
FILES = [('show_1080', '1_PLAY_THESE_IN_ORDER', n) for n in
         ('S1_a_RIGHT_gallery.mov', 'S1_b_RIGHT_gallery-blackout.mov', 'S10_RIGHT_gallery.mov')] + \
        [('loops_4K', '2_BACKUP_LOOPS_for_operator', n) for n in
         ('S1-and-S10_RIGHT_gallery_LIT_HOLD_loop.mov', 'S1_RIGHT_gallery_DARK_HOLD_loop.mov')]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''):
            h.update(b)
    return h.hexdigest()


os.makedirs(SUP, exist_ok=True)
for sub, folder, n in FILES:
    s, d, old = os.path.join(src_root, sub, n), os.path.join(FINAL, folder, n), os.path.join(SUP, n)
    if step == 'backup':
        if os.path.exists(d) and not os.path.exists(old):
            shutil.copyfile(d, old + '.tmp')
            assert sha(d) == sha(old + '.tmp'), n
            os.rename(old + '.tmp', old)
            print('backed up', n, flush=True)
    else:
        assert os.path.exists(old) or not os.path.exists(d), 'no backup of ' + n
        if os.path.exists(d) and sha(d) == sha(s):
            print('already', n, flush=True)
            continue
        shutil.copyfile(s, d + '.tmp')
        a = sha(s)
        assert a == sha(d + '.tmp'), n
        os.replace(d + '.tmp', d)
        print('OK', n, a, flush=True)
print('DONE', flush=True)
