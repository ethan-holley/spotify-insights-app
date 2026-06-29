import type {
  StatsResponse,
  WrappedResponse,
  TimeRange,
} from "../types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}` };
}

async function fetchJSON<T>(
  url: string,
  token: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: { ...authHeaders(token), ...(options.headers ?? {}) },
  });

  if (!res.ok) {
    let message = `API error ${res.status}: ${res.statusText}`;

    try {
      const body = await res.json();
      if (body.detail) message = String(body.detail);
    } catch {
      // keep default message
    }

    throw new Error(message);
  }

  return res.json() as Promise<T>;
}

export const api = {
  getStats: (token: string, range: TimeRange): Promise<StatsResponse> =>
    fetchJSON(`${BASE_URL}/stats/${range}`, token),

  getWrapped: (token: string): Promise<WrappedResponse> =>
    fetchJSON(`${BASE_URL}/wrapped/`, token),

  loginUrl: () => `${BASE_URL}/auth/login`,
};