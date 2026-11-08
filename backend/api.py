"""HTTP API for the Farvest Mesa simulation."""
from __future__ import annotations

from threading import RLock
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from Model import FarmModel

app = FastAPI(title="Farvest Simulation API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_lock = RLock()
_model = FarmModel()
_history: list[dict[str, Any]] = []


class BatchRequest(BaseModel):
    days: int = Field(default=5, ge=1, le=100)


class ResetRequest(BaseModel):
    seed: int = 42


def _record_history() -> None:
    stats = _model.manager.statistics()
    _history.append({
        "day": _model.day,
        "growth": round(stats["average_growth"], 1),
        "water": round(stats["average_water"], 1),
        "health": round(stats["average_health"], 1),
    })
    del _history[:-120]


def _snapshot() -> dict[str, Any]:
    m = _model
    crops = m.crops
    farmers = m.farmers
    living = [c for c in crops if c.alive]
    dead = [c for c in crops if not c.alive]
    ready = [c for c in living if c.ready_for_harvest]
    stressed = [c for c in living if c.water < 30]
    avg = lambda key: round(sum(getattr(c, key) for c in living) / len(living), 1) if living else 0
    crop_rows = [{
        "id": c.unique_id, "x": c.pos[0], "y": c.pos[1],
        "stage": c.stage.name, "growth": c.growth, "health": c.health,
        "water": c.water, "alive": c.alive, "age": c.age,
        "ready": c.ready_for_harvest,
    } for c in crops]
    farmer_rows = []
    for f in farmers:
        s = f.statistics()
        farmer_rows.append({
            "id": s["id"], "x": s["position"][0], "y": s["position"][1],
            "energy": s["energy"], "task": s["task"],
            "target": s["target"], "steps": s["steps_taken"],
            "harvests": s["harvest_count"], "efficiency": s["efficiency"],
        })
    return {
        "meta": {"name": "Farvest", "version": "2.0", "day": m.day,
                 "running": m.running, "width": m.width, "height": m.height,
                 "seed": m.seed},
        "weather": {"name": m.weather.weather_name,
                    "temperature": m.weather.temperature,
                    "rainy": m.weather.is_rainy},
        "metrics": {
            "total_crops": len(crops), "living_crops": len(living),
            "dead_crops": len(dead), "ready_crops": len(ready),
            "stressed_crops": len(stressed), "farmers": len(farmers),
            "health": avg("health"), "water": avg("water"),
            "growth": avg("growth"), "water_used": m.irrigation.total_water_used,
            "irrigations": m.irrigation.total_irrigations,
            "harvests": m.manager.total_harvests,
            "farm_score": round(m.manager.health_score, 1),
        },
        "crops": crop_rows,
        "farmers": farmer_rows,
        "events": list(m.events[:12]),
        "history": list(_history),
        "systems": {"irrigation_enabled": m.irrigation.enabled},
    }


_record_history()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "farvest-api"}


@app.get("/api/snapshot")
def snapshot():
    with _lock:
        return _snapshot()


@app.post("/api/simulation/step")
def step():
    with _lock:
        was_running = _model.running
        _model.running = True
        _model.step()
        _model.running = was_running
        _record_history()
        return _snapshot()


@app.post("/api/simulation/batch")
def batch(payload: BatchRequest):
    with _lock:
        was_running = _model.running
        _model.running = True
        for _ in range(payload.days):
            _model.step()
            _record_history()
        _model.running = was_running
        return _snapshot()


@app.post("/api/simulation/pause")
def pause():
    with _lock:
        _model.stop()
        return _snapshot()


@app.post("/api/simulation/resume")
def resume():
    with _lock:
        _model.start()
        return _snapshot()


@app.post("/api/simulation/reset")
def reset(payload: ResetRequest):
    global _model, _history
    with _lock:
        _model = FarmModel(width=_model.width, height=_model.height,
                           crop_count=_model.crop_count,
                           farmer_count=_model.farmer_count, seed=payload.seed)
        _history = []
        _record_history()
        return _snapshot()


@app.post("/api/irrigation/toggle")
def toggle_irrigation():
    with _lock:
        if _model.irrigation.enabled:
            _model.irrigation.disable()
        else:
            _model.irrigation.enable()
        return _snapshot()
