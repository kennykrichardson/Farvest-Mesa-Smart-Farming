# 🌾 Farvest

> **An intelligent Smart Farming simulation built with Mesa 3.5.1.**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Mesa](https://img.shields.io/badge/Mesa-3.5.1-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 🌱 Overview

Farvest is an **Agent-Based Smart Farming Simulation** that models crop growth, weather systems, irrigation, and autonomous farmers using **Mesa 3.5.1**.

Rather than scripting every action, Farvest allows intelligent agents to interact with their environment, creating an evolving farm ecosystem.

---

# ✨ Features

🌾 Crop Growth Simulation

👨‍🌾 Autonomous Farmers

🌦 Dynamic Weather System

💧 Intelligent Irrigation

🗺 2D Farm Grid

🧠 Agent-Based AI

📊 Live Simulation Dashboard *(In Progress)*

📈 Farm Statistics

🔄 Continuous Simulation

⚡ Mesa 3.5.1 Native

---

# 🧩 Simulation Components

## 🌾 Crops

- Seed lifecycle
- Water consumption
- Growth stages
- Harvest readiness
- Health tracking

---

## 👨‍🌾 Farmers

- Autonomous movement
- Crop inspection
- Watering
- Harvesting
- Energy management
- Intelligent target selection

---

## 🌦 Weather

- ☀️ Sunny
- ☁️ Cloudy
- 🌧 Rainy

Weather directly influences crop growth and irrigation.

---

## 💧 Irrigation

- Farm irrigation system
- Configurable water amount
- Rain integration
- Water usage statistics

---

# 🌱 Crop Lifecycle

```text
🌰 Seed
      ↓
🌿 Sprout
      ↓
🌱 Growing
      ↓
🌾 Ready
      ↓
🚜 Harvest
      ↓
🌰 Replanted
```

---

# 🧠 AI Philosophy

Farvest follows a **task-driven simulation**.

Instead of hardcoded sequences, autonomous farmers observe the world, choose work that matters, and react dynamically to changing farm conditions.

Future versions will include:

- 📋 Job Assignment
- 🤝 Cooperative Farmers
- 🚜 Tractors
- 🌱 Multiple Crop Types
- 🌡 Soil Quality
- 🦠 Diseases
- 🐦 Wildlife
- 📦 Storage
- 📈 Economy

---

# 📂 Project Structure

```
Farvest/

│
├── Main.py
├── Model.py
├── Field.py
├── Scheduler.py
├── Renderer.py
│
├── Crop.py
├── Farmer.py
│
├── FarmManager.py
├── Irrigation.py
├── Weather.py
│
├── Constants.py
├── Utils.py
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 🚀 Installation

```bash
git clone https://github.com/kennykrichardson/Farvest-Mesa-Smary-Farming.git

cd Farvest

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

# ▶️ Run

```bash
solara run Main.py
```

Open:

```
http://localhost:8765
```

---

# 🎯 Roadmap

## ✅ Phase 1

- Grid
- Crop System
- Weather
- Irrigation
- Farmers
- Mesa Migration

---

## 🚧 Phase 2

- Smarter Farmer AI
- Task Assignment
- Dashboard
- Live Charts
- Better Rendering

---

## 🌎 Phase 3

- Economy
- Seasons
- Marketplace
- Livestock
- Storage
- Multiple Farms

---

# 📊 Technologies

🐍 Python

🌾 Mesa 3.5.1

⚛️ Solara

📈 Agent-Based Modeling

🧠 Artificial Intelligence

---

# 🤝 Contributing

Contributions, ideas, and improvements are welcome.

Open an issue or submit a pull request.

---

# 👨‍💻 Author

**Kenny Richardson Kodipally**

Engineer • AI Developer • Simulation Enthusiast

---

# 🌟 Vision

Farvest isn't just a farming simulator.

It's the foundation for an intelligent agricultural ecosystem where autonomous agents collaborate, adapt, and learn from a living environment.

The long-term goal is to evolve Farvest into a research-quality agent-based simulation for smart agriculture and AI experimentation.

---

⭐ If you enjoyed this project, consider starring the repository!
