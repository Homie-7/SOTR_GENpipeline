"""Download a Higgsfield result and PROVE it is whole: the byte count must equal the server's Content-Length and
ffmpeg must decode every frame without an error. Retries until both hold.

WHY (2026-09-30): the CDN cut a 4K upscale off at 6.7 of 12.9 MB; ffprobe still reported the full header, so a
probe alone passed a broken file. (The same CDN had failed TLS handshakes on the Scene 6 Sequels.) Then it cut the
salon b8 upscale at EXACTLY the same byte on six whole-file tries, while a byte-range request for the rest came back
whole: so each try RESUMES from what is already on disk (curl -C -) instead of starting again.
ROOT CAUSE found the same day: DNS on this network is intercepted. Plain lookups (even to 8.8.8.8) answer
92.249.39.124 for the CloudFront host; DNS-over-HTTPS (dns.google) gives CloudFront's real 18.155.x addresses. The
stand-in machine cut files and failed TLS handshakes. So the host is resolved over HTTPS and curl is pinned to that
address with --resolve. The certificate is still verified for the real hostname (no -k), so an impostor fails.

  python tools/fetch.py URL OUT [--tries 6]
"""
import argparse
import json
import os
import urllib.parse
import subprocess
import sys
import time


def real_ip(url):
    """The host's A record from Google's DNS-over-HTTPS (the local resolver is intercepted)."""
    host = urllib.parse.urlparse(url).hostname
    r = subprocess.run(['curl', '-s', '-m', '20', f'https://dns.google/resolve?name={host}&type=A'],
                       capture_output=True, text=True).stdout
    try:
        ips = [a['data'] for a in json.loads(r).get('Answer', []) if a.get('type') == 1]
    except ValueError:
        ips = []
    return (['--resolve', f'{host}:443:{ips[0]}'] if ips else []), (ips[0] if ips else None)


PIN = []


def content_length(url):
    out = subprocess.run(['curl', '-sIL'] + PIN + [url], capture_output=True, text=True).stdout
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
    global PIN
    PIN, ip = real_ip(a.url)
    print(f'resolved via DNS-over-HTTPS: {ip}', file=sys.stderr)
    want = content_length(a.url)
    tmp = a.out + '.part'
    for k in range(a.tries):
        subprocess.run(['curl', '-sL', '--retry', '5', '-C', '-'] + PIN + ['-o', tmp, a.url])
        got = os.path.getsize(tmp) if os.path.exists(tmp) else 0
        if want and got == want and decodes(tmp):
            os.replace(tmp, a.out)
            print(f'OK {a.out} ({got} bytes, decodes clean)')
            return
        if want and got >= want:                                  # too long, or whole but broken: start clean
            os.remove(tmp)
        print(f'try {k + 1}: {got} of {want} bytes, resuming', file=sys.stderr)
        time.sleep(3)
    raise SystemExit(f'FAILED to fetch {a.url} whole')


if __name__ == '__main__':
    main()
