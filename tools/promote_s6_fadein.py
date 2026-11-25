"""Promote the S6 fade-in files (F43 build, Homie F44 yes) into 01_FINAL_FOR_SHOW, on D: and then on the T9.

Homie 2026-11-25: "the fade-in files are basically 100% same files as the final renders, just that it has the fade-in
in the beginning. If that is the case, then we can just replace the ones in the final for show files?"
The FADEIN files differ from the show files only in frames 0-47 (2 s eased fade from black, sound fades in);
frames 48.. are bit-identical (tools/s6_fadein.py log). No CLEAN masters exist for the French S6, so 03 is untouched.

Per file: old show file -> 04_WORKING_FILES/superseded/S6_wars_FR_nofade/[1080/]S6_<W>_wars_FR-nofade.mov (rename on the
same drive after a sha256), FADEIN copy -> show name, sha256 verified. Then _SHA256.txt lines updated. --t9 does the
same on G: from the D: show files. Never deletes anything.
"""
import hashlib, os, shutil, sys

T9 = '--t9' in sys.argv
ROOT = r'G:\SOTR\HF\SOTR_MEDIA' if T9 else r'D:\SOTR\SOTR_MEDIA'
SRC_ROOT = r'D:\SOTR\SOTR_MEDIA'
F = ROOT + r'\01_FINAL_FOR_SHOW'
SUP = ROOT + r'\04_WORKING_FILES\superseded\S6_wars_FR_nofade'
LOG = ROOT + r'\04_WORKING_FILES\S6_fadein_v1\_promote_log.txt'

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''):
            h.update(b)
    return h.hexdigest()

def log(s):
    print(s, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(s + '\n')

sets = [('4K', r'1_PLAY_THESE_IN_ORDER\S06_Napoleonic-wars', ''),
        ('1080', r'3_HD_1080_fallback\1_PLAY_THESE_IN_ORDER\S06_Napoleonic-wars', '1080')]
newsha = {}
for res, rel, sub in sets:
    for w in ('CENTRE', 'LEFT', 'RIGHT'):
        show = os.path.join(F, rel, f'S6_{w}_wars.mov')
        if T9:
            src = os.path.join(SRC_ROOT, '01_FINAL_FOR_SHOW', rel, f'S6_{w}_wars.mov')
        else:
            src = os.path.join(SRC_ROOT, r'04_WORKING_FILES\S6_fadein_v1', res, f'S6_{w}_wars_FADEIN.mov')
        sdir = os.path.join(SUP, sub)
        os.makedirs(sdir, exist_ok=True)
        old = os.path.join(sdir, f'S6_{w}_wars_FR-nofade.mov')
        src_sha = sha(src)
        if os.path.exists(show) and sha(show) == src_sha:
            log(f'{res} {w}: already promoted ({src_sha[:12]})')
            newsha[(rel, w)] = src_sha
            continue
        if os.path.exists(old):
            raise SystemExit(f'STOP: {old} exists already')
        h_old = sha(show)
        os.replace(show, old)  # same drive: a rename
        assert sha(old) == h_old
        tmp = show + '.part'
        shutil.copyfile(src, tmp)
        assert sha(tmp) == src_sha, 'copy sha mismatch'
        os.replace(tmp, show)
        newsha[(rel, w)] = src_sha
        log(f'{res} {w}: old {h_old[:12]} -> superseded; new {src_sha[:12]} OK')

# update _SHA256.txt
sp = os.path.join(F, '_SHA256.txt')
lines = open(sp, encoding='utf-8').read().splitlines()
out = []
for ln in lines:
    for (rel, w), h in newsha.items():
        p = (rel + '\\' + f'S6_{w}_wars.mov').replace('\\', '/')
        if ln.endswith('  ' + p):
            ln = f'{h}  {p}'
    out.append(ln)
open(sp, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
log('DONE promote_s6_fadein' + (' T9' if T9 else ''))
