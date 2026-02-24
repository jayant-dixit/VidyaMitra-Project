import React, { createContext, useContext, useState, useEffect } from "react";
import { apiClient } from "../services/apiClient.js";

const AuthContext = createContext(null);

export function AuthContextProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("vm_token"));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem("vm_token", token);
      apiClient.setToken(token);
      apiClient.get("/auth/me").then((res) => setUser(res.data)).catch(() => {});
    } else {
      localStorage.removeItem("vm_token");
      apiClient.setToken(null);
      setUser(null);
    }
  }, [token]);

  const login = async (email, password) => {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    const res = await apiClient.post("/auth/token", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    setToken(res.data.access_token);
  };

  const register = async (fullName, email, password) => {
    await apiClient.post("/auth/register", {
      full_name: fullName,
      email,
      password
    });
    await login(email, password);
  };

  const logout = () => setToken(null);

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthContextProvider");
  }
  return ctx;
}

