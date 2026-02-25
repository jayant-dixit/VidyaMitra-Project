import React, { useState } from "react";
import { Routes, Route, Navigate, Link } from "react-router-dom";
import { AuthContextProvider, useAuth } from "./auth/AuthContext.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ResumePage from "./pages/ResumePage.jsx";
import InterviewPage from "./pages/InterviewPage.jsx";
import CareerPage from "./pages/CareerPage.jsx";
import TrainingPage from "./pages/TrainingPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import AuthPage from "./pages/AuthPage.jsx";

function PrivateRoute({ children }) {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/auth" replace />;
  }
  return children;
}

function Shell() {
  const { token, logout } = useAuth();
  const [isNavOpen, setIsNavOpen] = useState(false);

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="brand">
          <span className="brand-logo">VM</span>
          <div>
            <div className="brand-title">VidyaMitra</div>
            <div className="brand-subtitle">AI-powered learning & careers</div>
          </div>
        </div>
        <nav className={`nav ${isNavOpen ? "nav-open" : ""}`}>
          {token && (
            <>
              <Link to="/" className="nav-link">
                Dashboard
              </Link>
              <Link to="/resume" className="nav-link">
                Resume Insights
              </Link>
              <Link to="/profile" className="nav-link">
                Profile
              </Link>
              <Link to="/interview" className="nav-link">
                Mock Interview
              </Link>
              <Link to="/career" className="nav-link">
                Career Path
              </Link>
              <Link to="/training" className="nav-link">
                Skills & Training
              </Link>
            </>
          )}
        </nav>
        <div className="header-actions">
          {token ? (
            <button className="btn-secondary" onClick={logout}>
              Logout
            </button>
          ) : (
            <Link to="/auth" className="btn-secondary">
              Login
            </Link>
          )}
          <button
            className="nav-toggle"
            onClick={() => setIsNavOpen((v) => !v)}
            aria-label="Toggle navigation"
          >
            ☰
          </button>
        </div>
      </header>
      <main className="app-main">
        <Routes>
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route path="/auth" element={<AuthPage />} />
          <Route
            path="/resume"
            element={
              <PrivateRoute>
                <ResumePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/interview"
            element={
              <PrivateRoute>
                <InterviewPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/career"
            element={
              <PrivateRoute>
                <CareerPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/training"
            element={
              <PrivateRoute>
                <TrainingPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <ProfilePage />
              </PrivateRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthContextProvider>
      <Shell />
    </AuthContextProvider>
  );
}

