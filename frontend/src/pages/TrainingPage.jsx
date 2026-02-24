import React, { useState } from "react";
import { apiClient } from "../services/apiClient.js";

export default function TrainingPage() {
  const [topic, setTopic] = useState("data visualization for beginners");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await apiClient.get("/learning/resources", {
        params: { topic }
      });
      setData(res.data);
    } catch {
      // ignore for now
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>Skills & training planner</h1>
      <p className="muted">
        Search a topic and let VidyaMitra curate YouTube videos, articles, visuals, and news to support your
        upskilling journey.
      </p>
      <form onSubmit={onSubmit} className="form">
        <div className="field">
          <label>What do you want to learn?</label>
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. cloud fundamentals, data visualization, product management basics"
          />
        </div>
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? "Fetching resources..." : "Find learning resources"}
        </button>
      </form>

      {data && (
        <section className="mt-lg grid-2">
          <div className="card">
            <h3>YouTube & video resources</h3>
            <ul>
              {data.videos.map((v) => (
                <li key={v.url}>
                  <a href={v.url} target="_blank" rel="noreferrer">
                    {v.title}
                  </a>
                  <div className="muted">{v.channel}</div>
                </li>
              ))}
            </ul>
            <h3 className="mt-md">Articles & documentation</h3>
            <ul>
              {data.articles.map((a) => (
                <li key={a.url}>
                  <a href={a.url} target="_blank" rel="noreferrer">
                    {a.title}
                  </a>
                  <div className="muted">{a.snippet}</div>
                </li>
              ))}
            </ul>
          </div>
          <div className="card">
            <h3>Visuals & current landscape</h3>
            <div className="grid-3">
              {data.visuals.map((img) => (
                <a
                  key={img.src}
                  href={img.url}
                  target="_blank"
                  rel="noreferrer"
                  style={{ textDecoration: "none" }}
                >
                  <img
                    src={img.src}
                    alt={img.alt || "learning visual"}
                    style={{ width: "100%", borderRadius: "0.6rem", marginBottom: "0.4rem" }}
                  />
                  <div className="muted" style={{ fontSize: "0.75rem" }}>
                    {img.photographer}
                  </div>
                </a>
              ))}
            </div>
            <h3 className="mt-md">News & market snapshot</h3>
            <ul>
              {data.news.map((n) => (
                <li key={n.url}>
                  <a href={n.url} target="_blank" rel="noreferrer">
                    {n.title}
                  </a>
                  <div className="muted" style={{ fontSize: "0.75rem" }}>
                    {n.source} – {n.published_at}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}

