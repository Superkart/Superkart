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

I'm a developer with a broad technical portfolio spanning **full-stack web applications**, **game development**, **data science**, and **VR/AR systems**. I enjoy solving real problems end-to-end from backend architecture and APIs to front-end interfaces, from simulation engines to data pipelines. I'm equally comfortable writing C++ for performance-critical systems, Java services in Spring Boot, Python for data analysis, and C# inside a Unity game engine.

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

### 🛒 [Store — Spring Boot](https://github.com/Superkart/Store_Spring_Boot)
> **Backend Application** &nbsp;·&nbsp; Java · Spring Boot

A RESTful store back-end built with Spring Boot, demonstrating clean layered architecture (controllers, services, repositories), entity modeling, and Spring Data JPA patterns for an e-commerce domain.

**What it does:**
- **Product catalogue management** — exposes CRUD endpoints for products, categories, and inventory levels; supports filtering, sorting, and pagination out of the box
- **Order & cart processing** — models the full purchase lifecycle from cart creation through order placement, with transactional guarantees via Spring Data JPA
- **Customer accounts** — handles user registration, authentication, and address book management with secure password storage
- **Service-layer business logic** — enforces stock-quantity checks, order-total calculation, and discount-code application cleanly separated from the persistence layer
- **Spring Data JPA repositories** — leverages derived query methods and `@Query` annotations for efficient database access without boilerplate SQL

**Architecture:** Classic three-layer Spring Boot application — `@RestController` → `@Service` → `@Repository` — wired together with dependency injection; entities mapped with JPA annotations to a relational database schema.

---

### 🤖 [AirSim API C++](https://github.com/Superkart/AirSimApiCpp)
> **Systems / Robotics** &nbsp;·&nbsp; C++ · AirSim · Unreal Engine

An external C++ project that interfaces with Microsoft's AirSim simulation platform via its native C++ API, enabling programmatic drone and vehicle control for autonomous navigation experiments. Showcases low-level systems programming and integration with a large simulation framework.

**What it does:**
- **Programmatic vehicle control** — sends velocity, position, and rotation commands to simulated drones and ground vehicles through AirSim's RPC-based C++ client
- **Sensor data retrieval** — captures real-time telemetry including GPS coordinates, IMU readings, barometer data, and lidar point clouds directly from the simulation environment
- **Autonomous flight scripting** — implements pre-planned waypoint navigation and mission sequences, letting the drone execute multi-step routes without manual input
- **Camera & image pipeline** — requests high-resolution images and depth maps from onboard simulated cameras for computer-vision algorithm testing
- **Collision & environment awareness** — monitors collision events and environment state to trigger conditional flight maneuvers or emergency responses

**Architecture:** Standalone C++ application linked against AirSim's client library; communicates with the Unreal Engine simulation host over msgpack-RPC, with mission logic cleanly separated from the low-level API wrapper calls.

---

### 🚁 [Drone Simulator](https://github.com/Superkart/Drone_Simulator)
> **Simulation / Systems** &nbsp;·&nbsp; C++

A drone flight simulator implementing realistic physics and control systems for autonomous and manual drone operation. Demonstrates applied knowledge of flight dynamics, control loops, and simulation architecture in C++.

**What it does:**
- **Realistic flight physics** — models rotor thrust, drag, gravity, and inertia to produce believable 6-DOF (six degrees of freedom) flight behaviour for multi-rotor drones
- **PID control loops** — implements proportional-integral-derivative controllers for altitude hold, attitude stabilisation, and position tracking, mirroring real autopilot firmware
- **Manual & autonomous modes** — accepts joystick-style control inputs for manual piloting and supports scripted waypoint missions for fully autonomous operation
- **Sensor emulation** — simulates noisy accelerometer, gyroscope, and barometer readings to test sensor-fusion and filtering algorithms under realistic conditions
- **Collision detection** — tracks the drone's bounding volume against terrain and obstacles, triggering crash events and enabling safe-landing logic testing
- **Telemetry logging** — records flight state (position, velocity, attitude, motor outputs) at each simulation tick for post-flight analysis and debugging

**Architecture:** C++ simulation loop with a fixed-step physics integrator, a modular controller layer (attitude → velocity → position), and an I/O abstraction that separates simulated sensor feeds from the control algorithms.

---

### 🐾 [My Puggle Runner](https://github.com/Superkart/PuglleRunner-)
> **Unity Game** &nbsp;·&nbsp; Unity · ShaderLab · C#

An endless runner game starring a puggle (beagle–pug mix) protagonist, built in Unity with custom shader effects for a visually distinctive look. Showcases Unity rendering-pipeline customization, procedural obstacle generation, and polished game-loop design.

**What it does:**
- **Endless procedural level generation** — spawns and recycles obstacle patterns ahead of the player at runtime, keeping the track fresh and memory footprint constant regardless of playtime
- **Custom ShaderLab visuals** — hand-written vertex and fragment shaders give the game its distinctive aesthetic, including stylised fur shading on the puggle character and dynamic background effects
- **Responsive character controller** — tight, frame-rate-independent movement and jump mechanics with coyote-time and input buffering for a satisfying player feel
- **Escalating difficulty curve** — gradually increases speed and obstacle density over time, maintaining a fair but ever-challenging experience
- **Score & leaderboard system** — tracks the current run distance and personal best, displayed on a polished HUD with smooth UI animations
- **Audio & juice** — synchronized sound effects and screen-shake feedback on collisions and power-up pickups amplify the game feel

**Architecture:** Unity MonoBehaviour-driven architecture with an object-pooling system for obstacles and collectibles, a central `GameManager` state machine (idle → playing → game-over), and separated rendering concerns handled through custom shader passes.

