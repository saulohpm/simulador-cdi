from src.calculos import calcular_titulo
from src.graficos import plotarcdb

def main():

    # ===============================
    # EXEMPLO SIMPLES: SIMULAÇÃO TESTE
    # ===============================
    periodo = 12 * 5
    CDI = 14.32
    CDB = 100
    capital = 20000
    aportes = 1500

    MCDB, MCDI, caixa, Mliq, t = calcular_titulo(periodo, CDI, CDB, capital, aportes)

    plotarcdb(MCDB, MCDI, caixa, Mliq, t)


if __name__ == "__main__":
    main()