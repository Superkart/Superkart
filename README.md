<h1 align="center">Hi, I'm Superkart 👋</h1>

<p align="center">
  <b>Full-Stack Developer · Game Developer · Data Engineer · VR/AR Builder</b><br/>
  Building ambitious projects across web, systems, data, and immersive tech.
</p>

<p align="center">
  <a href="https://github.com/Superkart"><img src="https://img.shields.io/github/followers/Superkart?label=Follow&style=social" alt="GitHub followers"/></a>
  &nbsp;
  <img src="https://komarev.com/ghpvc/?username=Superkart&color=blue&style=flat" alt="Profile views"/>
</p>

---

## 🚀 About Me

I'm a developer with a broad technical portfolio spanning **full-stack web applications**, **game development**, **data science**, and **VR/AR systems**. I enjoy solving real problems end-to-end — from backend architecture and APIs to front-end interfaces, from simulation engines to data pipelines. I'm equally comfortable writing C++ for performance-critical systems, Java services in Spring Boot, Python for data analysis, and C# inside a Unity game engine.

---

## 🛠️ Tech Stack

**Languages**

![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white)
![C#](https://img.shields.io/badge/C%23-239120?style=flat&logo=c-sharp&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

**Frameworks & Platforms**

![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat&logo=spring-boot&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![Astro](https://img.shields.io/badge/Astro-BC52EE?style=flat&logo=astro&logoColor=white)
![Unity](https://img.shields.io/badge/Unity-000000?style=flat&logo=unity&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)

**Tools & Infrastructure**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=flat&logo=cloudflare&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google_Colab-F9AB00?style=flat&logo=googlecolab&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)

---

## ⭐ Featured Projects

### 🎮 [Steam Accountabilibuddy](https://github.com/Superkart/Steam_Accountabilibuddy)
> **Full-Stack Web App** &nbsp;·&nbsp; Java · Spring Boot · React · Astro · PostgreSQL · Cloudflare Workers

A smart Steam library management platform that helps gamers fight backlog overload and never miss a deal. Users authenticate via Steam OpenID and the app automatically analyzes their full library of hundreds of games.

**What it does:**
- **Intelligent backlog analysis** — detects unplayed games in your library that are similar to your wishlist items using SteamSpy tag-based similarity scoring
- **Automated price tracking** — scheduled Spring Boot jobs monitor wishlist prices daily and send email alerts when titles hit user-defined thresholds
- **Library analytics** — visualizes playtime, spending patterns, and gaming habits across your entire Steam catalog
- **Shared wishlists** — generate shareable links for your curated game lists

**Architecture:** Spring Boot 3 backend with Spring Security (OpenID), Spring Data JPA, Spring Mail, and Spring Scheduling wired to a PostgreSQL database; React + Astro front-end deployed via Cloudflare Workers for edge performance.

---

### 🔭 [Immersive Cosmology Explorer (ICE)](https://github.com/Superkart/Immersive_Cosmology_Explorer)
> **VR / Desktop Visualization System** &nbsp;·&nbsp; Unity · C# · AR Foundation · Scientific Visualization

A research-grade Unity application that lets scientists explore multi-billion-particle cosmological simulations in both VR and traditional desktop environments simultaneously.

**What it does:**
- **Immersive 3D point-cloud rendering** — millions of particles (gas, stars, dark matter) rendered in real-time with perceptually uniform colormaps
- **Interactive filtering** — define numeric ranges on physical properties to isolate regions of interest; changes reflect instantly in both VR and desktop views
- **Desktop–VR synchronization** — asymmetric collaboration where a VR user and a desktop user work on the same dataset at the same time
- **Scientific analysis tools** — vector field overlays for particle velocities, time-lapse playback across simulation time-steps, save/load session states, and annotation sharing
- **Optimized for performance** — octree spatial indexing and Level-of-Detail system keep frame rates smooth even with massive datasets

**Architecture:** Three-layer Unity design: data management (import, octree indexing, LOD), visualization & interaction (VR controllers, radial menus, colormaps), and multi-device collaboration (real-time state sync, session history).

---

### 🧪 [Pandas Provenance Tracker](https://github.com/Superkart/Pandas_Provenance)
> **Python Library** &nbsp;·&nbsp; Python · pandas · Data Lineage · PyPI

An open-source Python library that adds **data provenance and lineage tracking** to standard pandas workflows — essential for reproducible data science, regulatory compliance, and pipeline debugging.

**What it does:**
- Tracks every transformation (`read_csv`, `filter`, `merge`, `drop_columns`) with operation-level metadata (table hash, schema, dimensions, timestamp)
- Records **row-level why-provenance** — for any output row you can query exactly which source rows and transformations produced it
- Persists provenance logs as JSON for sharing, auditing, and replay
- Clean query API: `get_table_why_provenance`, `get_row_why_provenance`
- **Published on PyPI** via a full release pipeline (setuptools / wheel / twine)

---

### 📊 [Student Survey Analysis](https://github.com/Superkart/Student_Survey_Analysis)
> **Data Analysis Project** &nbsp;·&nbsp; Python · pandas · Google Colab · Manipal University

A simulation of a real-world data analysis internship at **Manipal University**, covering the complete analytics lifecycle: survey design in Google Forms → data collection → data cleaning → exploratory visualization → stakeholder report. Demonstrates hands-on pandas techniques and the ability to turn raw survey responses into clear, actionable conclusions.

---

### 🛒 [Store — Spring Boot](https://github.com/Superkart/Store_Spring_Boot)
> **Backend Application** &nbsp;·&nbsp; Java · Spring Boot

A RESTful store back-end built with Spring Boot, demonstrating clean layered architecture (controllers, services, repositories), entity modeling, and Spring Data JPA patterns for an e-commerce domain.

---

### 🤖 [AirSim API C++](https://github.com/Superkart/AirSimApiCpp)
> **Systems / Robotics** &nbsp;·&nbsp; C++ · AirSim · Unreal Engine

An external C++ project that interfaces with Microsoft's AirSim simulation platform via its native C++ API, enabling programmatic drone and vehicle control for autonomous navigation experiments. Showcases low-level systems programming and integration with a large simulation framework.

---

### 🕶️ [AR Model Viewer](https://github.com/Superkart/ARModelViewer)
> **Augmented Reality** &nbsp;·&nbsp; Unity · C# · AR Foundation

A mobile AR app that places a detailed 3D model of an AC motor mid-air using the phone camera, letting users explore its internal components in augmented reality. First-hand experience shipping a production AR experience on Unity's AR Foundation stack.

---

### 🎲 Unity Game Development Portfolio

Games and interactive simulations spanning 2D/3D gameplay, physics, AI, procedural generation, and custom shaders:

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

---

### 💻 Learning & Practice Repositories

Structured, version-controlled practice documenting continuous growth:

| Repo | Focus |
|---|---|
| [Python Journey](https://github.com/Superkart/Python_Journey) | Python fundamentals, YouTube tutorials, and LeetCode problems |
| [C++ Journey](https://github.com/Superkart/Cpp_Journey) | C++ from basics to advanced — OOP, memory management, STL |
| [Text-Based Game (C++)](https://github.com/Superkart/TextBasedGame_F) | Console RPG / adventure game written entirely in C++ |

---

### 🌐 Web Projects

| Repo | Description | Tech |
|---|---|---|
| [MyExpenseTracker](https://github.com/Superkart/MyExpenseTracker) | Personal finance tracking web app | TypeScript |
| [PortfolioApp](https://github.com/Superkart/PortfolioApp) | Personal portfolio website | JavaScript |
| [FirstWebAppDeployed](https://github.com/Superkart/FirstWebAppDeployed) | First deployed web application | Astro |
| [BasicCounterWebPage](https://github.com/Superkart/BasicCounterWebPage) | Interactive counter page | TypeScript |

---

## 📈 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=Superkart&show_icons=true&theme=tokyonight&hide_border=true" alt="GitHub Stats" height="165"/>
  &nbsp;
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Superkart&layout=compact&theme=tokyonight&hide_border=true" alt="Top Languages" height="165"/>
</p>

---

## 📬 Contact

- **GitHub**: [github.com/Superkart](https://github.com/Superkart)
