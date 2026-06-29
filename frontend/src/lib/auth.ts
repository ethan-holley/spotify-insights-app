const ACCESS_TOKEN_KEY = "spotify_access_token";
const REFRESH_TOKEN_KEY = "spotify_refresh_token";

export const auth = {
  getToken: (): string | null => sessionStorage.getItem(ACCESS_TOKEN_KEY),

  getRefreshToken: (): string | null => sessionStorage.getItem(REFRESH_TOKEN_KEY),

  setToken: (token: string): void => {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, token);
  },

  setTokens: (accessToken: string, refreshToken?: string): void => {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, accessToken);

    if (refreshToken) {
      sessionStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    }
  },

  clearToken: (): void => {
    sessionStorage.removeItem(ACCESS_TOKEN_KEY);
    sessionStorage.removeItem(REFRESH_TOKEN_KEY);
  },

  isLoggedIn: (): boolean => !!sessionStorage.getItem(ACCESS_TOKEN_KEY),
};