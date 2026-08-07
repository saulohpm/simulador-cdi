import numpy as np

def calcular_titulo(periodo: int, taxa_indexador: float, percentual_indexador: float, capital: float = 0, aportes: float = 0, tipo: str = 'CDB'):
    """
    Calcula o rendimento de um título (CDB, LCI ou LCA) atrelado a uma taxa indexada.

    Args:
        periodo (int): número de meses.
        taxa_indexador (float): taxa anual do indexador em % (ex: CDI, IPCA ou prefixada).
        percentual_indexador (float): percentual do rendimento sobre o indexador em % (ex: 100, 110).
        capital (float, optional): capital inicial. Padrão é 0.
        aportes (float, optional): aporte mensal. Padrão é 0.
        tipo (str, optional): tipo do título ('CDB', 'LCI' ou 'LCA'). Padrão é 'CDB'.

    Returns:
        tuple: 
            - Mtitulo (np.ndarray): montante bruto do investimento ao longo do tempo.
            - Mtaxa (np.ndarray): montante do indexador puro (ex: CDI) ao longo do tempo.
            - caixa (np.ndarray): capital acumulado sem investir (capital + aportes).
            - Mliq (np.ndarray): montante líquido do investimento (após IR se aplicável).
            - t (np.ndarray): vetor de tempo em meses.
    
    Notes:
        - Para LCI e LCA, Mliq geralmente é igual a Mtitulo, pois são isentos de IR.
        - IR é aplicado apenas para CDB, conforme tabela regressiva.
    """

    p, A, C = periodo, aportes, capital

    taxa = taxa_indexador / 100
    percentual = percentual_indexador / 100

    taxa_meses = (1 + taxa) ** (1 / 12) - 1 # Converte a taxa anual da taxa indexada para mensal
    rendimento_meses = percentual * taxa_meses # Rendimento mensal em cima da taxa indexada

    t = np.arange(0, p + 1) # Domínio

    Mtitulo = C * (1 + rendimento_meses) ** t + A * ((1 + rendimento_meses) ** t - 1) / rendimento_meses # Montante Bruto
    Mtaxa = C * (1 + taxa_meses) ** t + A * ((1 + taxa_meses) ** t - 1) / taxa_meses
    caixa = C + A * t

    dias = t * 30

    # Calcula IR apenas para CDB
    if tipo.upper() == 'CDB':
        alpha = np.where(dias <= 180, 0.225, np.where(dias <= 360, 0.20, np.where(dias <= 720, 0.175, 0.15)))
        R = Mtitulo - (C + A * t) # Rendimento bruto
        IR = alpha * R
        Mliq = Mtitulo - IR

    else:  # LCI/LCA isento
        Mliq = Mtitulo

    return Mtitulo, Mtaxa, caixa, Mliq, t