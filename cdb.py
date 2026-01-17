import matplotlib.pyplot as plt
import numpy as np

def calcularcdb(periodo, CDI, CDB, capital, aportes):

    '''
    Variáveis (Exemplo):
    p = 12 * 10 -> Em meses * anos (Intervalo de tempo)
    CDI = 14.32 -> CDI (% a.a)
    CDB = 100.5 -> CDB (Rendimento do CDI em %)
    C = 20000 -> Capital Inicial (R$)
    A = 1500 -> Aportes Mensais (R$) 
    '''

    p = periodo
    C = capital
    A = aportes

    # Calculo
    CDI = CDI / 100
    CDB = CDB / 100
    CDI_meses = (1 + CDI) ** (1 / 12) -1
    CDB_meses = CDB * CDI_meses

    t = np.arange(0, p + 1)

    if CDB_meses == 0 or CDI_meses == 0:
        raise ValueError("❌ Impossível divisão por zero! Digite um CDB ou CDI válido!")

    MCDB = C * (1 + CDB_meses) ** t + A * ((1 + CDB_meses) ** t - 1) / CDB_meses # Montante Bruto
    MCDI = C * (1 + CDI_meses) ** t + A * ((1 + CDI_meses) ** t - 1) / CDI_meses
    caixa = C + A * t

    dias = t * 30

    # Alíquota do Imposto de Renda
    alpha = np.where(dias <= 180, 0.225,
            np.where(dias <= 360, 0.20,
            np.where(dias <= 720, 0.175, 0.15)))

    # Calculo do Imposto de Renda (Desconto Automático)
    R = MCDB - (C + A * t) # Rendimento Bruto
    IR = alpha * R # Imposto de Renda
    Mliq = MCDB - IR # Montante Líquido

    return MCDB, MCDI, caixa, Mliq, t


def plotarcdb(MCDB, MCDI, caixa, Mliq, t):

    # Plot do Gráfico
    plt.plot(t, MCDB, color='orange', label='CDB Bruto', linestyle='--')
    plt.plot(t, Mliq, color='orange', label='CDB Líquido', linestyle='-')
    plt.plot(t, MCDI,color='gray', label='CDI', linestyle='--')
    plt.plot(t, caixa,color='red', label='Não Investido', linestyle='--')


    plt.title("Simulação de CDI x CDB x Não Investido")
    plt.xlabel("tempo (meses)")
    plt.ylabel("Valor (R$)")
    plt.grid(True, alpha=0.75)
    plt.legend()

    plt.show()