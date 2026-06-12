"use client";
import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://turfgrid-ai-15593284604.europe-west1.run.app";

export default function DashboardPage() {
  const [health, setHealth] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [itineraries, setItineraries] = useState([]);
  const [staffingPlans, setStaffingPlans] = useState([]);
  const [lastRefresh, setLastRefresh] = useState(null);

  const fetchLiveData = () => {
    fetch(`${API_URL}/api/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: "offline", mongodb: "unknown", gemini_configured: false }));

    fetch(`${API_URL}/api/alerts`)
      .then((r) => r.json())
      .then((d) => setAlerts(d.alerts || []))
      .catch(() => {});

    fetch(`${API_URL}/api/itineraries`)
      .then((r) => r.json())
      .then((d) => setItineraries(d.itineraries || []))
      .catch(() => {});

    fetch(`${API_URL}/api/staffing-plans`)
      .then((r) => r.json())
      .then((d) => setStaffingPlans(d.plans || []))
      .catch(() => {});

    setLastRefresh(new Date().toLocaleTimeString());
  };

  useEffect(() => {
    fetchLiveData();
    const interval = setInterval(fetchLiveData, 30000); // Auto-refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const stats = [
    { value: "2", label: "Active Events", color: "var(--accent-blue)" },
    { value: "23", label: "Venues", color: "var(--accent-emerald)" },
    { value: String(alerts.length), label: "Live Alerts", color: "var(--accent-rose)" },
    { value: "4", label: "AI Agents", color: "var(--accent-amber)" },
    { value: String(itineraries.length), label: "Saved Itineraries", color: "var(--accent-purple)" },
    { value: String(staffingPlans.length), label: "Staffing Plans", color: "var(--accent-emerald)" },
  ];

  const severityColor = (s) => {
    if (s === "critical") return "var(--accent-rose)";
    if (s === "high") return "#ef4444";
    if (s === "medium") return "var(--accent-amber)";
    return "var(--accent-emerald)";
  };

  const severityEmoji = (s) => {
    if (s === "critical") return "🔴";
    if (s === "high") return "🟠";
    if (s === "medium") return "🟡";
    return "🟢";
  };

  const agentCapabilities = [
    { name: "Fan Logistics Agent", tools: 9, tasks: "Travel, itineraries, hotels, venues, matches, restaurants, save itineraries", color: "var(--accent-blue)" },
    { name: "Business Readiness Agent", tools: 7, tasks: "Demand forecasts, staffing, inventory, checklists, create staffing plans", color: "var(--accent-emerald)" },
    { name: "Crowd Intelligence Agent", tools: 8, tasks: "Crowd forecasts, congestion, routes, arrivals, live weather", color: "var(--accent-purple)" },
    { name: "Event Operations Agent", tools: 8, tasks: "Incidents, volunteers, resources, security, issue operational alerts", color: "var(--accent-amber)" },
  ];

  return (
    <div className="dashboard">
      <h1 className="section-title" style={{ marginBottom: 8 }}>
        <span className="gradient-text">Operations</span> Command Center
      </h1>
      <p className="section-subtitle" style={{ marginBottom: 40 }}>
        Live autonomous agent activity, alerts, and system state
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
        <span style={{ marginLeft: "auto", color: "var(--text-muted)", fontSize: "0.8rem" }}>
          Last refresh: {lastRefresh || "..."} 
          <button onClick={fetchLiveData} style={{ marginLeft: 8, background: "transparent", border: "1px solid var(--border-glass)", color: "var(--accent-blue)", padding: "4px 12px", borderRadius: 6, cursor: "pointer", fontSize: "0.75rem" }}>↻ Refresh</button>
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

      {/* Live Operational Alerts */}
      <h2 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: 16 }}>
        🚨 Live Operational Alerts
      </h2>
      {alerts.length === 0 ? (
        <div className="glass" style={{ padding: 24, textAlign: "center", marginBottom: 40, color: "var(--text-muted)" }}>
          <p>No active alerts. Ask the AI to analyze a venue's crowd risk to generate alerts.</p>
          <p style={{ fontSize: "0.8rem", marginTop: 8 }}>Example: &quot;Assess crowd risk at MetLife Stadium for the FIFA Final&quot;</p>
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 40 }}>
          {alerts.map((a, i) => (
            <div key={i} className="glass alert-card" style={{ padding: 20, borderLeft: `4px solid ${severityColor(a.severity)}` }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <span style={{ fontWeight: 700 }}>{a.venue_name}</span>
                <span style={{ fontSize: "0.75rem", padding: "2px 8px", borderRadius: 100, background: `${severityColor(a.severity)}22`, color: severityColor(a.severity), fontWeight: 600 }}>
                  {severityEmoji(a.severity)} {a.severity?.toUpperCase()}
                </span>
              </div>
              <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: 4 }}>{a.alert_type}</div>
              <div style={{ fontSize: "0.9rem", marginBottom: 8 }}>{a.message}</div>
              {a.recommended_actions && a.recommended_actions.length > 0 && (
                <div style={{ fontSize: "0.8rem", color: "var(--accent-amber)" }}>
                  Actions: {a.recommended_actions.join(", ")}
                </div>
              )}
              <div style={{ fontSize: "0.7rem", color: "var(--text-muted)", marginTop: 8 }}>
                {a.created_at ? new Date(a.created_at).toLocaleString() : ""}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Saved Itineraries */}
      <h2 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: 16 }}>
        ✈️ Saved Fan Itineraries
      </h2>
      {itineraries.length === 0 ? (
        <div className="glass" style={{ padding: 24, textAlign: "center", marginBottom: 40, color: "var(--text-muted)" }}>
          <p>No saved itineraries yet. Ask the AI to create and save a travel plan.</p>
          <p style={{ fontSize: "0.8rem", marginTop: 8 }}>Example: &quot;Plan a trip from Delhi to London for the ICC Women's T20 World Cup&quot;</p>
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 40 }}>
          {itineraries.map((it, i) => (
            <div key={i} className="glass" style={{ padding: 20, borderLeft: "4px solid var(--accent-blue)" }}>
              <div style={{ fontWeight: 700, marginBottom: 4 }}>{it.user_name}</div>
              <div style={{ fontSize: "0.85rem", color: "var(--accent-blue)", marginBottom: 8 }}>{it.event}</div>
              <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                ✈️ {it.origin} → {it.destination_city}
              </div>
              {it.hotel && <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>🏨 {it.hotel}</div>}
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: 8, alignItems: "center" }}>
                <span style={{ fontSize: "0.75rem", padding: "2px 8px", borderRadius: 100, background: "rgba(16,185,129,0.15)", color: "var(--accent-emerald)", fontWeight: 600 }}>
                  ✅ {it.status}
                </span>
                <span style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>{it._id}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Staffing Plans */}
      <h2 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: 16 }}>
        👥 Active Staffing Plans
      </h2>
      {staffingPlans.length === 0 ? (
        <div className="glass" style={{ padding: 24, textAlign: "center", marginBottom: 40, color: "var(--text-muted)" }}>
          <p>No staffing plans yet. Ask the AI to create a match-day staffing plan for a business.</p>
          <p style={{ fontSize: "0.8rem", marginTop: 8 }}>Example: &quot;I run a cafe near Lord's. Create a staffing plan for the final.&quot;</p>
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 40 }}>
          {staffingPlans.map((sp, i) => (
            <div key={i} className="glass" style={{ padding: 20, borderLeft: "4px solid var(--accent-emerald)" }}>
              <div style={{ fontWeight: 700, marginBottom: 4 }}>{sp.business_name}</div>
              <div style={{ fontSize: "0.85rem", color: "var(--accent-emerald)", marginBottom: 4 }}>{sp.venue_name}</div>
              <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: 8 }}>{sp.match_description}</div>
              <div style={{ fontSize: "0.9rem", fontWeight: 600, color: "var(--text-primary)" }}>
                Staff: {sp.normal_staff} → {sp.recommended_staff} (+{sp.additional_staff_needed || 0})
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: 8, alignItems: "center" }}>
                <span style={{ fontSize: "0.75rem", padding: "2px 8px", borderRadius: 100, background: "rgba(16,185,129,0.15)", color: "var(--accent-emerald)", fontWeight: 600 }}>
                  🟢 {sp.status}
                </span>
                <span style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>{sp._id}</span>
              </div>
            </div>
          ))}
        </div>
      )}

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
          {["Gemini 2.5 Flash", "Google ADK 2.0", "MongoDB Atlas", "FastAPI", "Next.js", "Groq Llama-3 (Failover)"].map((t, i) => (
            <span key={i} className="event-tag">{t}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
