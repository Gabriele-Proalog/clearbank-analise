# Desafio Final - ClearBank

Projeto do desafio final do módulo **Análise de Dados e Inteligência de Negócios com IA**.

## Descrição

Notebook Python que simula o trabalho de um analista de dados júnior na fintech ClearBank: lê o arquivo de transações `transacoes.csv` (que chega com problemas frequentes), valida e limpa os dados, calcula métricas financeiras mensais, sinaliza transações suspeitas, exibe um relatório formatado no terminal e exporta o resultado em JSON.

### O que o notebook faz

1. **Leitura do CSV** com o módulo nativo `csv` (`csv.DictReader`), sem pandas.
2. **Validação e limpeza** de cada linha (id, cliente_id, data, tipo, valor), descartando silenciosamente os registros inválidos e exibindo o resumo da limpeza.
3. **Manipulação de datas** com `datetime.strptime`, extração do mês (`AAAA-MM`) e cálculo do período analisado.
4. **Agrupamento mensal** com as métricas: quantidade, total de crédito, total de débito, saldo, média, maior e menor valor.
5. **Identificação de transações suspeitas** (valor acima de `LIMITE_SUSPEITO = 10000.00`).
6. **Exportação** do resultado em `relatorio.json`.
7. **Relatório formatado** no terminal com valores no padrão brasileiro (R$ 1.234,56).

### Requisitos opcionais implementados

- **RO1 (pandas):** `analise_pandas.py` refaz a leitura e o agrupamento com `pd.read_csv()` + `groupby` e compara os resultados com a solução nativa.
- **RO2 (matplotlib):** geração do gráfico `grafico.png` com barras empilhadas de crédito e débito por mês.

## Estrutura do repositório

```
clearbank-analise/
├── desafio-final.ipynb   ← notebook com o código e as saídas salvas
├── analise_pandas.py     ← (opcional) versão com pandas
├── transacoes.csv        ← arquivo de entrada com dados de teste
├── relatorio.json        ← gerado ao executar o notebook
├── grafico.png           ← (opcional) gráfico do matplotlib
└── README.md
```

## Como executar

**No Google Colab:** faça upload do notebook `desafio-final.ipynb` e do arquivo `transacoes.csv`, depois execute todas as células em ordem (Runtime → Run all).

**Localmente (Python 3.10+):**

```bash
pip install pandas matplotlib
jupyter notebook desafio-final.ipynb
```

Execute todas as células em ordem. O notebook cria `relatorio.json` e `grafico.png` na mesma pasta.

## Saídas geradas

- **Terminal:** relatório mensal formatado, lista de transações suspeitas e resumo da validação.
- **`relatorio.json`:** resumo mensal com todas as métricas, total de transações válidas/inválidas e data de geração.
- **`grafico.png`:** gráfico de barras empilhadas com crédito e débito por mês.
