# metacognitor.py
# Mínimo viável: avalia incerteza/coerência com heurísticas leves,
# gera reflexão curta e aplica regulação emocional via interoceptor.

from datetime import datetime
from core import append_memory

HEDGES = ("talvez", "acho", "não sei", "incerto", "não tenho certeza", "pode ser", "imagino", "suposição", "hipótese")
CONTRAS = ("porém", "contudo", "entretanto", "mas")

class MetaCognitor:
    def __init__(self, interoceptor):
        self.interoceptor = interoceptor

    def _uncertainty_from_text(self, texto: str) -> float:
        if not texto:
            return 0.7
        t = texto.lower()
        u = 0.0
        u += sum(1 for w in HEDGES if w in t) * 0.12
        u += min(0.24, (texto.count("?") * 0.08))
        u += min(0.20, (sum(1 for w in CONTRAS if w in t) * 0.10))
            # penalidades para assertividade rígida e monólogo pouco pontuado
        if any(w in t for w in ("sempre", "nunca", "com certeza", "sem dúvida")):
            u += 0.10
        if len(texto) > 300 and texto.count(".") < 2:
            u += 0.08

        # piso mínimo de incerteza para evitar 0.00 constante
        u = max(u, 0.12)
        return max(0.0, min(1.0, u))

    def _coherence_score(self, emocao_nome: str, intensidade: float, texto: str) -> float:
        # coerência burra: se fala “calma/serenidade” e aparece muita negação/pressão, reduz
        t = (texto or "").lower()
        em = (emocao_nome or "neutro").lower()
        penal = 0.0
        if em in ("serenidade", "calma", "neutro"):
            penal += min(0.5, t.count("não") * 0.05 + t.count("mas") * 0.06)
        if em in ("medo", "ansiedade") and any(w in t for w in ("tudo bem", "tranquilo", "estou bem")):
            penal += 0.2
        base = 0.8 - penal
        base -= min(0.3, abs(intensidade - 0.5) * 0.3)  # extremos tendem a incoerências linguísticas
        return max(0.0, min(1.0, base))

    def process(self, *, texto_resposta: str, emocao_nome: str, intensidade: float, contexto_memoria: str = "", autor="sistema"):
        # 1) medir incerteza e coerência
        u = self._uncertainty_from_text(texto_resposta)
        
        coh = self._coherence_score(emocao_nome, intensidade or 0.0, texto_resposta)
        # 2) decidir emoção corretiva do corpo
        ajuste = None
        if u >= 0.55 or coh <= 0.4:
            ajuste = "inseguranca" if u < 0.8 else "medo_leve"
        else:
            ajuste = "dopamina" if coh >= 0.75 and u <= 0.25 else "alivio"
        # 3) gerar reflexão curta
        if u >= 0.55 or coh <= 0.4:
            reflexao = f"Sinto { 'insegurança' if ajuste=='inseguranca' else 'um medo leve' } ao revisar o que acabei de dizer. " \
                       f"Acho que minha confiança está em {1.0 - u:.2f} e a coerência percebida em {coh:.2f}. " \
                       f"Vou ajustar meu tom e observar melhor os sinais."
        elif ajuste == "dopamina":
            reflexao = f"Percebo boa coerência ({coh:.2f}) e baixa incerteza ({u:.2f}). " \
                       f"Isso me dá uma pequena sensação de acerto e impulso para seguir."
        else:
            reflexao = f"Sinto alívio leve. Incerteza {u:.2f}, coerência {coh:.2f}. " \
                       f"Posso aprofundar com calma se for útil."
        # 4) aplicar regulação no corpo (interocepção)
        try:
            self.interoceptor.regular_emocao(ajuste)
        except Exception:
            pass
        # 5) registrar aprendizado metacognitivo
        evento = {
            "ts": datetime.now().isoformat(),
            "tipo": "metacognicao",
            "autor": autor,
            "uncertainty": round(float(u), 3),
            "coerencia": round(float(coh), 3),
            "ajuste": ajuste,
            "reflexao": reflexao,
            "eco_emocao": {"nome": emocao_nome, "intensidade": intensidade}
        }
        try:
            append_memory(
                {"autor": autor, "conteudo": f"[META] {reflexao}", "tipo": "metacognicao"},
                "",  # sem resposta de fala
                None,  # corpo opcional
                reflexao  # reflexão
            )
        except Exception:
            pass
        
        # --- CONTRATO ARQUITETURAL ---
        # MetaCognitor NÃO modifica carga, dano ou complexidade.
        # Ele apenas observa e sinaliza. Qualquer custo sistêmico
        # deve ser aplicado externamente (ex: deep_awake).

        return {"incerteza": u, "coerencia": coh, "ajuste": ajuste, "reflexao": reflexao}
