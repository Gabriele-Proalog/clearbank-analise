"""
Análise Financeira ClearBank - versão alternativa com pandas (Requisito Opcional 1).

Refaz a leitura e o agrupamento do desafio usando pd.read_csv() e groupby,
e compara os resultados com os obtidos pela solução nativa (relatorio.json).
Os valores de ambos devem ser iguais.
"""

import json
from pathlib import Path

import pandas as pd

ARQUIVO_CSV = Path("transacoes.csv")
ARQUIVO_JSON = Path("relatorio.json")
LIMITE_SUSPEITO = 10000.00


def ler_com_pandas(caminho: Path) -> pd.DataFrame:
    """Carrega o CSV com pd.read_csv() mantendo tudo como texto.

    dtype=str faz o pandas NÃO descartar nem corrigir linhas inválidas:
    elas chegam para a validação exatamente como na leitura nativa.
    """
    return pd.read_csv(caminho, dtype=str, keep_default_na=False)


def validar_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Aplica as mesmas regras de validação do desafio e retorna
    (somente válidos, total de inválidos)."""
    df = df.copy()
    df["valor_num"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data_dt"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")

    mask_valida = (
        df["id"].str.strip().str.isdigit()
        & df["cliente_id"].str.strip().ne("")
        & df["data_dt"].notna()
        & df["tipo"].isin(["credito", "debito"])
        & df["valor_num"].notna()
        & (df["valor_num"] > 0)
    )
    validos = df[mask_valida].copy()
    return validos, int((~mask_valida).sum())


def gerar_resumo_mensal(validos: pd.DataFrame) -> dict:
    """Agrupa por mês (AAAA-MM) com groupby e calcula as métricas."""
    validos["mes"] = validos["data_dt"].dt.strftime("%Y-%m")

    agrupado = validos.groupby("mes")
    resumo = agrupado["valor_num"].agg(quantidade="count", media="mean",
                                       maior="max", menor="min").to_dict("index")

    por_tipo = (validos.groupby(["mes", "tipo"])["valor_num"].sum()
                .unstack("tipo").fillna(0.0))

    resultado = {}
    for mes in sorted(resumo):
        credito = float(por_tipo.loc[mes, "credito"]) if "credito" in por_tipo.columns else 0.0
        debito = float(por_tipo.loc[mes, "debito"]) if "debito" in por_tipo.columns else 0.0
        resultado[mes] = {
            "quantidade": int(resumo[mes]["quantidade"]),
            "total_credito": round(credito, 2),
            "total_debito": round(debito, 2),
            "saldo": round(credito - debito, 2),
            "media": round(float(resumo[mes]["media"]), 2),
            "maior_valor": round(float(resumo[mes]["maior"]), 2),
            "menor_valor": round(float(resumo[mes]["menor"]), 2),
        }
    return resultado


def formatar_moeda(valor):
    """Formata um número no padrão monetário brasileiro: R$ 1.234,56."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def arredondar_resumo(resumo):
    """Arredonda os valores monetários para 2 casas (centavos).

    A solução nativa guarda a média com precisão completa (ex.:
    1960.1666666666667); para comparar, padronizamos em centavos.
    """
    return {
        mes: {k: round(v, 2) if isinstance(v, float) else v for k, v in m.items()}
        for mes, m in resumo.items()
    }


def main() -> None:
    df_bruto = ler_com_pandas(ARQUIVO_CSV)
    validos, total_invalidas = validar_dataframe(df_bruto)

    print(f"pandas -> linhas lidas: {len(df_bruto)} | "
          f"válidas: {len(validos)} | inválidas: {total_invalidas}")

    resumo = gerar_resumo_mensal(validos)
    for mes, metricas in resumo.items():
        print(f"  {mes}: {metricas}")

    # Comparação com a solução nativa (gerada pelo notebook)
    if ARQUIVO_JSON.exists():
        nativo = json.loads(ARQUIVO_JSON.read_text(encoding="utf-8"))
        mesmo_total = nativo["total_transacoes_validas"] == len(validos) \
            and nativo["total_transacoes_invalidas"] == total_invalidas
        mesmo_resumo = arredondar_resumo(nativo["resumo_mensal"]) == arredondar_resumo(resumo)
        print(f"\nComparação com a solução nativa:")
        print(f"  Totais de transações iguais: {mesmo_total}")
        print(f"  Resumo mensal idêntico:      {mesmo_resumo}")
    else:
        print("\nExecute antes o notebook desafio-final.ipynb para gerar "
              f"'{ARQUIVO_JSON.name}' e permitir a comparação.")

    suspeitas = validos[validos["valor_num"] > LIMITE_SUSPEITO]
    if not suspeitas.empty:
        print(f"\nSuspeitas (> {formatar_moeda(LIMITE_SUSPEITO)}):")
        for _, linha in suspeitas.iterrows():
            print(f"  ID {linha['id']} | {linha['cliente_id']} | "
                  f"{linha['data']} | {formatar_moeda(linha['valor_num'])}")


if __name__ == "__main__":
    main()
