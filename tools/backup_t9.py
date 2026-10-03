"""Bring the T9 (G:) in line with SOTR_MEDIA on D:, the CLAUDE.md way: COPY, NEVER MIRROR-DELETE.

For every file under D:/SOTR/SOTR_MEDIA (skipping _tmp_ names):
  - missing on the T9 -> copied (to a _tmp_ name, then renamed), sha256 checked against D:;
  - on the T9 with a different size, or older than D:'s -> the T9's copy is first MOVED to
    G:/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/superseded/t9_replaced_<date>/<same path>, then the new one copied + checked;
  - otherwise left alone. Nothing on the T9 is ever deleted; files that exist only on the T9 stay.
Prints one line per action and a summary; exits 1 if any checksum mismatched.

  python tools/backup_t9.py [--dry]
"""
import hashlib
import os
import shutil
import sys
import time

SRC = 'D:/SOTR/SOTR_MEDIA'
DST = 'G:/SOTR/HF/SOTR_MEDIA'
BIN = DST + '/04_WORKING_FILES/superseded/t9_replaced_' + time.strftime('%Y-%m-%d')
DRY = '--dry' in sys.argv


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def main():
    if not os.path.isdir(DST):
        raise SystemExit('the T9 is not connected (no ' + DST + ')')
    n_new = n_rep = n_ok = bad = 0
    gb = 0.0
    for root, _, files in os.walk(SRC):
        for fn in files:
            if fn.startswith('_tmp_'):
                continue
            s = os.path.join(root, fn)
            rel = os.path.relpath(s, SRC)
            d = os.path.join(DST, rel)
            ss = os.stat(s)
            if os.path.exists(d):
                ds = os.stat(d)
                if ds.st_size == ss.st_size and ds.st_mtime >= ss.st_mtime - 2:
                    n_ok += 1
                    continue
                print('REPLACE', rel, flush=True)
                n_rep += 1
                if not DRY:
                    old = os.path.join(BIN, rel)
                    os.makedirs(os.path.dirname(old), exist_ok=True)
                    shutil.move(d, old)
            else:
                print('NEW', rel, flush=True)
                n_new += 1
            gb += ss.st_size / 1e9
            if DRY:
                continue
            os.makedirs(os.path.dirname(d), exist_ok=True)
            tmp = os.path.join(os.path.dirname(d), '_tmp_' + fn)
            shutil.copy2(s, tmp)
            if sha(tmp) != sha(s):
                print('  MISMATCH', rel, flush=True)
                bad += 1
                continue
            os.replace(tmp, d)
    print(f'new {n_new}, replaced {n_rep} (old copies in {BIN}), unchanged {n_ok}, {gb:.1f} GB copied, mismatches {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
