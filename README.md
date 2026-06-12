# 🌐 TurfGrid AI

**Smart City Command Center — An autonomous agent swarm that protects cities and businesses from the logistical chaos of global sporting surges.**

> Built for the [Google Cloud Rapid Agent Hackathon](https://devpost.com/) — MongoDB Track

### 🚀 **[Play with the Live Demo Here!](https://turfgrid-ai-frontend-15593284604.europe-west1.run.app/)**


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Agent%20Builder-4285F4?logo=google-cloud)](https://cloud.google.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Vector%20Search-47A248?logo=mongodb)](https://www.mongodb.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?logo=google)](https://ai.google.dev/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203-F55036?logo=groq)](https://groq.com/)

---

## 🎯 What is TurfGrid AI?

TurfGrid AI is an autonomous **Smart City Command Center** that manages the complex logistics of large-scale sporting events. When 80,000 fans descend on a city, local infrastructure breaks — restaurants run out of inventory, roads congest, and security is overwhelmed. Our agents don't just recommend — they **execute actions**, save data to MongoDB, and maintain persistent user memory. Demonstrated with two real events happening simultaneously in 2026:

| Event | Dates | Location | Teams | Venues |
|-------|-------|----------|-------|--------|
| ⚽ **FIFA World Cup 2026** | June 11 – July 19 | USA, Mexico, Canada | 48 | 16 |
| 🏏 **ICC Women's T20 World Cup 2026** | June 12 – July 5 | England | 12 | 7 |

## 🔥 Key Hackathon Features

### 1. MongoDB Vector Search & Semantic Memory
Instead of relying on rigid keyword lookups, TurfGrid AI utilizes **MongoDB `$vectorSearch`**. Venue data is dynamically embedded into 768-dimensional vectors using Google's `gemini-embedding-2`. This allows users to ask natural language questions like *"Find me stadiums near water with large capacities"* and receive mathematically accurate results from Atlas!

### 2. High-Availability LLM Architecture (Gemini ➡️ Groq Failover)
Enterprise agents cannot afford downtime. TurfGrid AI implements a highly resilient architecture. It uses **Google Gemini 2.5 Flash** as its primary orchestrator. However, if the API quota is exhausted (`429 RESOURCE_EXHAUSTED`), the backend intercepts the failure and seamlessly fails over to **Groq's Llama-3.3-70b-versatile** model without dropping the user's session or breaking the UI. 

### 3. Autonomous State-Altering Actions (v2.0)
Our agents don't just recommend — they **execute**. When a fan approves a travel plan, the agent autonomously calls `save_itinerary()` and writes a confirmed booking to MongoDB. When a business owner asks for staffing advice, the agent calls `create_staffing_plan()` to persist an actionable schedule. Operations agents call `issue_operational_alert()` to flag safety concerns in real-time.

**New MongoDB Collections:**
- `user_itineraries` — Confirmed fan travel plans
- `staffing_plans` — Business match-day staffing schedules
- `operational_alerts` — Live safety and crowd alerts
- `user_profiles` — Persistent user preferences (diet, accessibility, budget)

### 4. Persistent User Memory
The system remembers users across sessions. If a fan says *"I'm vegetarian and need wheelchair access,"* the Orchestrator saves these preferences to MongoDB. The next time they ask for restaurant recommendations, the agent automatically filters for vegetarian, accessible options — without the user repeating themselves.

### 5. Real-Time API Agentic Tool Calling
Our agents are empowered with tools to fetch live data from the outside world:
- **Google Maps Distance Matrix API:** Agents calculate real-time driving durations and traffic delays from user locations to venues.
- **OpenWeatherMap API:** Agents fetch live atmospheric data to predict crowd congestion mitigation strategies.
- **Amadeus Travel API (Simulated):** Agents dynamically extract destinations using a custom NLP intent parser and generate highly realistic flight itineraries and hotel pricing.

### 6. Multi-Agent Transparency & Operations Dashboard
Every agent action is tracked and displayed in the chat UI with a visual orchestration chain (✅ Orchestrator → ✅ Fan Agent → ✅ Tool Called → ✅ MongoDB Updated). The Operations Dashboard polls MongoDB every 30 seconds to show live alerts, saved itineraries, and staffing plans in real-time.

---

## 🏗️ Project Architecture

```text
📦 TurfGrid-AI
 ├── 📂 backend/                 # FastAPI Backend Server
 │   ├── 📂 app/                 # Main Application Directory
 │   │   ├── 📂 agents/          # AI Orchestrator & Specialized Agents (Fan, Business, Crowd)
 │   │   ├── 📂 data/            # Seed Data & MongoDB Vector Search logic
 │   │   ├── 📂 tools/           # API Integrations (Weather, Maps, Amadeus)
 │   │   ├── 📄 config.py        # Environment & Configuration settings
 │   │   └── 📄 main.py          # Application Entry Point & API Routes
 │   ├── 📄 requirements.txt     # Python Dependencies
 │   ├── 📄 run_seed.py          # MongoDB Database Seeding Script
 │   └── 📄 run.py               # Uvicorn Development Server Runner
 │
 ├── 📂 frontend/                # Next.js React Frontend
 │   ├── 📂 src/
 │   │   ├── 📂 app/             # Next.js App Router structure
 │   │   │   ├── 📂 chat/        # LLM Agent Chat Interface
 │   │   │   ├── 📂 dashboard/   # Analytics & Insights Dashboard
 │   │   │   ├── 📂 events/      # Venue Explorer & Interactive Modals
 │   │   │   ├── 📄 globals.css  # Core styles, glassmorphism, animations
 │   │   │   ├── 📄 layout.js    # Root layout, Navbar, and Footer
 │   │   │   └── 📄 page.js      # Main Landing Page
 │   ├── 📄 package.json         # Node.js Dependencies
 │   └── 📄 next.config.mjs      # Next.js Configuration
 │
 ├── 📄 .env                     # Environment Variables (API Keys, DB URL)
 └── 📄 README.md                # Project Documentation
```

---

## 🔄 Project Workflow

```mermaid
graph TD
    %% User Interaction
    U[User Interaction<br/>Next.js UI] -->|Chat Query / UI Click| O
    
    %% Orchestrator & High Availability
    subgraph High Availability LLM Router
        O[TurfGrid Orchestrator]
        O -->|Primary: Success| G[Google Gemini 2.5 Flash]
        O -->|Primary: 429 Quota Exhausted| F[Failover Trigger]
        F -->|Fallback| L[Groq Llama-3.3-70b-versatile]
    end

    %% Specialized Agents
    G -->|Delegates| SA
    L -->|Delegates| SA

    subgraph Autonomous Agents
        SA{Specialized Agents}
        SA -->|Travel & Venues| FL[Fan Logistics Agent]
        SA -->|Demand & Checklists| BR[Business Readiness Agent]
        SA -->|Weather & Congestion| CI[Crowd Intelligence Agent]
        SA -->|Incidents & Staff| EO[Event Operations Agent]
    end

    %% External APIs & Tools
    FL -->|Simulated Data| T1((Amadeus Travel APIs))
    CI -->|Live Traffic| T2((Google Maps Distance Matrix))
    CI -->|Live Atmospheric| T3((OpenWeatherMap API))

    %% Database
    SA -->|Read/Write / Semantic Search| DB[(MongoDB Atlas<br/>w/ Vector Search)]
    
    %% Styling
    classDef primary fill:#4285F4,stroke:#fff,stroke-width:2px,color:#fff;
    classDef fallback fill:#F55036,stroke:#fff,stroke-width:2px,color:#fff;
    classDef db fill:#47A248,stroke:#fff,stroke-width:2px,color:#fff;
    classDef tool fill:#f59e0b,stroke:#fff,stroke-width:2px,color:#fff;
    
    class G primary;
    class L fallback;
    class DB db;
    class T1,T2,T3 tool;
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 22.13+
- MongoDB Atlas account
- Google Gemini API key (Primary)
- Groq API key (Failover)
- Google Maps & OpenWeatherMap keys (Optional for Live Data)

### 1. Clone & Configure

```bash
git clone https://github.com/ayus1234/turfgrid-ai.git
cd turfgrid-ai
# Update .env with your specific API Keys!
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
python run.py
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` to interact with the platform!

---

## 🤖 Agent Capabilities & Example Interactions

> **"I want to fly from London to New York for the World Cup. Book a hotel and tell me the traffic to MetLife Stadium."**
> → The system parses the intent, detects the 'JFK' and 'NYC' routing, simulates flight/hotel prices, checks the live Google Maps API for traffic, and returns a fully formatted response.

> **"I own a restaurant near Lord's. India vs England tomorrow — how should I prepare?"**
> → Business Agent predicts 2.5x demand, recommends adding 4 staff, increasing food stock 150% and beverages 225%.

> **"Find me stadiums near the water."**
> → Hits the MongoDB `$vectorSearch` pipeline, comparing the user's sentence embedding against the embedded dataset, correctly returning venues like SoFi Stadium.

## 📄 License
MIT License — see [LICENSE](LICENSE)

## 🙏 Acknowledgments
- [Google Cloud](https://cloud.google.com/) — Gemini AI & Agent Development Kit
- [MongoDB](https://www.mongodb.com/) — Atlas & Vector Search
- [Groq](https://groq.com/) — High-speed Llama 3 inference
- FIFA & ICC — for inspiring the challenge scenarios
