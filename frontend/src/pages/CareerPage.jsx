import React, { useState } from "react";
import { apiClient } from "../services/apiClient.js";

export default function CareerPage() {
  const [currentRole, setCurrentRole] = useState("");
  const [targetRole, setTargetRole] = useState("Data Scientist");
  const [experienceYears, setExperienceYears] = useState(2);
  const [interests, setInterests] = useState("communication, analysis, leadership");
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPlan(null);
    try {
      const res = await apiClient.post("/career/roadmap", {
        current_role: currentRole || "Working professional",
        target_role: targetRole,
        experience_years: Number(experienceYears),
        interests: interests.split(",").map((s) => s.trim())
      });
      setPlan(res.data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>Career path recommendation & upskilling planner</h1>
      <p className="muted">
        Describe where you are and where you want to go. VidyaMitra will suggest a roadmap, skills, and certifications.
      </p>
      <form onSubmit={onSubmit} className="form">
        <div className="field">
          <label>Current role</label>
          <input
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            placeholder="e.g. Software Engineer, Business Analyst"
          />
        </div>
        <div className="field">
          <label>Target role</label>
          <input
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            placeholder="e.g. Data Scientist, Product Manager"
          />
        </div>
        <div className="field">
          <label>Years of experience</label>
          <input
            type="number"
            min="0"
            value={experienceYears}
            onChange={(e) => setExperienceYears(e.target.value)}
          />
        </div>
        <div className="field">
          <label>Interests & strengths (comma separated)</label>
          <input
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
          />
        </div>
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? "Generating roadmap..." : "Generate roadmap"}
        </button>
      </form>

      {plan && (
        <section className="mt-lg grid-2">
          <div className="card">
            <h3>Summary</h3>
            <p>{plan.summary}</p>
            <h4>Transferable skills</h4>
            <ul>
              {plan.transferable_skills.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </div>
          <div className="card">
            <h3>Roadmap steps</h3>
            <ol className="roadmap">
              {plan.steps.map((step) => (
                <li key={step.title}>
                  <div className="roadmap-step-header">
                    <strong>{step.title}</strong>
                    <span className="badge">{step.duration_weeks} weeks</span>
                  </div>
                  <p className="muted">{step.description}</p>
                </li>
              ))}
            </ol>
            {plan.recommended_certifications.length > 0 && (
              <>
                <h4>Recommended certifications</h4>
                <ul>
                  {plan.recommended_certifications.map((c) => (
                    <li key={c}>{c}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        </section>
      )}
    </div>
  );
}

