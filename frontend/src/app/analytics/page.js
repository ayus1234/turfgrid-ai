"use client";
import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AnalyticsPage() {
  const [data, setData] = useState({ alerts_by_venue: [], staffing_impact: [], popular_destinations: [] });
  const [selectedCity, setSelectedCity] = useState("Global");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const query = selectedCity !== "Global" ? `?city=${encodeURIComponent(selectedCity)}` : "";
    fetch(`${API_URL}/api/analytics${query}`)
      .then(res => res.json())
      .then(d => {
        if (!d.error) setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [selectedCity]);

  // Simple CSS bar chart component
  const BarChart = ({ title, items, labelKey, valueKey, color }) => {
    const maxVal = Math.max(...items.map(i => i[valueKey]), 1);
    return (
      <div className="glass" style={{ padding: 24, flex: "1 1 300px" }}>
        <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: 16 }}>{title}</h3>
        {items.length === 0 ? <p style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>No data available</p> : null}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {items.map((item, idx) => {
            const width = Math.max((item[valueKey] / maxVal) * 100, 5);
            return (
              <div key={idx}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: 4 }}>
                  <span style={{ color: "var(--text-primary)" }}>{item[labelKey] || "Unknown"}</span>
                  <span style={{ fontWeight: 600 }}>{item[valueKey]}</span>
                </div>
                <div style={{ width: "100%", height: 8, background: "var(--bg-glass)", borderRadius: 4, overflow: "hidden" }}>
                  <div style={{ width: `${width}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.5s ease" }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div style={{ padding: 40, maxWidth: 1200, margin: "0 auto", minHeight: "100vh" }}>
      <h1 className="section-title" style={{ marginBottom: 8 }}>
        <span className="gradient-text">Historical</span> Analytics
      </h1>
      <p className="section-subtitle" style={{ marginBottom: 40 }}>
        Aggregate operational data and trends across venues and businesses.
      </p>

      {/* City Selector */}
      <div style={{ marginBottom: 32, display: "flex", alignItems: "center", gap: 12 }}>
        <span style={{ fontWeight: 600 }}>Filter by City:</span>
        <select 
          value={selectedCity} 
          onChange={(e) => setSelectedCity(e.target.value)}
          style={{ background: "var(--bg-glass)", border: "1px solid var(--border-glass)", color: "var(--text-primary)", padding: "8px 16px", borderRadius: 8, fontSize: "1rem" }}
        >
          <option value="Global">🌍 Global View</option>
          <option value="London">🇬🇧 London</option>
          <option value="Birmingham">🇬🇧 Birmingham</option>
          <option value="Manchester">🇬🇧 Manchester</option>
          <option value="New York">🇺🇸 New York</option>
          <option value="Los Angeles">🇺🇸 Los Angeles</option>
          <option value="Mexico City">🇲🇽 Mexico City</option>
        </select>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", padding: 40, color: "var(--text-muted)" }}>Loading analytics...</div>
      ) : (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 24 }}>
          <BarChart 
            title="🚨 Operational Alerts by Venue" 
            items={data.alerts_by_venue} 
            labelKey="venue" 
            valueKey="count" 
            color="var(--accent-rose)" 
          />
          <BarChart 
            title="👥 Extra Staff Needed by Business Type" 
            items={data.staffing_impact} 
            labelKey="type" 
            valueKey="extra_staff" 
            color="var(--accent-emerald)" 
          />
          <BarChart 
            title="✈️ Popular Fan Destinations" 
            items={data.popular_destinations} 
            labelKey="city" 
            valueKey="count" 
            color="var(--accent-blue)" 
          />
        </div>
      )}
    </div>
  );
}
