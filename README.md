<h1 align="center">Hi, I'm Karthik Ragi 😃</h1>

<p align="center">
  <b>Software Engineer · AI Systems · Backend · Computer Vision</b><br/>
  3 years building real-time systems and multi-agent pipelines.<br/>
  MS Computer Science at UIC &nbsp;·&nbsp; Open to full-time roles
</p>

<p align="center">
  <a href="https://github.com/Superkart"><img src="https://img.shields.io/github/followers/Superkart?label=Follow&style=social" alt="GitHub followers"/></a>
  &nbsp;
  <img src="https://komarev.com/ghpvc/?username=Superkart&color=blue&style=flat" alt="Profile views"/>
</p>

---

## 🚀 About Me

I build **real-time AI systems and production-grade backend infrastructure**. My work spans multi-agent LLM pipelines, CUDA-accelerated computer vision, and high-throughput data systems deployed at scale.

- **AI & Agents** — LangGraph multi-agent pipelines (Planner → Extractor → Critic → SME) benchmarked on real RE datasets; production incident response agent turning Prometheus alerts into auto-drafted GitHub PRs with full Loki/Grafana observability
- **Computer Vision** — CUDA-accelerated OpenCV detection at **10 Indian Air Force bases**, serving **3,000+ daily users** on a $1.8M project; classical pipeline at **96% hit detection accuracy** on Raspberry Pi
- **Backend & Systems** — multi-threaded .NET ingestion pipelines: 500ms → <50ms; Spring Boot + GCP batch API: 50s → <2s (10–25×)

📍 Chicago, IL &nbsp;·&nbsp; Open to remote &nbsp;·&nbsp; 📧 [kragi@uic.edu](mailto:kragi@uic.edu)

---

