"""
Enables GitHub Pages for henrynkoh/rightlydividingkjv
Run once in Terminal: python3 enable_pages.py
"""
import urllib.request, urllib.error, json

TOKEN = "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"
OWNER = "henrynkoh"
REPO  = "rightlydividingkjv"

def api(method, path, data=None):
    url = f"https://api.github.com{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

print("Enabling GitHub Pages...")
status, body = api("POST", f"/repos/{OWNER}/{REPO}/pages",
                   {"source": {"branch": "main", "path": "/"}})

if status in (201, 200):
    url = body.get("html_url", f"https://{OWNER}.github.io/{REPO}/")
    print(f"✅ GitHub Pages enabled!")
    print(f"🌐 Live at: {url}")
elif status == 409:
    # Already enabled — just update the source
    print("Pages already exists, updating source...")
    status2, body2 = api("PUT", f"/repos/{OWNER}/{REPO}/pages",
                         {"source": {"branch": "main", "path": "/"}})
    print(f"✅ Updated! Status: {status2}")
    print(f"🌐 Live at: https://{OWNER}.github.io/{REPO}/")
else:
    print(f"Response {status}: {json.dumps(body, indent=2)}")
