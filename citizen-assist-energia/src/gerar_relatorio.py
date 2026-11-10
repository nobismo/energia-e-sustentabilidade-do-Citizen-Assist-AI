"""Gera docs/resultados.md e data/resultados.csv com os cálculos e a comparação.

Execute:  python src/gerar_relatorio.py
"""
import csv
from pathlib import Path

from energia import calculos as c

RAIZ = Path(__file__).resolve().parents[1]


def main() -> None:
    P = c.carregar_premissas()
    meta = c.carregar_metadados()
    res = c.comparar(P)
    kwh = c.consumo_mensal_kwh(P)
    H = int(P["horizonte_anos"])

    with open(RAIZ / "data" / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["alternativa", "descricao", "renovavel", "investimento_rs", "kwh_evitados_mes",
                    "economia_ano1_rs", "saldo_liquido_rs", "vpl_rs", "payback_anos",
                    "rs_por_kwh_evitado", "co2_evitado_kg", "co2_liquido_ciclo_vida_kg"])
        for r in res:
            w.writerow([r.nome, r.descricao, r.renovavel, round(r.capex, 2), round(r.kwh_evitados_mes, 2),
                        round(r.economia_ano1, 2), round(r.saldo_liquido, 2), round(r.vpl, 2),
                        "" if r.payback_anos is None else round(r.payback_anos, 2),
                        "" if r.custo_por_kwh_evitado is None else round(r.custo_por_kwh_evitado, 3),
                        round(r.co2_evitado_kg, 1),
                        "" if r.co2_liquido_ciclo_vida_kg is None else round(r.co2_liquido_ciclo_vida_kg, 1)])

    L = []
    L.append("# Resultados da análise (gerado automaticamente)\n")
    L.append("> Gerado por `python src/gerar_relatorio.py`. Valores ESTIMADOS; veja `data/premissas.json`.\n")
    L.append("## 1. Consumo de referência (situação atual)\n")
    L.append("Fórmulas:\n")
    L.append("- Energia por banho: `E = vazão × tempo × c × ΔT / η / 3600` (kWh)")
    L.append("- Potência equivalente: `P = E / tempo` (kW)")
    L.append("- Consumo mensal: `E × pessoas × banhos/dia × dias`")
    L.append("- Custo mensal: `kWh × tarifa`\n")
    L.append("| Grandeza | Valor |\n|---|---|")
    L.append(f"| Energia por banho | {c.energia_por_banho_kwh(P):.3f} kWh |")
    L.append(f"| Potência equivalente do chuveiro | {c.potencia_equivalente_kw(P):.2f} kW |")
    L.append(f"| Banhos por mês | {c.banhos_por_mes(P):.0f} |")
    L.append(f"| Consumo mensal do banho | {kwh:.1f} kWh |")
    L.append(f"| Custo mensal do banho | R$ {c.custo_mensal_rs(P, kwh):.2f} |")
    L.append(f"| Emissão mensal (rede) | {kwh * P['emissao_rede_g_kwh'] / 1000:.2f} kgCO2 |\n")
    L.append(f"## 2. Comparação das alternativas (mesma necessidade, {H} anos)\n")
    L.append("| Alt. | Descrição | Renovável | Investimento | kWh evitados/mês | Economia 1º ano | Saldo líquido {0}a | VPL | Retorno | R$/kWh evitado |".format(H))
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in res:
        L.append(f"| {r.nome} | {r.descricao} | {'sim' if r.renovavel else 'não'} | R$ {r.capex:,.0f} | {r.kwh_evitados_mes:.1f} | "
                 f"R$ {r.economia_ano1:,.0f} | R$ {r.saldo_liquido:,.0f} | R$ {r.vpl:,.0f} | {c.fmt_anos(r.payback_anos)} | "
                 f"R$ {r.custo_por_kwh_evitado:.2f} |")
    L.append("\n*Saldo líquido = economia acumulada − investimento − manutenção (sem desconto). VPL com taxa de "
             f"{P['taxa_desconto_aa']:.0%} a.a. Tarifa com reajuste de {P['escalada_tarifa_aa']:.0%} a.a.*\n")
    L.append("## 3. Impacto ambiental\n")
    L.append("| Alt. | CO2 evitado (operação) | CO2 líquido com fabricação FV |\n|---|---|---|")
    for r in res:
        liq = "n/d" if r.co2_liquido_ciclo_vida_kg is None else f"{r.co2_liquido_ciclo_vida_kg:.0f} kg"
        L.append(f"| {r.nome} | {r.co2_evitado_kg:.0f} kg | {liq} |")
    L.append("\n*A fabricação do aquecedor solar NÃO foi quantificada (sem fonte confiável).* \n")
    L.append("## 4. Limitações por alternativa\n")
    for r in res:
        L.append(f"- **{r.nome}**: " + " ".join(r.notas))
    L.append("\n## 5. Premissas que o grupo ainda precisa verificar\n")
    for k, v in meta.items():
        if v.get("verificar"):
            L.append(f"- `{k}` = {v['valor']} {v['unidade']} ({v['tipo']}): {v['fonte']}")
    (RAIZ / "docs" / "resultados.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("OK: docs/resultados.md e data/resultados.csv gerados")


if __name__ == "__main__":
    main()
