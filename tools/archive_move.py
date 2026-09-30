"""Move files from C: to the D: archive SAFELY: copy, verify sha256, only then remove the C: copy.

WHY (Homie 2026-09-30): C: was 95% full ("my C drive is almost full… I prefer [moving to D]"). Nothing is deleted:
superseded versions, rejected takes and old tests move to D:\\SOTR\\SOTR_MEDIA_ARCHIVE\\ with the same folder layout;
exact duplicates and re-derivable intermediates go to its _SAFE_TO_DELETE… folder for Homie to delete himself.

  python tools/archive_move.py DEST_ROOT SRC [SRC ...] [--rel-to C:\\Users\\Homie\\Documents\\SOTR_MEDIA] [--flat]
         [--exclude-glob "*.npz"] [--same-as DIR]

--same-as DIR: move a file only if a byte-identical copy (sha256) of it exists under DIR with the same name
(for staging copies that were promoted). Writes a manifest (MOVED_<date>.txt) in DEST_ROOT.
"""
import argparse
import fnmatch
import hashlib
import os
import shutil
import sys
import time


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dest')
    ap.add_argument('srcs', nargs='+')
    ap.add_argument('--rel-to', default=r'C:\Users\Homie\Documents\SOTR_MEDIA')
    ap.add_argument('--exclude-glob', action='append', default=[])
    ap.add_argument('--same-as')
    a = ap.parse_args()
    files = []
    for s in a.srcs:
        if os.path.isfile(s):
            files.append(s)
        else:
            for root, _, fs in os.walk(s):
                files += [os.path.join(root, f) for f in fs]
    files = [f for f in files if not any(fnmatch.fnmatch(os.path.basename(f), g) for g in a.exclude_glob)]
    same = {}
    if a.same_as:
        for root, _, fs in os.walk(a.same_as):
            for f in fs:
                same.setdefault(f, []).append(os.path.join(root, f))
    os.makedirs(a.dest, exist_ok=True)
    log = open(os.path.join(a.dest, time.strftime('MOVED_%Y-%m-%d.txt')), 'a', encoding='utf-8')
    moved = skipped = bad = 0
    total = 0
    for f in files:
        h = sha(f)
        if a.same_as:
            twins = [p for p in same.get(os.path.basename(f), []) if os.path.getsize(p) == os.path.getsize(f) and sha(p) == h]
            if not twins:
                print('KEPT (no identical copy in --same-as):', f)
                skipped += 1
                continue
        rel = os.path.relpath(f, a.rel_to)
        dst = os.path.join(a.dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst) and sha(dst) != h:
            dst = dst + '.dup'
        shutil.copy2(f, dst)
        if sha(dst) != h:
            print('MISMATCH, C: copy kept:', f)
            bad += 1
            continue
        size = os.path.getsize(f)
        try:
            os.remove(f)
        except OSError as e:                     # open elsewhere: the verified D: copy stays, the C: copy too
            print('COPIED BUT NOT REMOVED (in use):', f, e)
            log.write(f'{h}  {rel}  ->  {dst}  (C: copy kept: in use)' + chr(10))
            continue
        total += size
        moved += 1
        log.write(f'{h}  {rel}  ->  {dst}\n')
    for s in a.srcs:                      # tidy empty folders left behind
        if os.path.isdir(s):
            for root, dirs, fs in os.walk(s, topdown=False):
                try:
                    if not os.listdir(root):
                        os.rmdir(root)
                except OSError:
                    pass
    log.close()
    print(f'moved {moved} files ({total / 1e9:.1f} GB), kept {skipped}, mismatches {bad}')


if __name__ == '__main__':
    main()
