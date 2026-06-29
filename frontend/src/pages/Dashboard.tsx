import { useState } from "react";
import { useStats } from "../hooks/useStats";
import type { TimeRange } from "../types";

const RANGES: { label: string; value: TimeRange }[] = [
  { label: "Last 4 weeks", value: "short" },
  { label: "Last 6 months", value: "medium" },
  { label: "All time", value: "long" },
];

const PROFILE_LABELS: { key: keyof import("../types").TasteProfile; label: string }[] = [
  { key: "mainstream_score", label: "Mainstream Score" },
  { key: "artist_variety", label: "Artist Variety" },
  { key: "genre_variety", label: "Genre Variety" },
  { key: "explicit_rate", label: "Explicit Track Rate" },
  { key: "track_depth", label: "Deep Cut Score" },
];

export default function Dashboard() {
  const [range, setRange] = useState<TimeRange>("medium");
  const { data, loading, error } = useStats(range);

  if (loading) return <div className="loading">Loading your stats…</div>;
  if (error) return <div className="error">{error}</div>;
  if (!data) return null;

  return (
    <div className="dashboard">
      <div className="section-header">
        <h2>Your Stats</h2>
        <div className="range-tabs">
          {RANGES.map((r) => (
            <button
              key={r.value}
              className={range === r.value ? "tab active" : "tab"}
              onClick={() => setRange(r.value)}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      <div className="personality-card">
        <span className="personality-label">Your listening personality</span>
        <h3 className="personality-name">{data.personality.name}</h3>
        <p className="personality-desc">{data.personality.description}</p>
      </div>

      <div className="two-col">
        <section>
          <h3>Top Tracks</h3>
          <ol className="track-list">
            {data.top_tracks.map((t, i) => (
              <li key={t.id} className="track-item">
                <span className="rank">{i + 1}</span>
                {t.album_art && (
                  <img src={t.album_art} alt={t.album} className="album-art" />
                )}
                <div className="track-info">
                  <a
                    href={t.external_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="track-name"
                  >
                    {t.name}
                  </a>
                  <span className="track-artist">{t.artist}</span>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section>
          <h3>Top Artists</h3>
          <ol className="artist-list">
            {data.top_artists.map((a, i) => (
              <li key={a.id} className="artist-item">
                <span className="rank">{i + 1}</span>
                {a.image_url && (
                  <img src={a.image_url} alt={a.name} className="artist-img" />
                )}
                <div className="artist-info">
                  <a
                    href={a.external_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="artist-name"
                  >
                    {a.name}
                  </a>
                  {a.genres[0] && <span className="genre-tag">{a.genres[0]}</span>}
                </div>
              </li>
            ))}
          </ol>
        </section>
      </div>

      <section className="fingerprint">
        <h3>Taste Profile</h3>
        <div className="feature-bars">
          {PROFILE_LABELS.map(({ key, label }) => {
            const val = data.profile[key];

            return (
              <div key={key} className="feature-row">
                <span className="feature-label">{label}</span>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: `${val}%` }} />
                </div>
                <span className="feature-val">{val}</span>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}