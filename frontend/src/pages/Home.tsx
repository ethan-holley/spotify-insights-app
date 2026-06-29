import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { auth } from "../lib/auth";
import { api } from "../lib/api";

export default function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.isLoggedIn()) navigate("/dashboard");
  }, [navigate]);

  return (
    <div className="home">
      <div className="hero">
        <h1>Spotify Insights</h1>
        <p className="tagline">
          Discover who you really are as a listener.
        </p>
        <p className="sub">
          Connect your Spotify to see your top tracks, taste fingerprint,
          personalized music discoveries, and your all-time Wrapped.
        </p>
        <a href={api.loginUrl()} className="btn-primary">
          Connect with Spotify
        </a>
      </div>

      <div className="features">
        <div className="feature-card">
          <span className="feature-icon">📊</span>
          <h3>Stats Dashboard</h3>
          <p>Top tracks and artists across 4 weeks, 6 months, or all time.</p>
        </div>
        <div className="feature-card">
          <span className="feature-icon">🎯</span>
          <h3>Taste Fingerprint</h3>
          <p>Your audio DNA — energy, mood, danceability, and more.</p>
        </div>
        <div className="feature-card">
          <span className="feature-icon">🔍</span>
          <h3>Discovery Engine</h3>
          <p>New music seeded from your profile. Save to Spotify in one click.</p>
        </div>
        <div className="feature-card">
          <span className="feature-icon">🎁</span>
          <h3>Your Wrapped</h3>
          <p>A shareable summary of your all-time listening identity.</p>
        </div>
      </div>
    </div>
  );
}
