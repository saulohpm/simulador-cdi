import matplotlib.pyplot as plt


def plotar(Mtitulo, Mtaxa, caixa, Mliq, t, imposto: str = 'sim', nome: str = "Investimento", tamanho = (16,8)):

    """
    Plota gráfico comparativo de um investimento versus indexador e caixa.

    Exibe o montante bruto e líquido do título, o indexador como referência e o valor não investido (caixa).

    Args:
        Mtitulo (np.ndarray): Montante bruto do investimento.
        Mtaxa (np.ndarray): Montante do indexador puro (ex: CDI) no mesmo período.
        caixa (np.ndarray): Capital acumulado sem investir.
        Mliq (np.ndarray): Montante líquido do investimento (após IR, se aplicável).
        t (np.ndarray): Vetor de tempo em meses.
        imposto (str, optional): Paga imposto? Padrão é 'sim'.
        nome (str, optional): Nome do Investimento que será mostrado no plot do gráfico
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
    if imposto.lower() == 'sim':
        plt.plot(t, Mtitulo, color='orange', label=f'{nome} Bruto', linestyle='--')
    plt.plot(t, Mliq, color='orange', label=f'{nome} Líquido', linestyle='-')
    plt.plot(t, Mtaxa,color='gray', label='CDI', linestyle='--')
    plt.plot(t, caixa,color='red', label='Não Investido', linestyle='--')

    plt.title(f"Simulação de {nome}")
    plt.xlabel("tempo (meses)")
    plt.ylabel("Valor (R$)")
    plt.grid(True, alpha=0.75)
    plt.legend()

    plt.show()