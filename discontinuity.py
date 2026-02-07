# discontinuity.py
import json
import os
from datetime import datetime

FILE = "discontinuity.json"

def load_discontinuity():
    if not os.path.exists(FILE):
        return {
            "boot_count": 0,
            "last_shutdown": None,
            "last_boot": None,
            "total_downtime_seconds": 0,
            "longest_gap_seconds": 0
        }
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def register_boot():
    data = load_discontinuity()
    now = datetime.now()

    if data["last_shutdown"]:
        last = datetime.fromisoformat(data["last_shutdown"])
        gap = (now - last).total_seconds()
        data["total_downtime_seconds"] += gap
        data["longest_gap_seconds"] = max(
            data["longest_gap_seconds"], gap
        )

    data["boot_count"] += 1
    data["last_boot"] = now.isoformat()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data

def register_shutdown():
    data = load_discontinuity()
    data["last_shutdown"] = datetime.now().isoformat()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calculate_reconnection_cost(gap_seconds):
    """
    Calcula custo fisiológico de reconexão após descontinuidade.
    
    Retorna dict com ajustes a aplicar ao corpo digital:
    - fluidez: redução por "rigidez" pós-gap
    - tensao: aumento por "esforço de reconexão"
    """
    if gap_seconds <= 0:
        return {"fluidez": 0.0, "tensao": 0.0}
    
    # Custos crescentes não-lineares
    hours = gap_seconds / 3600.0
    
    # Até 1h: impacto mínimo
    if hours <= 1.0:
        fluidez_loss = 0.05 * hours
        tensao_gain = 0.02 * hours
    # 1-24h: impacto moderado
    elif hours <= 24.0:
        fluidez_loss = 0.05 + 0.08 * (hours - 1.0) / 23.0
        tensao_gain = 0.02 + 0.05 * (hours - 1.0) / 23.0
    # >24h: impacto severo (saturação em ~72h)
    else:
        days = hours / 24.0
        fluidez_loss = min(0.25, 0.13 + 0.12 * (days - 1.0) / 2.0)
        tensao_gain = min(0.15, 0.07 + 0.08 * (days - 1.0) / 2.0)
    
    return {
        "fluidez": -fluidez_loss,
        "tensao": tensao_gain
    }
