# Simulador de CDB em Python

## 📌 Descrição
Este projeto tem como objetivo praticar **lógica de programação em Python**, **modularização de código** e **visualização de dados com matplotlib**, utilizando como contexto uma simulação de investimento em **CDB atrelado ao CDI**.

O foco do projeto é educacional, não sendo uma ferramenta de previsão ou recomendação financeira.

---

## 🎯 Objetivos do Projeto
- Aplicar conceitos de juros compostos
- Trabalhar com séries temporais utilizando `numpy`
- Exercitar a modularização do código em funções
- Visualizar dados financeiros com `matplotlib`
- Simular o desconto automático de Imposto de Renda regressivo

---

## 🧠 Conceitos de Programação Utilizados
- Funções e modularização
- Estruturas condicionais
- Vetorização com NumPy
- Tratamento básico de erros
- Visualização de dados

---

## 📊 Funcionalidades
- Cálculo do montante bruto do CDB
- Cálculo do montante líquido (após IR)
- Comparação com o CDI
- Simulação do valor não investido
- Geração de gráfico temporal comparativo

---

## 📁 Estrutura do Projeto
```text
simulador-cdb/
│── main.py
│── cdb.py
│── README.md

│── requirements.txt
```
---

## 🚀 Como Executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o simulador:

```bash
python main.py
```

3. Informe os dados solicitados pelo programa:
- Valor inicial a investir
- Prazo do investimento (em dias)
- Percentual do CDI a ser aplicado

3. O programa irá rodar a simulação de CDB definida no `main.py`, usando:
- Período: 12 * 5 meses
- CDI: 14.32%
- CDB: 100%
- Capital inicial: R$ 20.000
- Aportes mensais: R$ 1.500

4. O gráfico será gerado automaticamente mostrando:
- Evolução do CDB (bruto e líquido)
- Comparação com CDI
- Caixa disponível
