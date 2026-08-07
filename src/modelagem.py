import numpy as np

def taxa_de_juros_variavel(taxa: float, t: np.ndarray, taxa_max: float = 0.15, taxa_min: float = 0.02, mercado: str = "alta"):
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

    if mercado.lower() == "alta":
        fase = 0

    elif mercado.lower() == "baixa":
        fase = np.pi

    else:
        raise ValueError("ERRO: mercado deve ser 'alta' ou 'baixa'")

    alpha = (taxa_max - taxa_min) / 2
    beta = (taxa_min + taxa_max) / 2

    taxa_variavel = alpha * np.sin(t / 0.75 + fase) + beta

    return taxa_variavel