import httpx
from typing import Any

SPOTIFY_API_BASE = "https://api.spotify.com/v1"
SPOTIFY_AUTH_BASE = "https://accounts.spotify.com"


class SpotifyClient:
    """Thin async wrapper around the Spotify Web API."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def _get(self, path: str, params: dict | None = None) -> Any:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{SPOTIFY_API_BASE}{path}",
                headers=self.headers,
                params=params or {},
            )
            resp.raise_for_status()
            return resp.json()

    async def _post(self, path: str, json: dict) -> Any:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{SPOTIFY_API_BASE}{path}",
                headers={**self.headers, "Content-Type": "application/json"},
                json=json,
            )
            resp.raise_for_status()
            return resp.json()

    # ── User ──────────────────────────────────────────────────────────────
    async def get_me(self) -> dict:
        return await self._get("/me")

    # ── Top items ─────────────────────────────────────────────────────────
    async def get_top_tracks(self, time_range: str = "medium_term", limit: int = 20) -> dict:
        """time_range: short_term (4w) | medium_term (6mo) | long_term (all time)"""
        return await self._get("/me/top/tracks", {"time_range": time_range, "limit": limit})

    async def get_top_artists(self, time_range: str = "medium_term", limit: int = 20) -> dict:
        return await self._get("/me/top/artists", {"time_range": time_range, "limit": limit})

    # ── Recent plays ──────────────────────────────────────────────────────
    async def get_recently_played(self, limit: int = 50) -> dict:
        return await self._get("/me/player/recently-played", {"limit": limit})

    # ── Audio features ────────────────────────────────────────────────────
    async def get_audio_features(self, track_ids: list[str]) -> dict:
        """Batch fetch audio features for up to 100 tracks."""
        return await self._get("/audio-features", {"ids": ",".join(track_ids)})

    # ── Recommendations ───────────────────────────────────────────────────
    async def get_recommendations(
        self,
        seed_artists: list[str] | None = None,
        seed_tracks: list[str] | None = None,
        seed_genres: list[str] | None = None,
        target_features: dict | None = None,
        limit: int = 20,
    ) -> dict:
        params: dict = {"limit": limit}
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists[:2])
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks[:2])
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres[:1])
        if target_features:
            params.update({f"target_{k}": v for k, v in target_features.items()})
        return await self._get("/recommendations", params)

    # ── Playlists ─────────────────────────────────────────────────────────
    async def create_playlist(self, user_id: str, name: str, description: str = "") -> dict:
        return await self._post(
            f"/users/{user_id}/playlists",
            {"name": name, "description": description, "public": False},
        )

    async def add_tracks_to_playlist(self, playlist_id: str, track_uris: list[str]) -> dict:
        return await self._post(f"/playlists/{playlist_id}/tracks", {"uris": track_uris})
    
    async def get_artist(self, artist_id: str) -> dict:
        return await self._get(f"/artists/{artist_id}")
