"""2026-11-03: T9 (G:) in line with the S6 v14 promotion. Copy, never mirror-delete: the T9's old S6 files go to its own superseded/S6_v6.2_pre_v14map/<tag>/, the new ones are copied from D: and sha256-verified."""
import hashlib, os, shutil
M = 'D:/SOTR/SOTR_MEDIA'; T = 'G:/SOTR/HF/SOTR_MEDIA'
F = '01_FINAL_FOR_SHOW'
jobs = []
for w in ('LEFT', 'CENTRE', 'RIGHT'):
    jobs += [(f'{F}/1_PLAY_THESE_IN_ORDER/S6_{w}_wars.mov', '4K'), (f'{F}/3_HD_1080_fallback/1_PLAY_THESE_IN_ORDER/S6_{w}_wars.mov', '1080'),
             (f'03_CLEAN_MASTERS_no_edge/S6_{w}_wars_CLEAN.mov', 'CLEAN')]
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
for rel, tag in jobs:
    s, td = f'{M}/{rel}', f'{T}/{rel}'
    os.makedirs(os.path.dirname(td), exist_ok=True)
    if os.path.exists(td):
        if sha(td) == sha(s): print('same', td); continue
        d = f'{T}/04_WORKING_FILES/superseded/S6_v6.2_pre_v14map/{tag}'; os.makedirs(d, exist_ok=True)
        o = f'{d}/{os.path.basename(td)}'; assert not os.path.exists(o), o; os.rename(td, o)
    shutil.copyfile(s, td); assert sha(s) == sha(td), td; print('OK', td, flush=True)
wa = 'WHATSAPP_3_wall_previews/06_S6_wars.mp4'
t = f'G:/SOTR/HF/{wa}'
if os.path.exists(t):
    d = 'G:/SOTR/HF/WHATSAPP_3_wall_previews/_DELETE_ME_2026-11-03'; os.makedirs(d, exist_ok=True); os.replace(t, f'{d}/06_S6_wars_v6.2.mp4')
shutil.copyfile(f'D:/SOTR/{wa}', t); assert sha(f'D:/SOTR/{wa}') == sha(t); print('OK', t)
