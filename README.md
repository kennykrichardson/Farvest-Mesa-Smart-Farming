# 🌱🚜 Farvest 2.0

### 🌾 A Smart Farming Simulation Powered by Mesa, FastAPI, and React ⚡

Farvest is an interactive **🌱 smart farming simulation** built around a Python-based agricultural environment. It combines **Mesa's agent-based simulation engine 🤖** with a **FastAPI backend ⚡** and a **React + TypeScript operations console 🖥️**.

The project separates simulation logic, API communication, and visualization into independent layers, creating a cleaner architecture for observing, monitoring, and interacting with a simulated farm. 🌍

---

## ✨🌿 Overview

Farvest 2.0 introduces a decoupled architecture designed to bring together agricultural simulation, backend processing, and interactive visualization.

| 🧩 Layer | 🛠️ Technology | 🎯 Responsibility |
|---|---|---|
| 🌾 Simulation | Python, Mesa 3.5 | Farm simulation and agent behavior |
| ⚡ API | FastAPI | Simulation state and control endpoints |
| 🖥️ Frontend | React, TypeScript, Vite | Interactive farm operations console |

The Mesa model remains the **single source of truth** for simulation state. The frontend communicates with it through the FastAPI service.

The original Solara interface is no longer used by the React frontend. 🔄

## 🚜✨ Features

### 🌳 Interactive Farm Visualization

- 🟩 Native React-based farm grid.
- 🌱 Visual representation of crops and farmers.
- 🔍 Select individual crops to inspect their state.
- 🎨 Switch between crop-stage, water-stress, and crop-health visualization layers.

### 🎮 Simulation Controls

- ⏩ Advance the simulation by one day.
- 📅 Run multiple simulation days in a batch.
- ⏸️ Pause the simulation.
- ▶️ Resume the simulation.
- 🔄 Reset the simulation with a configurable seed.

### 📊 Farm Monitoring

- 🌾 Monitor crop population and survival.
- ❤️ Observe farm health.
- 💧 Track water-related metrics.
- 🧺 Monitor harvest-related statistics.
- 🌤️ View weather conditions.
- 📜 Inspect recent simulation events.

### 📈 Historical Metrics

- 🌱 View historical crop growth measurements.
- 💧 Track historical water measurements.
- ❤️ Monitor historical crop health.
- 🗃️ Retain up to 120 daily snapshots in backend memory.
- 🔄 Automatically refresh dashboard data every 2.5 seconds.

## 🧰💻 Technology Stack

### ⚙️ Backend

- 🐍 Python 3.12
- 🤖 Mesa 3.5
- ⚡ FastAPI
- 🚀 Uvicorn
- 📦 Pydantic

### 🎨 Frontend

- ⚛️ React
- 🔷 TypeScript
- ⚡ Vite
- 📊 Recharts
- 🎯 Lucide React

## 🏗️🧬 Architecture

Farvest follows a layered architecture that separates the simulation engine from the API and user interface.

```text
🌱 Farvest/
│
├── backend/
│   ├── api.py
│   ├── Model.py
│   ├── Crop.py
│   ├── Farmer.py
│   ├── Field.py
│   ├── FarmManager.py
│   ├── Irrigation.py
│   ├── Weather.py
│   ├── Scheduler.py
│   ├── Constants.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   └── types.ts
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── README.md
├── LICENSE
└── .gitignore
```

### 🔄 How It Works

The frontend communicates with FastAPI through HTTP requests, while the backend interacts with the Mesa simulation to retrieve and update farm state.

```text
┌──────────────────────────────┐
│        React Frontend        │
│                              │
│   Farm Grid ·  Metrics       │
│          Controls            │
└──────────────┬───────────────┘
               │
               │  HTTP / JSON
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│                              │
│    State ·  Controls         │
│           API                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Mesa Simulation       │
│                              │
│   Crops ·  Farmers           │
│   Weather ·  Irrigation      │
│        Farm Systems          │
└──────────────────────────────┘
```

## ⚙️🚀 Installation

### 📋 Prerequisites

Make sure the following are installed:

