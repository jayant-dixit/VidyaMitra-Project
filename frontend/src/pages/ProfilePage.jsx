import React, { useEffect, useState } from "react";
import { apiClient } from "../services/apiClient.js";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [summary, setSummary] = useState("");
  const [strengths, setStrengths] = useState("");
  const [interests, setInterests] = useState("");

  useEffect(() => {
    apiClient
      .get("/profile/me")
      .then((res) => {
        setProfile(res.data);
        setSummary(res.data.profile_summary || "");
        setStrengths((res.data.strengths || []).join(", "));
        setInterests((res.data.interests || []).join(", "));
      })
      .finally(() => setLoading(false));
  }, []);

  const onSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await apiClient.patch("/profile/me", {
        profile_summary: summary,
        strengths: strengths
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        interests: interests
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean)
      });
      setProfile(res.data);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="page">
        <p className="muted">Loading profile...</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="page">
        <h1>Profile</h1>
        <p className="muted">No profile data available yet. Upload a resume to get started.</p>
      </div>
    );
  }

  return (
    <div className="page">
      <h1>Your profile</h1>
      <p className="muted">
        This summary and your strengths are used to personalize resume analysis, career paths, and mock interviews.
      </p>

      <section className="grid-2 mt-lg">
        <div className="card">
          <h3>Account</h3>
          <p>
            <strong>Name:</strong> {profile.full_name}
          </p>
          <p>
            <strong>Email:</strong> {profile.email}
          </p>
          <p>
            <strong>Latest resume:</strong> {profile.resume_filename || "Not uploaded yet"}
          </p>
        </div>

        <div className="card">
          <h3>Profile summary & preferences</h3>
          <form onSubmit={onSave} className="form">
            <div className="field">
              <label>Profile summary (from your resume, editable)</label>
              <textarea
                rows={4}
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="Short summary of your experience, goals, and domains."
              />
            </div>
            <div className="field">
              <label>Strengths (comma separated)</label>
              <input
                value={strengths}
                onChange={(e) => setStrengths(e.target.value)}
                placeholder="e.g. Python, stakeholder communication, analytics"
              />
            </div>
            <div className="field">
              <label>Interests (comma separated)</label>
              <input
                value={interests}
                onChange={(e) => setInterests(e.target.value)}
                placeholder="e.g. data science, product strategy"
              />
            </div>
            <button className="btn-primary" type="submit" disabled={saving}>
              {saving ? "Saving..." : "Save profile"}
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}

