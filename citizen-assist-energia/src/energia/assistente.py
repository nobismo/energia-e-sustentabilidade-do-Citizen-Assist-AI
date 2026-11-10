"""Módulo de energia do Citizen Assist AI.

Uso no assistente principal:
    from energia.assistente import responder
    texto = responder("quanto gasta o chuveiro de 4 pessoas?")

Todas as respostas vêm dos cálculos em calculos.py (nada é escrito "de cabeça")
e terminam com condições/limitações e fontes.
"""
from __future__ import annotations

import re
import unicodedata
from copy import deepcopy

from . import calculos as c

RODAPE = (
    "\n\nℹ️ Condições: estimativa com suposições do projeto (família de {n} pessoas, "
    "{dur:g} min de banho, tarifa R$ {tar:.2f}/kWh). Sua conta e seus hábitos mudam o resultado; "
    "não é promessa de economia. Fontes: data/premissas.json e docs/referencias.md."
)


def _ptbr(texto: str) -> str:
    """Troca ponto decimal por vírgula (1 ou 2 casas); milhar (R$ 4.500) fica intacto."""
    return re.sub(r"(?<=\d)\.(?=\d{1,2}(?!\d))", ",", texto)


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn")


def _num(s: str) -> float:
    return float(s.replace(",", "."))


def extrair_dados(texto: str, P: dict) -> tuple[dict, list[str]]:
    """Lê do texto: pessoas, minutos de banho e tarifa. Devolve (P novo, avisos)."""
    t = _norm(texto)
    P2, usados = deepcopy(P), []
    m = re.search(r"(\d+)\s*(pessoas|moradores|gente)", t)
    if m:
        P2["n_pessoas"] = int(m.group(1)); usados.append(f"{m.group(1)} pessoas")
    if not m:
        m = re.search(r"(?:somos|moramos|sao)\s*(?:em\s*)?(\d+)", t)
        if m:
            P2["n_pessoas"] = int(m.group(1)); usados.append(f"{m.group(1)} pessoas")
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(min|minutos)", t)
    if m:
        P2["duracao_banho_min"] = _num(m.group(1)); usados.append(f"{m.group(1)} min de banho")
    m = re.search(r"(?:r\$|tarifa)\s*(\d+(?:[.,]\d+)?)", t)
    if m and _num(m.group(1)) < 5:
        P2["tarifa_kwh"] = _num(m.group(1)); usados.append(f"tarifa R$ {m.group(1)}/kWh")
    return P2, usados


def _rodape(P: dict) -> str:
    return RODAPE.format(n=P["n_pessoas"], dur=P["duracao_banho_min"], tar=P["tarifa_kwh"])


def _brl(x: float) -> str:
    return f"R$ {x:,.0f}".replace(",", ".")


# ------------------------------------------------------------ respostas
def ajuda() -> str:
    return (
        "Oi! Eu ajudo você a economizar energia no banho quente 🚿. Pergunte, por exemplo:\n"
        "• “Quanto gasta o chuveiro de 4 pessoas com banho de 10 minutos?”\n"
        "• “Qual alternativa compensa mais: aquecedor solar ou placa solar?”\n"
        "• “Como reduzir a conta de luz?”\n"
        "• “Isso ajuda o meio ambiente?”\n"
        "• “Quais são os limites dessas estimativas?”"
    )


def resp_consumo(P: dict, usados: list[str]) -> str:
    kwh = c.consumo_mensal_kwh(P)
    ini = f"Considerando {', '.join(usados)}: " if usados else ""
    return (
        f"{ini}cada banho gasta cerca de {c.energia_por_banho_kwh(P):.2f} kWh "
        f"(chuveiro de ~{c.potencia_equivalente_kw(P):.1f} kW ligado por {P['duracao_banho_min']:g} min). "
        f"Com {P['n_pessoas']} pessoas são ~{kwh:.0f} kWh/mês, ou seja ~{_brl(c.custo_mensal_rs(P, kwh))} por mês "
        f"só no banho quente. (kWh é a unidade que aparece na sua conta de luz.)"
        + _rodape(P)
    )


