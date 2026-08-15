import numpy as np

def taxa_de_juros_variavel(taxa_atual: float, t: np.ndarray, taxa_max: float = 0.15, taxa_min: float = 0.02, mercado: str = "alta"):
    """
    Gera uma taxa anual de juros variável ao longo do tempo, modelada
    por uma função senoidal entre uma taxa mínima e uma taxa máxima.

    A taxa atual é utilizada para determinar a fase inicial da oscilação.
    O parâmetro `mercado` define se a taxa inicia seguindo uma tendência
    de alta ou de baixa.

    Args:
        taxa_atual (float):
            Taxa anual de juros atual, expressa em formato decimal
            (não mais em porcentagem). Exemplo: 0.145 representa 14,5%.

        t (np.ndarray):
            Vetor de tempo, expresso em meses, para os quais as taxas
            serão calculadas.

        taxa_max (float, optional):
            Taxa anual máxima permitida, em formato decimal.
            Padrão: 0.15 (15%).

        taxa_min (float, optional):
            Taxa anual mínima permitida, em formato decimal.
            Padrão: 0.02 (2%).

        mercado (str, optional):
            Tendência inicial do mercado. Deve ser "alta" para representar
            uma tendência de aumento da taxa ou "baixa" para representar
            uma tendência de redução.
            Padrão: "alta".

    Returns:
        np.ndarray:
            Vetor contendo as taxas anuais variáveis, em formato
            decimal (não mais em porcentagem), correspondentes aos
            valores de tempo fornecidos em `t`.

    Raises:
        ValueError:
            Se `mercado` não for igual a "alta" ou "baixa".
    """

    alpha = (taxa_max - taxa_min) / 2
    beta = (taxa_min + taxa_max) / 2

    x = (taxa_atual - beta) / alpha
    phi = np.arcsin(x)

    if mercado.lower() == "baixa" or mercado.lower() == "queda":
        phi = np.pi - phi
        
    elif mercado.lower() != "alta":
        raise ValueError("ERRO: mercado deve ser 'alta' ou 'baixa'")

    taxa_variavel = alpha * np.sin(t / 8 + phi) + beta

    return taxa_variavel