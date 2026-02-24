import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext.jsx";

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="page">
      <section className="hero">
        <div>
          <h1>Hello {user?.full_name || "there"}, your AI career co-pilot is ready.</h1>
          <p className="muted">
            Use VidyaMitra to analyse your resume, practice interviews, and plan a personalized upskilling roadmap.
          </p>
          <div className="hero-actions">
            <Link to="/resume" className="btn-primary">
              Analyze my resume
            </Link>
            <Link to="/interview" className="btn-outline">
              Start mock interview
            </Link>
          </div>
        </div>
      </section>
      <section className="grid-3">
        <div className="card">
          <h3>Resume insights</h3>
          <p>Upload your resume and instantly identify gaps in skills, tools, and industry keywords.</p>
        </div>
        <div className="card">
          <h3>Mock interviews</h3>
          <p>Get question sets, answer at your pace, and receive AI-powered feedback on tone and clarity.</p>
        </div>
        <div className="card">
          <h3>Career roadmap</h3>
          <p>Generate a step-by-step plan with courses, projects, and certifications tailored to your goals.</p>
        </div>
      </section>
    </div>
  );
}

