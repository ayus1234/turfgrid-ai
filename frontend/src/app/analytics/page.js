"use client";
import { useState, useEffect } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://turfgrid-ai-15593284604.europe-west1.run.app";

// Recharts color palette
const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

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

  // Dynamic Pie Chart Component
  const CustomPieChart = ({ title, items, labelKey, valueKey }) => {
    return (
      <div className="glass" style={{ padding: 24, flex: "1 1 350px", minHeight: "350px", display: "flex", flexDirection: "column" }}>
        <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: 16 }}>{title}</h3>
        {items.length === 0 ? (
          <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
            No data available
          </p>
        ) : (
          <div style={{ flex: 1, width: "100%" }}>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={items}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={95}
                  paddingAngle={5}
                  dataKey={valueKey}
                  nameKey={labelKey}
                  stroke="none"
                >
                  {items.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: "rgba(15, 23, 42, 0.9)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px", color: "#fff", backdropFilter: "blur(10px)" }}
                  itemStyle={{ color: "#fff", fontWeight: "600" }}
                  formatter={(value, name) => [value, name]}
                />
                <Legend 
                  wrapperStyle={{ fontSize: "0.85rem", paddingTop: "20px" }}
                  layout="horizontal"
                  verticalAlign="bottom"
                  align="center"
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="dashboard">
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
          style={{ background: "var(--bg-glass)", border: "1px solid var(--border-glass)", color: "var(--text-primary)", padding: "8px 16px", borderRadius: 8, fontSize: "1rem", outline: "none", cursor: "pointer" }}
        >
          <option value="Global" style={{ background: "#0f172a", color: "white" }}>🌍 Global View</option>
          <option value="London" style={{ background: "#0f172a", color: "white" }}>🇬🇧 London</option>
          <option value="Birmingham" style={{ background: "#0f172a", color: "white" }}>🇬🇧 Birmingham</option>
          <option value="Manchester" style={{ background: "#0f172a", color: "white" }}>🇬🇧 Manchester</option>
          <option value="New York" style={{ background: "#0f172a", color: "white" }}>🇺🇸 New York</option>
          <option value="Los Angeles" style={{ background: "#0f172a", color: "white" }}>🇺🇸 Los Angeles</option>
          <option value="Mexico City" style={{ background: "#0f172a", color: "white" }}>🇲🇽 Mexico City</option>
        </select>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", padding: 40, color: "var(--text-muted)" }}>
          <div className="skeleton skeleton-card" style={{ height: 350 }}></div>
        </div>
      ) : (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 24 }}>
          <CustomPieChart 
            title="🚨 Operational Alerts by Venue" 
            items={data.alerts_by_venue} 
            labelKey="venue" 
            valueKey="count" 
          />
          <CustomPieChart 
            title="👥 Extra Staff Needed by Business Type" 
            items={data.staffing_impact} 
            labelKey="type" 
            valueKey="extra_staff" 
          />
          <CustomPieChart 
            title="✈️ Popular Fan Destinations" 
            items={data.popular_destinations} 
            labelKey="city" 
            valueKey="count" 
          />
        </div>
      )}
    </div>
  );
}
