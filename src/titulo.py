import matplotlib.pyplot as plt
import numpy as np

def calcular_titulo(periodo: int, CDI: float, percentual: float, capital: float, aportes: float, tipo: str = 'CDB'):
    
    """
    Calcula o rendimento de CDB, LCI ou LCA atrelado ao CDI
    
    Args:
        periodo (int): número de meses.
        CDI (float): taxa CDI anual em %.
        percentual (float): percentual do CDI ou prefixado em %.
        capital (float): capital inicial.
        aportes (float): aporte mensal.
        tipo (str): 'CDB', 'LCI' ou 'LCA'. Padrão 'CDB'.

    Returns:
        tuple: (Mtitulo, MCDI, caixa, Mliq, t), com arrays de valores.
    """

    p = periodo
    C = capital
    A = aportes

    CDI = CDI / 100
    percentual = percentual / 100
    CDI_meses = (1 + CDI) ** (1 / 12) - 1 # Converte a taxa anual do CDI para mensal
    rendimento_meses = percentual * CDI_meses # Rendimento mensal em cima do CDI

    t = np.arange(0, p + 1) # Domínio

    Mtitulo = C * (1 + rendimento_meses) ** t + A * ((1 + rendimento_meses) ** t - 1) / rendimento_meses # Montante Bruto
    MCDI = C * (1 + CDI_meses) ** t + A * ((1 + CDI_meses) ** t - 1) / CDI_meses
    caixa = C + A * t

    dias = t * 30

    # Calcula IR apenas para CDB
    if tipo.upper() == 'CDB':
        alpha = np.where(dias <= 180, 0.225,
                np.where(dias <= 360, 0.20,
                np.where(dias <= 720, 0.175, 0.15)))
        R = Mtitulo - (C + A * t) # Rendimento bruto
        IR = alpha * R
        Mliq = Mtitulo - IR
    else:  # LCI/LCA isento
        Mliq = Mtitulo

    return Mtitulo, MCDI, caixa, Mliq, t

def plotarcdb(Mtitulo, MCDI, caixa, Mliq, t, tipo: str = 'CDB', tamanho=(16,8)):

    """
    Plota gráfico comparativo de um investimento versus CDI e caixa.

    Exibe o montante bruto e líquido do título, CDI como referência e valor não investido (caixa).

    Args:
        Mtitulo (array-like): Montante bruto do investimento.
        MCDI (array-like): Valores do CDI no mesmo período.
        caixa (array-like): Valor acumulado caso o capital não fosse investido.
        Mliq (array-like): Montante líquido do investimento (após IR, se aplicável).
        t (array-like): Vetor de tempo em meses.
        tipo (str, optional): Tipo do investimento ('CDB', 'LCI', 'LCA'). Padrão é 'CDB'.
        tamanho (tuple, optional): Tamanho da figura em polegadas (largura, altura). Padrão é (16,8).

    Returns:
        None. Mostra o gráfico usando matplotlib.

    Notes:
        - Para LCI/LCA, Mliq geralmente é igual a Mtitulo, pois são isentos de IR.
        - Cores padrão: laranja para investimento, cinza para CDI, vermelho para caixa.
        - Linha tracejada representa montante bruto ou CDI; linha sólida representa montante líquido.
    """

    plt.figure(figsize=tamanho)

    # Plot do Gráfico
    if tipo.upper() == 'CDB':
        plt.plot(t, Mtitulo, color='orange', label=f'{tipo} Bruto', linestyle='--')
    plt.plot(t, Mliq, color='orange', label=f'{tipo} Líquido', linestyle='-')
    plt.plot(t, MCDI,color='gray', label='CDI', linestyle='--')
    plt.plot(t, caixa,color='red', label='Não Investido', linestyle='--')


    plt.title(f"Simulação de CDI x {tipo} x Não Investido")
    plt.xlabel("tempo (meses)")
    plt.ylabel("Valor (R$)")
    plt.grid(True, alpha=0.75)
    plt.legend()

    plt.show()