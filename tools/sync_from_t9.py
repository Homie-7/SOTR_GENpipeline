"""Bring D: in line with the T9, the OTHER way round from backup_t9.py (8 Oct 2026).

WHY: since 5 Oct all work happened on the MacBook, straight on the T9 (the gallery, the ship, the 8 Oct clean-up and the
rewritten READMEs). The T9 is now the newer copy. backup_t9.py (D: -> T9) must NOT run before this: it would replace the
T9's newer READMEs (different size) with D:'s old ones, and copy back everything the clean-up binned.

For every file under the T9's SOTR_MEDIA (skipping macOS '._' sidecars, .DS_Store and _tmp_ names):
  - missing on D:                 -> copied to a _tmp_ name, sha256 checked against the T9, renamed into place;
  - on D: with a different size   -> D:'s copy is first MOVED to the bin (same path inside), then the T9's copied + checked;
    (--hash: equal-size files are compared by sha256 too: slow, reads everything twice)
  - otherwise left alone.
Nothing is ever deleted. Files that exist only on D: are LISTED (to the log), never touched: after reorg_2026-10-05 and
cleanup_2026-10-08 have run on D:, that list should be empty or near it; Homie decides what's left.
Refuses to start if D: lacks the free space for the copies (+5%). Dry run by default.

  python tools/sync_from_t9.py                 dry run: what would be copied / replaced, GB, the D:-only list
  python tools/sync_from_t9.py --go            does it (one line per file, a summary; exit 1 on any checksum mismatch)
  [--src G:/SOTR/HF/SOTR_MEDIA] [--dst D:/SOTR/SOTR_MEDIA] [--bin D:/SOTR/_DELETE_ME_2026-10-08/replaced_by_t9]
  [--log D:/SOTR/SYNC_FROM_T9_2026-10-08.tsv] [--hash]
"""
import argparse
import hashlib
import os
import shutil
import sys


def skip(name):
    return name.startswith('._') or name.startswith('_tmp_') or name == '.DS_Store'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def files_under(root):
    out = {}
    for r, ds, fs in os.walk(root):
        ds[:] = [d for d in ds if not skip(d)]
        for f in fs:
            if not skip(f):
                p = os.path.join(r, f)
                out[os.path.relpath(p, root).replace('\\', '/')] = os.path.getsize(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='G:/SOTR/HF/SOTR_MEDIA')
    ap.add_argument('--dst', default='D:/SOTR/SOTR_MEDIA')
    ap.add_argument('--bin', default='D:/SOTR/_DELETE_ME_2026-10-08/replaced_by_t9')
    ap.add_argument('--log', default='D:/SOTR/SYNC_FROM_T9_2026-10-08.tsv')
    ap.add_argument('--hash', action='store_true')
    ap.add_argument('--go', action='store_true')
    a = ap.parse_args()
    for d in (a.src, a.dst):
        if not os.path.isdir(d):
            sys.exit(f'not found: {d} (is the T9 connected? is D: right?)')
    src, dst = files_under(a.src), files_under(a.dst)
    new = [p for p in src if p not in dst]
    rep = [p for p in src if p in dst and src[p] != dst[p]]
    if a.hash:
        rep += [p for p in src if p in dst and src[p] == dst[p]
                and sha(os.path.join(a.src, p)) != sha(os.path.join(a.dst, p))]
    only_d = sorted(p for p in dst if p not in src)
    need = sum(src[p] for p in new + rep)
    free = shutil.disk_usage(a.dst).free
    print(f'T9 files {len(src)}, D: files {len(dst)}')
    print(f'to COPY (missing on D:): {len(new)}   to REPLACE (D: differs; its copy to the bin): {len(rep)}   '
          f'{need / 1e9:.2f} GB; D: free {free / 1e9:.1f} GB')
    for p in sorted(new):
        print('  new  ', p)
    for p in sorted(rep):
        print('  repl ', p, f'(T9 {src[p]} B, D: {dst[p]} B)')
    print(f'only on D: (listed, NOT touched): {len(only_d)}')
    for p in only_d[:200]:
        print('  D-only', p)
    if not a.go:
        print('dry run: nothing changed (--go to do it)'); return
    if need * 1.05 > free:
        sys.exit('not enough free space on D: for the copies: empty the bins first')
    bad = 0
    with open(a.log, 'a', encoding='utf-8') as log:
        for p in only_d:
            log.write(f'D-ONLY\t{p}\t{dst[p]}\n')
        for p in sorted(rep) + sorted(new):
            s, d = os.path.join(a.src, p), os.path.join(a.dst, p)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            if p in rep:
                b = os.path.join(a.bin, p)
                os.makedirs(os.path.dirname(b), exist_ok=True)
                os.replace(d, b)
                log.write(f'BINNED-OLD\t{d}\t{b}\n')
            tmp = os.path.join(os.path.dirname(d), '_tmp_' + os.path.basename(d))
            shutil.copyfile(s, tmp)
            hs, hd = sha(s), sha(tmp)
            if hs != hd:
                bad += 1
                print('CHECKSUM MISMATCH (left as _tmp_):', p)
                log.write(f'MISMATCH\t{p}\t{hs}\t{hd}\n')
                continue
            os.replace(tmp, d)
            shutil.copystat(s, d)
            log.write(f'{"REPLACED" if p in rep else "COPIED"}\t{p}\t{src[p]}\t{hs}\n')
            print('ok', 'repl' if p in rep else 'new ', p)
    print(f'done: {len(new)} copied, {len(rep)} replaced, {bad} mismatches; log {a.log}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
