import { useState, useEffect } from "react";
import { api } from "../lib/api";
import { auth } from "../lib/auth";
import type { WrappedResponse } from "../types";

export default function Wrapped() {
  const [data, setData] = useState<WrappedResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = auth.getToken();

    if (!token) {
      setError("Not authenticated");
      setLoading(false);
      return;
    }

    api
      .getWrapped(token)
      .then(setData)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Generating your Wrapped…</div>;
  if (error) return <div className="error">{error}</div>;
  if (!data) return null;

  const shareText = `My Spotify listening personality is ${data.personality.name}. My top artist is ${data.top_artist.name}. #SpotifyInsights`;

  return (
    <div className="wrapped">
      <div className="wrapped-card">
        <div className="wrapped-header">
          <h2>{data.display_name}'s Wrapped</h2>
          <span className="wrapped-sub">All-time listening identity</span>
        </div>

        <div className="wrapped-personality">
          <span className="personality-eyebrow">You are</span>
          <h1 className="personality-big">{data.personality.name}</h1>
          <p>{data.personality.description}</p>
        </div>

        <div className="wrapped-highlights">
          <div className="highlight">
            <span className="hl-label">Top track</span>
            <div className="hl-content">
              {data.top_track.album_art && (
                <img src={data.top_track.album_art} alt="" className="hl-art" />
              )}
              <div>
                <span className="hl-primary">{data.top_track.name}</span>
                <span className="hl-secondary">{data.top_track.artist}</span>
              </div>
            </div>
          </div>

          <div className="highlight">
            <span className="hl-label">Top artist</span>
            <div className="hl-content">
              {data.top_artist.image_url && (
                <img
                  src={data.top_artist.image_url}
                  alt=""
                  className="hl-art round"
                />
              )}
              <span className="hl-primary">{data.top_artist.name}</span>
            </div>
          </div>

          <div className="highlight">
            <span className="hl-label">Top genre</span>
            <span className="hl-primary genre-text">{data.top_genre}</span>
          </div>
        </div>

        <div className="wrapped-fingerprint">
          <div className="fp-item">
            <span className="fp-val">{data.profile.mainstream_score}</span>
            <span className="fp-label">Mainstream</span>
          </div>

          <div className="fp-item">
            <span className="fp-val">{data.profile.artist_variety}</span>
            <span className="fp-label">Artist Variety</span>
          </div>

          <div className="fp-item">
            <span className="fp-val">{data.profile.track_depth}</span>
            <span className="fp-label">Deep Cuts</span>
          </div>
        </div>

        <button
          className="btn-share"
          onClick={() => {
            if (navigator.share) {
              navigator.share({ text: shareText });
            } else {
              navigator.clipboard.writeText(shareText);
              alert("Copied to clipboard!");
            }
          }}
        >
          Share your Wrapped
        </button>
      </div>
    </div>
  );
}