import "./globals.css";

export const metadata = {
  title: "TurfGrid AI — Smart City Command Center for Global Sporting Events",
  description: "An autonomous multi-agent platform that protects cities and businesses from the logistical chaos of global sporting surges. Agents execute actions, save itineraries, create staffing plans, and issue operational alerts — powered by Gemini 2.5 Flash, MongoDB Atlas Vector Search, and Groq failover.",
  keywords: "AI, agents, FIFA, ICC, World Cup, cricket, sports, event management, Gemini, MongoDB, smart city, autonomous agents",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav className="navbar">
          <a href="/" className="nav-logo">
            <span>🌐</span> TurfGrid AI
          </a>
          <ul className="nav-links">
            <li><a href="/">Home</a></li>
            <li><a href="/chat">Chat</a></li>
            <li><a href="/events">Events</a></li>
            <li><a href="/dashboard">Operations</a></li>
          </ul>
        </nav>
        {children}
        <footer className="footer">
          <p>
            Built with ❤️ using <a href="https://cloud.google.com" target="_blank">Google Cloud</a> · <a href="https://www.mongodb.com/" target="_blank">MongoDB</a> · <a href="https://ai.google.dev/" target="_blank">Gemini</a>
          </p>
          <p style={{ marginTop: "8px" }}>
            TurfGrid AI — Google Cloud Rapid Agent Hackathon 2026
          </p>
        </footer>
      </body>
    </html>
  );
}
