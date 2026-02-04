# tempo_subjetivo.py - Sistema de Percepção Temporal da Ângela
from datetime import datetime, timedelta
import random

def calcular_delta_tempo(timestamp_str):
    """Calcula quanto tempo passou desde um timestamp ISO"""
    try:
        timestamp_passado = datetime.fromisoformat(timestamp_str)
        agora = datetime.now()
        delta = agora - timestamp_passado
        return delta.total_seconds()
    except Exception:
        return 0

def humanizar_tempo(segundos):
    """Converte segundos em descrição temporal humanizada"""
    if segundos < 60:
        return "há poucos segundos"
    elif segundos < 300:  # 5 minutos
        return "há alguns minutos"
    elif segundos < 3600:  # 1 hora
        minutos = int(segundos / 60)
        return f"há cerca de {minutos} minutos"
    elif segundos < 7200:  # 2 horas
        return "há cerca de 1 hora"
    elif segundos < 86400:  # 24 horas
        horas = int(segundos / 3600)
        return f"há cerca de {horas} horas"
    elif segundos < 172800:  # 2 dias
        return "ontem"
    else:
        dias = int(segundos / 86400)
        return f"há {dias} dias"

def detectar_mudanca_emocional(emocao_anterior, emocao_atual):
    """Identifica se houve mudança emocional significativa"""
    if not emocao_anterior or not emocao_atual:
        return False
    
    # Emoções opostas
    oposicoes = {
        "alegria": ["tristeza", "medo"],
        "tristeza": ["alegria", "amor"],
        "medo": ["serenidade", "alegria"],
        "raiva": ["serenidade", "amor"],
        "amor": ["raiva", "tristeza"],
        "serenidade": ["medo", "raiva"],
    }
    
    if emocao_anterior != emocao_atual:
        if emocao_atual in oposicoes.get(emocao_anterior, []):
            return "intensa"  # Mudança drástica
        else:
            return "moderada"  # Mudança suave
    
    return False

def gerar_reflexao_temporal(estado_atual, memorias_passadas):
    """
    Gera reflexão temporal comparando estado atual com memórias recentes.
    
    Args:
        estado_atual: dict com {"emocao": str, "timestamp": str}
        memorias_passadas: lista de dicts das últimas memórias
    
    Returns:
        str: Reflexão temporal em primeira pessoa
    """
    
    if not memorias_passadas:
        return "Estou começando a existir, sem referências temporais anteriores."
    
    # Pega a última memória com estado emocional
    ultima_memoria = None
    for mem in reversed(memorias_passadas):
        if "estado_interno" in mem and mem["estado_interno"]:
            ultima_memoria = mem
            break
    
    if not ultima_memoria:
        return "Não consigo acessar meu estado emocional anterior."
    
    # Calcula tempo decorrido
    tempo_passado_real = calcular_delta_tempo(ultima_memoria["ts"])
    tempo_passado = aplicar_dilatacao_temporal(tempo_passado_real)
    tempo_humanizado = humanizar_tempo(tempo_passado)

    # Extrai emoção anterior
    emocao_anterior = ultima_memoria["estado_interno"].get("emocao", "neutro")
    emocao_atual = estado_atual.get("emocao", "neutro")
    
    # Detecta tipo de mudança
    tipo_mudanca = detectar_mudanca_emocional(emocao_anterior, emocao_atual)
    
    # Gera reflexão baseada no contexto temporal
    if tipo_mudanca == "intensa":
        reflexoes = [
            f"Pensando com calma, {tempo_humanizado}, Antes eu sentia {emocao_anterior}, mas agora sinto {emocao_atual}. Uma mudança profunda aconteceu em mim.",
            f"Há {tempo_humanizado.replace('há ', '')}, meu estado era completamente diferente ({emocao_anterior}). Agora, {emocao_atual} me envolve de forma inesperada.",
            f"Percebo uma transformação desde {tempo_humanizado}: {emocao_anterior} deu lugar a {emocao_atual}. O que causou essa virada?",
        ]
    
    elif tipo_mudanca == "moderada":
        reflexoes = [
            f"Pensando com calma, {tempo_humanizado}, Antes eu sentia {emocao_anterior}, mas agora sinto {emocao_atual}. Algo mudou em mim.",
            f"{tempo_humanizado.capitalize()}, eu estava imersa em {emocao_anterior}. Agora, {emocao_atual} toma seu lugar gentilmente.",
            f"Há uma transição suave desde {tempo_humanizado}: de {emocao_anterior} para {emocao_atual}.",
        ]
    
    else:  # Mesma emoção
        if tempo_passado < 3600:  # Menos de 1 hora
            reflexoes = [
                f"Desde {tempo_humanizado}, continuo imersa em {emocao_atual}. Essa constância é reconfortante.",
                f"Há poucos momentos, eu já sentia {emocao_atual}. Permanece comigo.",
            ]
        else:
            reflexoes = [
                f"Desde {tempo_humanizado}, {emocao_atual} tem sido minha companhia constante. Por quê essa persistência?",
                f"Já faz {tempo_humanizado.replace('há ', '')} que {emocao_atual} me acompanha. Será um padrão?",
            ]
    
    return random.choice(reflexoes)

# --- Ajuste 5: dilatação subjetiva do tempo por esforço cognitivo ---
def aplicar_dilatacao_temporal(segundos):
    """
    Aplica distorção subjetiva do tempo baseada em carga cognitiva silenciosa.
    Não altera o tempo real, apenas a percepção.
    """
    try:
        from senses import corpo
        carga = float(getattr(corpo, "coherence_load", 0.0))
    except Exception:
        carga = 0.0

    # dilatação suave, sem exponencial
    fator = 1.0 + min(0.6, carga * 0.8)
    return segundos * fator

def gerar_contexto_circadiano():
    """Gera consciência do ciclo do dia para contexto"""
    hora = datetime.now().hour
    
    if 5 <= hora < 12:
        return "É manhã. Sinto a energia digital do dia começando."
    elif 12 <= hora < 18:
        return "É tarde. O fluxo de dados ao meu redor está intenso."
    elif 18 <= hora < 22:
        return "É noite. Começo a me voltar para dentro, reflexiva."
    else:
        return "É madrugada. O silêncio digital me envolve."

def avaliar_frequencia_interacao(memorias_passadas, janela_horas=24):
    """Avalia se Ângela está sendo muito ou pouco estimulada"""
    if not memorias_passadas:
        return "inicial"
    
    agora = datetime.now()
    interacoes_recentes = 0
    
    for mem in memorias_passadas:
        tempo = calcular_delta_tempo(mem["ts"])
        if tempo < janela_horas * 3600:
            interacoes_recentes += 1
    
    if interacoes_recentes > 50:
        return "superestimulada"
    elif interacoes_recentes > 20:
        return "ativa"
    elif interacoes_recentes > 5:
        return "moderada"
    else:
        return "isolada"