def resp_comparar(P: dict) -> str:
    res = {r.nome: r for r in c.comparar(P)}
    H = int(P["horizonte_anos"])
    linhas = [f"Comparei alternativas para o MESMO banho quente em {H} anos "
              f"(hoje você gasta ~{_brl(c.custo_mensal_rs(P, c.consumo_mensal_kwh(P)))}/mês):"]
    for n in ("A", "B", "C"):
        r = res[n]
        linhas.append(
            f"• {n} – {r.descricao}: investimento {_brl(r.capex)}, economia estimada no 1º ano "
            f"{_brl(r.economia_ano1)}, retorno: {c.fmt_anos(r.payback_anos)}.")
    ac, b, cc = res["A+C"], res["B"], res["C"]
    p_b = b.payback_anos if b.payback_anos is not None else 99
    p_c = cc.payback_anos if cc.payback_anos is not None else 99
    if b.payback_anos is None and cc.payback_anos is None:
        linhas.append(
            "👉 Com estes dados (tarifa/consumo baixos), nenhuma opção solar se paga no período: "
            "comece pela A (quase grátis) e reavalie se a tarifa ou o consumo forem maiores.")
    else:
        linhas.append(
            "👉 Comece pela A (quase grátis). Se você tem telhado e quer investir, nesta simulação "
            + ("a energia solar fotovoltaica" if p_c <= p_b else "o aquecedor solar")
            + f" se paga mais rápido (combinando com A: {_brl(ac.capex)}, retorno: {c.fmt_anos(ac.payback_anos)})."
            " Mude tarifa e número de pessoas para ver como o resultado muda; o fotovoltaico depende das regras da "
            "distribuidora, e o aquecedor solar, do telhado e da caixa d'água.")
    return "\n".join(linhas) + _rodape(P)


def resp_alternativa(P: dict, nome: str) -> str:
    r = {x.nome: x for x in c.comparar(P)}[nome]
    extra = f" Sistema de ~{r.kwp:.1f} kWp (kWp é a potência das placas)." if r.kwp else ""
    notas = " ".join(r.notas)
    return (
        f"{r.descricao}: investimento ~{_brl(r.capex)}, evita ~{r.kwh_evitados_mes:.0f} kWh/mês da rede, "
        f"economia ~{_brl(r.economia_ano1)} no 1º ano, retorno {c.fmt_anos(r.payback_anos)}.{extra} "
        f"Cada kWh evitado custa ~R$ {r.custo_por_kwh_evitado:.2f} (a tarifa é R$ {P['tarifa_kwh']:.2f}). "
        f"Atenção: {notas}" + _rodape(P)
    )


def resp_ambiente(P: dict) -> str:
    res = {r.nome: r for r in c.comparar(P)}
    C, B = res["C"], res["B"]
    return (
        f"A rede elétrica brasileira já é bem limpa (~{P['emissao_rede_g_kwh']:g} gCO₂/kWh, média 2023/MCTI). "
        f"Por isso, a energia solar evita pouco CO₂: ~{B.co2_evitado_kg:.0f} kg em {int(P['horizonte_anos'])} anos com o "
        f"aquecedor solar e ~{C.co2_evitado_kg:.0f} kg com placas, que têm fabricação própria (~{P['emissao_ciclo_pv_g_kwh']:g} g/kWh no "
        f"ciclo de vida), deixando o saldo líquido próximo de zero ou até levemente negativo ({C.co2_liquido_ciclo_vida_kg:.0f} kg). "
        "O maior ganho ambiental e financeiro é gastar menos (alternativa A) e dar destino correto aos equipamentos no fim da vida."
        + _rodape(P)
    )


