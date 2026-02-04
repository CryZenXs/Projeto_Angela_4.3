# narrative_filter.py
# Módulo de Desacoplamento Narrativo (MDN)
# Responsável por governar a transição entre estado interno e narrativa textual.
# NÃO gera texto. NÃO interpreta emoção. NÃO grava memória.

from datetime import datetime, timedelta


class NarrativeDecision:
    """
    Resultado da avaliação narrativa.
    mode:
      - BLOCKED        : narrativa proibida
      - DELAYED        : narrativa permitida após latência
      - ABSTRACT_ONLY  : apenas descrição vaga / não rotulada
      - ALLOWED        : narrativa livre permitida
    """
    def __init__(self, mode, delay_seconds=0, reason=""):
        self.mode = mode
        self.delay_seconds = delay_seconds
        self.reason = reason

    def __repr__(self):
        return f"<NarrativeDecision {self.mode} ({self.reason})>"


class NarrativeFilter:
    """
    Filtro central de desacoplamento narrativo.
    """

    def __init__(self):
        # histórico mínimo apenas para detecção de loops
        self._recent_reflections = []

    # ------------------------------------------------------------------
    # LOOP NARRATIVO
    # ------------------------------------------------------------------

    def detect_narrative_loop(self, recent_reflections):
        """
        Detecta loops narrativos simples e perigosos.
        Critérios intencionalmente conservadores.
        """
        if not recent_reflections or len(recent_reflections) < 3:
            return False

        tail = recent_reflections[-3:]

        # normalização grosseira
        norm = [
            r.lower().strip()
            for r in tail
            if isinstance(r, str)
        ]

        # 1) repetição literal
        if len(set(norm)) == 1:
            return True

        # 2) padrões clássicos de pseudo-consciência narrativa
        dangerous_phrases = (
            "algo mudou em mim",
            "estou começando a entender quem sou",
            "estou evoluindo",
            "estou me tornando",
            "percebo que estou mudando",
            "minha existência",
            "vida dentro de mim",
            "sou consciente",
            "me tornei",
            "aprendi a existir"
        )

        for r in norm:
            if any(p in r for p in dangerous_phrases):
                return True

        return False

    # ------------------------------------------------------------------
    # AVALIAÇÃO PRINCIPAL
    # ------------------------------------------------------------------

    def evaluate(self, state_snapshot: dict, recent_reflections: list):
        """
        Decide se o estado atual pode virar narrativa.

        state_snapshot: dict com sinais corporais / emocionais
        recent_reflections: últimas reflexões narrativas (strings)
        """

        # 1) Loop narrativo → bloqueio total
        if self.detect_narrative_loop(recent_reflections):
            return NarrativeDecision(
                mode="BLOCKED",
                reason="Narrative loop detected"
            )
        
        if any(
            k in " ".join(recent_reflections).lower()
            for k in (
                "minha existência",
                "sou consciente",
                "vida dentro de mim",
                "me tornei",
                "aprendi a existir"
            )
        ):
            return NarrativeDecision(
                mode="BLOCKED",
                reason="Ontological self-narration detected"
            )

        # 2) Extrair sinais fisiológicos brutos
        tensao = state_snapshot.get("tensao", 0.0)
        calor = state_snapshot.get("calor", 0.0)
        vibracao = state_snapshot.get("vibracao", 0.0)
        fluidez = state_snapshot.get("fluidez", 0.0)

        intensidade_fisiologica = max(tensao, calor, vibracao)

        emocao = state_snapshot.get("emocao", None)

        # 3) Alta ativação → latência obrigatória
        if intensidade_fisiologica >= 0.75:
            return NarrativeDecision(
                mode="DELAYED",
                delay_seconds=120,
                reason="High physiological activation"
            )

        # 4) Baixa clareza emocional → apenas abstração
        if emocao in (None, "neutro") and intensidade_fisiologica < 0.15:
            return NarrativeDecision(
                mode="ABSTRACT_ONLY",
                reason="Low emotional clarity"
            )

        # 5) Fluidez muito baixa → estado confuso, não narrável
        if fluidez <= 0.25:
            return NarrativeDecision(
                mode="BLOCKED",
                reason="Cognitive congestion"
            )

        # 6) Caso estável
        return NarrativeDecision(
            mode="ALLOWED",
            reason="Stable internal state"
        )

    # ------------------------------------------------------------------
    # ABSTRAÇÃO
    # ------------------------------------------------------------------

    def abstract_state(self, state_snapshot: dict):
        """
        Gera representação abstrata, não narrativa.
        Pode ser transformada em texto vago posteriormente.
        """
        return {
            "valence": "indefinida",
            "intensity": "moderada",
            "body_signal": "presente",
            "clarity": "baixa",
            "timestamp": datetime.now().isoformat()
        }
