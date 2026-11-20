"""Measure Darren's S9 judge mix against our S9 timeline (tools/s9_animatic.py). Read-only, 0 credits.

    python tools/s9_mix_measure.py [--mix PATH] [--step 0.5] [--out CSV]

Prints, per 0.5 s: Darren's level (dBFS RMS), our preview's level (the files' own sound, s9_animatic.audio), and which
beat file is on each wall. Then: Darren's digital-silence runs, his loud (speech-like) runs, and per-beat summaries.
Also cross-correlates his mix against ours in 10 s windows to show whether his sound sits on our clock (lag in s).
"""
import argparse, csv, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s9_animatic as s9

MIX = r'G:\SOTR\HF\Final changes\the judge TO BE CUT DOWN 19112026.mov'
SR = 8000


def pcm(path, sr=SR):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def env(x, step, sr=SR):
    n = int(step * sr)
    k = len(x) // n
    r = np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(1))
    return np.where(r > 0, 20 * np.log10(np.maximum(r, 1e-12)), -200.0)


def runs(mask, step, min_s):
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j < len(mask) and mask[j]:
                j += 1
            if (j - i) * step >= min_s:
                out.append((i * step, j * step))
            i = j
        else:
            i += 1
    return out


def beat_at(t):
    on = {}
    for name, wall, start in s9.CLIPS:
        st = start / s9.FPS
        if st <= t:
            on[wall] = name
    return on


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mix', default=MIX)
    ap.add_argument('--step', type=float, default=0.5)
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    tmp = os.path.join(os.environ.get('TEMP', '.'), '_tmp_s9_ours.wav')
    if not os.path.exists(tmp):
        s9.audio(tmp, 0, s9.TOTAL)
    d, o = pcm(a.mix), pcm(tmp)
    ed, eo = env(d, a.step), env(o, a.step)
    n = min(len(ed), len(eo))
    print(f'Darren {len(d) / SR:.2f} s, ours {len(o) / SR:.2f} s')
    print('\nDigital silence in Darren (< -90 dB, >= 1 s):')
    for s0, s1 in runs(ed < -90, a.step, 1.0):
        print(f'  {s0:7.1f} - {s1:7.1f}  ({s1 - s0:5.1f} s)  on: {beat_at(s0)}')
    print('\nPer beat file: Darren mean / max dB, ours mean dB, % of Darren silent')
    for name, wall, start in s9.CLIPS:
        st = start / s9.FPS
        info = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                               os.path.join(s9.SRC, name)], capture_output=True, text=True).stdout.strip()
        en = st + float(info)
        i0, i1 = int(st / a.step), min(n, int(en / a.step))
        seg = ed[i0:i1]
        print(f'  {name:26s} {st:6.1f}-{en:6.1f}  D {np.mean(seg[seg > -90]) if (seg > -90).any() else -200:6.1f}'
              f' / {seg.max():6.1f}   ours {np.mean(eo[i0:i1]):6.1f}   silent {100 * np.mean(seg < -90):5.1f}%')
    print('\nLag of Darren vs ours, 10 s windows where both have sound (s, corr):')
    w = 10 * SR
    for t0 in range(0, int(n * a.step) - 10, 10):
        x, y = d[t0 * SR:t0 * SR + w], o[t0 * SR:t0 * SR + w]
        if np.std(x) < 1e-4 or np.std(y) < 1e-4:
            continue
        X, Y = np.fft.rfft(x, 2 * w), np.fft.rfft(y, 2 * w)
        c = np.fft.irfft(X * np.conj(Y))
        c = np.concatenate([c[-w:], c[:w]])
        k = int(np.argmax(np.abs(c)))
        corr = c[k] / (np.linalg.norm(x) * np.linalg.norm(y))
        print(f'  {t0:4d}s  lag {(k - w) / SR:+7.3f}  corr {corr:5.2f}')
    if a.out:
        with open(a.out, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['t', 'darren_db', 'ours_db', 'walls'])
            for i in range(n):
                wr.writerow([f'{i * a.step:.1f}', f'{ed[i]:.1f}', f'{eo[i]:.1f}', beat_at(i * a.step)])


if __name__ == '__main__':
    main()
