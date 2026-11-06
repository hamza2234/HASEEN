"""End-to-end verification of the web app's live detection endpoints."""
import json
import re
import subprocess
import sys
import urllib.request

BASE = "http://127.0.0.1:12000"
PAGES = ["/", "/detect/spambase", "/detect/phishing", "/experiments",
         "/results", "/params", "/methodology"]


def post(path, payload):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def get(path):
    return urllib.request.urlopen(BASE + path).read().decode()


fails = 0

print("=== 1. Pages ===")
for p in PAGES:
    code = urllib.request.urlopen(BASE + p).status
    ok = code == 200
    fails += not ok
    print(f"  {'OK ' if ok else 'BAD'} {p:<22} {code}")

print("\n=== 2. JavaScript validity ===")
for p in PAGES:
    html = get(p)
    js = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    if not js.strip():
        print(f"  OK  {p:<22} (no inline JS)")
        continue
    with open("/tmp/_chk.js", "w") as fh:
        fh.write(js)
    r = subprocess.run(["node", "--check", "/tmp/_chk.js"],
                       capture_output=True)
    ok = r.returncode == 0
    fails += not ok
    print(f"  {'OK ' if ok else 'BAD'} {p:<22} JS")

print("\n=== 3. E-mail detection ===")
EMAILS = [
    ("fake", "URGENT! Your account will be suspended. Verify your password "
             "and credit card now. FREE money $5000 prize claim today! "
             "Act NOW limited offer. Reply with your bank account details."),
    ("fake", "Congratulations winner! You have been selected for a FREE "
             "cash bonus. Click here to claim your prize money. Order today, "
             "receive $1000 free! Limited time offer expires TODAY."),
    ("fake", "MAKE MONEY FAST!!! Free credit report. Remove your address "
             "from our list. Business opportunity - work from home. "
             "Call 650-857-4155 NOW! Visit http://money.tk"),
    ("real", "Hi team, reminder that our project meeting is tomorrow at 10am "
             "in the conference room. Please bring the report and the data "
             "table. Thanks, George, Dept of Computer Science"),
    ("real", "Dear colleagues, the conference proceedings are now available. "
             "Please review the attached table before our meeting next week. "
             "Regards, the project team at the university lab"),
]
for exp, text in EMAILS:
    v = post("/api/analyze_text", {"text": text})["verdict"]
    ok = (exp == "fake") == v["is_fake"]
    fails += not ok
    print(f"  {'OK ' if ok else 'BAD'} expect={exp:<5} "
          f"-> {v['prediction_label']:<14} conf={v['confidence']:.3f}")

print("\n=== 4. URL detection ===")
URLS = [
    ("fake", "http://paypal-secure-login.verify-account.tk/login.php?id=1"),
    ("fake", "http://192.168.1.1/secure/banking/update"),
    ("fake", "http://appleid.apple.com.verify-account.ml/signin"),
    ("fake", "http://netflix-billing-update.cf/payment"),
    ("fake", "http://paypa1.com/login"),
    ("real", "https://www.google.com/search?q=hello"),
    ("real", "https://www.paypal.com/signin"),
    ("real", "https://github.com/openai"),
    ("real", "https://en.wikipedia.org/wiki/Phishing"),
    ("real", "https://www.amazon.com/dp/B08N5WRWNW"),
]
for exp, url in URLS:
    v = post("/api/analyze_url", {"url": url})["verdict"]
    ok = (exp == "fake") == v["is_fake"]
    fails += not ok
    print(f"  {'OK ' if ok else 'BAD'} expect={exp:<5} "
          f"-> {v['prediction_label']:<18} conf={v['confidence']:.3f}")

print("\n=== 5. Manual vector (all-suspicious / all-safe) ===")
sys.path.insert(0, "/workspace/project/app")
from feature_meta import PHISHING_CODING, PHISHING_FEATURES  # noqa: E402

sus = [PHISHING_CODING[n]["sus"] for n, _, _ in PHISHING_FEATURES]
safe = [PHISHING_CODING[n]["safe"] for n, _, _ in PHISHING_FEATURES]
r1 = post("/api/predict_manual", {"dataset": "phishing", "values": sus})
r2 = post("/api/predict_manual", {"dataset": "phishing", "values": safe})
ok1, ok2 = r1["is_fake"], not r2["is_fake"]
fails += (not ok1) + (not ok2)
print(f"  {'OK ' if ok1 else 'BAD'} all-suspicious -> {r1['prediction_label']} "
      f"{r1['confidence']:.3f}")
print(f"  {'OK ' if ok2 else 'BAD'} all-safe       -> {r2['prediction_label']} "
      f"{r2['confidence']:.3f}")

print("\n=== 6. Samples endpoint ===")
for key in ("spambase", "phishing"):
    rows = post("/api/samples", {"dataset": key, "n": 10})["rows"]
    correct = sum(r["correct"] for r in rows)
    ok = correct >= 8
    fails += not ok
    print(f"  {'OK ' if ok else 'BAD'} {key:<10} {correct}/10 correct")

print(f"\n{'ALL CHECKS PASSED' if not fails else str(fails) + ' FAILURES'}")
sys.exit(1 if fails else 0)
