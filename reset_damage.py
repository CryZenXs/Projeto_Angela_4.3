#!/usr/bin/env python3
"""
Script de Emergência: Reset de Damage Cognitivo
Uso: python reset_damage.py [--level VALOR]

ATENÇÃO: Use apenas em casos de damage causado por bugs, não por uso normal!
"""

import json
import os
import sys
from datetime import datetime

DAMAGE_FILE = "friction_damage.persistent"

def reset_damage(target_level=0.0, reason="manual_reset"):
    """
    Reseta damage para um nível específico.
    
    Args:
        target_level: Nível de damage desejado (0.0 = completamente limpo)
        reason: Razão do reset (para auditoria)
    """
    if not os.path.exists(DAMAGE_FILE):
        print(f"❌ Arquivo {DAMAGE_FILE} não encontrado!")
        return False
    
    # Carrega estado atual
    with open(DAMAGE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    old_damage = data.get("damage", 0.0)
    old_load = data.get("load", 0.0)
    
    print(f"📊 Estado atual:")
    print(f"   Damage: {old_damage:.4f}")
    print(f"   Load: {old_load:.4f}")
    print(f"   Chronic: {data.get('chronic', False)}")
    print(f"   Sessions: {data.get('total_sessions', 0)}")
    
    # Pede confirmação se damage for alto
    if old_damage > 0.5:
        print(f"\n⚠️  Damage está muito alto ({old_damage:.4f})!")
        print("   Isso pode indicar bug ou uso extremo.")
        confirm = input("   Confirmar reset? (sim/não): ").lower()
        if confirm not in ("sim", "s", "yes", "y"):
            print("❌ Reset cancelado.")
            return False
    
    # Aplica reset
    data["damage"] = float(target_level)
    data["load"] = max(0.0, old_load * 0.5)  # Reduz load pela metade
    data["chronic"] = False if target_level < 0.35 else data["chronic"]
    data["last_updated"] = datetime.now().isoformat()
    data["reset_history"] = data.get("reset_history", [])
    data["reset_history"].append({
        "timestamp": datetime.now().isoformat(),
        "old_damage": old_damage,
        "new_damage": target_level,
        "reason": reason
    })
    
    # Salva
    with open(DAMAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Reset aplicado:")
    print(f"   Damage: {old_damage:.4f} → {target_level:.4f}")
    print(f"   Load: {old_load:.4f} → {data['load']:.4f}")
    print(f"   Razão: {reason}")
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Reset de damage cognitivo (emergência)"
    )
    parser.add_argument(
        "--level",
        type=float,
        default=0.0,
        help="Nível de damage alvo (0.0 = limpo, padrão: 0.0)"
    )
    parser.add_argument(
        "--reason",
        type=str,
        default="manual_reset",
        help="Razão do reset (para auditoria)"
    )
    
    args = parser.parse_args()
    
    if args.level < 0.0 or args.level > 1.0:
        print("❌ Erro: --level deve estar entre 0.0 e 1.0")
        sys.exit(1)
    
    success = reset_damage(args.level, args.reason)
    sys.exit(0 if success else 1)
