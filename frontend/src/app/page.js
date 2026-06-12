"use client";

export default function Home() {
  const events = [
    {
      icon: "⚽",
      title: "FIFA World Cup 2026",
      dates: "June 11 — July 19, 2026",
      desc: "The first 48-team World Cup, co-hosted across 16 cities in the United States, Mexico, and Canada. 104 matches of the beautiful game.",
      tags: ["48 Teams", "16 Venues", "3 Countries"],
      color: "#e11d48",
    },
    {
      icon: "🏏",
      title: "ICC Women's T20 World Cup 2026",
      dates: "June 12 — July 5, 2026",
      desc: "The premier women's T20 cricket tournament across 7 iconic English cricket grounds. 12 teams battle for glory.",
      tags: ["12 Teams", "7 Venues", "England"],
      color: "#2563eb",
    },
  ];

  const features = [
    { icon: "✈️", title: "Fan Portal", desc: "Plan trips, create itineraries, find hotels & transport. Agents save confirmed plans directly to MongoDB.", action: "Saves itineraries" },
    { icon: "📊", title: "Business Protection", desc: "Demand forecasts, staffing plans & preparation checklists. Agents autonomously generate and persist staffing schedules.", action: "Creates staffing plans" },
    { icon: "👥", title: "City Crowd Control", desc: "Real-time congestion predictions, optimal arrival times & alternative routes. Live weather-driven crowd impact analysis.", action: "Live weather + traffic" },
    { icon: "🛡️", title: "Operations Command", desc: "Incident management, volunteer scheduling & resource allocation. Agents issue and persist operational alerts.", action: "Issues live alerts" },
  ];

  return (
    <>
      {/* Hero */}
      <section className="hero">
        <div className="hero-badge">🏙️ Smart City Command Center for Global Sporting Events</div>
        <h1>
          <span className="gradient-text">TurfGrid</span> AI
        </h1>
        <p>
          When 80,000 fans descend on a city, local infrastructure breaks. TurfGrid AI is an <strong>autonomous agent swarm</strong> that protects cities and businesses from the logistical chaos of global sporting surges — demonstrated on{" "}
          <strong>FIFA World Cup 2026</strong> and <strong>ICC Women's T20 World Cup 2026</strong>.
        </p>
        <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", justifyContent: "center", position: "relative", zIndex: 1, animation: "fadeUp 0.8s 0.3s ease both" }}>
          <a href="/chat" className="btn btn-primary">💬 Talk to the Agent</a>
          <a href="/dashboard" className="btn btn-secondary">📡 Operations Dashboard</a>
          <a href="/events" className="btn btn-secondary">🗓️ Explore Events</a>
        </div>
      </section>

      {/* Events */}
      <section className="section">
        <h2 className="section-title">
          Two <span className="gradient-text">Global Events</span>. One Platform.
        </h2>
        <p className="section-subtitle">
          Same agents. Same architecture. Different event data. That's what makes TurfGrid AI a platform, not an app.
        </p>
        <div className="events-grid">
          {events.map((e, i) => (
            <div key={i} className="event-card glass">
              <span className="event-icon">{e.icon}</span>
              <h3>{e.title}</h3>
              <div className="event-dates">{e.dates}</div>
              <p className="event-desc">{e.desc}</p>
              <div className="event-meta">
                {e.tags.map((t, j) => (
                  <span key={j} className="event-tag">{t}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="section">
        <h2 className="section-title">
          4 Autonomous <span className="gradient-text-2">AI Agents</span>
        </h2>
        <p className="section-subtitle">
          Each agent is powered by Gemini 2.5 Flash and backed by MongoDB Atlas. They don't just recommend — they <strong>execute actions</strong> and change system state.
        </p>
        <div className="features-grid">
          {features.map((f, i) => (
            <div key={i} className="feature-card glass">
              <div className="feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
              <div style={{ marginTop: 12, fontSize: "0.8rem", padding: "4px 12px", borderRadius: 100, background: "rgba(16,185,129,0.1)", color: "var(--accent-emerald)", border: "1px solid rgba(16,185,129,0.2)", display: "inline-block", fontWeight: 600 }}>
                ⚡ {f.action}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Architecture */}
      <section className="section" style={{ textAlign: "center" }}>
        <h2 className="section-title">
          How It <span className="gradient-text">Works</span>
        </h2>
        <p className="section-subtitle">
          Ask anything about either event. The orchestrator routes your query to the right specialist agent, which executes tools and saves results to MongoDB.
        </p>
        <div className="glass-strong" style={{ maxWidth: 700, margin: "0 auto", padding: 40, fontFamily: "'JetBrains Mono', monospace", fontSize: "0.85rem", lineHeight: 2, textAlign: "left", color: "var(--text-secondary)" }}>
          <span style={{ color: "var(--accent-blue)" }}>User</span> → "I want to attend India vs Pakistan in London"<br/>
          <span style={{ color: "var(--accent-purple)" }}>Orchestrator</span> → Routes to <span style={{ color: "var(--accent-emerald)" }}>FanLogisticsAgent</span><br/>
          <span style={{ color: "var(--accent-emerald)" }}>FanAgent</span> → Calls <span style={{ color: "var(--accent-amber)" }}>search_matches</span>(team="India")<br/>
          <span style={{ color: "var(--accent-amber)" }}>MongoDB</span> → Returns match at The Oval, June 20<br/>
          <span style={{ color: "var(--accent-emerald)" }}>FanAgent</span> → Calls <span style={{ color: "var(--accent-amber)" }}>create_itinerary</span>(...)<br/>
          <span style={{ color: "var(--accent-blue)" }}>User</span> → "Looks good, save it!"<br/>
          <span style={{ color: "var(--accent-emerald)" }}>FanAgent</span> → Calls <span style={{ color: "#10b981", fontWeight: 700 }}>save_itinerary</span>() → <span style={{ color: "#f59e0b" }}>MongoDB write ✅</span><br/>
          <span style={{ color: "var(--accent-blue)" }}>Response</span> → "✅ Itinerary ITN-3FA92B1C saved! View it on the Dashboard."
        </div>
      </section>

      {/* CTA */}
      <section className="section" style={{ textAlign: "center" }}>
        <h2 className="section-title" style={{ marginBottom: 24 }}>
          Ready to <span className="gradient-text">Experience</span> It?
        </h2>
        <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
          <a href="/chat" className="btn btn-primary" style={{ fontSize: "1.1rem", padding: "16px 40px" }}>
            🚀 Start Chatting with TurfGrid AI
          </a>
          <a href="/dashboard" className="btn btn-secondary" style={{ fontSize: "1.1rem", padding: "16px 40px" }}>
            📡 View Operations Dashboard
          </a>
        </div>
      </section>
    </>
  );
}
