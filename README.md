# Spotify Insights

A full-stack web app that connects to your Spotify account to surface listening stats, generate a personalized "Wrapped" dashboard, and recommend new music based on your taste profile.

## Features

- **Stats Dashboard** — Top tracks, artists, and genres across 4 weeks / 6 months / all time
- **Listening Profile** — Audio feature breakdown (energy, valence, danceability, acousticness)
- **Discovery Engine** — AI-generated recommendations seeded from your taste fingerprint, pushed as a Spotify playlist
- **Wrapped Card** — Shareable summary of your listening year

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.11+, FastAPI, httpx |
| Frontend | React 18, TypeScript, Vite |
| Auth | Spotify OAuth 2.0 (Authorization Code + PKCE) |
| Deployment | Vercel (frontend), Railway or Render (backend) |

## Project Structure

```
spotify-insights/
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/  # auth, stats, discovery, wrapped
│   │   ├── services/ # spotify_client, recommendations
│   │   └── models/   # pydantic response models
│   └── requirements.txt
├── frontend/         # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/    # Home, Dashboard, Discovery, Wrapped
│   │   ├── components/
│   │   ├── hooks/    # useSpotify, useStats, useDiscovery
│   │   └── lib/      # api client, auth utils
│   └── package.json
└── docs/             # API docs, setup guides
```

## Getting Started

See [docs/setup.md](./docs/setup.md) for full setup instructions.

Quick start:
```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```
