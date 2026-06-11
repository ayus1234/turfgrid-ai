"use client";
import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function DashboardPage() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/api/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: "offline", mongodb: "unknown", gemini_configured: false }));
  }, []);

  const stats = [
    { value: "2", label: "Active Events", color: "var(--accent-blue)" },
    { value: "23", label: "Venues", color: "var(--accent-emerald)" },
    { value: "18", label: "Key Matches", color: "var(--accent-purple)" },
    { value: "4", label: "AI Agents", color: "var(--accent-amber)" },
    { value: "137", label: "Total Matches", color: "var(--accent-rose)" },
    { value: "60", label: "Teams", color: "var(--accent-blue)" },
  ];

  const crowdAlerts = [
    { venue: "MetLife Stadium", match: "FIFA Final", level: "🔴 Extreme", attendance: "82,500 / 82,500", arrival: "4 hours early" },
    { venue: "The Oval", match: "India vs Pakistan", level: "🔴 Extreme", attendance: "25,500 / 25,500", arrival: "3 hours early" },
    { venue: "Lord's", match: "India vs England", level: "🟠 Very High", attendance: "30,000 / 30,000", arrival: "2 hours early" },
    { venue: "Estadio Azteca", match: "Opening Match", level: "🔴 Extreme", attendance: "87,000 / 87,523", arrival: "4 hours early" },
  ];

  const agentCapabilities = [
    { name: "Fan Logistics Agent", tools: 6, tasks: "Travel, itineraries, hotels, venues, matches, restaurants", color: "var(--accent-blue)" },
    { name: "Business Readiness Agent", tools: 5, tasks: "Demand forecasts, staffing, inventory, checklists, venues", color: "var(--accent-emerald)" },
    { name: "Crowd Intelligence Agent", tools: 6, tasks: "Crowd forecasts, congestion, routes, arrivals, venues, matches", color: "var(--accent-purple)" },
    { name: "Event Operations Agent", tools: 6, tasks: "Incidents, volunteers, resources, security, venues, matches", color: "var(--accent-amber)" },
  ];

  return (
    <div className="dashboard">
      <h1 className="section-title" style={{ marginBottom: 8 }}>
        <span className="gradient-text">Intelligence</span> Dashboard
      </h1>
      <p className="section-subtitle" style={{ marginBottom: 40 }}>
        Platform overview and real-time crowd intelligence
      </p>

      {/* System Status */}
      <div className="glass-strong" style={{ padding: 20, marginBottom: 24, display: "flex", gap: 24, flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ fontWeight: 700 }}>System Status</span>
        <span style={{ color: health?.status === "healthy" ? "var(--accent-emerald)" : "var(--accent-rose)" }}>
          ● {health?.status === "healthy" ? "Online" : "Connecting..."}
        </span>
        <span style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          MongoDB: {health?.mongodb || "..."} | Gemini: {health?.gemini_configured ? "✅" : "❌"}
        </span>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {stats.map((s, i) => (
          <div key={i} className="stat-card glass">
            <div className="stat-value" style={{ color: s.color }}>{s.value}</div>
            <div className="stat-label">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Crowd Alerts */}
      <h2 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: 16 }}>
        ⚠️ Crowd Alerts
      </h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 40 }}>
        {crowdAlerts.map((a, i) => (
          <div key={i} className="glass" style={{ padding: 20 }}>
            <div style={{ fontWeight: 700, marginBottom: 4 }}>{a.venue}</div>
            <div style={{ color: "var(--text-secondary)", fontSize: "0.85rem", marginBottom: 8 }}>{a.match}</div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem" }}>
              <span>{a.level}</span>
              <span style={{ color: "var(--text-muted)" }}>{a.attendance}</span>
            </div>
            <div style={{ marginTop: 8, fontSize: "0.8rem", color: "var(--accent-amber)" }}>
              🕐 Arrive {a.arrival}
            </div>
          </div>
        ))}
      </div>

      {/* Agent Capabilities */}
      <h2 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: 16 }}>
        🤖 Agent Team
      </h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16 }}>
        {agentCapabilities.map((a, i) => (
          <div key={i} className="glass" style={{ padding: 20 }}>
            <div style={{ fontWeight: 700, marginBottom: 4, color: a.color }}>{a.name}</div>
            <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: 8 }}>
              {a.tools} tools available
            </div>
            <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{a.tasks}</div>
          </div>
        ))}
      </div>

      {/* Tech Stack */}
      <div className="glass-strong" style={{ padding: 32, marginTop: 40, textAlign: "center" }}>
        <h3 style={{ marginBottom: 16, fontWeight: 700 }}>Tech Stack</h3>
        <div style={{ display: "flex", gap: 24, justifyContent: "center", flexWrap: "wrap", color: "var(--text-secondary)", fontSize: "0.9rem" }}>
          {["Gemini 2.0 Flash", "Google ADK 2.0", "MongoDB MCP", "FastAPI", "Next.js", "MongoDB Atlas"].map((t, i) => (
            <span key={i} className="event-tag">{t}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
