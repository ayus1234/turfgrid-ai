"use client";
import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function EventsPage() {
  const [tab, setTab] = useState("all");
  const [venues, setVenues] = useState([]);
  const [matches, setMatches] = useState([]);
  
  // Modal State
  const [selectedVenue, setSelectedVenue] = useState(null);
  const [weather, setWeather] = useState(null);
  const [weatherLoading, setWeatherLoading] = useState(false);
  
  const [origin, setOrigin] = useState("");
  const [distance, setDistance] = useState(null);
  const [distanceLoading, setDistanceLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/api/venues${tab !== "all" ? `?event_id=${tab}` : ""}`)
      .then((r) => r.json())
      .then((d) => setVenues(d.venues || []))
      .catch(() => setVenues(fallbackVenues(tab)));

    fetch(`${API_URL}/api/matches${tab !== "all" ? `?event_id=${tab}` : ""}`)
      .then((r) => r.json())
      .then((d) => setMatches(d.matches || []))
      .catch(() => setMatches([]));
  }, [tab]);

  const openVenueModal = (venue) => {
    setSelectedVenue(venue);
    setWeather(null);
    setDistance(null);
    setOrigin("");
    
    // Fetch live weather
    setWeatherLoading(true);
    fetch(`${API_URL}/api/weather/${venue._id}`)
      .then((r) => r.json())
      .then((data) => {
        setWeather(data);
        setWeatherLoading(false);
      })
      .catch(() => {
        setWeather({ error: "Failed to load weather" });
        setWeatherLoading(false);
      });
  };

  const calculateDistance = (e) => {
    e.preventDefault();
    if (!origin.trim()) return;
    
    setDistanceLoading(true);
    fetch(`${API_URL}/api/distance?origin=${encodeURIComponent(origin)}&venue_id=${selectedVenue._id}`)
      .then((r) => r.json())
      .then((data) => {
        setDistance(data);
        setDistanceLoading(false);
      })
      .catch(() => {
        setDistance({ error: "Failed to calculate distance" });
        setDistanceLoading(false);
      });
  };

  return (
    <div className="events-page">
      <h1 className="section-title" style={{ marginBottom: 8 }}>
        <span className="gradient-text">Event</span> Explorer
      </h1>
      <p className="section-subtitle" style={{ marginBottom: 32 }}>
        Browse venues and match schedules across both events
      </p>

      <div className="tabs">
        {[
          ["all", "All Events"],
          ["fifa_wc_2026", "⚽ FIFA WC 2026"],
          ["icc_wt20_2026", "🏏 ICC WT20 2026"],
        ].map(([id, label]) => (
          <button
            key={id}
            className={`tab ${tab === id ? "active" : ""}`}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </div>

      <h2
        style={{
          fontSize: "1.4rem",
          fontWeight: 700,
          marginBottom: 20,
          textAlign: "center",
        }}
      >
        🏟️ Venues ({venues.length})
      </h2>

      <div className="events-page-grid">
        {venues.map((v, i) => (
          <div key={i} className="venue-card glass" onClick={() => openVenueModal(v)} style={{ cursor: 'pointer' }}>
            <h4>
              {v.hosts_final ? "🏆 " : ""}
              {v.name}
            </h4>
            <div className="venue-location">
              📍 {v.city}, {v.country}
            </div>
            <div className="venue-capacity">
              👥 Capacity: {(v.capacity || 0).toLocaleString()}
            </div>
            {v.transport && (
              <div className="venue-tags">
                {(v.transport || []).slice(0, 3).map((t, j) => (
                  <span key={j} className="venue-tag">
                    🚇 {t}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {matches.length > 0 && (
        <>
          <h2
            style={{
              fontSize: "1.4rem",
              fontWeight: 700,
              margin: "48px 0 20px",
              textAlign: "center",
            }}
          >
            📅 Key Matches ({matches.length})
          </h2>
          <div className="events-page-grid">
            {matches.map((m, i) => (
              <div key={i} className="venue-card glass">
                <h4>{m.round}</h4>
                <div className="venue-location">
                  {(m.teams || []).join(" vs ")}
                </div>
                <div className="venue-capacity">
                  🏟️ {m.venue_name || m.venue_id} — {m.venue_city || ""}
                </div>
                <div
                  style={{
                    color: "var(--text-muted)",
                    fontSize: "0.8rem",
                    marginTop: 6,
                  }}
                >
                  📅 {new Date(m.date).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" })}
                </div>
                {m.significance && (
                  <div
                    style={{
                      marginTop: 8,
                      fontSize: "0.8rem",
                      color: "var(--accent-amber)",
                    }}
                  >
                    ⭐ {m.significance}
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}

      {/* Venue Detail Modal */}
      {selectedVenue && (
        <div className="modal-overlay" onClick={() => setSelectedVenue(null)}>
          <div className="modal-content glass-strong" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedVenue(null)}>&times;</button>
            
            <h2 style={{ fontSize: "1.8rem", marginBottom: "8px", fontWeight: "800" }}>{selectedVenue.name}</h2>
            <p style={{ color: "var(--accent-blue)", marginBottom: "20px" }}>📍 {selectedVenue.city}, {selectedVenue.country}</p>
            
            <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px", marginBottom: "24px" }}>
              <h3 style={{ fontSize: "1.1rem", marginBottom: "12px", borderBottom: "1px solid var(--border-glass)", paddingBottom: "8px" }}>☁️ Live Weather</h3>
              {weatherLoading ? (
                <p style={{ color: "var(--text-muted)" }}>Fetching from OpenWeatherMap...</p>
              ) : weather ? (
                weather.error ? (
                  <p style={{ color: "var(--accent-rose)" }}>{weather.error}</p>
                ) : (
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                    <div>
                      <p style={{ fontSize: "2rem", fontWeight: "800", color: "var(--text-primary)" }}>{weather.temperature}</p>
                      <p style={{ color: "var(--text-secondary)", textTransform: "capitalize" }}>{weather.condition}</p>
                    </div>
                    <div style={{ alignSelf: "center", fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                      <p>💧 Humidity: {weather.humidity}</p>
                      <p>💨 Wind: {weather.wind_speed}</p>
                    </div>
                    {weather.impact_on_crowd && weather.impact_on_crowd !== "minimal" && (
                      <div style={{ gridColumn: "1 / -1", marginTop: "8px", padding: "8px", background: "rgba(245, 158, 11, 0.1)", border: "1px solid rgba(245, 158, 11, 0.3)", borderRadius: "6px", color: "var(--accent-amber)", fontSize: "0.85rem" }}>
                        ⚠️ <strong>Crowd Impact:</strong> {weather.impact_on_crowd}
                      </div>
                    )}
                  </div>
                )
              ) : null}
            </div>

            <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px" }}>
              <h3 style={{ fontSize: "1.1rem", marginBottom: "12px", borderBottom: "1px solid var(--border-glass)", paddingBottom: "8px" }}>🚗 Live Traffic & Distance</h3>
              <form onSubmit={calculateDistance} style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
                <input 
                  type="text" 
                  value={origin}
                  onChange={(e) => setOrigin(e.target.value)}
                  placeholder="Where are you staying? (e.g. Times Square)" 
                  style={{ flex: 1, padding: "10px 12px", borderRadius: "8px", border: "1px solid var(--border-glass)", background: "var(--bg-secondary)", color: "white", outline: "none" }}
                />
                <button type="submit" disabled={!origin.trim() || distanceLoading} className="btn btn-primary" style={{ padding: "10px 20px" }}>
                  {distanceLoading ? "..." : "Calculate"}
                </button>
              </form>
              
              {distance && !distanceLoading && (
                <div style={{ background: "var(--bg-primary)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border-glass)" }}>
                  {distance.error ? (
                    <p style={{ color: "var(--accent-amber)", fontSize: "0.9rem" }}>{distance.error} (Note: Check Google Maps API Key)</p>
                  ) : distance.note ? (
                    <div>
                      <p style={{ color: "var(--text-secondary)", fontSize: "0.85rem", marginBottom: "8px" }}>{distance.note}</p>
                      <p style={{ fontSize: "1.1rem", fontWeight: "600" }}>Distance: {distance.distance}</p>
                      <p style={{ fontSize: "1.1rem", fontWeight: "600", color: "var(--accent-blue)" }}>Time: {distance.duration}</p>
                    </div>
                  ) : (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                      <div>
                        <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>Distance</p>
                        <p style={{ fontSize: "1.2rem", fontWeight: "700" }}>{distance.distance}</p>
                      </div>
                      <div>
                        <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>Live Driving Time</p>
                        <p style={{ fontSize: "1.2rem", fontWeight: "700", color: "var(--accent-emerald)" }}>{distance.current_duration_with_traffic}</p>
                        {distance.normal_duration !== distance.current_duration_with_traffic && (
                          <p style={{ fontSize: "0.75rem", color: "var(--text-muted)", textDecoration: "line-through" }}>Normally: {distance.normal_duration}</p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

function fallbackVenues(tab) {
  const all = [
    { name: "MetLife Stadium", city: "East Rutherford", country: "United States", capacity: 82500, hosts_final: true, event_id: "fifa_wc_2026", transport: ["NJ Transit", "PATH Train"] },
    { name: "SoFi Stadium", city: "Inglewood", country: "United States", capacity: 70240, hosts_final: false, event_id: "fifa_wc_2026", transport: ["Metro C Line", "LAX Shuttle"] },
    { name: "Estadio Azteca", city: "Mexico City", country: "Mexico", capacity: 87523, hosts_final: false, event_id: "fifa_wc_2026", transport: ["Metro Line 2", "Metrobus"] },
    { name: "Lord's Cricket Ground", city: "London", country: "England", capacity: 30000, hosts_final: true, event_id: "icc_wt20_2026", transport: ["Jubilee Line", "Metropolitan Line"] },
    { name: "The Oval", city: "London", country: "England", capacity: 25500, hosts_final: false, event_id: "icc_wt20_2026", transport: ["Northern Line", "Bus 36"] },
    { name: "Edgbaston", city: "Birmingham", country: "England", capacity: 25000, hosts_final: false, event_id: "icc_wt20_2026", transport: ["Train to Five Ways", "Bus 45"] },
    { name: "Old Trafford Cricket Ground", city: "Manchester", country: "England", capacity: 26000, hosts_final: false, event_id: "icc_wt20_2026", transport: ["Metrolink Tram"] },
  ];
  if (tab === "all") return all;
  return all.filter((v) => v.event_id === tab);
}
