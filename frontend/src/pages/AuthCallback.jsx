import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { Logo } from "@/components/common/Logo";
import { Loader2 } from "lucide-react";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
export default function AuthCallback() {
  const location = useLocation();
  const navigate = useNavigate();
  const { loginWithToken } = useAuth();
  const processed = useRef(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;
    const hash = location.hash || window.location.hash;
    const match = hash.match(/session_id=([^&]+)/);
    if (!match) { navigate("/login", { replace: true }); return; }
    const session_id = decodeURIComponent(match[1]);
    (async () => {
      try {
        const { data } = await api.post("/auth/google/session", { session_id });
        await loginWithToken(data.token);
        window.history.replaceState(null, "", "/app");
        navigate("/app", { replace: true });
      } catch (e) {
        setError("Google sign-in failed. Please try again.");
        setTimeout(() => navigate("/login", { replace: true }), 1800);
      }
    })();
  }, []); // eslint-disable-line

  return (
    <div className="min-h-screen hero-wash flex flex-col items-center justify-center gap-4">
      <Logo />
      {error ? (
        <p className="text-sm text-[hsl(var(--danger-fg))]">{error}</p>
      ) : (
        <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))]">
          <Loader2 className="h-5 w-5 animate-spin" /> Signing you in…
        </div>
      )}
    </div>
  );
}
