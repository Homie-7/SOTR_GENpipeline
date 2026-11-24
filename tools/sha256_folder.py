r"""Write <folder>\_SHA256.txt: one line per file, "<sha256>  <relative/path>" (shasum / sha256sum format).
Reuses hashes from a moves TSV (status, src, dst, sha256, time; paths relative to --base) when the file's dst matches
(a same-drive rename keeps the bytes). Every other file, and every .txt, is hashed. --check re-hashes everything.
Usage: sha256_folder.py FOLDER [--tsv MOVES.tsv --base D:\SOTR] [--check]   --check verifies an existing _SHA256.txt."""
import os, sys, hashlib

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while (b := f.read(8 << 20)):
            h.update(b)
    return h.hexdigest()

def arg(k):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None

folder = os.path.abspath(sys.argv[1])
out = os.path.join(folder, '_SHA256.txt')
if '--check' in sys.argv:
    bad = 0
    for line in open(out, encoding='utf-8'):
        h, rel = line.rstrip('\n').split('  ', 1)
        p = os.path.join(folder, rel.replace('/', os.sep))
        ok = os.path.exists(p) and sha(p) == h
        bad += not ok
        print('OK ' if ok else 'BAD', rel, flush=True)
    print('CHECK DONE, bad =', bad)
    sys.exit(1 if bad else 0)

known = {}
tsv, base = arg('--tsv'), arg('--base')
if tsv:
    for l in open(tsv, encoding='utf-8'):
        r = l.rstrip('\n').split('\t')
        if r[0] == 'MOVED' and len(r) >= 4 and r[3]:
            known[os.path.normcase(os.path.join(base, r[2]))] = r[3]
rows, reused = [], 0
for root, dirs, files in os.walk(folder):
    dirs.sort()
    for fn in sorted(files):
        p = os.path.join(root, fn)
        if os.path.normcase(p) == os.path.normcase(out):
            continue
        rel = os.path.relpath(p, folder).replace(os.sep, '/')
        if fn.lower().endswith('.txt') or os.path.normcase(p) not in known:
            h = sha(p)        # text files are hashed fresh (read-mes are edited after the move)
        else:
            h = known[os.path.normcase(p)]; reused += 1
        rows.append(f'{h}  {rel}')
        print(rel, flush=True)
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(rows) + '\n')
print('WROTE', out, len(rows), 'files,', reused, 'hashes reused from the TSV')
