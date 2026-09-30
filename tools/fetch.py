"""Download a Higgsfield result and PROVE it is whole: the byte count must equal the server's Content-Length and
ffmpeg must decode every frame without an error. Retries until both hold.

WHY (2026-09-30): the CDN cut a 4K upscale off at 6.7 of 12.9 MB; ffprobe still reported the full header, so a
probe alone passed a broken file. (The same CDN had failed TLS handshakes on the Scene 6 Sequels.)

  python tools/fetch.py URL OUT [--tries 6]
"""
import argparse
import os
import subprocess
import sys
import time


def content_length(url):
    out = subprocess.run(['curl', '-sIL', url], capture_output=True, text=True).stdout
    n = [l.split(':', 1)[1].strip() for l in out.splitlines() if l.lower().startswith('content-length')]
    return int(n[-1]) if n else None


def decodes(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'null', '-'], capture_output=True, text=True)
    return r.returncode == 0 and not r.stderr.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('out')
    ap.add_argument('--tries', type=int, default=6)
    a = ap.parse_args()
    want = content_length(a.url)
    tmp = a.out + '.part'
    for k in range(a.tries):
        subprocess.run(['curl', '-sL', '--retry', '5', '-o', tmp, a.url])
        got = os.path.getsize(tmp) if os.path.exists(tmp) else 0
        if want and got == want and decodes(tmp):
            os.replace(tmp, a.out)
            print(f'OK {a.out} ({got} bytes, decodes clean)')
            return
        print(f'try {k + 1}: {got} of {want} bytes, retrying', file=sys.stderr)
        time.sleep(3)
    raise SystemExit(f'FAILED to fetch {a.url} whole')


if __name__ == '__main__':
    main()
