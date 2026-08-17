import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { toast } from "sonner";
import { Smartphone, ShieldCheck, ArrowRight } from "lucide-react";

export default function Login() {
  const nav = useNavigate();
  const loc = useLocation();
  const { loginWithToken } = useAuth();
  const next = loc.state?.next;

  // client OTP
  const [mobile, setMobile] = useState("");
  const [name, setName] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [devOtp, setDevOtp] = useState("");
  const [busy, setBusy] = useState(false);

  // admin
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mfa, setMfa] = useState("");
  const [mfaReq, setMfaReq] = useState(false);

  const requestOtp = async () => {
    if (mobile.length < 8) return toast.error("Enter a valid mobile number");
    setBusy(true);
    try {
      const { data } = await api.post("/auth/otp/request", { mobile, name });
      setOtpSent(true); setDevOtp(data.dev_otp);
      toast.success("OTP sent (simulated)");
    } catch (e) { toast.error("Could not send OTP"); } finally { setBusy(false); }
  };

  const verifyOtp = async () => {
    setBusy(true);
    try {
      const { data } = await api.post("/auth/otp/verify", { mobile, code: otp, name });
      await loginWithToken(data.token);
      toast.success("Welcome!");
      nav(next || "/app");
    } catch (e) { toast.error(e?.response?.data?.detail || "Invalid OTP"); } finally { setBusy(false); }
  };

  const adminLogin = async () => {
    setBusy(true);
    try {
      const { data } = await api.post("/auth/admin/login", { email, password, mfa_code: mfaReq ? mfa : undefined });
      if (data.mfa_required) { setMfaReq(true); toast.message("Enter your MFA code"); setBusy(false); return; }
      await loginWithToken(data.token);
      toast.success("Admin signed in");
      nav("/admin");
    } catch (e) { toast.error(e?.response?.data?.detail || "Login failed"); } finally { setBusy(false); }
  };

  return (
    <div className="min-h-screen hero-wash flex flex-col">
      <header className="border-b bg-white/80 backdrop-blur">
        <div className="max-w-6xl mx-auto flex h-16 items-center px-4 sm:px-6"><button onClick={() => nav("/")}><Logo /></button></div>
      </header>
      <div className="flex-1 flex items-center justify-center px-4 py-10">
        <Card className="card-shadow w-full max-w-md p-6">
          <h1 className="text-2xl font-display text-center">Sign in to FaizZab</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))] text-center mt-1">Client access via mobile OTP · Admin via credentials</p>
          <Tabs defaultValue="client" className="mt-6">
            <TabsList className="grid grid-cols-2 w-full">
              <TabsTrigger value="client" data-testid="tab-client"><Smartphone className="h-4 w-4 mr-1" />Client</TabsTrigger>
              <TabsTrigger value="admin" data-testid="tab-admin"><ShieldCheck className="h-4 w-4 mr-1" />Admin</TabsTrigger>
            </TabsList>

            <TabsContent value="client" className="space-y-3 mt-4">
              {/* REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH */}
              <Button variant="outline" className="w-full" data-testid="google-signin-button"
                onClick={() => { window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(window.location.origin + "/auth/callback")}`; }}>
                <svg className="h-4 w-4 mr-2" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.4 29.3 35 24 35c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.5 5.1 29.5 3 24 3 12.4 3 3 12.4 3 24s9.4 21 21 21 21-9.4 21-21c0-1.2-.1-2.3-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.5 5.1 29.5 3 24 3 16 3 9.1 7.6 6.3 14.7z"/><path fill="#4CAF50" d="M24 45c5.2 0 10-2 13.6-5.2l-6.3-5.2C29.2 36 26.7 37 24 37c-5.3 0-9.7-2.6-11.3-6.9l-6.5 5C9.1 42.3 16 47 24 45z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.3-2.3 4.3-4.3 5.6l6.3 5.2C41.9 36 45 30.6 45 24c0-1.2-.1-2.3-.4-3.5z"/></svg>
                Continue with Google
              </Button>
              <div className="relative py-1"><div className="border-t"></div><span className="absolute left-1/2 -translate-x-1/2 -top-2 bg-white px-2 text-[11px] text-[hsl(var(--muted-foreground))]">or use mobile OTP</span></div>
              {!otpSent ? (
                <>
                  <div><Label>Your name</Label><Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Priya Sharma" data-testid="otp-name-input" /></div>
                  <div><Label>Mobile number</Label><Input value={mobile} onChange={(e) => setMobile(e.target.value)} placeholder="9999999999" data-testid="otp-mobile-input" /></div>
                  <Button className="w-full" onClick={requestOtp} disabled={busy} data-testid="request-otp-button">Send OTP <ArrowRight className="ml-1 h-4 w-4" /></Button>
                </>
              ) : (
                <>
                  {devOtp && <div className="rounded-md bg-[hsl(var(--info-bg))] text-[hsl(var(--info-fg))] text-xs p-2 text-center">Simulated OTP: <b className="font-mono">{devOtp}</b></div>}
                  <div><Label>Enter OTP</Label><Input value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="6-digit code" data-testid="otp-code-input" /></div>
                  <Button className="w-full" onClick={verifyOtp} disabled={busy} data-testid="verify-otp-button">Verify &amp; continue</Button>
                  <button className="text-xs text-[hsl(var(--muted-foreground))] w-full" onClick={() => setOtpSent(false)}>Change number</button>
                </>
              )}
            </TabsContent>

            <TabsContent value="admin" className="space-y-3 mt-4">
              <div><Label>Email</Label><Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="admin@faizzab.com" data-testid="admin-email-input" /></div>
              <div><Label>Password</Label><Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} data-testid="admin-password-input" /></div>
              {mfaReq && <div><Label>MFA Code</Label><Input value={mfa} onChange={(e) => setMfa(e.target.value)} placeholder="123456" data-testid="admin-mfa-input" /></div>}
              <Button className="w-full" onClick={adminLogin} disabled={busy} data-testid="admin-login-button">{mfaReq ? "Verify MFA" : "Sign in"}</Button>
            </TabsContent>
          </Tabs>
        </Card>
      </div>
    </div>
  );
}
