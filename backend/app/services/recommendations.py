from app.services.spotify_client import SpotifyClient


PERSONALITY_TYPES = [
    {
        "name": "The Deep Cutter",
        "condition": lambda f: f["popularity"] < 40 and f["acousticness"] > 0.5,
        "description": "You dig past the algorithm. Your taste lives in B-sides and bedroom recordings.",
    },
    {
        "name": "The Hype Machine",
        "condition": lambda f: f["popularity"] > 70 and f["energy"] > 0.7,
        "description": "You're on the pulse. If it's blowing up, you were probably there first.",
    },
    {
        "name": "The Mood Architect",
        "condition": lambda f: f["valence"] < 0.4 and f["instrumentalness"] > 0.3,
        "description": "Music is atmosphere for you. You curate feelings, not playlists.",
    },
    {
        "name": "The Floor Filler",
        "condition": lambda f: f["danceability"] > 0.7 and f["energy"] > 0.6,
        "description": "High BPM, high energy. Every song is a potential party.",
    },
    {
        "name": "The Eclectic",
        "condition": lambda f: True,
        "description": "Your taste defies easy labels. That's a flex.",
    },
]


def compute_taste_fingerprint(audio_features: list[dict]) -> dict:
    """Average audio features across top tracks to build a taste profile."""
    keys = ["danceability", "energy", "valence", "acousticness", "instrumentalness", "speechiness"]
    totals = {k: 0.0 for k in keys}
    popularity_total = 0

    valid = [f for f in audio_features if f is not None]
    if not valid:
        return {}

    for f in valid:
        for k in keys:
            totals[k] += f.get(k, 0)
        popularity_total += f.get("popularity", 50)

    n = len(valid)
    fingerprint = {k: round(totals[k] / n, 3) for k in keys}
    fingerprint["popularity"] = round(popularity_total / n)
    return fingerprint


def get_personality_type(fingerprint: dict) -> dict:
    for p in PERSONALITY_TYPES:
        if p["condition"](fingerprint):
            return {"name": p["name"], "description": p["description"]}
    return {"name": "The Eclectic", "description": "Your taste defies easy labels."}


async def build_recommendations(client: SpotifyClient, fingerprint: dict, seed_artists: list[str], seed_tracks: list[str]) -> list[dict]:
    """Generate recommendations using taste fingerprint as target audio features."""
    target_features = {
        k: fingerprint[k]
        for k in ["danceability", "energy", "valence", "acousticness"]
    }

    data = await client.get_recommendations(
        seed_artists=seed_artists[:2],
        seed_tracks=seed_tracks[:3],
        target_features=target_features,
        limit=20,
    )

    return [
        {
            "id": t["id"],
            "uri": t["uri"],
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "album_art": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
            "preview_url": t.get("preview_url"),
            "external_url": t["external_urls"]["spotify"],
        }
        for t in data.get("tracks", [])
    ]
