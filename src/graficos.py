import matplotlib.pyplot as plt


def plotarcdb(Mtitulo, Mtaxa, caixa, Mliq, t, tipo: str = 'CDB', tamanho=(16,8)):

    """
    Plota gráfico comparativo de um investimento versus indexador e caixa.

    Exibe o montante bruto e líquido do título, o indexador como referência e o valor não investido (caixa).

    Args:
        Mtitulo (np.ndarray): Montante bruto do investimento.
        Mtaxa (np.ndarray): Montante do indexador puro (ex: CDI) no mesmo período.
        caixa (np.ndarray): Capital acumulado sem investir.
        Mliq (np.ndarray): Montante líquido do investimento (após IR, se aplicável).
        t (np.ndarray): Vetor de tempo em meses.
        tipo (str, optional): Tipo do investimento ('CDB', 'LCI', 'LCA'). Padrão é 'CDB'.
        tamanho (tuple, optional): Tamanho da figura em polegadas (largura, altura). Padrão é (16,8).

    Returns:
        None. Mostra o gráfico usando matplotlib.

    Notes:
        - Para LCI/LCA, Mliq geralmente é igual a Mtitulo, pois são isentos de IR.
        - Linha tracejada representa montante bruto ou indexador; linha sólida representa montante líquido.
        - Cores padrão: laranja para investimento, cinza para indexador, vermelho para caixa.
    """

    plt.figure(figsize=tamanho)

    # Plot do Gráfico
    if tipo.upper() == 'CDB':
        plt.plot(t, Mtitulo, color='orange', label=f'{tipo} Bruto', linestyle='--')
    plt.plot(t, Mliq, color='orange', label=f'{tipo} Líquido', linestyle='-')
    plt.plot(t, Mtaxa,color='gray', label='CDI', linestyle='--')
    plt.plot(t, caixa,color='red', label='Não Investido', linestyle='--')

    plt.title(f"Simulação de {tipo}")
    plt.xlabel("tempo (meses)")
    plt.ylabel("Valor (R$)")
    plt.grid(True, alpha=0.75)
    plt.legend()

    plt.show()