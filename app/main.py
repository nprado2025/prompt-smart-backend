from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI(title="Prompt Smart Backend")

# ⚠️ TEMPORÁRIO: em memória
TRIALS = {}

TRIAL_DAYS = 30

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.post("/app/status")
def app_status(payload: dict):
    device_id = payload.get("device_id")

    if not device_id:
        return {"error": "device_id obrigatório"}

    now = datetime.utcnow()

    # Primeiro acesso
    if device_id not in TRIALS:
        TRIALS[device_id] = {
            "started_at": now,
            "ends_at": now + timedelta(days=TRIAL_DAYS)
        }

    trial = TRIALS[device_id]
    days_left = (trial["ends_at"] - now).days

    if now <= trial["ends_at"]:
        return {
            "trial": {
                "active": True,
                "days_left": max(days_left, 0)
            },
            "features": {
                "simple": True,
                "intermediate": True,
                "extended": True
            },
            "auth": {
                "login_required": False
            },
            "billing": {
                "subscription_required": False
            },
            "message": "Trial ativo"
        }

    # Trial expirado
    return {
        "trial": {
            "active": False,
            "days_left": 0
        },
        "features": {
            "simple": True,
            "intermediate": False,
            "extended": False
        },
        "auth": {
            "login_required": True
        },
        "billing": {
            "subscription_required": True
        },
        "message": "Trial encerrado. Faça login para desbloquear."
    }
