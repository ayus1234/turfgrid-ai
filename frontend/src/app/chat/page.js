"use client";
import { useState, useRef, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://turfgrid-ai-15593284604.europe-west1.run.app";

const SUGGESTIONS = [
  "🏏 Plan a trip to see India play at Lord's",
  "⚽ What matches are at MetLife Stadium?",
  "📊 How crowded will the FIFA Final be?",
  "🍽️ I own a restaurant near The Oval. Big match tomorrow!",
  "🛡️ Volunteer schedule for Edgbaston",
  "✈️ Travel from Ranchi to England for the Women's T20 World Cup",
];

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const messagesEnd = useRef(null);

  useEffect(() => {
    setSessionId("s_" + Math.random().toString(36).slice(2, 10));
  }, []);

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
