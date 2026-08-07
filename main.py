from src.calculos import calcular_titulo
from src.graficos import plotarcdb
from src.modelagem import taxa_de_juros_variavel
import numpy as np

def main():

    # ===============================
    # EXEMPLO SIMPLES: SIMULAÇÃO TESTE
    # ===============================
    periodo = 12 * 5
    CDI = taxa_de_juros_variavel(14, np.arange(periodo + 1))
    CDB = 100
    capital = 15000
    aportes = 500

    MCDB, MCDI, caixa, Mliq, t = calcular_titulo(periodo, CDI, CDB, capital, aportes)

    plotarcdb(MCDB, MCDI, caixa, Mliq, t)


if __name__ == "__main__":
    main()