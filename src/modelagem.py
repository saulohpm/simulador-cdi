import numpy as np
import matplotlib.pyplot as plt

def taxa_de_juros_variavel(taxa_atual: float, t: np.ndarray, taxa_max: float = 0.15, taxa_min: float = 0.02, mercado: str = "alta"):
    """
    Gera uma taxa anual variável ao longo do tempo.

    Args:
        taxa_media (float): taxa anual média em decimal.
        t (np.ndarray): vetor de tempo em meses.
        mercado (str): tendência do mercado ('alta' ou 'baixa').
        variacao (float): amplitude da oscilação anual.

    Returns:
        np.ndarray: taxa anual variável.
    """

    alpha = (taxa_max - taxa_min) / 2
    beta = (taxa_min + taxa_max) / 2

    x = (taxa_atual - beta) / alpha
    phi = np.arcsin(x)

    if mercado.lower() == "baixa":
        phi = np.pi - phi

    elif mercado.lower() != "alta":
        raise ValueError("ERRO: mercado deve ser 'alta' ou 'baixa'")

    taxa_variavel = alpha * np.sin(t / 8 + phi) + beta

    return taxa_variavel