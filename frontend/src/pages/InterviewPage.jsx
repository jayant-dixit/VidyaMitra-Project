import React, { useEffect, useState } from "react";
import { apiClient } from "../services/apiClient.js";

export default function InterviewPage() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    apiClient
      .get("/interview/questions")
      .then((res) => setQuestions(res.data))
      .catch(() => {});
  }, []);

  const onSubmit = async (e) => {
    e.preventDefault();
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
        Answer the questions below. VidyaMitra will evaluate tone, confidence, and accuracy and generate feedback.
      </p>
      <form onSubmit={onSubmit} className="form">
        {questions.map((q) => (
          <div key={q.id} className="field">
            <label>
              {q.question} <span className="badge badge-soft">{q.competency}</span>
            </label>
            <textarea
              rows={4}
              value={answers[q.id] || ""}
              onChange={(e) =>
                setAnswers((prev) => ({
                  ...prev,
                  [q.id]: e.target.value
                }))
              }
              placeholder="Type your answer here..."
            />
          </div>
        ))}
        <button className="btn-primary" type="submit" disabled={loading || !questions.length}>
          {loading ? "Evaluating..." : "Get feedback"}
        </button>
      </form>

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

