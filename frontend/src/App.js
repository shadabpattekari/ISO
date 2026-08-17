import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { AuthProvider, useAuth } from "@/context/AuthContext";

import Landing from "@/pages/Landing";
import ToolkitDetail from "@/pages/ToolkitDetail";
import Login from "@/pages/Login";
import AuthCallback from "@/pages/AuthCallback";

import ClientDashboard from "@/pages/client/Dashboard";
import OrgProfile from "@/pages/client/OrgProfile";
import Checkout from "@/pages/client/Checkout";
import Onboarding from "@/pages/client/Onboarding";
import Downloads from "@/pages/client/Downloads";
import AdditionalRequirements from "@/pages/client/AdditionalRequirements";
import Invoices from "@/pages/client/Invoices";

import AdminDashboard from "@/pages/admin/AdminDashboard";
import ReviewQueue from "@/pages/admin/ReviewQueue";
import ReviewDetail from "@/pages/admin/ReviewDetail";
import GenerationMonitor from "@/pages/admin/GenerationMonitor";
import Clients from "@/pages/admin/Clients";
import Commerce from "@/pages/admin/Commerce";
import Content from "@/pages/admin/Content";
import AdminAdditional from "@/pages/admin/AdminAdditional";
import AuditLogs from "@/pages/admin/AuditLogs";

const Loading = () => (
  <div className="min-h-screen flex items-center justify-center text-[hsl(var(--muted-foreground))]">Loading…</div>
);

const Guard = ({ role, children }) => {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  if (!user) return <Navigate to="/login" replace />;
  if (role && user.role !== role) return <Navigate to={user.role === "admin" ? "/admin" : "/app"} replace />;
  return children;
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/toolkits/:slug" element={<ToolkitDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/auth/callback" element={<AuthCallback />} />

            {/* Client */}
            <Route path="/app" element={<Guard role="client"><ClientDashboard /></Guard>} />
            <Route path="/app/organization" element={<Guard role="client"><OrgProfile /></Guard>} />
            <Route path="/app/checkout/:slug" element={<Guard role="client"><Checkout /></Guard>} />
            <Route path="/app/onboarding" element={<Guard role="client"><Onboarding /></Guard>} />
            <Route path="/app/onboarding/:slug" element={<Guard role="client"><Onboarding /></Guard>} />
            <Route path="/app/downloads" element={<Guard role="client"><Downloads /></Guard>} />
            <Route path="/app/additional" element={<Guard role="client"><AdditionalRequirements /></Guard>} />
            <Route path="/app/invoices" element={<Guard role="client"><Invoices /></Guard>} />

            {/* Admin */}
            <Route path="/admin" element={<Guard role="admin"><AdminDashboard /></Guard>} />
            <Route path="/admin/reviews" element={<Guard role="admin"><ReviewQueue /></Guard>} />
            <Route path="/admin/reviews/:id" element={<Guard role="admin"><ReviewDetail /></Guard>} />
            <Route path="/admin/generation" element={<Guard role="admin"><GenerationMonitor /></Guard>} />
            <Route path="/admin/clients" element={<Guard role="admin"><Clients /></Guard>} />
            <Route path="/admin/commerce" element={<Guard role="admin"><Commerce /></Guard>} />
            <Route path="/admin/content" element={<Guard role="admin"><Content /></Guard>} />
            <Route path="/admin/additional" element={<Guard role="admin"><AdminAdditional /></Guard>} />
            <Route path="/admin/audit" element={<Guard role="admin"><AuditLogs /></Guard>} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          <Toaster position="top-right" richColors />
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
