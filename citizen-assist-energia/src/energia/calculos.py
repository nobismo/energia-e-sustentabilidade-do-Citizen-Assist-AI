"""Cálculos de energia: banho com chuveiro elétrico x alternativas.

Todas as alternativas atendem à MESMA necessidade (banho quente de uma
família) e são comparadas no MESMO período (horizonte_anos).
Unidades: energia em kWh, potência em kW, dinheiro em R$, CO2 em kg.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

PREMISSAS_PATH = Path(__file__).resolve().parents[2] / "data" / "premissas.json"


def carregar_premissas(caminho: Path = PREMISSAS_PATH) -> dict:
    """Lê o JSON e devolve {nome: valor}."""
    with open(caminho, encoding="utf-8") as f:
        bruto = json.load(f)["parametros"]
    return {k: v["valor"] for k, v in bruto.items()}


def carregar_metadados(caminho: Path = PREMISSAS_PATH) -> dict:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)["parametros"]


# ---------------------------------------------------------------- física
def energia_por_banho_kwh(P: dict, duracao_min=None, vazao_l_min=None) -> float:
    """E = m * c * ΔT / η  (kJ -> kWh dividindo por 3600)."""
    duracao = P["duracao_banho_min"] if duracao_min is None else duracao_min
    vazao = P["vazao_l_min"] if vazao_l_min is None else vazao_l_min
    massa_kg = vazao * duracao  # 1 L de água ≈ 1 kg
    delta_t = P["temp_banho_c"] - P["temp_agua_fria_c"]
    energia_kj = massa_kg * P["calor_especifico_agua"] * delta_t
    return energia_kj / 3600 / P["eficiencia_chuveiro"]


def potencia_equivalente_kw(P: dict) -> float:
    """Potência elétrica necessária: P = E / t."""
    return energia_por_banho_kwh(P) / (P["duracao_banho_min"] / 60)


def banhos_por_mes(P: dict) -> float:
    return P["n_pessoas"] * P["banhos_dia_pessoa"] * P["dias_mes"]


def consumo_mensal_kwh(P: dict, duracao_min=None, vazao_l_min=None) -> float:
    return energia_por_banho_kwh(P, duracao_min, vazao_l_min) * banhos_por_mes(P)


def custo_mensal_rs(P: dict, kwh: float) -> float:
    return kwh * P["tarifa_kwh"]


# ------------------------------------------------------------- resultados
@dataclass
class Resultado:
    nome: str
    descricao: str
    renovavel: bool
    capex: float                 # investimento inicial (R$)
    kwh_evitados_mes: float      # redução de compra de energia da rede (ano 1)
    fator_valor: float           # quanto de cada kWh evitado vira R$ (1 = tarifa cheia)
    manutencao_aa: float         # R$/ano
    vida_util: int
    kwh_gerados_mes: float = 0.0 # geração FV (para CO2 de ciclo de vida)
    degradacao_aa: float = 0.0
    kwp: float = 0.0
    notas: list = field(default_factory=list)
    # preenchidos por avaliar()
    economia_ano1: float = 0.0
    economia_total: float = 0.0
    saldo_liquido: float = 0.0   # economia - capex - manutenção, sem desconto
    vpl: float = 0.0
    payback_anos: float | None = None
    custo_por_kwh_evitado: float | None = None
    co2_evitado_kg: float = 0.0
    co2_liquido_ciclo_vida_kg: float | None = None
    kwh_evitados_total: float = 0.0


def avaliar(P: dict, r: Resultado) -> Resultado:
    """Fluxo de caixa ano a ano no horizonte comum."""
    H = int(P["horizonte_anos"])
    esc, taxa = P["escalada_tarifa_aa"], P["taxa_desconto_aa"]
    acumulado = -r.capex
    vpl = -r.capex
    soma_econ = soma_kwh = soma_manut = 0.0
    payback = None
    for t in range(1, H + 1):
        degr = (1 - r.degradacao_aa) ** (t - 1)
        kwh_ano = r.kwh_evitados_mes * 12 * degr
        econ = kwh_ano * P["tarifa_kwh"] * (1 + esc) ** (t - 1) * r.fator_valor
        manut = r.manutencao_aa if t <= r.vida_util else 0.0
        fluxo = econ - manut
        if payback is None and acumulado + fluxo >= 0:
            payback = (t - 1) + (-acumulado / fluxo if fluxo > 0 else 0)
        acumulado += fluxo
        vpl += fluxo / (1 + taxa) ** t
        soma_econ += econ
        soma_kwh += kwh_ano
        soma_manut += manut
        if t == 1:
            r.economia_ano1 = econ - manut
    r.economia_total = soma_econ
    r.saldo_liquido = acumulado
    r.vpl = vpl
    r.payback_anos = payback
    r.kwh_evitados_total = soma_kwh
    r.custo_por_kwh_evitado = (r.capex + soma_manut) / soma_kwh if soma_kwh > 0 else None
    r.co2_evitado_kg = soma_kwh * P["emissao_rede_g_kwh"] / 1000
    if r.kwh_gerados_mes > 0:  # FV: desconta emissões de fabricação (ciclo de vida)
        ger = sum(r.kwh_gerados_mes * 12 * (1 - r.degradacao_aa) ** (t - 1) for t in range(1, H + 1))
        r.co2_liquido_ciclo_vida_kg = (soma_kwh * P["emissao_rede_g_kwh"] - ger * P["emissao_ciclo_pv_g_kwh"]) / 1000
    return r


# -------------------------------------------------------------- cenários
def _economia_A(P: dict) -> float:
    base = consumo_mensal_kwh(P)
    nova = consumo_mensal_kwh(P, P["A_duracao_banho_min"], P["A_vazao_l_min"])
    return (base - nova) * P["A_adesao"]


def alternativa_A(P: dict) -> Resultado:
    return Resultado(
        "A", "Eficiência: banho mais curto + restritor de vazão", False,
        capex=P["A_custo_rs"], kwh_evitados_mes=_economia_A(P), fator_valor=1.0,
        manutencao_aa=0.0, vida_util=99,
        notas=["Depende de hábito (considerada adesão de {:.0%}).".format(P["A_adesao"])])


def alternativa_B(P: dict, demanda_kwh_mes: float | None = None, capex_extra: float = 0.0) -> Resultado:
    d = consumo_mensal_kwh(P) if demanda_kwh_mes is None else demanda_kwh_mes
    return Resultado(
        "B", "Renovável térmica: aquecedor solar de água", True,
        capex=P["B_custo_rs"] + capex_extra, kwh_evitados_mes=d * P["B_fracao_solar"], fator_valor=1.0,
        manutencao_aa=P["B_custo_rs"] * P["B_manutencao_aa"], vida_util=int(P["B_vida_util_anos"]),
        notas=["Exige telhado com sol, reservatório e pressão adequada; o resto é apoio elétrico.",
               "Vida útil menor que o horizonte pode exigir reparo/troca."])


def alternativa_C(P: dict, demanda_kwh_mes: float | None = None, capex_extra: float = 0.0) -> Resultado:
    d = consumo_mensal_kwh(P) if demanda_kwh_mes is None else demanda_kwh_mes
    kwp = math.ceil(d / P["C_produtividade_kwh_kwp_mes"] * 10) / 10  # arredonda p/ 0,1 kWp
    gerado = kwp * P["C_produtividade_kwh_kwp_mes"]
    evitado = min(gerado, d)
    fator = (1 - P["C_perc_injecao"]) + P["C_perc_injecao"] * P["C_fator_credito"]
    capex = kwp * 1000 * P["C_custo_wp_rs"]
    return Resultado(
        "C", "Renovável elétrica: energia solar fotovoltaica", True,
        capex=capex + capex_extra, kwh_evitados_mes=evitado, fator_valor=fator,
        manutencao_aa=capex * P["C_manutencao_aa"], vida_util=int(P["C_vida_util_anos"]),
        kwh_gerados_mes=gerado, degradacao_aa=P["C_degradacao_aa"], kwp=kwp,
        notas=["Sistemas muito pequenos podem não ser ofertados; kits comuns começam em ~1,5 a 2 kWp.",
               "A conta nunca zera: há o custo de disponibilidade (mínimo cobrado).",
               "Vale a pena considerar o Fio B (Lei 14.300) e a aprovação da distribuidora."])


def alternativa_AC(P: dict) -> Resultado:
    """Combinação: primeiro reduzir o consumo (A), depois dimensionar o FV menor (C)."""
    a = alternativa_A(P)
    demanda = consumo_mensal_kwh(P) - a.kwh_evitados_mes
    c = alternativa_C(P, demanda_kwh_mes=demanda)
    r = Resultado(
        "A+C", "Combinação: eficiência (A) + fotovoltaico menor (C)", True,
        capex=a.capex + c.capex,
        kwh_evitados_mes=a.kwh_evitados_mes + c.kwh_evitados_mes,
        fator_valor=(a.kwh_evitados_mes + c.kwh_evitados_mes * c.fator_valor)
                    / (a.kwh_evitados_mes + c.kwh_evitados_mes),
        manutencao_aa=c.manutencao_aa, vida_util=c.vida_util,
        kwh_gerados_mes=c.kwh_gerados_mes, degradacao_aa=c.degradacao_aa, kwp=c.kwp,
        notas=["Reduzir a demanda antes reduz o tamanho (e o custo) do sistema solar."])
    return r


def alternativa_AB(P: dict) -> Resultado:
    a = alternativa_A(P)
    demanda = consumo_mensal_kwh(P) - a.kwh_evitados_mes
    b = alternativa_B(P, demanda_kwh_mes=demanda)
    return Resultado(
        "A+B", "Combinação: eficiência (A) + aquecedor solar (B)", True,
        capex=a.capex + b.capex, kwh_evitados_mes=a.kwh_evitados_mes + b.kwh_evitados_mes,
        fator_valor=1.0, manutencao_aa=b.manutencao_aa, vida_util=b.vida_util,
        notas=["Combina hábito e equipamento; a economia da parte B incide sobre a demanda já reduzida."])


def comparar(P: dict | None = None) -> list[Resultado]:
    """Devolve as alternativas avaliadas (A, B, C e combinações)."""
    P = P or carregar_premissas()
    return [avaliar(P, f(P)) for f in (alternativa_A, alternativa_B, alternativa_C, alternativa_AB, alternativa_AC)]


def fmt_anos(x):
    if x is None:
        return "não se paga em 10 anos"
    if x < 1:
        return f"cerca de {max(1, round(x * 12))} meses"
    return f"{x:.1f} anos".replace(".", ",")