- 🐍 Python 3.12
- 🟢 Node.js 20 or later
- 📦 npm
- 💻 PowerShell (for the Windows commands below)

### 1️⃣ 📥 Clone the Repository

```bash
git clone https://github.com/kennykrichardson/Farvest.git
cd Farvest
```

### 2️⃣ ⚙️ Configure the Backend

Open a terminal in the project directory:

```powershell
cd backend

# 🐍 Create a virtual environment
py -3.12 -m venv .venv

# ⚡ Activate the environment
.\.venv\Scripts\Activate.ps1

# 📦 Upgrade pip
python -m pip install --upgrade pip

# 📥 Install dependencies
python -m pip install -r requirements.txt
```

### 🚀 Start the Simulation API

```powershell
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

The backend should now be accessible at:

- 🌐 API: http://127.0.0.1:8000
- 💚 Health Check: http://127.0.0.1:8000/api/health
- 📚 Interactive API Documentation: http://127.0.0.1:8000/docs

### 3️⃣ 🖥️ Configure the Frontend

Open a second terminal:

```powershell
cd frontend

# 📦 Install dependencies
npm install

# 🚀 Start the development server
npm run dev
```

### 🌍 Open Farvest

**http://localhost:5173**

Both services must be running for the frontend to communicate with the simulation. 🔗

## 🔌📡 API Reference

Farvest exposes the following endpoints through FastAPI:

| 🔧 Method | 📍 Endpoint | 📝 Description |
|---|---|---|
| 🟢 GET | `/api/health` | Check backend availability |
| 🟢 GET | `/api/snapshot` | Retrieve the current farm state |
| 🔵 POST | `/api/simulation/step` | Advance one simulation step |
| 🔵 POST | `/api/simulation/batch` | Advance multiple simulation days |
| 🔵 POST | `/api/simulation/pause` | Pause the simulation |
| 🔵 POST | `/api/simulation/resume` | Resume the simulation |
| 🔵 POST | `/api/simulation/reset` | Reset the simulation |
| 🔵 POST | `/api/irrigation/toggle` | Toggle irrigation |

### 📅 Example Request: Advance Five Days

```json
{
  "days": 5
}
```

### 🔄 Example Request: Reset with a Seed

```json
{
  "seed": 42
}
```

## 📊🌾 Simulation Data

The frontend retrieves simulation snapshots from the backend.

The dashboard includes:

- 🏡 Farm metadata and simulation status.
- 🌤️ Weather conditions.
- 🌱 Crop state and spatial coordinates.
- 👨‍🌾 Farmer state and spatial coordinates.
- 📈 Farm-level performance metrics.
- 📜 Recent simulation events.
- 📉 Historical growth, water, and health measurements.

The backend maintains a single in-memory simulation instance. 🧠

### ⚠️ Important Runtime Notes

- 🔄 Restarting the backend resets the in-memory simulation.
- 🧹 Resetting the simulation also resets its historical metrics.
- 🗃️ Historical metrics are limited to the latest 120 daily snapshots.
- ⏱️ Dashboard polling occurs every 2.5 seconds.
- 🎮 Simulation time advances through operator controls, not through dashboard polling.

## 🛠️🐛 Troubleshooting

### 🔌 Frontend Cannot Connect to the Backend

1. Confirm the FastAPI server is running.
2. Open `http://127.0.0.1:8000/api/health`.
3. Check that the frontend is using the correct API URL.

### 🐍 Python Dependency Errors

Ensure the virtual environment is activated and dependencies are installed:

```powershell
python -m pip install -r requirements.txt
```

### 📦 Frontend Dependency or Build Errors

From the `frontend/` directory:

```powershell
npm install
npm run build
```

### 🚧 Port Conflicts

If either development server's default port is occupied, stop the conflicting process or configure an available port.

## 📜⚖️ License

Farvest is distributed under the **MIT License**.

You are free to use, modify, distribute, and build upon the project under the terms of the license.

See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>🌱 FARVEST 2.0 🚜</strong>
  <br/>
  <em>Simulating smarter agriculture, one day at a time. 🌍</em>
  <br/><br/>
  🌾 💧 🌱 🤖 🚜
</p>