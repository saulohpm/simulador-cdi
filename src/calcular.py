import numpy as np

def posfixado(periodo: int, taxa_indexador, percentual_indexador: float, capital: float = 0, aportes: float = 0,
              imposto: str = 'sim'):
    """
    Calcula o rendimento de um título de renda fixa pós-fixado
    atrelado a um indexador, como CDI, Selic ou outro indicador.

    O rendimento do título acompanha a variação do indexador,
    multiplicado pelo percentual contratado do investimento.

    Exemplos:
        - CDB 100% CDI
        - CDB 110% CDI
        - LCI 90% CDI
        - LCA 95% CDI

    Args:
        periodo (int):
            Número de meses do investimento.

        taxa_indexador (float):
            Taxa anual do indexador em percentual (%).

            Exemplos:
                CDI de 14,5% deve ser informado como 14.5.

        percentual_indexador (float):
            Percentual aplicado sobre o indexador em percentual (%).

            Exemplos:
                100 -> 100% do CDI
                110 -> 110% do CDI
                90  -> 90% do CDI

        capital (float, optional):
            Capital inicial investido.

            Valor aplicado no início da simulação.

        aportes (float, optional):
            Valor aportado mensalmente durante o período
            do investimento.

        imposto (str, optional):
            Define se haverá desconto de Imposto de Renda.

            Valores aceitos:
                'sim' -> aplica IR regressivo sobre o rendimento
                'não' -> não aplica imposto

            Observações:
                - CDB normalmente utiliza IR regressivo.
                - LCI e LCA são isentos de IR.

    Returns:
        tuple:
            Mtitulo:
                Vetor contendo a evolução do valor bruto acumulado
                do título ao longo dos meses.

            Mtaxa:
                Vetor contendo a evolução de uma aplicação equivalente
                a 100% do indexador, sem considerar o percentual contratado.

            caixa:
                Vetor contendo a evolução do valor acumulado apenas
                com os aportes realizados, sem rendimento.

            Mliq:
                Vetor contendo o valor líquido acumulado após o desconto
                do Imposto de Renda, quando aplicável.

            t:
                Vetor contendo o período em meses da simulação.

    Notes:
        - As taxas de entrada são informadas em percentual (%).
        - Internamente, as taxas são convertidas para formato decimal.
        - A taxa anual do indexador é convertida para uma taxa mensal
          equivalente utilizando juros compostos.
        - O rendimento mensal é calculado considerando o percentual
          contratado sobre o indexador.
        - A função permite simular diferentes produtos pós-fixados,
          alterando apenas o indexador e o percentual contratado.
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
    Calcula o rendimento de um título de renda fixa prefixado.

    O título prefixado possui uma taxa fixa definida no momento da aplicação,
    portanto seu rendimento não depende de nenhum indexador externo como CDI
    ou IPCA.

    Exemplos:
        - CDB Prefixado 12% a.a.
        - LCI Prefixada 10% a.a.
        - LCA Prefixada 11% a.a.

    Args:
        periodo (int):
            Número de meses do investimento.

        taxa_anual (float):
            Taxa fixa anual contratada em percentual (%).

            Exemplos:
                12 significa 12% ao ano.
                10.5 significa 10,5% ao ano.

        capital (float, optional):
            Capital inicial investido. Padrão é 0.

        aportes (float, optional):
            Valor aportado mensalmente. Padrão é 0.

        imposto (str, optional):
            Tipo do título:
                'sim' -> sujeito a IR regressivo.
                'não' -> isento de IR.

            Padrão é 'sim'.

    Returns:
        tuple:
            - Mtitulo (np.ndarray):
                Montante bruto acumulado do investimento ao longo do tempo.

            - Mtaxa (np.ndarray):
                Evolução da aplicação considerando a taxa contratada.

            - caixa (np.ndarray):
                Capital acumulado sem rendimento (capital + aportes).

            - Mliq (np.ndarray):
                Montante líquido após desconto de IR quando aplicável.

            - t (np.ndarray):
                Vetor de tempo em meses.

    Notes:
        - A taxa de entrada utiliza percentual (%).
        - Internamente a taxa é convertida para decimal.
        - A taxa anual é convertida para uma taxa mensal equivalente
          utilizando juros compostos.
        - Diferente do pós-fixado, a taxa permanece constante durante
          todo o período da simulação.
        - CDB sofre incidência de IR regressivo.
        - LCI e LCA são isentos de IR.
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
    Calcula o valor líquido de um investimento após a aplicação do
    Imposto de Renda regressivo.

    A função recebe o montante bruto acumulado de um investimento e
    aplica a alíquota correspondente ao período de permanência do
    capital, seguindo a tabela regressiva de IR utilizada em aplicações
    de renda fixa tributáveis, como CDBs.

    Args:
        dias (np.ndarray):
            Vetor contendo o tempo de investimento em dias.
            É utilizado para determinar a alíquota de Imposto de Renda
            aplicável em cada período.

        Mtitulo (np.ndarray):
            Vetor contendo o montante bruto acumulado do investimento
            ao longo do tempo.

        caixa (np.ndarray):
            Vetor contendo o valor acumulado sem rendimento,
            representando o capital inicial mais os aportes realizados.

    Returns:
        np.ndarray:
            Mliq:
                Vetor contendo o montante líquido do investimento após
                o desconto do Imposto de Renda sobre o rendimento obtido.

    Notes:
        - O Imposto de Renda é aplicado somente sobre o rendimento,
          não sobre o valor investido.

        - A alíquota segue a tabela regressiva:

            Até 180 dias:
                22,5%

            De 181 a 360 dias:
                20%

            De 361 a 720 dias:
                17,5%

            Acima de 720 dias:
                15%

        - A função não valida se o investimento possui isenção de IR.
          A decisão de aplicar ou não o imposto deve ser feita pela
          função principal do investimento (exemplo: CDB, LCI ou LCA).
    """

    alpha = np.where(dias <= 180, 0.225, np.where(dias <= 360, 0.20, np.where(dias <= 720, 0.175, 0.15)))
    rendimento = Mtitulo - caixa
    IR = alpha * rendimento
    Mliq = Mtitulo - IR

    return Mliq