"use client";
import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://turfgrid-ai-15593284604.europe-west1.run.app";

const TICKET_URLS = {
  fifa_wc_2026: "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/tickets",
  icc_wt20_2026: "https://tickets.womens.t20worldcup.com/selection/event/date?lang=en&productId=10228814154367",
};

export default function EventsPage() {
  const [tab, setTab] = useState("all");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const eventParam = params.get("event");
      if (eventParam && (eventParam === "fifa_wc_2026" || eventParam === "icc_wt20_2026")) {
        setTab(eventParam);
      }
    }
  }, []);

  const [venues, setVenues] = useState([]);
  const [matches, setMatches] = useState([]);

  // Venue Modal State
  const [selectedVenue, setSelectedVenue] = useState(null);
  const [weather, setWeather] = useState(null);
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [origin, setOrigin] = useState("");
  const [distance, setDistance] = useState(null);
  const [distanceLoading, setDistanceLoading] = useState(false);
  const [venueTab, setVenueTab] = useState("weather");
  const [venueFlightSource, setVenueFlightSource] = useState("");
  const [venueFlights, setVenueFlights] = useState(null);
  const [venueFlightsLoading, setVenueFlightsLoading] = useState(false);

  // Match Detail Modal State
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [matchTab, setMatchTab] = useState("tickets");
  const [matchWeather, setMatchWeather] = useState(null);
  const [matchWeatherLoading, setMatchWeatherLoading] = useState(false);
  const [matchOrigin, setMatchOrigin] = useState("");
  const [matchDistance, setMatchDistance] = useState(null);
  const [matchDistanceLoading, setMatchDistanceLoading] = useState(false);

  // Hotels State
  const [hotels, setHotels] = useState([]);
  const [hotelsLoading, setHotelsLoading] = useState(false);

  // Flights State
  const [flightSource, setFlightSource] = useState("");
  const [flightDate, setFlightDate] = useState("2026-06-15");
  const [flights, setFlights] = useState(null);
  const [flightsLoading, setFlightsLoading] = useState(false);

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
    setVenueTab("weather");
    setWeather(null);
    setDistance(null);
    setOrigin("");
    setVenueFlightSource("");
    setVenueFlights(null);
    setWeatherLoading(true);
    fetch(`${API_URL}/api/weather/${venue._id}`)
      .then((r) => r.json())
      .then((data) => { setWeather(data); setWeatherLoading(false); })
      .catch(() => { setWeather({ error: "Failed to load weather" }); setWeatherLoading(false); });
  };

  const calculateDistance = (e) => {
    e.preventDefault();
    if (!origin.trim()) return;
    setDistanceLoading(true);
    fetch(`${API_URL}/api/distance?origin=${encodeURIComponent(origin)}&venue_id=${selectedVenue._id}`)
      .then((r) => r.json())
      .then((data) => { setDistance(data); setDistanceLoading(false); })
      .catch(() => { setDistance({ error: "Failed to calculate distance" }); setDistanceLoading(false); });
  };

  const handleVenueTabChange = (t) => {
    setVenueTab(t);
    if (t === "hotels" && hotels.length === 0 && !hotelsLoading) loadHotels(selectedVenue._id);
  };

  const searchVenueFlights = (e) => {
    e.preventDefault();
    if (!venueFlightSource.trim()) return;
    setVenueFlightsLoading(true);
    fetch(`${API_URL}/api/booking/flights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: venueFlightSource, venue_id: selectedVenue._id, departure_date: "2026-06-11" }),
    })
      .then((r) => r.json())
      .then((d) => { setVenueFlights(d); setVenueFlightsLoading(false); })
      .catch(() => { setVenueFlights({ error: "Failed to search flights" }); setVenueFlightsLoading(false); });
  };

  // ─── Match Modal Handlers ──────────────────────────────────────
  const openMatchModal = (match) => {
    setSelectedMatch(match);
    setMatchTab("tickets");
    setHotels([]);
    setFlights(null);
    setMatchWeather(null);
    setMatchDistance(null);
    setMatchOrigin("");
    setFlightSource("");
    setFlightDate(match.date ? match.date.split("T")[0] : "2026-06-15");
  };

  const loadHotels = (venueId) => {
    setHotelsLoading(true);
    fetch(`${API_URL}/api/booking/hotels/${venueId}`)
      .then((r) => r.json())
      .then((d) => { setHotels(d.hotels || []); setHotelsLoading(false); })
      .catch(() => { setHotels([]); setHotelsLoading(false); });
  };

  const loadMatchWeather = (venueId) => {
    setMatchWeatherLoading(true);
    fetch(`${API_URL}/api/weather/${venueId}`)
      .then((r) => r.json())
      .then((d) => { setMatchWeather(d); setMatchWeatherLoading(false); })
      .catch(() => { setMatchWeather({ error: "Failed" }); setMatchWeatherLoading(false); });
  };

  const searchFlights = (e) => {
    e.preventDefault();
    if (!flightSource.trim()) return;
    const venueId = selectedMatch.venue_id;
    setFlightsLoading(true);
    fetch(`${API_URL}/api/booking/flights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: flightSource, venue_id: venueId, departure_date: flightDate }),
    })
      .then((r) => r.json())
      .then((d) => { setFlights(d); setFlightsLoading(false); })
      .catch(() => { setFlights({ error: "Failed to search flights" }); setFlightsLoading(false); });
  };

  const calcMatchDistance = (e) => {
    e.preventDefault();
    if (!matchOrigin.trim()) return;
    setMatchDistanceLoading(true);
    fetch(`${API_URL}/api/distance?origin=${encodeURIComponent(matchOrigin)}&venue_id=${selectedMatch.venue_id}`)
      .then((r) => r.json())
      .then((d) => { setMatchDistance(d); setMatchDistanceLoading(false); })
      .catch(() => { setMatchDistance({ error: "Failed" }); setMatchDistanceLoading(false); });
  };

  const handleMatchTabChange = (t) => {
    setMatchTab(t);
    if (t === "hotels" && hotels.length === 0 && !hotelsLoading) loadHotels(selectedMatch.venue_id);
    if (t === "weather" && !matchWeather && !matchWeatherLoading) loadMatchWeather(selectedMatch.venue_id);
  };

  const renderStars = (rating) => "⭐".repeat(Math.round(rating));

  return (
    <div className="events-page">
      <h1 className="section-title" style={{ marginBottom: 8 }}>
        <span className="gradient-text">Event</span> Explorer
      </h1>
      <p className="section-subtitle" style={{ marginBottom: 32 }}>
        Browse venues and match schedules across both events
      </p>

      <div className="tabs">
        {[["all", "All Events"], ["fifa_wc_2026", "⚽ FIFA WC 2026"], ["icc_wt20_2026", "🏏 ICC WT20 2026"]].map(([id, label]) => (
          <button key={id} className={`tab ${tab === id ? "active" : ""}`} onClick={() => setTab(id)}>{label}</button>
        ))}
      </div>

      <h2 style={{ fontSize: "1.4rem", fontWeight: 700, marginBottom: 20, textAlign: "center" }}>
        🏟️ Venues ({venues.length})
      </h2>

      <div className="events-page-grid">
        {venues.map((v, i) => (
          <div key={i} className="venue-card glass" onClick={() => openVenueModal(v)} style={{ cursor: "pointer" }}>
            <h4>{v.hosts_final ? "🏆 " : ""}{v.name}</h4>
            <div className="venue-location">📍 {v.city}, {v.country}</div>
            <div className="venue-capacity">👥 Capacity: {(v.capacity || 0).toLocaleString()}</div>
            {v.transport && (
              <div className="venue-tags">
                {(v.transport || []).slice(0, 3).map((t, j) => (
                  <span key={j} className="venue-tag">🚇 {t}</span>
                ))}
              </div>
            )}
            
            <div style={{ marginTop: 12, marginBottom: 8, fontSize: "0.85rem", color: "var(--text-secondary)" }}>
              {matches.filter(m => m.venue_id === v._id).length > 0 ? (
                <span>📅 Hosting {matches.filter(m => m.venue_id === v._id).length} Matches</span>
              ) : <span>📅 No matches scheduled</span>}
            </div>

            <div className="booking-actions" style={{ marginTop: 12 }}>
              <span className="booking-btn booking-btn-ticket" onClick={(e) => { e.stopPropagation(); openVenueModal(v); setTimeout(() => handleVenueTabChange("matches"), 100); }}>🎫 Tickets</span>
              <span className="booking-btn booking-btn-hotel" onClick={(e) => { e.stopPropagation(); openVenueModal(v); setTimeout(() => handleVenueTabChange("hotels"), 100); }}>🏨 Hotels</span>
              <span className="booking-btn booking-btn-flight" onClick={(e) => { e.stopPropagation(); openVenueModal(v); setTimeout(() => handleVenueTabChange("flights"), 100); }}>✈️ Flights</span>
            </div>
          </div>
        ))}
      </div>

      {matches.length > 0 && (
        <>
          <h2 style={{ fontSize: "1.4rem", fontWeight: 700, margin: "48px 0 20px", textAlign: "center" }}>
            📅 Key Matches ({matches.length})
          </h2>
          <div className="events-page-grid">
            {matches.map((m, i) => (
              <div key={i} className="venue-card glass" style={{ cursor: "pointer" }} onClick={() => openMatchModal(m)}>
                <h4>{m.round}</h4>
                <div className="venue-location">{(m.teams || []).join(" vs ")}</div>
                <div className="venue-capacity">🏟️ {m.venue_name || m.venue_id} — {m.venue_city || ""}</div>
                <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", marginTop: 6 }}>
                  📅 {new Date(m.date).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" })}
                </div>
                {m.significance && (
                  <div style={{ marginTop: 8, fontSize: "0.8rem", color: "var(--accent-amber)" }}>⭐ {m.significance}</div>
                )}
                <div className="booking-actions">
                  <span className="booking-btn booking-btn-ticket" onClick={(e) => { e.stopPropagation(); window.open(TICKET_URLS[m.event_id], "_blank"); }}>🎫 Book Tickets</span>
                  <span className="booking-btn booking-btn-hotel" onClick={(e) => { e.stopPropagation(); openMatchModal(m); setTimeout(() => handleMatchTabChange("hotels"), 100); }}>🏨 Hotels</span>
                  <span className="booking-btn booking-btn-flight" onClick={(e) => { e.stopPropagation(); openMatchModal(m); setTimeout(() => handleMatchTabChange("flights"), 100); }}>✈️ Flights</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* ─── Venue Detail Modal ─── */}
      {selectedVenue && (
        <div className="modal-overlay" onClick={() => setSelectedVenue(null)}>
          <div className="modal-content glass-strong" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedVenue(null)}>&times;</button>
            <h2 style={{ fontSize: "1.8rem", marginBottom: "8px", fontWeight: "800" }}>{selectedVenue.name}</h2>
            <p style={{ color: "var(--accent-blue)", marginBottom: "20px" }}>📍 {selectedVenue.city}, {selectedVenue.country}</p>

            <div className="modal-tabs">
              <button className={`modal-tab ${venueTab === "matches" ? "active" : ""}`} onClick={() => handleVenueTabChange("matches")}>📅 Matches</button>
              <button className={`modal-tab ${venueTab === "weather" ? "active" : ""}`} onClick={() => handleVenueTabChange("weather")}>☁️ Weather</button>
              <button className={`modal-tab ${venueTab === "distance" ? "active" : ""}`} onClick={() => handleVenueTabChange("distance")}>🚗 Traffic</button>
              <button className={`modal-tab ${venueTab === "hotels" ? "active" : ""}`} onClick={() => handleVenueTabChange("hotels")}>🏨 Hotels</button>
              <button className={`modal-tab ${venueTab === "flights" ? "active" : ""}`} onClick={() => handleVenueTabChange("flights")}>✈️ Flights</button>
            </div>

            {venueTab === "matches" && (
            <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px", marginBottom: "24px" }}>
              <h3 style={{ fontSize: "1.1rem", marginBottom: "12px", borderBottom: "1px solid var(--border-glass)", paddingBottom: "8px" }}>📅 Matches at {selectedVenue.name}</h3>
              {matches.filter(m => m.venue_id === selectedVenue._id).length > 0 ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {matches.filter(m => m.venue_id === selectedVenue._id).map((m, idx) => (
                    <div key={idx} style={{ background: "var(--bg-secondary)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border-glass)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "4px" }}>{m.round} • {new Date(m.date).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" })}</div>
                        <div style={{ fontWeight: 700 }}>{(m.teams || []).join(" vs ")}</div>
                        {m.significance && <div style={{ fontSize: "0.8rem", color: "var(--accent-amber)", marginTop: "4px" }}>⭐ {m.significance}</div>}
                      </div>
                      <a href={TICKET_URLS[m.event_id]} target="_blank" rel="noopener noreferrer" className="btn-ticket" style={{ padding: "8px 16px", fontSize: "0.85rem" }}>
                        🎫 Book Tickets
                      </a>
                    </div>
                  ))}
                </div>
              ) : (
                <p style={{ color: "var(--text-muted)" }}>No matches scheduled here.</p>
              )}
            </div>
            )}

            {venueTab === "weather" && (
            <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px", marginBottom: "24px" }}>
              <h3 style={{ fontSize: "1.1rem", marginBottom: "12px", borderBottom: "1px solid var(--border-glass)", paddingBottom: "8px" }}>☁️ Live Weather</h3>
              {weatherLoading ? (
                <p style={{ color: "var(--text-muted)" }}>Fetching from OpenWeatherMap...</p>
              ) : weather ? (
                weather.error ? <p style={{ color: "var(--accent-rose)" }}>{weather.error}</p> : (
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                    <div>
                      <p style={{ fontSize: "2rem", fontWeight: "800" }}>{weather.temperature}</p>
                      <p style={{ color: "var(--text-secondary)", textTransform: "capitalize" }}>{weather.condition}</p>
                    </div>
                    <div style={{ alignSelf: "center", fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                      <p>💧 Humidity: {weather.humidity}</p>
                      <p>💨 Wind: {weather.wind_speed}</p>
                    </div>
                    {weather.impact_on_crowd && weather.impact_on_crowd !== "minimal" && (
                      <div style={{ gridColumn: "1 / -1", marginTop: "8px", padding: "8px", background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.3)", borderRadius: "6px", color: "var(--accent-amber)", fontSize: "0.85rem" }}>
                        ⚠️ <strong>Crowd Impact:</strong> {weather.impact_on_crowd}
                      </div>
                    )}
                  </div>
                )
              ) : null}
            </div>
            )}

            {venueTab === "distance" && (
            <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px" }}>
              <h3 style={{ fontSize: "1.1rem", marginBottom: "12px", borderBottom: "1px solid var(--border-glass)", paddingBottom: "8px" }}>🚗 Live Traffic & Distance</h3>
              <form onSubmit={calculateDistance} style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
                <input type="text" value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="Where are you staying? (e.g. Times Square)"
                  style={{ flex: 1, padding: "10px 12px", borderRadius: "8px", border: "1px solid var(--border-glass)", background: "var(--bg-secondary)", color: "white", outline: "none" }} />
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
            )}

            {venueTab === "hotels" && (
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px" }}>
                <h3 style={{ fontSize: "1.1rem", marginBottom: "12px" }}>🏨 Nearby Hotels</h3>
                {hotelsLoading ? <p style={{ color: "var(--text-muted)" }}>Finding best hotels...</p> : hotels.length > 0 ? (
                  <div className="hotels-grid">
                    {hotels.map((h, i) => (
                      <div key={i} className="hotel-card">
                        <div className="hotel-name">{h.hotel_name}</div>
                        <div className="hotel-stars">{renderStars(h.rating)} {h.rating}</div>
                        <div className="hotel-meta">
                          <span className="hotel-price">{h.price}</span>
                          <span className="hotel-distance">📍 {h.distance_km} km</span>
                        </div>
                        <a href={h.booking_url} target="_blank" rel="noopener noreferrer" className="hotel-book-btn">Book Now →</a>
                      </div>
                    ))}
                  </div>
                ) : <p style={{ color: "var(--text-muted)" }}>No hotels found. Try again later.</p>}
              </div>
            )}

            {venueTab === "flights" && (
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px" }}>
                <h3 style={{ fontSize: "1.1rem", marginBottom: "12px" }}>✈️ Flights to Venue</h3>
                <form onSubmit={searchVenueFlights} className="flight-search-row">
                  <input type="text" value={venueFlightSource} onChange={(e) => setVenueFlightSource(e.target.value)} placeholder="Origin City (e.g. Mumbai)" className="flight-input" />
                  <button type="submit" disabled={!venueFlightSource.trim() || venueFlightsLoading} className="flight-search-btn">
                    {venueFlightsLoading ? "Searching..." : "🔍 Search"}
                  </button>
                </form>
                {venueFlights && !venueFlightsLoading && (
                  <>
                    <div className="flights-list">
                      {(venueFlights.flights || []).map((f, i) => (
                        <div key={i} className="flight-card">
                          <div>
                            <div className="flight-airline">✈️ {f.airline}</div>
                            <div className="flight-details">
                              <span>⏱️ {f.duration}</span>
                              <span>&nbsp;•&nbsp;</span>
                              <span className={`stops-badge ${f.stops === 0 ? "stops-direct" : "stops-one"}`}>
                                {f.stops === 0 ? "Direct" : `${f.stops} Stop`}
                              </span>
                            </div>
                          </div>
                          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                            <span className="flight-price">{f.price}</span>
                            <a href={f.booking_url} target="_blank" rel="noopener noreferrer" className="flight-book-btn">Book →</a>
                          </div>
                        </div>
                      ))}
                    </div>
                    {venueFlights.last_mile && (
                      <div className="last-mile">
                        <div className="last-mile-title">🚕 Last Mile: Airport → Venue</div>
                        <div className="last-mile-desc">
                          {venueFlights.last_mile.description} <br/> <span className="last-mile-cost">Est. {venueFlights.last_mile.estimate}</span>
                        </div>
                      </div>
                    )}
                  </>
                )}
                {venueFlights && venueFlights.error && <p style={{ color: "var(--accent-rose)" }}>{venueFlights.error}</p>}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ─── Match Detail Modal ─── */}
      {selectedMatch && (
        <div className="modal-overlay" onClick={() => setSelectedMatch(null)}>
          <div className="modal-content modal-wide glass-strong" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedMatch(null)}>&times;</button>

            <div className="modal-header">
              <h2>{(selectedMatch.teams || []).join(" vs ")}</h2>
              <div className="modal-sub">🏟️ {selectedMatch.venue_name || selectedMatch.venue_id} — {selectedMatch.venue_city || ""}</div>
              <div className="modal-date">📅 {new Date(selectedMatch.date).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" })}</div>
              {selectedMatch.significance && <div style={{ marginTop: 4, fontSize: "0.85rem", color: "var(--accent-amber)" }}>⭐ {selectedMatch.significance}</div>}
            </div>

            <div className="modal-tabs">
              {[["tickets", "🎫 Tickets"], ["hotels", "🏨 Hotels"], ["flights", "✈️ Flights"], ["weather", "☁️ Weather"], ["distance", "🚗 Distance"]].map(([id, label]) => (
                <button key={id} className={`modal-tab ${matchTab === id ? "active" : ""}`} onClick={() => handleMatchTabChange(id)}>{label}</button>
              ))}
            </div>

            {/* Tickets Tab */}
            {matchTab === "tickets" && (
              <div className="ticket-cta">
                <div className="ticket-icon">🎫</div>
                <h3 style={{ fontSize: "1.2rem", fontWeight: 700, marginBottom: 8 }}>{selectedMatch.round}</h3>
                <p>Get official match tickets from the tournament organizer</p>
                <a href={TICKET_URLS[selectedMatch.event_id]} target="_blank" rel="noopener noreferrer" className="btn-ticket">
                  🎫 Book Official Tickets →
                </a>
              </div>
            )}

            {/* Hotels Tab */}
            {matchTab === "hotels" && (
              <div>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: 16 }}>🏨 Hotels near {selectedMatch.venue_name || selectedMatch.venue_id}</h3>
                {hotelsLoading ? (
                  <div><div className="skeleton skeleton-card"></div><div className="skeleton skeleton-card"></div></div>
                ) : hotels.length > 0 ? (
                  <div className="hotels-grid">
                    {hotels.map((h, i) => (
                      <div key={i} className="hotel-card">
                        <div className="hotel-name">{h.hotel_name}</div>
                        <div className="hotel-stars">{renderStars(h.rating)} {h.rating}</div>
                        <div className="hotel-meta">
                          <span className="hotel-price">{h.price}</span>
                          <span className="hotel-distance">📍 {h.distance_km} km</span>
                        </div>
                        <a href={h.booking_url} target="_blank" rel="noopener noreferrer" className="hotel-book-btn">Book Now →</a>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ color: "var(--text-muted)" }}>No hotels found. Try again later.</p>
                )}
              </div>
            )}

            {/* Flights Tab */}
            {matchTab === "flights" && (
              <div>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: 16 }}>✈️ Flights to {selectedMatch.venue_city || selectedMatch.venue_name}</h3>
                <form onSubmit={searchFlights} className="flight-search-row">
                  <input type="text" value={flightSource} onChange={(e) => setFlightSource(e.target.value)} placeholder="Your city (e.g. Delhi, New York)" className="flight-input" />
                  <input type="date" value={flightDate} onChange={(e) => setFlightDate(e.target.value)} className="flight-input" style={{ maxWidth: 180 }} />
                  <button type="submit" disabled={!flightSource.trim() || flightsLoading} className="flight-search-btn">
                    {flightsLoading ? "Searching..." : "🔍 Search"}
                  </button>
                </form>

                {flightsLoading && <div><div className="skeleton skeleton-card"></div><div className="skeleton skeleton-card"></div></div>}

                {flights && !flights.error && (
                  <>
                    <div className="flights-list">
                      {(flights.flights || []).map((f, i) => (
                        <div key={i} className="flight-card">
                          <div>
                            <div className="flight-airline">✈️ {f.airline}</div>
                            <div className="flight-details">
                              <span>⏱️ {f.duration}</span>
                              <span>&nbsp;•&nbsp;</span>
                              <span className={`stops-badge ${f.stops === 0 ? "stops-direct" : "stops-one"}`}>
                                {f.stops === 0 ? "Direct" : `${f.stops} Stop`}
                              </span>
                              <span>&nbsp;•&nbsp;</span>
                              <span>{f.origin} → {f.destination}</span>
                            </div>
                          </div>
                          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                            <span className="flight-price">{f.price}</span>
                            <a href={f.booking_url} target="_blank" rel="noopener noreferrer" className="flight-book-btn">Book →</a>
                          </div>
                        </div>
                      ))}
                    </div>
                    {flights.last_mile && (
                      <div className="last-mile">
                        <div className="last-mile-title">🚕 Last Mile: Airport → Venue</div>
                        <div className="last-mile-desc">
                          {flights.last_mile.description} <br/> <span className="last-mile-cost">Est. {flights.last_mile.estimate}</span>
                        </div>
                      </div>
                    )}
                  </>
                )}
                {flights && flights.error && <p style={{ color: "var(--accent-rose)" }}>{flights.error}</p>}
              </div>
            )}

            {/* Weather Tab */}
            {matchTab === "weather" && (
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px" }}>
                <h3 style={{ fontSize: "1.1rem", marginBottom: "12px" }}>☁️ Live Weather at Venue</h3>
                {matchWeatherLoading ? <p style={{ color: "var(--text-muted)" }}>Loading...</p> : matchWeather ? (
                  matchWeather.error ? <p style={{ color: "var(--accent-rose)" }}>{matchWeather.error}</p> : (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                      <div>
                        <p style={{ fontSize: "2rem", fontWeight: "800" }}>{matchWeather.temperature}</p>
                        <p style={{ color: "var(--text-secondary)", textTransform: "capitalize" }}>{matchWeather.condition}</p>
                      </div>
                      <div style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                        <p>💧 Humidity: {matchWeather.humidity}</p>
                        <p>💨 Wind: {matchWeather.wind_speed}</p>
                      </div>
                    </div>
                  )
                ) : <p style={{ color: "var(--text-muted)" }}>Click to load weather data</p>}
              </div>
            )}

            {/* Distance Tab */}
            {matchTab === "distance" && (
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "16px", borderRadius: "12px" }}>
                <h3 style={{ fontSize: "1.1rem", marginBottom: "12px" }}>🚗 Distance to Venue</h3>
                <form onSubmit={calcMatchDistance} style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
                  <input type="text" value={matchOrigin} onChange={(e) => setMatchOrigin(e.target.value)} placeholder="Your location (e.g. Times Square)" className="flight-input" />
                  <button type="submit" disabled={!matchOrigin.trim() || matchDistanceLoading} className="btn btn-primary" style={{ padding: "10px 20px" }}>
                    {matchDistanceLoading ? "..." : "Calculate"}
                  </button>
                </form>
                {matchDistance && !matchDistanceLoading && (
                  <div style={{ background: "var(--bg-primary)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border-glass)" }}>
                    {matchDistance.error ? (
                      <p style={{ color: "var(--accent-amber)" }}>{matchDistance.error}</p>
                    ) : matchDistance.note ? (
                      <div>
                        <p style={{ color: "var(--text-secondary)", fontSize: "0.85rem", marginBottom: 8 }}>{matchDistance.note}</p>
                        <p style={{ fontSize: "1.1rem", fontWeight: "600" }}>Distance: {matchDistance.distance}</p>
                        <p style={{ fontSize: "1.1rem", fontWeight: "600", color: "var(--accent-blue)" }}>Time: {matchDistance.duration}</p>
                      </div>
                    ) : (
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                        <div>
                          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>Distance</p>
                          <p style={{ fontSize: "1.2rem", fontWeight: "700" }}>{matchDistance.distance}</p>
                        </div>
                        <div>
                          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>Live Driving Time</p>
                          <p style={{ fontSize: "1.2rem", fontWeight: "700", color: "var(--accent-emerald)" }}>{matchDistance.current_duration_with_traffic}</p>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function fallbackVenues(tab) {
  const all = [
    { name: "MetLife Stadium", city: "East Rutherford", country: "United States", capacity: 82500, hosts_final: true, event_id: "fifa_wc_2026", transport: ["NJ Transit", "PATH Train"], _id: "metlife_stadium" },
    { name: "SoFi Stadium", city: "Inglewood", country: "United States", capacity: 70240, hosts_final: false, event_id: "fifa_wc_2026", transport: ["Metro C Line", "LAX Shuttle"], _id: "sofi_stadium" },
    { name: "Estadio Azteca", city: "Mexico City", country: "Mexico", capacity: 87523, hosts_final: false, event_id: "fifa_wc_2026", transport: ["Metro Line 2", "Metrobus"], _id: "estadio_azteca" },
    { name: "Lord's Cricket Ground", city: "London", country: "England", capacity: 30000, hosts_final: true, event_id: "icc_wt20_2026", transport: ["Jubilee Line", "Metropolitan Line"], _id: "lords" },
    { name: "The Oval", city: "London", country: "England", capacity: 25500, hosts_final: false, event_id: "icc_wt20_2026", transport: ["Northern Line", "Bus 36"], _id: "the_oval" },
    { name: "Edgbaston", city: "Birmingham", country: "England", capacity: 25000, hosts_final: false, event_id: "icc_wt20_2026", transport: ["Train to Five Ways", "Bus 45"], _id: "edgbaston" },
    { name: "Old Trafford Cricket Ground", city: "Manchester", country: "England", capacity: 26000, hosts_final: false, event_id: "icc_wt20_2026", transport: ["Metrolink Tram"], _id: "old_trafford" },
  ];
  if (tab === "all") return all;
  return all.filter((v) => v.event_id === tab);
}
