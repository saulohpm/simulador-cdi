from src.calcular import posfixado
from src.graficos import plotar
from src import modelagem
import numpy as np


def main():

    periodo = 12 * 5 # Meses
    capital = 5000 # Reais
    aportes = 500 # Reais
    CDI_atual = 0.12 # % a.a
    CDB = 1.05

    t = np.arange(periodo + 1) # Domínio Temporal

    # CDB 100% CDI
    CDI = modelagem.floor(t, CDI_atual)
    MCDB, MCDI, caixa, Mliq, t = posfixado(periodo, CDI, CDB, capital, aportes)
    plotar(MCDB, MCDI, caixa, Mliq, t, "sim", "CDB")


if __name__ == "__main__":
    main()