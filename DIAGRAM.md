# PhishGuard — System Diagram & Flow

---

## 🔁 How a Scan Works (End-to-End)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                             │
│                                                                     │
│   1. User pastes a URL / message / email                           │
│   2. Clicks "Scan"                                                  │
│   3. JavaScript sends data to the backend API                      │
│                                                                     │
│         ┌──────────────┐                                            │
│         │  index.html  │  ← What the user sees                     │
│         │  style.css   │  ← How it looks                           │
│         │  app.js      │  ← Tab switching, theme toggle            │
│         │  scanner.js  │  ← Handles "Scan" button click            │
│         │  api.js      │  ← Sends HTTP request to backend          │
│         │  ui.js       │  ← Shows the result dashboard             │
│         │  history.js  │  ← Saves scan to localStorage             │
│         └──────┬───────┘                                            │
│                │                                                    │
│                │  POST /api/scan-url   (JSON body: { url: "..." })  │
│                │  POST /api/scan-message                            │
│                │  POST /api/scan-email                              │
│                ▼                                                    │
└────────────────────────────────────────────────────────────────────┘
                 │
                 │  HTTP Request (fetch)
                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FASTAPI BACKEND                              │
│                       (Python Server)                              │
│                                                                     │
│   main.py receives the request                                     │
│         │                                                           │
│         ├──► /api/scan-url ──► url_detector.py                     │
│         │                         │                                 │
│         │                         ├── Check 1: HTTPS?              │
│         │                         ├── Check 2: IP address?         │
│         │                         ├── Check 3: URL too long?       │
│         │                         ├── Check 4: @ symbol?           │
│         │                         ├── Check 5: Suspicious keywords?│
│         │                         ├── Check 6: Bad TLD (.xyz)?     │
│         │                         ├── Check 7: Too many subdomains?│
│         │                         ├── Check 8: Punycode/hyphens?   │
│         │                         ├── Check 9: Typosquatting?      │
│         │                         ├── Check 10: DNS resolution     │ ◄─ dns_service.py
│         │                         ├── Check 11: SSL certificate    │ ◄─ ssl_service.py
│         │                         ├── Check 12: Redirects          │ ◄─ url_service.py
│         │                         ├── Check 13: URL shortener?     │
│         │                         └── Check 14: Suspicious pattern?│
│         │                                  │                        │
│         │                                  ▼                        │
│         │                         scoring.py                       │
│         │                         ┌─────────────────┐              │
│         │                         │ Add up all the  │              │
│         │                         │ risk points     │              │
│         │                         │ (cap at 100)    │              │
│         │                         │                 │              │
│         │                         │ 0-24  = SAFE    │              │
│         │                         │ 25-49 = LOW     │              │
│         │                         │ 50-74 = SUS     │              │
│         │                         │ 75-100= HIGH    │              │
│         │                         └────────┬────────┘              │
│         │                                  │                        │
│         │                                  ▼                        │
│         │                         JSON Response sent back          │
│         │                                                           │
│         ├──► /api/scan-message ──► message_detector.py              │
│         │         (checks urgency, credentials, rewards, URLs)     │
│         │                                                           │
│         └──► /api/scan-email ──► email_detector.py                 │
│                 (checks sender, subject + runs message detector)   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                 │
                 │  JSON Response
                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      BACK IN THE BROWSER                           │
│                                                                     │
│   ui.js receives JSON response                                     │
│         │                                                           │
│         ├── Animates the circular risk score (0 → final)           │
│         ├── Shows threat level badge (SAFE / HIGH RISK)            │
│         ├── Lists each security check (✓ PASS / ✗ DANGER)         │
│         ├── Shows "Why was this flagged?" reasons                  │
│         └── Shows recommendations                                  │
│                                                                     │
│   history.js saves to localStorage (last 20 scans)                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Risk Scoring — How Points Add Up

```
 Check                          Points Added
 ─────────────────────────────  ────────────
 HTTP (no HTTPS)                   +10
 IP address as domain              +20
 @ symbol in URL                   +25
 URL too long (>75 chars)          +10
 Suspicious keywords (each)         +5  (max +15)
 Suspicious TLD (.xyz, .tk)        +10
 Too many subdomains               +10
 Punycode / excessive hyphens      +15
 Typosquatting (looks like brand)  +25
 SSL certificate issue             +10
 Multiple redirects                +15
 URL shortener                      +5
 Brand + security word combo       +20
 DNS resolution failed              +5
                                ────────────
 TOTAL:  Capped at 100


 Score Range     Label          Color
 ───────────     ─────          ─────
  0 – 24        SAFE           🟢 Green
 25 – 49        LOW RISK       🔵 Blue
 50 – 74        SUSPICIOUS     🟡 Yellow
 75 – 100       HIGH RISK      🔴 Red
```

---

## 🗄️ Where is Data Stored?

```
 ┌──────────────────────────────────────────────┐
 │  There is NO database.                       │
 │  There is NO server-side storage.            │
 │                                               │
 │  Scan history is saved in the browser's      │
 │  localStorage (key: "phishguard_history")    │
 │                                               │
 │  • Max 20 scans stored                       │
 │  • Only stores: type, input, score, result   │
 │  • User can clear it anytime                 │
 │  • Private — never leaves the browser        │
 └──────────────────────────────────────────────┘
```

---

## 🔄 Message Scanner Flow

```
 User pastes message
       │
       ▼
 ┌─────────────────────────┐
 │  Check for:             │
 │  • Urgency words        │  "urgent", "act now"
 │  • Credential requests  │  "password", "OTP"
 │  • Financial keywords   │  "bank", "payment"
 │  • Reward scams         │  "winner", "prize"
 │  • Threats              │  "account suspended"
 │  • Embedded URLs        │──────┐
 └──────────┬──────────────┘      │
            │                     │ If URLs found,
            ▼                     │ run URL detector
     Calculate score              │ on first URL
     Return result   ◄────────────┘
```