## 🛠️ Tech Stack

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![C#](https://img.shields.io/badge/C%23-239120?style=flat&logo=c-sharp&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)

**AI / ML**

![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Claude API](https://img.shields.io/badge/Claude_API-D97757?style=flat&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-76B900?style=flat&logo=nvidia&logoColor=white)
![sentence-transformers](https://img.shields.io/badge/sentence--transformers-FF6B35?style=flat&logoColor=white)

**Backend & Data**

![.NET](https://img.shields.io/badge/.NET-512BD4?style=flat&logo=dotnet&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat&logo=spring-boot&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=flat&logo=rabbitmq&logoColor=white)

**Infrastructure**

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)

**Simulation**

![Unity](https://img.shields.io/badge/Unity-000000?style=flat&logo=unity&logoColor=white)
![Unreal Engine](https://img.shields.io/badge/Unreal_Engine_5-0E1128?style=flat&logo=unrealengine&logoColor=white)
![AirSim](https://img.shields.io/badge/AirSim-0078D4?style=flat&logo=microsoft&logoColor=white)

---

## ⭐ Featured Projects

### 🚨 [Incident Response Agent](https://github.com/Superkart/Incident_Response_Agent)
> **AI Agent System** &nbsp;·&nbsp; Python · Claude API · Prometheus · Loki · Grafana · Docker

Production-grade incident response automation: a Prometheus alert fires and triggers a 3-agent triage pipeline that investigates root cause, correlates Loki logs, and auto-drafts a GitHub PR with a proposed fix.

**What it does:**
- **Alert ingestion** — Prometheus firing alert → agent pipeline activates automatically
- **3-agent triage** — Investigator queries Loki/Grafana for context → Analyst identifies root cause → Drafter writes the GitHub PR
- **Full observability** — every agent step traced in Grafana; alert-to-PR latency tracked end-to-end

---

### 📐 [RE Elicitation Agents](https://github.com/Superkart/RequirementsEngineering_Agents)
> **AI Research** &nbsp;·&nbsp; LangGraph · Claude API · sentence-transformers

Rigorous benchmark comparing single-agent vs multi-agent LLM approaches for requirements elicitation, run against two real-world RE datasets.

**What it does:**
- **Multi-agent pipeline** — Planner → Extractor → Critic → SME review loop built in LangGraph
- **Honest result** — single-agent outperformed multi-agent at 1/5 the token cost on both datasets
- **Reproducible evaluation** — sentence-transformer similarity scoring against gold-standard requirements

---

### 🎮 [Steam Accountabilibuddy](https://github.com/Superkart/Steam_Accountabilibuddy)
> **Full-Stack Web App** &nbsp;·&nbsp; Java · Spring Boot · React · PostgreSQL · GCP

A Steam library manager that fights backlog overload and tracks deals. Authenticates via Steam OpenID and analyzes your full library automatically.

**What it does:**
- **Backlog analysis** — detects unplayed games similar to your wishlist via SteamSpy tag-based scoring
- **Price alerts** — scheduled Spring Boot jobs monitor wishlist prices daily; email when thresholds hit
- **10–25× API speedup** — batch Steam API calls cut fetch time from 50s → <2s
- **Library analytics** — playtime, spending, and gaming habit visualizations

**Architecture:** Spring Boot 3 (Spring Security OpenID, Data JPA, Mail, Scheduling) + PostgreSQL + GCP; React front-end.

---

### 🚁 [Drone Simulator](https://github.com/Superkart/Drone_Simulator)
> **HITL Simulation Platform** &nbsp;·&nbsp; C++ · AirSim · Unreal Engine 5 · PX4

Hardware-in-the-Loop drone simulation with high-fidelity physics across a 16 km² terrain at 30–120 Hz telemetry rates.

**What it does:**
- **HITL integration** — real PX4 flight controller drives a simulated drone in Unreal Engine 5 via AirSim MAVLink bridge
- **High-frequency telemetry** — 30–120 Hz state updates (position, attitude, velocity) across the full mission area
- **16 km² environment** — large-scale terrain with realistic atmospheric and sensor simulation
- **Mission scripting** — C++ API for waypoint navigation, sensor injection, and failure modes

---

### 🔭 [Immersive Cosmology Explorer (ICE)](https://github.com/Superkart/Immersive_Cosmology_Explorer)
> **VR / Desktop Visualization** &nbsp;·&nbsp; Unity · C# · GPU Compute Shaders · AR Foundation

Research-grade Unity application for exploring multi-billion-particle cosmological simulations in VR and desktop simultaneously, with real-time state sync at <100ms latency.

**What it does:**
- **Real-time point-cloud rendering** — millions of gas/star/dark-matter particles with GPU compute shaders and perceptually uniform colormaps
- **Interactive filtering** — define numeric ranges on physical properties; changes reflect instantly in both views
- **Desktop–VR sync** — asymmetric collaboration at <100ms state latency
- **Scientific tools** — vector field overlays, time-lapse playback, save/load sessions, annotation sharing
- **Octree + LOD** — spatial indexing keeps frame rates smooth on massive datasets

---

### 🎮 Game Development Portfolio

Games and interactive simulations spanning 2D/3D gameplay, physics, AI, procedural generation, and custom shaders:

<!-- UNITY-GAMES-START -->
| Project | Description | Tech |
|---|---|---|
| [MiniTankMania](https://github.com/Superkart/MiniTankMania) | 3D wave-based tank combat — miniature player tank vs escalating enemy waves | Unity · C# |
| [SimpleFollowAI](https://github.com/Superkart/SimpleFollowAi) | Stealth-style game with NPC proximity-detection and patrol AI | Unity · C# |
| [Bounce Ball](https://github.com/Superkart/Bounce-Ball) | Angry-Birds-style 2D projectile physics puzzle | Unity · C# |
| [The Lost Isle](https://github.com/Superkart/The-Lost-Isle) | Exploration / adventure game | Unity · C# |
| [Random Puzzle Generator](https://github.com/Superkart/Random-PuzzleGenerator) | Procedurally generates color-based puzzles at runtime | Unity · C# |
| [Wall Touch](https://github.com/Superkart/Wall-Touch) | 2D precision platformer — reach the goal without touching walls | Unity · C# |
| [Ball Experiments](https://github.com/Superkart/BallExperiments) | Physics sandbox for learning Unity 3D rigidbody dynamics | Unity · C# |
| [PuglleRunner](https://github.com/Superkart/PuglleRunner-) | Endless runner with custom shader effects | Unity · ShaderLab |
| [Calculator](https://github.com/Superkart/Calculator) | Fully functional calculator built inside Unity 3D | Unity · C# |
| [Mario Game](https://github.com/Superkart/Mario-Game) | 2D side-scroller inspired by classic Mario mechanics | Unity · C# |
| [Quiz Defender](https://github.com/Superkart/QuizDefender) | Educational quiz-based tower defense hybrid | Unity · C# |
| [Shooter Concept](https://github.com/Superkart/ShooterConcept) | Third-person shooter movement and combat prototype | Unity |
| [ARModelViewer](https://github.com/Superkart/ARModelViewer) | First AR project that can be used to view a AC motor and its parts by placing it midair using mobile phone. | Unity · C# |
<!-- UNITY-GAMES-END -->

---

### 🌐 Web Projects

<!-- WEB-PROJECTS-START -->
| Repo | Description | Tech |
|---|---|---|
| [MyExpenseTracker](https://github.com/Superkart/MyExpenseTracker) | Personal finance tracking web app | TypeScript |
| [PortfolioApp](https://github.com/Superkart/PortfolioApp) | Personal portfolio website | JavaScript |
| [FirstWebAppDeployed](https://github.com/Superkart/FirstWebAppDeployed) | First deployed web application | Astro |
| [BasicCounterWebPage](https://github.com/Superkart/BasicCounterWebPage) | Interactive counter page | TypeScript |
| [DataScience1](https://github.com/Superkart/DataScience1) | This is a repository that contains the homework 1 of my Data Science class | HTML |
| [hw5](https://github.com/Superkart/hw5) | — | TypeScript |
| [uic-hackathon-my-agent](https://github.com/Superkart/uic-hackathon-my-agent) | — | TypeScript |
<!-- WEB-PROJECTS-END -->

---

### ⚙️ Backend & APIs

<!-- BACKEND-START -->
| Repo | Description | Tech |
|---|---|---|
| [hotel_management_app](https://github.com/Superkart/hotel_management_app) | — | Java |
| [Store_Spring_Boot](https://github.com/Superkart/Store_Spring_Boot) | — | Java |
<!-- BACKEND-END -->

---

### 📊 Data Engineering

<!-- DATA-ENG-START -->
| Repo | Description | Tech |
|---|---|---|
<!-- DATA-ENG-END -->

---

### 🤖 ML & AI Projects

<!-- ML-AI-PROJECTS-START -->
| Repo | Description | Tech |
|---|---|---|
| [Applied-ML-Case-Studies](https://github.com/Superkart/Applied-ML-Case-Studies) | — | Jupyter Notebook |
| [ML-Foundations-Python-Numpy](https://github.com/Superkart/ML-Foundations-Python-Numpy) | — | Jupyter Notebook |
| [ML-From-Scratch-Neural-Networks](https://github.com/Superkart/ML-From-Scratch-Neural-Networks) | — | Jupyter Notebook |
| [Reddit_Moderator_Tool](https://github.com/Superkart/Reddit_Moderator_Tool) | — | Jupyter Notebook |
| [Student_Survey_Analysis](https://github.com/Superkart/Student_Survey_Analysis) | A simulation of a real-world student data analysis internship using Google Forms, Python (pandas), and Google Colab. This project walks through survey design, data cleaning, visualization, and reporting — based on an internship experience at Manipal University. | Jupyter Notebook |
<!-- ML-AI-PROJECTS-END -->

---

### 🔧 Systems & Robotics

<!-- SYSTEMS-START -->
| Repo | Description | Tech |
|---|---|---|
| [AirSimApiCpp](https://github.com/Superkart/AirSimApiCpp) | AirSim Api controls using external c++ project | C++ |
<!-- SYSTEMS-END -->

---

### 💻 Learning & Practice

Structured, version-controlled practice documenting continuous growth:

<!-- LEARNING-REPOS-START -->
| Repo | Focus |
|---|---|
| [Python Journey](https://github.com/Superkart/Python_Journey) | Python fundamentals, YouTube tutorials, and LeetCode problems |
| [C++ Journey](https://github.com/Superkart/Cpp_Journey) | C++ from basics to advanced — OOP, memory management, STL |
| [Text-Based Game (C++)](https://github.com/Superkart/TextBasedGame_F) | Console RPG / adventure game written entirely in C++ |
<!-- LEARNING-REPOS-END -->

---

### 📁 Other Projects

<!-- OTHER-PROJECTS-START -->
| Repo | Description | Tech |
|---|---|---|
| [OpenCV_Python](https://github.com/Superkart/OpenCV_Python) | Just learning how to implement cv from some studying. | Python |
| [Pandas_Provenance](https://github.com/Superkart/Pandas_Provenance) | # Pandas Provenance Tracker  ## Description This project enables manual provenance tracking for data transformations in the pandas library. It logs operations like filtering and joins, helping users trace data changes at each step. Provenance tracking supports transparency, reproducibility, and accountability in data workflows. | Python |
| [SQL_Hackathon](https://github.com/Superkart/SQL_Hackathon) | — | — |
<!-- OTHER-PROJECTS-END -->

---

## 📈 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=Superkart&show_icons=true&theme=tokyonight&hide_border=true" alt="GitHub Stats" height="165"/>
  &nbsp;
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Superkart&layout=compact&theme=tokyonight&hide_border=true" alt="Top Languages" height="165"/>
</p>

---

## 📬 Contact

📍 Chicago, IL &nbsp;·&nbsp; Open to remote
📧 [kragi@uic.edu](mailto:kragi@uic.edu)
🐙 [github.com/Superkart](https://github.com/Superkart)
