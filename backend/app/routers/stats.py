from collections import Counter

from fastapi import APIRouter, Header, HTTPException

from app.services.spotify_client import SpotifyClient
from app.models.responses import (
    StatsResponse,
    Track,
    Artist,
    GenreCount,
    TasteProfile,
    PersonalityType
)

router = APIRouter()

TIME_RANGES = {
    "short": "short_term",
    "medium": "medium_term",
    "long": "long_term",
}


def _get_token(authorization: str) -> str:
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return token


def _extract_track(t: dict) -> Track:
    artists = t.get("artists", [])
    artist_names = ", ".join(a.get("name", "Unknown Artist") for a in artists)

    album = t.get("album", {})
    images = album.get("images", [])

    return Track(
        id=t.get("id", ""),
        name=t.get("name", "Unknown Track"),
        artist=artist_names or "Unknown Artist",
        album=album.get("name", "Unknown Album"),
        album_art=images[0]["url"] if images else None,
        preview_url=t.get("preview_url"),
        external_url=t.get("external_urls", {}).get("spotify", ""),
        popularity=t.get("popularity", 0),
        explicit=t.get("explicit", False),
        uri=t.get("uri"),
    )


def _extract_artist(a: dict) -> Artist:
    images = a.get("images", [])

    return Artist(
        id=a.get("id", ""),
        name=a.get("name", "Unknown Artist"),
        image_url=images[0]["url"] if images else None,
        genres=a.get("genres", []),
        popularity=a.get("popularity", 0),
        external_url=a.get("external_urls", {}).get("spotify", ""),
    )


def _genre_breakdown(artists: list[Artist], limit: int = 8) -> list[GenreCount]:
    counter: Counter[str] = Counter()

    for artist in artists:
        for genre in artist.genres:
            counter[genre] += 1

    return [
        GenreCount(name=genre, count=count)
        for genre, count in counter.most_common(limit)
    ]


def _compute_profile(tracks: list[Track], artists: list[Artist], genres: list[GenreCount]) -> TasteProfile:
    if not tracks:
        return TasteProfile(
            mainstream_score=0,
            artist_variety=0,
            genre_variety=0,
            explicit_rate=0,
            track_depth=0,
        )

    avg_track_popularity = round(
        sum(track.popularity for track in tracks) / len(tracks)
    )

    unique_track_artists = {
        artist.strip()
        for track in tracks
        for artist in track.artist.split(",")
        if artist.strip()
    }

    artist_variety = min(100, len(unique_track_artists) * 5)
    genre_variety = min(100, len(genres) * 12)
    explicit_rate = round(
        sum(1 for track in tracks if track.explicit) / len(tracks) * 100
    )

    # Lower popularity means more "deep cut" taste.
    track_depth = max(0, 100 - avg_track_popularity)

    return TasteProfile(
        mainstream_score=avg_track_popularity,
        artist_variety=artist_variety,
        genre_variety=genre_variety,
        explicit_rate=explicit_rate,
        track_depth=track_depth,
    )


def _get_personality(profile: TasteProfile, genres: list[GenreCount]) -> PersonalityType:
    top_genre = genres[0].name if genres else "different genres"

    if profile.track_depth >= 45 and profile.genre_variety >= 50:
        return PersonalityType(
            name="The Deep Cutter",
            description="You dig past the obvious hits and jump across different sounds.",
        )

    if profile.mainstream_score >= 70:
        return PersonalityType(
            name="The Hype Machine",
            description="Your taste is plugged into popular tracks, major artists, and songs people are talking about.",
        )

    if profile.artist_variety >= 75:
        return PersonalityType(
            name="The Explorer",
            description="You rarely stay in one lane and your top tracks cover a wide range of artists.",
        )

    if profile.genre_variety >= 60:
        return PersonalityType(
            name="The Genre Hopper",
            description=f"You move across styles often, with {top_genre} showing up as one of your strongest lanes.",
        )

    return PersonalityType(
        name="The Loyalist",
        description="You know what you like and tend to come back to a focused group of artists and sounds.",
    )


@router.get("/{time_range}", response_model=StatsResponse)
async def get_stats(
    time_range: str = "medium",
    authorization: str = Header(...),
):
    token = _get_token(authorization)

    spotify_range = TIME_RANGES.get(time_range, "medium_term")
    client = SpotifyClient(token)

    tracks_data = await client.get_top_tracks(spotify_range, limit=20)
    artists_data = await client.get_top_artists(spotify_range, limit=20)

    raw_tracks = tracks_data.get("items", [])
    raw_artists = artists_data.get("items", [])

    tracks = [_extract_track(t) for t in raw_tracks]
    artists = [_extract_artist(a) for a in raw_artists]

    if not tracks and not artists:
        raise HTTPException(status_code=404, detail="Not enough Spotify listening data yet")

    top_genres = _genre_breakdown(artists)
    profile = _compute_profile(tracks, artists, top_genres)
    personality = _get_personality(profile, top_genres)

    return StatsResponse(
        top_tracks=tracks[:10],
        top_artists=artists[:10],
        top_genres=top_genres,
        profile=profile,
        personality=personality,
        time_range=time_range,
    )