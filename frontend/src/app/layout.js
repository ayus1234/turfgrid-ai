import "./globals.css";

export const metadata = {
  title: "EventSphere AI — Multi-Agent Platform for Global Sporting Events",
  description: "An autonomous multi-agent platform powered by Gemini and MongoDB MCP for managing fan logistics, business readiness, and event operations during FIFA World Cup 2026 and ICC Women's T20 World Cup 2026.",
  keywords: "AI, agents, FIFA, ICC, World Cup, cricket, sports, event management, Gemini, MongoDB",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav className="navbar">
          <a href="/" className="nav-logo">
            <span>🌐</span> EventSphere AI
          </a>
          <ul className="nav-links">
            <li><a href="/">Home</a></li>
            <li><a href="/chat">Chat</a></li>
            <li><a href="/events">Events</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
          </ul>
        </nav>
        {children}
        <footer className="footer">
          <p>
            Built with ❤️ using <a href="https://cloud.google.com" target="_blank">Google Cloud</a> · <a href="https://www.mongodb.com/" target="_blank">MongoDB</a> · <a href="https://ai.google.dev/" target="_blank">Gemini</a>
          </p>
          <p style={{ marginTop: "8px" }}>
            EventSphere AI — Google Cloud Rapid Agent Hackathon 2026
          </p>
        </footer>
      </body>
    </html>
  );
}
