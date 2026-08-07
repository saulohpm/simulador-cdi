from src.calcular import posfixado, prefixado
from src.graficos import plotar
from src.modelagem import taxa_de_juros_variavel
import numpy as np


def main():

    periodo = 12 * 5 # Meses
    capital = 15000 # Reais
    aportes = 500 # Reais
    CDI_atual = 14 # a.a

    t = np.arange(periodo + 1) # Domínio Temporal

    # CDB 100% CDI
    CDI = taxa_de_juros_variavel(CDI_atual / 100, t)
    MCDB, MCDI, caixa, Mliq, t = posfixado(periodo, CDI, 100, capital, aportes)
    plotar(MCDB, MCDI, caixa, Mliq, t)


if __name__ == "__main__":
    main()