export type TimeRange = "short" | "medium" | "long";

export interface Track {
  id: string;
  name: string;
  artist: string;
  album: string;
  album_art?: string | null;
  preview_url?: string | null;
  external_url: string;
  popularity: number;
  explicit: boolean;
  uri?: string | null;
}

export interface Artist {
  id: string;
  name: string;
  image_url?: string | null;
  genres: string[];
  popularity: number;
  external_url: string;
}

export interface GenreCount {
  name: string;
  count: number;
}

export interface TasteProfile {
  mainstream_score: number;
  artist_variety: number;
  genre_variety: number;
  explicit_rate: number;
  track_depth: number;
}

export interface PersonalityType {
  name: string;
  description: string;
}

export interface StatsResponse {
  top_tracks: Track[];
  top_artists: Artist[];
  top_genres: GenreCount[];
  profile: TasteProfile;
  personality: PersonalityType;
  time_range: TimeRange;
}

export interface WrappedResponse {
  display_name: string;
  top_track: Track;
  top_artist: Artist;
  top_genre: string;
  top_genres: GenreCount[];
  personality: PersonalityType;
  profile: TasteProfile;
  total_top_tracks: number;
  total_top_artists: number;
}

export interface RecommendedTrack {
  id: string;
  uri: string;
  name: string;
  artist: string;
  album_art?: string | null;
  preview_url?: string | null;
  external_url: string;
}

export interface DiscoveryResponse {
  tracks: RecommendedTrack[];
  playlist_url?: string | null;
}