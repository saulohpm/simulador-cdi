import numpy as np

def posfixado(periodo: int, taxa_indexador, percentual_indexador: float, capital: float = 0, aportes: float = 0,
              imposto: str = 'sim'):
    """
    Calcula a evolução de um investimento de renda fixa pós-fixado
    atrelado a um indexador.

    O rendimento do título é calculado a partir da taxa anual do
    indexador, convertida para uma taxa mensal equivalente, e do
    percentual contratado sobre esse indexador.

    Exemplos de investimentos:
        - CDB 100% do CDI
        - CDB 110% do CDI
        - LCI 90% do CDI
        - LCA 95% do CDI

    Args:
        periodo (int):
            Número de meses da simulação.

        taxa_indexador (float or np.ndarray):
            Taxa anual do indexador em porcentagem (%).

            Pode ser:
                - um valor único, representando uma taxa constante;
                - um vetor de taxas, permitindo simular um indexador
                  variável ao longo do tempo.

            Exemplo:
                14.5 representa uma taxa anual de 14,5%.

        percentual_indexador (float):
            Percentual do indexador contratado pelo investimento,
            expresso em porcentagem (%).

            Exemplos:
                100 -> 100% do indexador
                110 -> 110% do indexador
                90  -> 90% do indexador

        capital (float, optional):
            Capital inicial investido no início da simulação.
            Padrão: 0.

        aportes (float, optional):
            Valor aportado mensalmente durante o período da simulação.
            Padrão: 0.

        imposto (str, optional):
            Define se o Imposto de Renda será aplicado sobre o
            rendimento.

            Valores aceitos:
                'sim' -> aplica IR regressivo.
                'não' -> não aplica IR.

            Padrão: 'sim'.

    Returns:
        tuple:
            Mtitulo (np.ndarray):
                Montante bruto acumulado do investimento ao longo
                dos meses, considerando o percentual contratado
                do indexador.

            Mtaxa (np.ndarray):
                Montante bruto acumulado de uma aplicação que acompanha
                100% do indexador, independentemente do percentual
                contratado pelo título.

            caixa (np.ndarray):
                Valor acumulado das quantias efetivamente investidas,
                sem considerar rendimentos.

            Mliq (np.ndarray):
                Montante líquido acumulado após o desconto do Imposto
                de Renda, quando aplicável.

            t (np.ndarray):
                Vetor contendo os períodos da simulação, em meses,
                iniciando em zero.

    Notes:
        - As taxas de entrada são informadas em porcentagem (%).
        - As taxas são convertidas internamente para formato decimal.
        - A taxa anual do indexador é convertida para uma taxa mensal
          equivalente utilizando juros compostos.
        - O rendimento mensal do título corresponde à taxa mensal do
          indexador multiplicada pelo percentual contratado.
        - O Imposto de Renda, quando habilitado, é calculado sobre o
          rendimento e não sobre o capital investido.
        - A função permite simular indexadores constantes ou variáveis
          ao longo do tempo.
    """

    t = np.arange(periodo + 1)

    taxa_convertida = taxa_indexador / 100
    taxa = np.full(periodo + 1, taxa_convertida)
    taxa_meses = (1 + taxa) ** (1 / 12) - 1

    percentual = percentual_indexador / 100

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
        Mliq = _imposto(dias, Mtitulo, caixa)

    else:
        Mliq = Mtitulo

    return Mtitulo, Mtaxa, caixa, Mliq, t


