"""Copy SOTR_MEDIA sub-folders to the T9 (G:/SOTR/HF/SOTR_MEDIA), verified by sha256. Copy only, never delete.

usage: python tools/t9_sync.py REL [REL ...]      (REL = path under SOTR_MEDIA, a folder or a file)
A file that already exists on the T9 with the same size and sha256 is skipped. A different file on the T9 is
NOT overwritten: the new one is reported as CONFLICT (move the old one by hand first).
"""
import hashlib, os, shutil, sys

SRC = os.environ.get('SOTR_MEDIA', 'C:/Users/Homie/Documents/SOTR_MEDIA')
DST = os.environ.get('SOTR_T9', 'G:/SOTR/HF/SOTR_MEDIA')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''):
            h.update(b)
    return h.hexdigest()


def files(rel):
    p = os.path.join(SRC, rel)
    if os.path.isfile(p):
        yield rel
        return
    for root, _, fs in os.walk(p):
        for f in fs:
            yield os.path.relpath(os.path.join(root, f), SRC)


def main():
    n = {'copied': 0, 'same': 0, 'conflict': 0}
    for rel in sys.argv[1:]:
        for r in files(rel):
            s, d = os.path.join(SRC, r), os.path.join(DST, r)
            hs = sha(s)
            if os.path.exists(d):
                if os.path.getsize(d) == os.path.getsize(s) and sha(d) == hs:
                    n['same'] += 1
                    continue
                print('CONFLICT (T9 differs, not overwritten):', r)
                n['conflict'] += 1
                continue
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            if sha(d) != hs:
                raise SystemExit(f'SHA MISMATCH after copy: {r}')
            print('copied', r)
            n['copied'] += 1
    print('DONE t9_sync', n)


if __name__ == '__main__':
    main()
