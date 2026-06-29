from pydantic import BaseModel, Field
from typing import Optional


class Artist(BaseModel):
    id: str
    name: str
    image_url: Optional[str] = None
    genres: list[str] = Field(default_factory=list)
    popularity: int = 0
    external_url: str


class Track(BaseModel):
    id: str
    name: str
    artist: str
    album: str
    album_art: Optional[str] = None
    preview_url: Optional[str] = None
    external_url: str
    popularity: int = 0
    explicit: bool = False
    uri: Optional[str] = None


class GenreCount(BaseModel):
    name: str
    count: int


class TasteProfile(BaseModel):
    mainstream_score: int
    artist_variety: int
    genre_variety: int
    explicit_rate: int
    track_depth: int


class PersonalityType(BaseModel):
    name: str
    description: str

class StatsResponse(BaseModel):
    top_tracks: list[Track]
    top_artists: list[Artist]
    top_genres: list[GenreCount]
    profile: TasteProfile
    personality: PersonalityType
    time_range: str

class RecommendedTrack(BaseModel):
    id: str
    uri: str
    name: str
    artist: str
    album_art: Optional[str] = None
    preview_url: Optional[str] = None
    external_url: str


class DiscoveryResponse(BaseModel):
    tracks: list[RecommendedTrack]
    playlist_url: Optional[str] = None


class WrappedResponse(BaseModel):
    display_name: str
    top_track: Track
    top_artist: Artist
    top_genre: str
    top_genres: list[GenreCount]
    personality: PersonalityType
    profile: TasteProfile
    total_top_tracks: int
    total_top_artists: int