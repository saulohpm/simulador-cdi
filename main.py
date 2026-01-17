from cdb import calcularcdb, plotarcdb

def main():

    # ===============================
    # SIMULAÇÃO CDB
    # ===============================
    periodo = 12 * 5
    CDI = 14.32
    CDB = 100
    capital = 20000
    aportes = 1500

    MCDB, MCDI, caixa, Mliq, t = calcularcdb(periodo, CDI, CDB, capital, aportes)

    plotarcdb(MCDB, MCDI, caixa, Mliq, t)


if __name__ == "__main__":
    main()