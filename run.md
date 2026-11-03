# PhishGuard — How to Run

## Prerequisites
- Python 3.10+

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start the server
uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```
`
## Open in Browser

```
http://127.0.0.1:8000
```

