"""2026-11-03: bring the T9 (G:) in line with promote_court_behind_2026-11-03.py. Copy, never mirror-delete: the T9's old court files move
to its own superseded/S9_court_pre_behind_paper/<tag>/; the new files are copied from D: and sha256-verified."""
import hashlib, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
M = 'C:/Users/Homie/Documents/SOTR_MEDIA'; T = 'G:/SOTR/HF/SOTR_MEDIA'
src = open(os.path.join(os.path.dirname(__file__), 'promote_court_behind_2026-11-03.py'), encoding='utf-8').read()
ns = {}; exec(src.split('def sha')[0].replace("M = 'C:/Users/Homie/Documents/SOTR_MEDIA'", "M = '%s'" % M), ns)
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
for new, dest, tag in ns['jobs']:
    rel = os.path.relpath(dest, M)
    td = f'{T}/{rel}'; os.makedirs(os.path.dirname(td), exist_ok=True)
    if os.path.exists(td):
        d = f'{T}/04_WORKING_FILES/superseded/S9_court_pre_behind_paper/{tag}'; os.makedirs(d, exist_ok=True)
        o = f'{d}/{os.path.basename(td)}'
        assert not os.path.exists(o), o
        os.rename(td, o)
    shutil.copyfile(dest, td)
    assert sha(dest) == sha(td), td
    print('OK', td, flush=True)
