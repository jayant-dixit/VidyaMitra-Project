import React, { useState } from "react";
import { apiClient } from "../services/apiClient.js";

export default function InterviewPage() {
  const [questions, setQuestions] = useState([]);
  const [jobRole, setJobRole] = useState("Data Scientist");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [started, setStarted] = useState(false);
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchQuestions = async () => {
    setLoading(true);
    setFeedback(null);
    try {
      const res = await apiClient.get("/interview/questions", {
        params: { target_role: jobRole || "Data Scientist" }
      });
      setQuestions(res.data);
      setCurrentIndex(0);
      setStarted(true);
      setAnswers({});
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!questions.length) return;
    setLoading(true);
    setFeedback(null);
    try {
      const payload = questions.map((q) => ({
        question_id: q.id,
        question: q.question,
        answer: answers[q.id] || ""
      }));
      const res = await apiClient.post("/interview/feedback", payload);
      setFeedback(res.data);
    } catch {
      // ignore for now
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>AI-driven mock interview</h1>
      <p className="muted">
        Enter a target role, then answer one question at a time. VidyaMitra will evaluate tone, confidence, and accuracy
        and generate structured feedback.
      </p>

      <div className="form">
        <div className="field">
          <label>Target role for this mock interview</label>
          <input
            value={jobRole}
            onChange={(e) => setJobRole(e.target.value)}
            placeholder="e.g. Data Scientist, Product Manager"
          />
        </div>
        <button className="btn-primary" type="button" onClick={fetchQuestions} disabled={loading}>
          {loading ? "Preparing interview..." : "Start interview"}
        </button>
      </div>

      {started && questions[currentIndex] && (
        <form onSubmit={onSubmit} className="form mt-lg">
          <div className="card">
            <h3>
              Question {currentIndex + 1} of {questions.length}
            </h3>
            <p>
              {questions[currentIndex].question}{" "}
              <span className="badge badge-soft">{questions[currentIndex].competency}</span>
            </p>
            <div className="field">
              <label>Your answer</label>
              <textarea
                rows={5}
                value={answers[questions[currentIndex].id] || ""}
                onChange={(e) =>
                  setAnswers((prev) => ({
                    ...prev,
                    [questions[currentIndex].id]: e.target.value
                  }))
                }
                placeholder="Type your answer here or click Skip to move on."
              />
            </div>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => {
                  setCurrentIndex((idx) => Math.min(idx + 1, questions.length - 1));
                }}
              >
                Skip & Next
              </button>
              {currentIndex < questions.length - 1 ? (
                <button
                  type="button"
                  className="btn-primary"
                  onClick={() => {
                    setCurrentIndex((idx) => Math.min(idx + 1, questions.length - 1));
                  }}
                >
                  Save & Next
                </button>
              ) : (
                <button className="btn-primary" type="submit" disabled={loading}>
                  {loading ? "Evaluating..." : "Finish & get feedback"}
                </button>
              )}
            </div>
          </div>
        </form>
      )}

      {feedback && (
        <section className="mt-lg">
          <div className="card">
            <h3>Overall summary</h3>
            <p>{feedback.overall_summary}</p>
          </div>
          <div className="grid-3 mt-md">
            {feedback.feedback.map((f) => (
              <div className="card" key={f.question_id}>
                <h4>Question {f.question_id}</h4>
                <p className="muted">{f.feedback}</p>
                <div className="score-row">
                  <span>Tone: {f.tone_score}/100</span>
                  <span>Confidence: {f.confidence_score}/100</span>
                  <span>Accuracy: {f.accuracy_score}/100</span>
                </div>
                <ul>
                  {f.suggestions.map((s, idx) => (
                    <li key={idx}>{s}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

