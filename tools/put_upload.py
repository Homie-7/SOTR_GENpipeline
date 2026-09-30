"""PUT local files to Higgsfield presigned upload URLs, through the DNS-over-HTTPS pin (this network intercepts DNS).

  python tools/put_upload.py PLAN.json      PLAN = [{"file": "...", "url": "https://...", "content_type": "video/mp4"}, ...]

Prints one line per file: OK <http code> or FAIL. Retries each up to 4 times. Then call media_confirm on the ids.
WHY: media_upload hands back presigned URLs; a plain curl resolves the host through the intercepted DNS (the same
stand-in machine that cut downloads, LOG 2026-09-30), so the host is resolved over HTTPS and curl pinned to it,
certificate still verified (fetch.py's method).
"""
import json
import subprocess
import sys

sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
from fetch import real_ip  # noqa: E402


def main():
    plan = json.load(open(sys.argv[1]))
    for p in plan:
        pin, ip = real_ip(p['url'])
        code = '000'
        for _ in range(4):
            code = subprocess.run(['curl', '-s', '-o', '/dev/null' if sys.platform != 'win32' else 'NUL', '-w', '%{http_code}',
                                   '-X', 'PUT', '-H', f"Content-Type: {p.get('content_type', 'video/mp4')}",
                                   '--upload-file', p['file']] + pin + [p['url']],
                                  capture_output=True, text=True).stdout.strip()
            if code == '200':
                break
        print(('OK ' if code == '200' else 'FAIL ') + code, p['file'].rsplit('/', 1)[-1], 'via', ip, flush=True)


if __name__ == '__main__':
    main()
