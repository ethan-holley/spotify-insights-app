import { useState, useEffect } from "react";
import { api } from "../lib/api";
import { auth } from "../lib/auth";
import type { StatsResponse, TimeRange } from "../types";

export function useStats(range: TimeRange = "medium") {
  const [data, setData] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = auth.getToken();
    if (!token) {
      setError("Not authenticated");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    api
      .getStats(token, range)
      .then(setData)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [range]);

  return { data, loading, error };
}
