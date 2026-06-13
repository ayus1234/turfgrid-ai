"use client";
import { useState, useRef, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://turfgrid-ai-15593284604.europe-west1.run.app";

const SUGGESTIONS = [
  "🏏 Plan a trip to see India play at Lord's",
  "⚽ What matches are at MetLife Stadium?",
  "📊 How crowded will the FIFA Final be?",
  "🎫 Book tickets for India vs Pakistan",
  "🏨 Find hotels near Lord's Cricket Ground",
  "✈️ Book flights from Delhi to London for the ICC Final",
  "🍽️ I own a restaurant near The Oval. Big match tomorrow!",
  "🛡️ Volunteer schedule for Edgbaston",
];

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const [workflows, setWorkflows] = useState([]);
  const [shownWorkflowIds, setShownWorkflowIds] = useState(new Set());
  const messagesEnd = useRef(null);

  useEffect(() => {
    setSessionId("s_" + Math.random().toString(36).slice(2, 10));
    
    // Poll for background workflows
    const interval = setInterval(() => {
      fetch(`${API_URL}/api/workflows`)
        .then((r) => r.json())
        .then((d) => {
          if (d.workflows && d.workflows.length > 0) {
            setWorkflows((prev) => {
              const newWorkflows = d.workflows.filter(w => !shownWorkflowIds.has(w._id));
              if (newWorkflows.length > 0) {
                setShownWorkflowIds(new Set([...shownWorkflowIds, ...newWorkflows.map(w => w._id)]));
                return [...prev, ...newWorkflows].slice(-3); // Keep max 3 toasts
              }
              return prev;
            });
          }
        })
        .catch(() => {});
    }, 5000);
    return () => clearInterval(interval);
  }, [shownWorkflowIds]);

  // Auto-dismiss workflow toasts after 8 seconds
  useEffect(() => {
    if (workflows.length > 0) {
      const timer = setTimeout(() => {
        setWorkflows(prev => prev.slice(1));
      }, 8000);
      return () => clearTimeout(timer);
    }
  }, [workflows]);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text) => {
    const msg = text || input.trim();
    if (!msg || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: msg }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg, session_id: sessionId }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: data.response,
          agent: data.agent_used,
          steps: data.agent_steps || [],
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content:
            "⚠️ Unable to reach the backend. Make sure the FastAPI server is running on " +
            API_URL +
            "\n\nRun: `cd backend && python run.py`",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatContent = (text) => {
    // Simple markdown-like formatting
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\[(.*?)\]\((.*?)\)/g, "<a href='$2' target='_blank' rel='noopener noreferrer' style='color: var(--accent-blue); text-decoration: underline; word-break: break-all;'>$1</a>")
      .replace(/\n/g, "<br/>")
      .replace(/- /g, "• ");
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-header">
          <h1>
            <span className="gradient-text">TurfGrid</span> AI Chat
          </h1>
          <p>
            Ask about FIFA World Cup 2026, ICC Women's T20 World Cup 2026, or
            anything about fan travel, business readiness, crowds, or operations.
          </p>
        </div>

        <div className="chat-messages">
          {messages.length === 0 && (
            <>
              <div className="message message-ai">
                👋 Welcome to <strong>TurfGrid AI</strong>! I'm your
                autonomous Smart City Command Center for global sporting events.
                <br />
                <br />
                I don't just recommend — I <strong>execute actions</strong>:
                <br />• 🎫 <strong>Book match tickets</strong> — redirect to
                official FIFA & ICC ticket portals
                <br />• 🏨 <strong>Find & book hotels</strong> — nearby
                accommodation with prices & booking links
                <br />• ✈️ <strong>Search flights</strong> — find the best
                flights with last-mile transport info
                <br />• ✈️ <strong>Save travel itineraries</strong> — plan and
                persist your trip to MongoDB
                <br />• 📊 <strong>Create staffing plans</strong> — generate
                match-day schedules for businesses
                <br />• 🚨 <strong>Issue operational alerts</strong> — flag
                safety and crowd concerns
                <br />• 🧠 <strong>Remember your preferences</strong> — diet,
                budget, accessibility
                <br />
                <br />
                Try one of the suggestions below or ask anything!
              </div>
              <div className="chat-suggestions">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={i}
                    className="suggestion"
                    onClick={() => sendMessage(s.replace(/^[^\s]+\s/, ""))}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </>
          )}

          {messages.map((m, i) => (
            <div key={i}>
              {/* Agent Steps — Multi-Agent Transparency */}
              {m.role === "ai" && m.steps && m.steps.length > 0 && (
                <div className="agent-steps">
                  <div className="agent-steps-header">
                    <span>🤖 Agent Activity</span>
                  </div>
                  <div className="agent-steps-list">
                    {m.steps.map((step, j) => (
                      <div
                        key={j}
                        className={`agent-step ${step.status === "warning" ? "step-warning" : "step-done"}`}
                        style={{ animationDelay: `${j * 0.1}s` }}
                      >
                        <span className="step-icon">
                          {step.status === "warning" ? "⚠️" : "✅"}
                        </span>
                        <span className="step-agent">{step.agent}</span>
                        <span className="step-action">{step.action}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              <div className={`message message-${m.role}`}>
                {m.role === "ai" ? (
                  <div
                    dangerouslySetInnerHTML={{ __html: formatContent(m.content) }}
                  />
                ) : (
                  m.content
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message message-ai typing-indicator">
              <div className="typing-dot" />
              <div className="typing-dot" />
              <div className="typing-dot" />
            </div>
          )}

          <div ref={messagesEnd} />
        </div>

        {/* Workflow Toasts */}
        <div style={{ position: "absolute", bottom: 100, right: 32, display: "flex", flexDirection: "column", gap: 12, zIndex: 50 }}>
          {workflows.map((w, i) => (
            <div key={i} className="glass-strong" style={{ padding: "12px 16px", borderLeft: "4px solid var(--accent-amber)", animation: "slideIn 0.3s ease-out", maxWidth: 350, boxShadow: "0 10px 25px rgba(0,0,0,0.5)" }}>
              <div style={{ fontWeight: 700, fontSize: "0.85rem", color: "var(--accent-amber)", marginBottom: 4 }}>
                ⚙️ Background System Workflow
              </div>
              <div style={{ fontSize: "0.9rem" }}>{w.message}</div>
              <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: 6, textAlign: "right" }}>
                {w.event} • {new Date(w.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
        </div>

        <div className="chat-input-area">
          <div className="chat-input-wrapper glass-strong">
            <input
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask about FIFA World Cup, ICC Cricket, travel plans..."
              disabled={loading}
            />
            <button
              className="chat-send"
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
            >
              {loading ? "..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
