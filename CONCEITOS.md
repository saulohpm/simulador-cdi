## Conceitos Matemáticos Usados no Simulador de Rendimentos atrelados ao CDI

O simulador calcula o crescimento de investimentos atrelados ao CDI, considerando capital inicial, aportes mensais e Imposto de Renda (quando aplicável).  

### 1. Conversão do CDI anual para mensal

O CDI fornecido é anual, mas os cálculos são feitos mês a mês:

$
CDI_{\text{mes}} = (1 + CDI_{\text{anual}})^{1/12} - 1
$

- `CDI_anual` é a taxa do CDI em decimal (ex.: 13,15% → 0.1315)  
- `CDI_mes` é a taxa equivalente mensal.

---

### 2. Rendimento mensal do título

Para um título atrelado ao CDI:

$
r_{\text{mensal}} = \text{percentual do título} \times CDI_{\text{mes}}
$

- `percentual do título` é a porcentagem do CDI que o título paga (ex.: 115% → 1.15)  
- Para títulos prefixados, basta usar a taxa mensal correspondente.

---

### 3. Montante bruto com aportes mensais

O montante acumulado mês a mês é dado por:

$
M_{\text{bruto}}(t) = C \cdot (1 + r_{\text{mensal}})^t + A \cdot \frac{(1 + r_{\text{mensal}})^t - 1}{r_{\text{mensal}}}
$

- $C$ = capital inicial  
- $A$ = aporte mensal  
- $t$ = número de meses  
- $r_{\text{mensal}}$ = rendimento mensal do título  

A segunda parte da fórmula corresponde ao **montante acumulado pelos aportes periódicos** (fórmula de **progressão geométrica**).

---

### 4. Montante do CDI como referência

Para comparar, calculamos o montante equivalente caso o dinheiro acompanhasse apenas o CDI:

$
M_{\text{CDI}}(t) = C \cdot (1 + CDI_{\text{mes}})^t + A \cdot \frac{(1 + CDI_{\text{mes}})^t - 1}{CDI_{\text{mes}}}
$

---

### 5. Caixa ou valor não investido

Caso o capital fosse apenas guardado sem rendimento:

$
\text{Caixa}(t) = C + A \cdot t
$

---

### 6. Imposto de Renda para CDB

O IR sobre o rendimento do CDB é aplicado de acordo com o prazo em **dias**:

$
\alpha =
\begin{cases} 
22,5\% & \text{até 180 dias} \\
20\% & 181 a 360 dias \\
17,5\% & 361 a 720 dias \\
15\% & acima de 720 dias
\end{cases}
$

O rendimento líquido é então:

$
M_{\text{líquido}} = M_{\text{bruto}} - \alpha \cdot R
$

onde $R = M_{\text{bruto}} - (C + A \cdot t)$ é o **lucro bruto**.

Para LCI e LCA, **não há IR**, então:

$
M_{\text{líquido}} = M_{\text{bruto}}
$

---

### 7. Visualização

O gráfico compara:

- Montante bruto do título (`Mtitulo`) — linha tracejada laranja (apenas CDB)  
- Montante líquido do título (`Mliq`) — linha sólida laranja  
- CDI (`MCDI`) — linha tracejada cinza  
- Caixa (`caixa`) — linha tracejada vermelha

---

Essa estrutura permite analisar rapidamente **qual investimento rende mais líquido e como se comporta frente ao CDI e ao capital não investido**.
