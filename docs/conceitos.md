---
marp: true
theme: default
paginate: true
_class: lead
math: katex
---

# Conceitos Matemáticos Usados no Simulador de Rendimentos atrelados ao CDI

---

### Sumário

1. [Conversão do CDI anual para mensal](#3)
2. [Rendimento mensal do título](#4)
3. [Montante bruto com aportes mensais](#5)
4. [Montante do CDI como referência](#6)
5. [Caixa ou valor não investido](#6)
6. [Imposto de Renda para CDB](#7)
7. [Modelagem da Taxa de Juros Variável](#8)
    - 7.1 [Modelo senoidal](#9)
    - 7.2 [Modelo em escada (floor)](#14)
8. [Visualização](#22)

[Referências](#23)

---

O simulador calcula o crescimento de investimentos atrelados ao CDI, considerando capital inicial, aportes mensais e Imposto de Renda (quando aplicável).

### 1. Conversão do CDI anual para mensal

O CDI fornecido é anual, mas os cálculos são feitos mês a mês:

$$
CDI_{\text{mes}} = (1 + CDI_{\text{anual}})^{1/12} - 1
$$

- `CDI_anual` é a taxa do CDI em decimal (ex.: 13,15% → 0.1315)  
- `CDI_mes` é a taxa equivalente mensal.

---

### 2. Rendimento mensal do título

Para um título atrelado ao CDI:

$$
r_{\text{mensal}} = \text{percentual do título} \times CDI_{\text{mes}}
$$

- `percentual do título` é a porcentagem do CDI que o título paga (ex.: 115% → 1.15)  
- Para títulos prefixados, basta usar a taxa mensal correspondente.

---

### 3. Montante bruto com aportes mensais

O montante acumulado mês a mês é dado por:

$$
M_{\text{bruto}}(t) = C \cdot (1 + r_{\text{mensal}})^t + A \cdot \frac{(1 + r_{\text{mensal}})^t - 1}{r_{\text{mensal}}}
$$

- $C$ = capital inicial  
- $A$ = aporte mensal  
- $t$ = número de meses  
- $r_{\text{mensal}}$ = rendimento mensal do título  

A segunda parte da fórmula corresponde ao montante acumulado pelos aportes periódicos.

---

### 4. Montante do CDI como referência

Para comparar, calculamos o montante equivalente caso o dinheiro acompanhasse apenas o CDI:

$$
M_{\text{CDI}}(t) = C \cdot (1 + CDI_{\text{mes}})^t + A \cdot \frac{(1 + CDI_{\text{mes}})^t - 1}{CDI_{\text{mes}}}
$$

### 5. Caixa ou valor não investido

Caso o capital fosse apenas guardado sem rendimento:

$$
\text{Caixa}(t) = C + A \cdot t
$$

---

### 6. Imposto de Renda para CDB

O IR sobre o rendimento do CDB é aplicado de acordo com o prazo em **dias**:

$$
\alpha =
\begin{cases} 
22,5\% & \text{até 180 dias} \\
20\% & \text{181 a 360 dias} \\
17,5\% & \text{361 a 720 dias} \\
15\% & \text{acima de 720 dias}
\end{cases}
$$

O rendimento líquido é então:

$$
M_{\text{líquido}} = M_{\text{bruto}} - \alpha \cdot R
$$

onde $R = M_{\text{bruto}} - (C + A \cdot t)$ é o lucro bruto.

Para LCI e LCA, não há IR, então:

$$
M_{\text{líquido}} = M_{\text{bruto}}
$$

---

### 7. Modelagem da Taxa de Juros Variável

Para simular um cenário de mercado onde a taxa de juros não permanece constante ao longo do tempo, foram criadas duas funções de variação da taxa anual:

- **7.1 Modelo senoidal:** oscilação suave entre uma taxa mínima e uma taxa máxima;
- **7.2 Modelo em escada (floor):** aplica o *floor* sobre a senoide para obter patamares e degraus, como nas decisões do COPOM.

> É importante ressaltar que a série do CDI não é periódica de verdade. Ela responde a decisões de política monetária (COPOM), então vai possuir patamares e degraus, não uma oscilação suave.
---

#### 7.1 Modelo senoidal

Vamos definir a taxa variável por:

$$
i(t)=\alpha \cdot \sin\left(\frac{t}{9}+\phi\right)+\beta
$$

onde:

$$
\alpha=\frac{i_{max}-i_{min}}{2}
$$

representa a amplitude da oscilação, e

$$
\beta=\frac{i_{min}+i_{max}}{2}
$$

representa a taxa média do ciclo.

---

Os parâmetros são:

* $i(t)$: taxa anual variável no período $t$;
* $i_{max}$: taxa máxima esperada;
* $i_{min}$: taxa mínima esperada;
* $t$: tempo em meses;
* $\alpha$: amplitude da variação da taxa;
* $\beta$: valor médio entre as taxas máxima e mínima;
* $\phi$: fase do ciclo;

---

O número nove na função é divisor do tempo, ele controla a velocidade da oscilação. Assim, o período do ciclo é $2\pi \cdot 9 \approx 56.5$ meses.

A fase $\phi$ é calculada de forma que a função passe pela **taxa atual** no instante inicial:

$$
i(0)=i_{atual}
$$

Substituindo $t=0$ na função:

$$
i_{atual} = \alpha\sin(\phi) + \beta
\Rightarrow
i_{atual} - \beta = \alpha\sin(\phi)
\Rightarrow
\left(\frac{i_{atual}-\beta}{\alpha}\right) = \sin(\phi)
$$

Logo, uma das soluções possíveis é:

$$
\phi=\arcsin\left(\frac{i_{atual}-\beta}{\alpha}\right)
$$

---

Entretanto, existem duas fases possíveis para o mesmo valor de seno. A escolha entre elas permite determinar a direção inicial da curva.

Para um **mercado em alta**, é utilizada a fase correspondente a uma derivada inicial positiva, isto é $\frac{di(t)}{dt} > 0$, fazendo com que a taxa comece a subir.

Para um **mercado em baixa**, é utilizada a segunda solução:

$$
\phi=\pi-\arcsin\left(\frac{i_{atual}-\beta}{\alpha}\right)
$$

fazendo com que a derivada inicial seja negativa e, portanto, a taxa comece a cair.

---

A implementação:

```python
def senoide(t, taxa_atual, taxa_max = 0.15, taxa_min = 0.02, mercado = "alta"):
    ...
```

A função, portanto, garante que:

$$
i(0)=i_{atual}
$$

enquanto o parâmetro `mercado` determina se a função inicia em uma trajetória de alta ou de baixa.

---

#### 7.2 Modelo em escada (floor)

Como o CDI está diretamente atrelado a Selic, e ela só muda nas reuniões do COPOM e em passos de 0,25 ponto percentual. Para reproduzir isso, foi aplicado o *floor* sobre a senoide $i(t)$ da seção 7.1, portanto:

$$
S(\tau)=\frac{\left\lfloor 400\; i\!\left(\tau\right)\right\rfloor}{400}
$$

tal que $\tau$ é:

$$
\qquad \tau=1{,}5\left\lfloor \frac{t}{1{,}5}\right\rfloor
$$

e $i(\tau)$ é a taxa senoidal mostrada no tópico anterior:

$$
i(\tau)=\alpha \cdot \sin\left(\frac{\tau}{9}+\phi\right)+\beta
$$

---

Os parâmetros são:

* $S(\tau)$: taxa anual em escada no período $t$;
* $i(\tau)$: a senoide da seção 7.1, com os mesmos $\alpha$, $\beta$ e $\phi$;
* $\tau$: tempo em meses, adaptado com as novas regras;
* $t$: tempo em meses;

---

O COPOM faz 8 reuniões por ano, então $12/8 = 1{,}5$, logo foi escolhido 1.5 meses de intervalo. O  passo do COPOM é $0{,}25$ pp, que em decimal é $0{,}0025 = 1/400$. Multiplicar por $400$ faz cada degrau valer $1$, e o floor passa a contar degraus inteiros.

Então, a função floor arredonda para o degrau de baixo, deixando a taxa com a estrutura em degraus do CDI. Por isso $S(t) \le i(\tau(t))$. Em relação a $i(t)$ isso só vale quando a senoide está subindo, porque na descida o atraso até a próxima reunião pode deixar $S(t)$ acima da senoide.

---

A implementação:

```python
def floor(t, taxa_atual, taxa_max = 0.15, taxa_min = 0.02, mercado = "alta"):
    ...
```

A função aplica a senoide na data da última reunião e quantiza em degraus de $0{,}25$ pp. O parâmetro `mercado` define a direção da curva, como na seção 7.1.

---

### 8. Visualização

O gráfico compara:

- Montante bruto do título (`Mtitulo`) — linha tracejada laranja (sem desconto do imposto)  
- Montante líquido do título (`Mliq`) — linha sólida laranja  
- CDI (`MCDI`) — linha tracejada cinza  
- Caixa (`caixa`) — linha tracejada vermelha  

Essa estrutura permite analisar rapidamente qual investimento rende mais líquido e como se comporta frente ao CDI e ao capital não investido.

---

## Referências

ASSAF NETO, Alexandre. *Matemática Financeira e suas Aplicações*. 
15. ed. São Paulo: Atlas, 2022.

PEREIRA, Luana Cristina Santos. *Funções Seno e Cosseno: Fenômenos Periódicos*. 2013. 50 f. Trabalho de Conclusão de Curso (Licenciatura em Matemática) — Centro de Educação e Saúde, Universidade Federal de Campina Grande, Cuité, 2013. Disponível em: [Biblioteca Digital da UFCG — Funções Seno e Cosseno: Fenômenos Periódicos](https://dspace.sti.ufcg.edu.br/handle/riufcg/20654). Acesso em: 7 ago. 2026.

BRASIL. *Lei nº 11.033, de 21 de dezembro de 2004*. Altera a tributação do mercado financeiro e de capitais e dá outras providências. Brasília, DF: Presidência da República. Disponível em: [Lei nº 11.033/2004 — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033compilado.htm). Acesso em: 7 ago. 2026.

---

BANCO CENTRAL DO BRASIL. *Histórico das taxas de juros fixadas pelo Copom e evolução da taxa Selic*. Brasília, DF: Banco Central do Brasil. Disponível em: [Histórico das taxas de juros — Banco Central do Brasil](https://www.bcb.gov.br/controleinflacao/historicotaxasjuros). Acesso em: 16 out. 2026.