import numpy as np

def calcular_titulo(periodo: int, taxa_indexador: float, percentual_indexador: float, capital: float = 0, aportes: float = 0, imposto: str = 'sim'):
    """
    Calcula o rendimento de um título (CDB, LCI ou LCA) atrelado a um indexador.

    Args:
        periodo (int):
            Número de meses do investimento.

        taxa_indexador (float):
            Taxa anual do indexador em percentual (%).
            Exemplo: CDI de 14,5% deve ser informado como 14.5.

        percentual_indexador (float):
            Percentual aplicado sobre o indexador em percentual (%).
            Exemplos:
                100 para 100% do CDI
                110 para 110% do CDI
                90 para 90% do CDI

        capital (float, optional):
            Capital inicial investido.

        aportes (float, optional):
            Valor aportado mensalmente.

        tipo (str, optional):
            Tipo do título:
                'CDB' -> sujeito a IR regressivo
                'LCI' -> isento de IR
                'LCA' -> isento de IR

    Returns:
        tuple:
            Mtitulo:
                Valor bruto acumulado do título.

            Mtaxa:
                Evolução do indexador puro (100% do indexador).

            caixa:
                Valor acumulado sem rendimento.

            Mliq:
                Valor líquido após impostos.

            t:
                Vetor de tempo em meses.

    Notes:
        - Taxas de entrada usam percentual (%).
        - Internamente são convertidas para decimal.
        - LCI e LCA não sofrem IR.
        - CDB utiliza tabela regressiva de IR.
    """

    t = np.arange(periodo + 1)

    taxa_convertida = taxa_indexador / 100

    if np.isscalar(taxa_convertida):
        taxa = np.full(periodo + 1, taxa_convertida)
    else:
        taxa = taxa_convertida

    percentual = percentual_indexador / 100

    taxa_meses = (1 + taxa) ** (1 / 12) - 1

    rendimento_meses = percentual * taxa_meses

    Mtitulo = np.zeros(periodo + 1)
    Mtaxa = np.zeros(periodo + 1)
    caixa = np.zeros(periodo + 1)

    Mtitulo[0] = capital
    Mtaxa[0] = capital
    caixa[0] = capital

    for i in range(1, periodo + 1):

        Mtitulo[i] = (Mtitulo[i - 1] + aportes) * (1 + rendimento_meses[i])

        Mtaxa[i] = (Mtaxa[i - 1] + aportes) * (1 + taxa_meses[i])

        caixa[i] = caixa[i - 1] + aportes

    dias = t * 30

    if imposto.lower() == "sim":
        alpha = np.where(dias <= 180, 0.225,np.where(dias <= 360, 0.20,np.where(dias <= 720, 0.175, 0.15)))

        rendimento = Mtitulo - caixa

        IR = alpha * rendimento

        Mliq = Mtitulo - IR

    else:
        Mliq = Mtitulo

    return Mtitulo, Mtaxa, caixa, Mliq, t