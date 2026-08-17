import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import api, { setToken, clearToken, getToken } from "@/lib/api";

const AuthCtx = createContext(null);
export const useAuth = () => useContext(AuthCtx);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [org, setOrg] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    if (!getToken()) { setUser(null); setOrg(null); setLoading(false); return; }
    try {
      const { data } = await api.get("/auth/me");
      setUser(data.user);
      setOrg(data.org);
    } catch {
      setUser(null); setOrg(null); clearToken();
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { refresh(); }, [refresh]);

  const loginWithToken = async (token) => {
    setToken(token);
    await refresh();
  };

  const logout = () => {
    clearToken(); setUser(null); setOrg(null);
    window.location.href = "/";
  };

  return (
    <AuthCtx.Provider value={{ user, org, loading, refresh, loginWithToken, logout, setOrg }}>
      {children}
    </AuthCtx.Provider>
  );
};
