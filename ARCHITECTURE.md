# PhishGuard — Complete Architecture Guide (For Beginners)

> This document explains the **entire project** — the frontend, backend, every
> folder, every file, and all the important programming terms — in plain language.
> If you are new to web development or to this codebase, start here.

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [The Big Picture (Client ↔ Server)](#2-the-big-picture)
3. [Complete Folder Structure](#3-complete-folder-structure)
4. [The Frontend (What the User Sees)](#4-the-frontend)
5. [The Backend (The Brain / Server)](#5-the-backend)
6. [A Full Request Walk-Through](#6-a-full-request-walk-through)
7. [The Risk Score System](#7-the-risk-score-system)
8. [Where Data Is Stored](#8-where-data-is-stored)
9. [Key Terms Glossary](#9-key-terms-glossary)
10. [How to Run the Project](#10-how-to-run-the-project)

---

## 1. What Is This Project?

**PhishGuard** is a **web application** that helps people detect **phishing attacks**.

> **What is phishing?** Phishing is when a scammer pretends to be a trusted
> company (like Google or your bank) to trick you into giving away your
> password, money, or personal information.

The app lets a user scan **three things**:

| Type        | What you paste                    | What it checks                 |
|-------------|-----------------------------------|--------------------------------|
| **URL**     | A suspicious link                 | HTTPS, IP, TLDs, SSL, etc.     |
| **Message** | A suspicious SMS / chat message   | Urgency, credentials, threats  |
| **Email**   | Sender, subject, and body         | Impersonation, urgency, body   |

After scanning, the app gives a **risk score from 0 to 100** and explains
**why** it flagged something — so the user can decide whether to trust it.

---

## 2. The Big Picture

This is a **client–server** application. There are two big pieces:

```
┌──────────────────────────────┐         ┌──────────────────────────────┐
│         FRONTEND             │         │           BACKEND            │
│         (Browser)            │  HTTP   │          (Server)            │
│                              │  ───►   │                              │
│  index.html, style.css,      │         │  FastAPI (Python)            │
│  app.js, scanner.js,         │ requests│  main.py                     │
│  api.js, ui.js, history.js   │  ◄───   │  detector/  (the brain)      │
│                              │  JSON   │  services/  (external calls) │
└──────────────────────────────┘         └──────────────────────────────┘
```

- **Frontend** = the part that runs in the user's **browser**.
  It draws the buttons you click and sends your input to the server.
- **Backend** = the part that runs on the **server** (your computer, in this case).
  It does the real "thinking" — analyzing the URL/message/email and returning a result.

They talk to each other using **HTTP requests** and **JSON**:

> - **HTTP Request** = a message the browser sends to the server asking it to do something.
> - **JSON** = a simple text format for data, made of `{ "key": "value" }` pairs.
> - **API** = a set of rules the server exposes so the frontend can ask it questions.

You can think of it like a **restaurant**:
- The **frontend** is the menu and the waiter (what you interact with).
- The **backend** is the kitchen (where the actual cooking/thinking happens).
- The **waiter** (frontend) carries your order (**request**) to the kitchen (**backend**)
  and brings back your food (**response**).
---

## 3. Complete Folder Structure

```
phishing-detector/
│
├── .kilo/                          # (A tool's workspace folder — ignore it)
│
├── venv/                           # Python virtual environment (don't touch)
│
├── backend/                        # ↓↓↓ THE SERVER (Python) ↓↓↓
│   ├── main.py                     #   The entry point / API routes
│   ├── requirements.txt            #   List of Python packages to install
│   ├── detector/                   #   The "brain" — analysis logic
│   │   ├── __init__.py             #     Marks this folder as a Python package
│   │   ├── url_detector.py         #     Analyzes URLs
│   │   ├── message_detector.py     #     Analyzes messages
│   │   ├── email_detector.py       #     Analyzes emails
│   │   ├── rules.py                #     The keyword / rule "dictionary"
│   │   ├── scoring.py              #     Converts checks into a 0–100 score
│   │   └── utils.py                #     Small helper functions
│   └── services/                   #   External network services
│       ├── __init__.py             #     Marks this folder as a Python package
│       ├── dns_service.py          #     Looks up a domain's IP address
│       ├── ssl_service.py          #     Checks SSL certificate validity
│       └── url_service.py          #     Traces URL redirects
│
├── frontend/                       # ↓↓↓ THE BROWSER (HTML/CSS/JS) ↓↓↓
│   ├── index.html                  #   The single page users see
│   ├── css/
│   │   ├── style.css               #   Main styling (colors, layout)
│   │   └── animations.css          #   Fancy moving effects
│   └── js/
│       ├── app.js                  #   Main app setup (tabs, theme, menu)
│       ├── scanner.js              #   Handles "Scan" button clicks
│       ├── api.js                  #   Talks to the backend (fetch)
│       ├── ui.js                   #   Draws the result dashboard
│       └── history.js              #   Saves past scans in the browser
│
├── DIAGRAM.md                      # A visual diagram of the flow
├── run.md                          # Instructions to start the app
└── ARCHITECTURE.md                 # ← You are here
```

> **What is a `__init__.py` file?** In Python, it marks a folder as an
> **importable package** — meaning you can `from detector.rules import ...`.
> Without it, Python won't know the folder is a usable module.

---

## 4. The Frontend

The frontend is everything the user interacts with. It is all static files
served by the backend, meaning the browser just loads them.

```html
frontend/
├── index.html        →  The only page (all tabs live here)
├── css/              →  How it looks
└── js/               →  How it behaves
```

### 4.1 `index.html` — The Page

- The single HTML page that defines the whole user interface.
- It contains **3 scanner forms** (URL, Message, Email) inside **tabs**.
- It also has a "How It Works" page and a "History" table.
- At the bottom you can see `<script>` tags that load each JavaScript file
  **in order** — this order matters because files depend on each other.

### 4.2 `css/style.css` — Styling

- Contains all the **layout and colors** — the "look" of the site.
- Uses **CSS variables** like `var(--border-color)` so colors are easy to change in one place.

### 4.3 `css/animations.css` — Effects

- Small CSS rules for animations like fading and glowing — just visual polish.

### 4.4 `js/app.js` — Main App Setup

Loads first and sets up the "non-scan" parts of the interface:

- Draws the floating **background particles**.
- Handles the **mobile menu** (hamburger).
- Handles **tab switching** between URL / Message / Email.
- Handles the **dark / light theme toggle** (saved in `localStorage`).
- Handles **navigation routing** between the Scanner, History, and How-It-Works pages.
### 4.5 `js/api.js` — Talks to the Backend

This is the **bridge** between frontend and backend. It defines 3 functions:

| Function         | Calls backend endpoint | Sends              |
|------------------|------------------------|--------------------|
| `scanURL(url)`   | `POST /api/scan-url`    | `{ "url": "..." }` |
| `scanMessage(m)` | `POST /api/scan-message`| `{ "message": "..." }` |
| `scanEmail(s,sub,body)` | `POST /api/scan-email` | `{ sender, subject, body }` |

Each function uses JavaScript's built-in **`fetch()`** to send an HTTP request
to the backend and get back a JSON result. If the server is unreachable, it
returns a **fake error result** so the UI still has something to show.

> **Globals note:** At the end, `window.API = { scanURL, scanMessage, scanEmail }`
> makes these functions available to other JS files. In the browser, `window` is
> the global "shared space."

### 4.6 `js/scanner.js` — Handles "Scan" Clicks

- Listens for the **form submit** events on all three forms.
- Reads the input the user typed, then calls the matching `API` function.
- Shows a **loading animation** ("Checking structure...", etc.) for at least 2 seconds.
- On success, calls `UI.showResult(result)` and `History.add(...)`.

### 4.7 `js/ui.js` — Draws the Result

Takes the JSON result from the backend and draws it on screen:

- Animates the **circular score** from 0 to the final number.
- Shows the **threat level badge** (SAFE / LOW RISK / SUSPICIOUS / HIGH RISK).
- Lists **"Why was this flagged?"** reasons.
- Lists **recommendations**.
- Lists every **detailed check** (PASS / INFO / WARNING / DANGER).

### 4.8 `js/history.js` — Saves Scan History

- Saves past scans into the browser's **`localStorage`** (max 20).
- Renders the history **table** on the History page with stats.
- Lets the user **clear** history.

> **What is `localStorage`?** A small storage area inside the browser that
> persists even after you close the page. It belongs to the browser, not the server.

---

## 5. The Backend

The backend is a **FastAPI** application written in Python. It receives
requests, runs the analysis, and returns JSON.

```html
backend/
├── main.py              →  Entry point + API routes
├── requirements.txt     →  Dependencies
├── detector/            →  The analysis logic ("the brain")
└── services/            →  External network lookups
```

### 5.1 `main.py` — The Entry Point & API Routes

- Creates the FastAPI app: `app = FastAPI(title="PhishGuard API")`.
- Adds **CORS middleware** (lets browsers from other origins call it during development).
- Defines **Pydantic models** (`URLScanRequest`, etc.) that automatically
  validate incoming request data.
- Defines **3 routes** (the public API):

| Route              | Function called in brain       |
|--------------------|--------------------------------|
| `POST /api/scan-url`    | `analyze_url(url)`        |
| `POST /api/scan-message`| `analyze_message(message)`|
| `POST /api/scan-email`  | `analyze_email(sender, subject, body)` |

- **Serves the frontend**: it mounts the `frontend/` folder as static files,
  so opening `http://127.0.0.1:8000` shows the page.

> **What is a route / endpoint?** A specific URL+method combination the server
> responds to, e.g. `POST /api/scan-url`. FastAPI matches each request to a Python function.

### 5.2 `detector/` — The Brain

These files contain all the rules and logic that decide if something is phishing.

| File                    | Job |
|-------------------------|-----|
| `rules.py`              | The **dictionary** of suspicious keywords, TLDs, brands, shorteners. |
| `url_detector.py`       | Checks a **URL** against 14+ checks. |
| `message_detector.py`   | Checks a **message** for scam language and embedded URLs. |
| `email_detector.py`     | Checks **sender + subject + body**, including impersonation. |
| `scoring.py`            | Adds up `score_impact` from all checks → final 0–100 score. |
| `utils.py`              | Helpers: extract URLs from text, compare string similarity. |

#### `rules.py` — The Rule Dictionary
This file holds plain Python lists that drive everything:

- `SUSPICIOUS_KEYWORDS` — "verify", "login", "password", "prize"...
- `SUSPICIOUS_TLDS` — `.xyz`, `.top`, `.click`, `.tk`...
- `KNOWN_BRANDS` — google.com, paypal.com, apple.com...
- `URL_SHORTENERS` — bit.ly, tinyurl.com...
- `URGENCY_KEYWORDS` — "urgent", "act now", "last warning"...
- `CREDENTIAL_KEYWORDS` — "password", "otp", "pin", "cvv"...
- `FINANCIAL_KEYWORDS` — "bank", "payment", "refund"...
- `REWARD_KEYWORDS` — "winner", "prize", "congratulations"...
- `THREAT_KEYWORDS` — "account suspended", "legal action"...

> This is the easiest place to extend the app — just add a keyword or brand!
#### `url_detector.py` — URL Checks
`analyze_url(url)` performs checks and records each result as a **check**
dictionary with: `id`, `title`, `status` (PASS/INFO/WARNING/DANGER),
`explanation`, and `score_impact` (how many risk points it's worth).

Checks include: **HTTPS**, **IP address**, **URL length**, **@ symbol**,
**suspicious keywords**, **suspicious TLD**, **excessive subdomains**,
**punycode/hyphens**, **typosquatting**, **DNS resolution**,
**SSL certificate**, **redirects**, **URL shorteners**, and
**suspicious domain patterns** (brand + "secure" combo).

It uses helper functions from `services/` to do real network lookups, and
`scoring.py` to compute the final score.

#### `message_detector.py` — Message Checks
`analyze_message(message)` checks for **urgency**, **credential requests**,
**financial requests**, **rewards**, **threats**, and **embedded URLs**.
If a URL is found inside the message, it runs `analyze_url()` on it too.

#### `email_detector.py` — Email Checks
`analyze_email(sender, subject, body)` treats the subject + body as a message,
then adds email-specific checks like **free-provider impersonation**
(e.g. `paypal.verify@gmail.com`) and **urgent subject lines**.

#### `scoring.py` — Turning Checks Into a Score
- `calculate_risk_score(checks)` sums every check's `score_impact`, caps it at **0–100**,
  and labels the result: SAFE / LOW RISK / SUSPICIOUS / HIGH RISK.
- `generate_recommendations(score, checks)` builds helpful safety advice based on what was flagged.

#### `utils.py` — Small Helpers
- `extract_urls(text)` — finds URLs inside a message using **regex**.
- `compute_string_similarity(a, b)` — measures how similar two strings look
  (used to detect typosquatting, e.g. `paypa1.com` vs `paypal`).

> **What is regex?** A pattern-matching language for text. `r'https?://\S+'` is a
> pattern that matches web links inside a string.

### 5.3 `services/` — Talking to the Outside World

The main `detector` files stay mostly "text-based." For real-world checks they
call these services:

| File             | What it does |
|------------------|--------------|
| `dns_service.py` | Uses `dnspython` to look up the **IP address** a domain resolves to (DNS). |
| `ssl_service.py` | Opens a network connection to check the **SSL certificate** is valid. |
| `url_service.py` | Uses the `requests` library to **follow redirects** and count them. |

> **What is DNS?** The "phonebook of the internet" — it turns a domain name
> like `paypal.com` into a numeric IP address.
>
> **What is SSL?** The encryption technology (the padlock 🔒) that keeps a
> website's connection secure and proves identity via a certificate.

---

## 6. A Full Request Walk-Through

Let's trace **one URL scan** from start to finish:

```

1. USER types "mybank-secure-login.xyz" into the URL box & clicks "Scan Now"

2. scanner.js  →  reads the input, calls  window.API.scanURL(url)
   │
3. api.js      →  fetch('/api/scan-url', { method: 'POST', body: { url } })
   │
   │   ▼  (HTTP request over the network / localhost)
4. main.py     →  FastAPI matches POST /api/scan-url → calls analyze_url(url)
   │
5. url_detector.py
   │    ├─ checks HTTPS ............ (uses http -> WARNING +10)
   │    ├─ checks keywords ......... ("secure", "login" -> WARNING +15)
   │    ├─ checks TLD .............. (".xyz" -> WARNING +10)
   │    ├─ checks DNS .............. (services/dns_service.py)
   │    ├─ checks SSL .............. (services/ssl_service.py)
   │    ├─ checks redirects ........ (services/url_service.py)
   │    └─ ... more checks
   │
6. scoring.py  →  adds up score_impact  →  e.g. 35 → "LOW RISK"
   │
   │   ▼  (JSON response)
7. main.py     →  returns JSON { risk_score: 35, threat_level: "LOW RISK", checks: [...], ... }
   │
8. api.js      →  receives the JSON, returns it to scanner.js
   │
9. scanner.js  →  calls  UI.showResult(result)  and  History.add(...)
   │
10. ui.js      →  animates the score ring, shows the badge, lists the checks
11. history.js →  saves the scan to localStorage (last 20 scans)

```

The same pattern applies to message and email scans — they just call different
detectors.
---

## 7. The Risk Score System

Every check adds **points** via its `score_impact`. Points are summed and
**capped between 0 and 100**.

| Score Range | Threat Level | Color  |
|-------------|--------------|--------|
| 0 – 24      | SAFE         | 🟢 Green |
| 25 – 49     | LOW RISK     | 🔵 Blue |
| 50 – 74     | SUSPICIOUS   | 🟡 Yellow |
| 75 – 100    | HIGH RISK    | 🔴 Red |

Example point values (see `url_detector.py`):
- HTTP (no HTTPS) → **+10**
- Direct IP address → **+20**
- `@` symbol → **+25**
- Suspicious keyword → **+5** each (max +15)
- Suspicious TLD → **+10**
- Typosquatting lookalike → **+25**

> A check with `status: "PASS"` or `"INFO"` usually adds 0 points.
> `"WARNING"` and `"DANGER"` add points and are highlighted in the UI.

---

## 8. Where Data Is Stored

**There is no database and no server-side storage in this project.**

- Scan history is stored in the **browser's `localStorage`** under the key
  `phishguard_history`.
- Max **20 scans** are kept.
- It only stores: type, input, score, and result.
- The user can clear it anytime.
- It's **private** — it never leaves the browser.

> This keeps the app simple and privacy-friendly. If you later wanted shared or
> persistent history across devices, you'd add a real database (like SQLite/PostgreSQL)
> to the backend.
---

## 9. Key Terms Glossary

Below are the most important terms a beginner will see, explained simply.

| Term | Plain meaning |
|------|---------------|
| **Frontend** | The part of an app that runs in the browser (what you see/click). |
| **Backend** | The server-side code that does the real work and returns data. |
| **API** | A set of rules/endpoints the backend exposes so the frontend can request data. |
| **Endpoint / Route** | One specific URL+method (`POST /api/scan-url`) the server answers. |
| **HTTP Request** | A message from client to server asking for something. |
| **HTTP Response** | The server's answer to a request. |
| **JSON** | A text data format: `{ "name": "value" }` used to send/receive data. |
| **fetch()** | A built-in browser function to send HTTP requests from JavaScript. |
| **HTTP methods** | Verbs like GET (read) and POST (send data). This app uses POST. |
| **CORS** | A browser security rule; lets a frontend from another origin call the API. |
| **Static files** | Files (HTML/CSS/JS) served as-is, no processing. |
| **Server** | A computer/program that listens for requests and responds. |
| **Client** | The device/program requesting things (here: the browser). |
| **Port** | A "doorway" number (e.g. `8000`) a server listens on. |
| **localhost / 127.0.0.1** | "This computer" — where the dev server runs. |
| **Framework** | A pre-built toolkit. Here: **FastAPI** (Python) and plain JS on the front. |
| **Function** | A named block of reusable code. |
| **Module / Package** | A `.py` file / a folder of `.py` files (`detector/`). |
| **Import** | Bringing another module's code into yours (`from x import y`). |
| **Dictionary (dict)** | A Python key→value container: `{ "a": 1 }`. |
| **List (array)** | An ordered collection: `[1, 2, 3]`. |
| **Boolean** | `True` or `False`. |
| **Dependency** | An external library your project needs (listed in `requirements.txt`). |
| **Virtual env (venv)** | An isolated Python install so project packages don't clash globally. |
| **Pydantic** | A library that validates data in FastAPI request models. |
| **Regex** | Text pattern-matching used to find URLs/patterns. |
| **DNS** | The "internet phonebook" mapping domain names → IP addresses. |
| **IP address** | The numeric address of a machine on a network (e.g. `142.250.72.14`). |
| **Domain / TLD** | Domain = `paypal.com`; TLD = the final `.com` (or `.xyz`, `.tk`). |
| **Subdomain** | The part before the domain, e.g. `login.paypal.com` → `login`. |
| **SSL / HTTPS** | Encryption + identity (the padlock 🔒) for secure connections. |
| **Certificate** | A digital identity document a server proves it owns its domain. |
| **Redirect** | When a URL silently forwards to another URL. |
| **Punycode** | Encoding for non-Latin characters that can hide fake domains (`xn--`). |
| **Typosquatting** | Registering a domain that looks like a real brand (`paypa1.com`). |
| **URL shortener** | A service that makes tiny links hiding the real destination (bit.ly). |
| **localStorage** | A small, persistent storage area inside the browser. |
| **UI (user interface)** | Everything the user sees and interacts with. |
| **Threat level** | The final label: SAFE / LOW RISK / SUSPICIOUS / HIGH RISK. |
| **Logging** | Printing messages (e.g. `console.error`) to help debug. |
---

## 10. How to Run the Project

See `run.md` for the official steps. Quick version (Windows):

```bash
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start the server (runs backend AND serves the frontend)
uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Then open **http://127.0.0.1:8000** in your browser.

> The backend serves the frontend too (via `main.py`'s static mount), so you
> don't need a separate frontend dev server. Both run from one command.

---

## Where to Go Next (Suggested Learning Path)

1. Read `run.md` and get the app running.
2. Follow the [Full Request Walk-Through](#6-a-full-request-walk-through) while
   pressing F12 in the browser (Network tab) to watch requests live.
3. Add your own keyword to `rules.py` and test it.
4. Change a `score_impact` value in `url_detector.py` and see the score change.
5. When you're comfortable, try adding a new scan type (e.g. a phone-number scanner)
   by adding a route in `main.py` + a detector in `detector/`.

Happy hacking! 🚀