def prefixado(periodo: int, taxa_anual: float, capital: float = 0, aportes: float = 0, imposto: str = 'sim'):
    """
    Calcula a evolução de um investimento de renda fixa prefixado.

    Um investimento prefixado possui uma taxa anual fixa definida
    no momento da aplicação. Dessa forma, seu rendimento não depende
    da variação de um indexador externo, como CDI ou IPCA.

    Exemplos de investimentos:
        - CDB Prefixado 12% a.a.
        - LCI Prefixada 10% a.a.
        - LCA Prefixada 11% a.a.

    Args:
        periodo (int):
            Número de meses da simulação.

        taxa_anual (float):
            Taxa fixa anual contratada, expressa em porcentagem (%).

            Exemplos:
                12 -> 12% ao ano.
                10.5 -> 10,5% ao ano.

        capital (float, optional):
            Capital inicial investido no início da simulação.
            Padrão: 0.

        aportes (float, optional):
            Valor aportado mensalmente durante o período da simulação.
            Padrão: 0.

        imposto (str, optional):
            Define se o Imposto de Renda será aplicado sobre o
            rendimento.

            Valores aceitos:
                'sim' -> aplica IR regressivo.
                'não' -> não aplica IR.

            Padrão: 'sim'.

    Returns:
        tuple:
            Mtitulo (np.ndarray):
                Montante bruto acumulado do investimento ao longo
                dos meses.

            Mtaxa (np.ndarray):
                Cópia do montante bruto calculado com a taxa prefixada.
                É mantido como uma saída separada para manter a mesma
                estrutura de retorno utilizada pela função `posfixado`.

            caixa (np.ndarray):
                Valor acumulado das quantias efetivamente investidas,
                sem considerar rendimentos.

            Mliq (np.ndarray):
                Montante líquido acumulado após o desconto do Imposto
                de Renda, quando aplicável.

            t (np.ndarray):
                Vetor contendo os períodos da simulação, em meses,
                iniciando em zero.

    Notes:
        - A taxa anual é informada em porcentagem (%).
        - Internamente, a taxa é convertida para formato decimal.
        - A taxa anual é convertida para uma taxa mensal equivalente
          utilizando juros compostos.
        - A taxa mensal permanece constante durante toda a simulação.
        - Os aportes são considerados no início de cada período mensal.
        - O Imposto de Renda, quando habilitado, é aplicado somente
          sobre o rendimento e não sobre o capital investido.
    """

    taxa = taxa_anual / 100
    taxa_meses = (1 + taxa) ** (1 / 12) - 1

    t = np.arange(0, periodo + 1)

    Mtitulo = capital * (1 + taxa_meses) ** t + aportes * ((1 + taxa_meses) ** t - 1) / taxa_meses

    Mtaxa = Mtitulo.copy()

    caixa = capital + aportes * t

    dias = t * 30

    if imposto.lower() == 'sim':
        Mliq = _imposto(dias, Mtitulo, caixa)

    else:
        Mliq = Mtitulo

    return Mtitulo, Mtaxa, caixa, Mliq, t


def _imposto(dias, Mtitulo, caixa):
    """
    Calcula o montante líquido de um investimento após a aplicação
    do Imposto de Renda regressivo sobre o rendimento.

    A função determina a alíquota de Imposto de Renda de acordo com
    o tempo de permanência do investimento e aplica essa alíquota
    somente sobre o rendimento obtido.

    Args:
        dias (np.ndarray):
            Vetor contendo o tempo de investimento em dias.
            É utilizado para determinar a alíquota de Imposto de Renda
            aplicável em cada período.

        Mtitulo (np.ndarray):
            Vetor contendo os valores brutos acumulados do investimento
            ao longo dos períodos.

        caixa (np.ndarray):
            Vetor contendo os valores efetivamente investidos,
            correspondentes ao capital inicial somado aos aportes,
            sem considerar os rendimentos.

    Returns:
        np.ndarray:
            Vetor contendo os valores líquidos acumulados após o
            desconto do Imposto de Renda.

    Notes:
        - O Imposto de Renda é calculado somente sobre o rendimento,
          determinado pela diferença entre `Mtitulo` e `caixa`.
        - O capital investido não sofre incidência de Imposto de Renda.
        - A alíquota utilizada segue a tabela regressiva:

            Até 180 dias:
                22,5%

            De 181 a 360 dias:
                20%

            De 361 a 720 dias:
                17,5%

            Acima de 720 dias:
                15%

        - A função não verifica se o investimento é isento de Imposto
          de Renda. Essa decisão deve ser feita pela função que a chama,
          como `posfixado` ou `prefixado`.

        - Esta é uma função interna, indicada pelo prefixo `_`, e seu
          uso é destinado principalmente às funções de cálculo dos
          investimentos.
    """

    alpha = np.where(dias <= 180, 0.225, np.where(dias <= 360, 0.20, np.where(dias <= 720, 0.175, 0.15)))
    rendimento = Mtitulo - caixa
    IR = alpha * rendimento
    Mliq = Mtitulo - IR

    return Mliq