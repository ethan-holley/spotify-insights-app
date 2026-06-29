# Setup Guide

## 1. Create a Spotify App

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Click **Create app**
3. Fill in Name and Description
4. Set **Redirect URI** to `http://localhost:8000/auth/callback`
5. Save — copy your **Client ID** and **Client Secret**

## 2. Backend Setup

```bash
cd backend
cp .env.example .env
# Fill in your SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET in .env

pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will be running at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

## 3. Frontend Setup

```bash
cd frontend
cp .env.example .env
# VITE_API_URL=http://localhost:8000 (default is fine for local dev)

npm install
npm run dev
```

App will be running at `http://localhost:5173`.

## 4. Test the flow

1. Open `http://localhost:5173`
2. Click **Connect with Spotify**
3. Authorize the app in the Spotify popup
4. You'll be redirected to your dashboard

## Deployment

### Frontend → Vercel
```bash
cd frontend && npm run build
# Deploy /dist to Vercel
# Set VITE_API_URL to your deployed backend URL
```

### Backend → Railway or Render
- Connect your GitHub repo
- Set environment variables (same as .env)
- Update `SPOTIFY_REDIRECT_URI` to your production backend URL
- Update `FRONTEND_URL` to your Vercel frontend URL
- Add the production redirect URI to your Spotify app dashboard

## Spotify API Scopes Used

| Scope | Purpose |
|---|---|
| `user-top-read` | Top tracks and artists |
| `user-read-recently-played` | Recent listening history |
| `playlist-modify-private` | Save discovery playlists |
| `user-read-private` | User profile (display name, ID) |
