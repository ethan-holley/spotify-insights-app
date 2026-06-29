import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { auth } from "../lib/auth";

export default function Callback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [message, setMessage] = useState("Connecting your Spotify account...");

  useEffect(() => {
    const token = searchParams.get("token");
    const refreshToken = searchParams.get("refresh_token");
    const error = searchParams.get("error");

    if (error) {
      setMessage("Spotify login failed. Please try again.");
      setTimeout(() => navigate("/", { replace: true }), 1500);
      return;
    }

    if (!token) {
      setMessage("No Spotify token found. Please try logging in again.");
      setTimeout(() => navigate("/", { replace: true }), 1500);
      return;
    }

    auth.setTokens(token, refreshToken || undefined);
    navigate("/dashboard", { replace: true });
  }, [navigate, searchParams]);

  return <div className="loading">{message}</div>;
}