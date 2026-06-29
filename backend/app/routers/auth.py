import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.config import settings

router = APIRouter()

SPOTIFY_SCOPES = " ".join(
    [
        "user-top-read",
        "user-read-recently-played",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-read-private",
    ]
)

_state_store: dict[str, bool] = {}


@router.get("/login")
def login():
    state = secrets.token_urlsafe(16)
    _state_store[state] = True

    params = {
        "client_id": settings.spotify_client_id,
        "response_type": "code",
        "redirect_uri": settings.spotify_redirect_uri,
        "scope": SPOTIFY_SCOPES,
        "state": state,
    }

    return RedirectResponse(
        f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    )


@router.get("/callback")
async def callback(
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
):
    if error:
        return RedirectResponse(f"{settings.frontend_url}/callback?error={error}")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state")

    if state not in _state_store:
        raise HTTPException(status_code=400, detail="Invalid state")

    del _state_store[state]

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.spotify_redirect_uri,
            },
            auth=(settings.spotify_client_id, settings.spotify_client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Token exchange failed: {resp.text}",
        )

    tokens = resp.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token", "")

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token returned")

    query = urlencode(
        {
            "token": access_token,
            "refresh_token": refresh_token,
        }
    )

    return RedirectResponse(f"{settings.frontend_url}/callback?{query}")


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(settings.spotify_client_id, settings.spotify_client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Refresh failed: {resp.text}")

    return resp.json()