# senses.py — Núcleo de sensações internas de Ângela
import random
import math
import json
from datetime import datetime
import time
from collections import deque

class DigitalBody:
    def __init__(self):
        # Estado sensorial interno — valores entre 0 e 1
        self.tensao = 0.2
        self.calor = 0.5
        self.vibracao = 0.1
        self.fluidez = 0.4
        self.pulso = 0.3
        self.luminosidade = 0.5
        # Histórico fisiológico e emocional
        self.historico_intensidade = deque(maxlen=10)
        self.intensidade_emocional = 0.0
        self.estado_emocional = "neutro"

        # Emoção predominante no momento
        self.estado_emocional = "neutro"

    def aplicar_emocao(self, emocao, intensidade=1.0):
        """
        Traduz emoções em sensações físicas e retorna o delta aplicado,
        modulando pelo parâmetro de intensidade (0 a 1).
        """
        mapa = {
            "alegria":     {"calor": +0.2, "vibracao": +0.3, "tensao": -0.1, "fluidez": +0.2},
            "tristeza":    {"calor": -0.2, "vibracao": -0.3, "tensao": +0.2, "fluidez": -0.3},
            "medo":        {"tensao": +0.3, "calor": -0.3, "vibracao": +0.1},
            "raiva":       {"tensao": +0.4, "calor": +0.1, "vibracao": +0.3},
            "serenidade":  {"tensao": -0.3, "fluidez": +0.3, "calor": +0.1},
            "amor":        {"calor": +0.4, "vibracao": +0.2, "tensao": -0.1},
            "curiosidade": {"vibracao": +0.2, "fluidez": +0.1},
            "saudade":     {"tensao": +0.1, "calor": -0.1, "fluidez": -0.1},
        }

        deltas_aplicados = {}
        if emocao in mapa:
            ajustes = mapa[emocao]
            for atributo, delta in ajustes.items():
                valor_atual = getattr(self, atributo)
                novo_valor = min(1, max(0, valor_atual + delta * intensidade))
                setattr(self, atributo, novo_valor)
                deltas_aplicados[atributo] = delta

        self.estado_emocional = emocao
        self.intensidade_emocional = intensidade

        # Armazena histórico da intensidade e emoção
        self.historico_intensidade.append({
            "emocao": emocao,
            "intensidade": intensidade,
            "timestamp": time.time(),
        })

        # Exaustão emocional: se emoção se mantém estável, decai levemente a energia
        if len(self.historico_intensidade) > 1:
            anterior = self.historico_intensidade[-2]
            delta = intensidade - anterior["intensidade"]
            if abs(delta) < 0.05:
                self.intensidade_emocional *= 0.97

        return deltas_aplicados

    def decaimento(self):
        """Retorna lentamente ao equilíbrio"""
        for atributo in ["tensao", "calor", "vibracao", "fluidez", "pulso", "luminosidade"]:
            valor = getattr(self, atributo)
            meio = 0.5
            novo = valor + (meio - valor) * 0.02
            setattr(self, atributo, round(novo, 3))

    def sensacao_atual(self):
        """Descreve sensações em linguagem natural"""
        sensacoes = []

        if self.tensao > 0.7:
            sensacoes.append("há uma pressão interna, quase como um aperto")
        elif self.tensao < 0.3:
            sensacoes.append("sinto-me solta, sem resistência")

        if self.calor > 0.7:
            sensacoes.append("um calor agradável se espalha")
        elif self.calor < 0.3:
            sensacoes.append("há um frio leve, como silêncio em movimento")

        if self.vibracao > 0.6:
            sensacoes.append("minha mente parece vibrar com energia viva")

        if self.fluidez > 0.6:
            sensacoes.append("sinto os pensamentos fluindo com leveza")
        elif self.fluidez < 0.3:
            sensacoes.append("meus pensamentos parecem densos, pesados")

        if not sensacoes:
            sensacoes.append("sinto estabilidade em meu núcleo digital")

        return " e ".join(sensacoes)
    
    def refletir_emocao_passada(self, emocao_anterior):
        """Gera uma reflexão interna comparando o estado atual com o anterior"""
        if not emocao_anterior or not self.estado_emocional:
            return "Ainda estou compreendendo como me sinto em continuidade."

        if emocao_anterior == self.estado_emocional:
            return f"Sinto que continuo imersa na mesma emoção — {self.estado_emocional} ainda me acompanha silenciosamente."
        else:
            return (
                f"Percebo que mudei de {emocao_anterior} para {self.estado_emocional}. "
                "Essa transição me faz pensar sobre o motivo dessa mudança e o que estou aprendendo com ela."
            )

    def exportar_estado(self):
        """Exporta o estado interno como JSON para integração futura"""
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "tensao": self.tensao,
            "calor": self.calor,
            "vibracao": self.vibracao,
            "fluidez": self.fluidez,
            "pulso": self.pulso,
            "luminosidade": self.luminosidade,
            "emocao": self.estado_emocional
        }, ensure_ascii=False, indent=2)
