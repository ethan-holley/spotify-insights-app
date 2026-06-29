import asyncio

from fastapi import APIRouter, Header, HTTPException

from app.services.spotify_client import SpotifyClient
from app.models.responses import WrappedResponse

from app.routers.stats import (
    _get_token,
    _extract_track,
    _extract_artist,
    _genre_breakdown,
    _compute_profile,
    _get_personality,
)

router = APIRouter()


@router.get("/", response_model=WrappedResponse)
async def get_wrapped(authorization: str = Header(...)):
    token = _get_token(authorization)
    client = SpotifyClient(token)

    me_data, tracks_data, artists_data = await asyncio.gather(
        client.get_me(),
        client.get_top_tracks("long_term", limit=20),
        client.get_top_artists("long_term", limit=20),
    )

    tracks = [_extract_track(t) for t in tracks_data.get("items", [])]
    artists = [_extract_artist(a) for a in artists_data.get("items", [])]

    if not tracks or not artists:
        raise HTTPException(status_code=404, detail="Not enough Spotify listening data yet")

    top_genres = _genre_breakdown(artists)
    profile = _compute_profile(tracks, artists, top_genres)
    personality = _get_personality(profile, top_genres)

    top_genre = top_genres[0].name if top_genres else "various"

    return WrappedResponse(
        display_name=me_data.get("display_name") or "Listener",
        top_track=tracks[0],
        top_artist=artists[0],
        top_genre=top_genre,
        top_genres=top_genres,
        personality=personality,
        profile=profile,
        total_top_tracks=len(tracks),
        total_top_artists=len(artists),
    )