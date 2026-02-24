import React, { useState } from "react";
import { apiClient } from "../services/apiClient.js";

export default function ResumePage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState(null);
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await apiClient.post("/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setInsights(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to analyze resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>Personalized resume evaluation</h1>
      <p className="muted">
        Upload your latest resume. VidyaMitra will highlight strengths, skill gaps, and recommend targeted courses.
      </p>
      <form onSubmit={onSubmit} className="form">
        <div className="field">
          <label>Resume file (PDF, DOCX, or TXT)</label>
          <input
            type="file"
            accept=".pdf,.doc,.docx,.txt"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button className="btn-primary" type="submit" disabled={!file || loading}>
          {loading ? "Analyzing..." : "Analyze resume"}
        </button>
      </form>

      {insights && (
        <section className="grid-2 mt-lg">
          <div className="card">
            <h3>Summary</h3>
            <p>{insights.summary}</p>
            <h4>Strengths</h4>
            <ul>
              {insights.strengths.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </div>
          <div className="card">
            <h3>Skill gaps & recommendations</h3>
            <ul className="gap-list">
              {insights.gaps.map((gap) => (
                <li key={gap.skill}>
                  <strong>{gap.skill}</strong>
                  <span className="badge">{gap.level}</span>
                  <p className="muted">{gap.recommendation}</p>
                </li>
              ))}
            </ul>
            <h4>Suggested courses</h4>
            <ul>
              {insights.suggested_courses.map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}