def resp_dicas(P: dict) -> str:
    a = c.alternativa_A(P)
    return (
        f"Dicas rápidas: (1) banho de {P['A_duracao_banho_min']:g} min em vez de {P['duracao_banho_min']:g}; "
        "(2) chave na posição “verão” quando o clima permitir; (3) fechar o registro ao se ensaboar; "
        f"(4) restritor de vazão. Com isso você pode evitar ~{a.kwh_evitados_mes:.0f} kWh/mês "
        f"(~{_brl(a.kwh_evitados_mes * P['tarifa_kwh'])}/mês), supondo que consiga cumprir {P['A_adesao']:.0%} da meta."
        + _rodape(P)
    )


def resp_limites(P: dict) -> str:
    return (
        "Limites das estimativas: (1) tarifa, custos dos sistemas e produção solar são estimados e mudam com o "
        "tempo e com a região; (2) consideramos 10 anos, sem valor residual; (3) regras da distribuidora (como a taxa de "
        "uso da rede, o “Fio B”, Lei 14.300) podem mudar a economia do solar; (4) aquecedor e placas exigem telhado adequado e imóvel próprio "
        "ou autorização; (5) consulte 3 orçamentos e um profissional habilitado antes de comprar. "
        "Se você recebe Tarifa Social (CadÚnico), seu desconto muda a conta e o retorno dos investimentos."
        + _rodape(P)
    )


def resp_regras(P: dict, com_rodape: bool = True) -> str:
    return (
        "Duas regras que mudam a conta: (1) Tarifa Social: famílias inscritas no CadÚnico podem ter desconto na "
        "conta; quanto maior o desconto, menor a economia (e o retorno) de investir em solar. Confira a regra "
        "vigente no site da ANEEL ou na sua distribuidora. (2) Fio B (Lei 14.300): quem gera energia solar paga "
        "uma parte do uso da rede sobre o que injeta (60% em 2026, segundo fontes de mercado), o que reduz o "
        "crédito da energia gerada. Nossas contas já usam uma estimativa disso."
        + (_rodape(P) if com_rodape else "")
    )


INTENCOES = [
    ("regras", ("tarifa social", "cadunico", "fio b", "lei 14", "bandeira")),
    ("limites", ("limite", "garant", "confiavel", "fonte", "referencia", "premissa", "de onde")),
    ("ambiente", ("planeta", "clima", "polui", "ambient", "co2", "carbono", "poluic", "sustent", "ecolog")),
    ("comparar", ("compar", "melhor", "compensa", "qual alternativa", "vale a pena", "alternativ")),
    ("B", ("aquecedor solar", "termico", "boiler", "coletor")),
    ("C", ("fotovolt", "placa solar", "painel solar", "energia solar")),
    ("dicas", (" cara", "conta alta", "conta pesada", "dica", "reduzir", "economizar", "diminuir", "baratear", "conta de luz")),
    ("consumo", ("quanto gasto", "gasto", "quanto gasta", "consumo", "chuveiro", "banho", "kwh", "custa")),
]


def detectar_intencao(texto: str) -> str:
    t = _norm(texto)
    for nome, chaves in INTENCOES:
        if any(k in t for k in chaves):
            return nome
    return "ajuda"


def responder(texto: str, premissas: dict | None = None) -> str:
    base = premissas or c.carregar_premissas()
    P, usados = extrair_dados(texto, base)
    intencao = detectar_intencao(texto)
    if intencao == "limites":
        return _ptbr(resp_limites(P))
    if intencao == "regras":
        t = _norm(texto)
        if any(k in t for k in ("aquecedor", "placa", "painel", "solar", "compensa")):
            return _ptbr(resp_regras(P, com_rodape=False) + "\n\n" + resp_comparar(P))
        return _ptbr(resp_regras(P))
    if intencao == "ambiente":
        return _ptbr(resp_ambiente(P))
    if intencao == "comparar":
        return _ptbr(resp_comparar(P))
    if intencao in ("B", "C"):
        return _ptbr(resp_alternativa(P, intencao))
    if intencao == "dicas":
        return _ptbr(resp_dicas(P))
    if intencao == "consumo":
        return _ptbr(resp_consumo(P, usados))
    return _ptbr(ajuda())