---

### 🛠️ [Reddit Moderator Tool](https://github.com/Superkart/Reddit_Moderator_Tool)
> **ML / Data Science Tool** &nbsp;·&nbsp; Python · Jupyter Notebook

A machine-learning–powered assistant for Reddit moderation tasks. Uses natural language processing to analyse post and comment content, helping moderators identify rule-breaking content efficiently.

**What it does:**
- **Automated rule-violation detection** — trains a text classification model on labelled Reddit posts and comments to flag content that likely breaks community rules, dramatically reducing manual review workload
- **Toxic & spam content filtering** — applies NLP techniques (TF-IDF, word embeddings) to distinguish toxic language, spam patterns, and off-topic submissions from legitimate posts
- **Sentiment & intent analysis** — scores posts for hostility, harassment indicators, and low-quality signals to surface the most problematic items first
- **Subreddit-specific fine-tuning** — the model can be retrained on a subreddit's own moderation history, adapting to niche community standards without manual rule writing
- **Exploratory analysis notebooks** — Jupyter notebooks walk through data collection via the Reddit API (PRAW), feature engineering, model evaluation, and result visualisation for transparent, reproducible experiments
- **Moderator-friendly output** — produces ranked lists of suspicious content with confidence scores and highlighted trigger phrases, making it easy for humans to audit and act on model predictions

**Architecture:** Python data-science stack (pandas, scikit-learn, matplotlib) with PRAW for Reddit API access; Jupyter notebooks for exploration and training; serialised model artifacts for batch inference on new content.

---

### 🏝️ [The Lost Isle](https://github.com/Superkart/The-Lost-Isle)
> **Unity Game** &nbsp;·&nbsp; Unity · C#

An exploration and adventure game built in Unity, featuring hand-crafted level design, narrative-driven gameplay, and polished mechanics that guide the player through a mysterious island environment.

**What it does:**
- **Narrative-driven exploration** — players uncover the island's backstory through environmental storytelling, collectible journal entries, and scripted NPC encounters woven into the level design
- **Hand-crafted level design** — each area of the island is individually designed with distinct biomes, puzzle layouts, and pacing beats to create a varied and memorable journey
- **Puzzle & interaction systems** — environmental puzzles (pressure plates, rotating mechanisms, hidden switches) gate progression and reward observant players without breaking immersion
- **Character controller & traversal** — responsive movement with climbing, swimming, and interaction prompts that feel natural across diverse terrain types
- **Dynamic lighting & atmosphere** — real-time Unity lighting, fog, and ambient audio adapt to the time-of-day cycle and story beats, reinforcing the mysterious island mood
- **Save & checkpoint system** — persistent save data records story progress, collected items, and explored areas, allowing players to resume exactly where they left off

**Architecture:** Unity scene-management system with a persistent `GameManager` that tracks global state; modular puzzle and trigger components communicate via C# events to keep level logic decoupled from core gameplay systems.

---

### 🎲 Unity Game Development Portfolio

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
| [AR Model Viewer](https://github.com/Superkart/ARModelViewer) | Mobile AR app placing a 3D AC motor model in augmented reality | Unity · C# |
<!-- UNITY-GAMES-END -->

---

### 💻 Learning & Practice Repositories

Structured, version-controlled practice documenting continuous growth:

<!-- LEARNING-REPOS-START -->
| Repo | Focus |
|---|---|
| [Python Journey](https://github.com/Superkart/Python_Journey) | Python fundamentals, YouTube tutorials, and LeetCode problems |
| [C++ Journey](https://github.com/Superkart/Cpp_Journey) | C++ from basics to advanced — OOP, memory management, STL |
| [Text-Based Game (C++)](https://github.com/Superkart/TextBasedGame_F) | Console RPG / adventure game written entirely in C++ |
<!-- LEARNING-REPOS-END -->

---

### 🌐 Web Projects

<!-- WEB-PROJECTS-START -->
| Repo | Description | Tech |
|---|---|---|
| [MyExpenseTracker](https://github.com/Superkart/MyExpenseTracker) | Personal finance tracking web app | TypeScript |
| [PortfolioApp](https://github.com/Superkart/PortfolioApp) | Personal portfolio website | JavaScript |
| [FirstWebAppDeployed](https://github.com/Superkart/FirstWebAppDeployed) | First deployed web application | Astro |
| [BasicCounterWebPage](https://github.com/Superkart/BasicCounterWebPage) | Interactive counter page | TypeScript |
| [hw5](https://github.com/Superkart/hw5) | — | TypeScript |
<!-- WEB-PROJECTS-END -->

---

### 🤖 ML & AI Projects

<!-- ML-AI-PROJECTS-START -->
| Repo | Description | Tech |
|---|---|---|
| [Applied-ML-Case-Studies](https://github.com/Superkart/Applied-ML-Case-Studies) | — | Jupyter Notebook |
| [DataScience1](https://github.com/Superkart/DataScience1) | This is a repository that contains the homework 1 of my Data Science class | HTML |
| [ML-Foundations-Python-Numpy](https://github.com/Superkart/ML-Foundations-Python-Numpy) | — | Jupyter Notebook |
| [ML-From-Scratch-Neural-Networks](https://github.com/Superkart/ML-From-Scratch-Neural-Networks) | — | Jupyter Notebook |
| [Student_Survey_Analysis](https://github.com/Superkart/Student_Survey_Analysis) | Data analysis project covering survey design, cleaning, and visualization | Python |
| [SQL_Hackathon](https://github.com/Superkart/SQL_Hackathon) | SQL-based hackathon and data analysis project for a database systems course | — |
<!-- ML-AI-PROJECTS-END -->

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
