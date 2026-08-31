# CO2 Cooling + Direct Air Capture Simulator (v2 — using engine2.py logic)

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
Opens at http://localhost:8501

## Push this folder to GitHub
Easiest way, no git command line needed:
1. Go to github.com/new, name the repo (e.g. `co2-cooling-simulator`), keep it
   Public (required for the free tier of Streamlit Community Cloud), and
   create it empty (no README/gitignore).
2. On the new repo's page, click "uploading an existing file" and drag in
   `engine.py`, `app.py`, `requirements.txt`, and this `README.md`.
3. Click "Commit changes".

Or with git installed locally, from inside this folder:
```
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/co2-cooling-simulator.git
git push -u origin main
```

## Deploy for free
Two good options:

### Option A — Streamlit Community Cloud
1. Push this folder to a GitHub repo (must include engine.py, app.py, requirements.txt) — see above
2. Go to https://share.streamlit.io -> sign in with GitHub
3. "New app" -> pick the repo -> set main file to app.py -> Deploy
4. Public link like yourapp.streamlit.app in ~1-2 minutes

### Option B — Render (needed if you also want other backend services alongside it)
1. Push this folder to a GitHub repo
2. On render.com: New -> Web Service -> connect the repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy — public URL provided automatically

## Files
- engine.py — the simulation logic (renamed from engine2.py, team's latest version)
- app.py — Streamlit UI: slider, live metrics, chart, sourced context panel
