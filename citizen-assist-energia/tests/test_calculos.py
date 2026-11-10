import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest  # noqa: E402

from energia import calculos as c  # noqa: E402
from energia.assistente import responder, detectar_intencao  # noqa: E402


@pytest.fixture
def P():
    return c.carregar_premissas()


def test_energia_por_banho_formula(P):
    # 3,5 L/min x 8 min = 28 kg; ΔT=20 K; c=4,186 -> 2344 kJ -> 0,651 kWh; /0,98
    assert c.energia_por_banho_kwh(P) == pytest.approx(28 * 4.186 * 20 / 3600 / 0.98, rel=1e-6)


def test_potencia_coerente_com_chuveiro_real(P):
    assert 4.0 <= c.potencia_equivalente_kw(P) <= 6.0  # chuveiros: ~4,5 a 7,5 kW


def test_banho_mais_curto_gasta_menos(P):
    assert c.consumo_mensal_kwh(P, 6) < c.consumo_mensal_kwh(P, 8)


def test_todas_alternativas_economizam(P):
    for r in c.comparar(P):
        assert r.kwh_evitados_mes > 0
        assert r.economia_ano1 > 0


def test_fv_nao_evita_mais_que_a_demanda(P):
    r = c.avaliar(P, c.alternativa_C(P))
    assert r.kwh_evitados_mes <= c.consumo_mensal_kwh(P) + 1e-9


def test_tarifa_zero_nao_ha_economia(P):
    P["tarifa_kwh"] = 0
    r = c.avaliar(P, c.alternativa_B(P))
    assert r.economia_total == 0 and r.payback_anos is None


def test_co2_proporcional_ao_fator(P):
    r = c.comparar(P)[1]
    assert r.co2_evitado_kg == pytest.approx(r.kwh_evitados_total * P["emissao_rede_g_kwh"] / 1000)


def test_assistente_intencoes():
    assert detectar_intencao("quanto gasta o chuveiro de 4 pessoas?") == "consumo"
    assert detectar_intencao("qual compensa mais, aquecedor solar ou placa?") == "comparar"
    assert detectar_intencao("isso ajuda o meio ambiente?") == "ambiente"
    assert detectar_intencao("bom dia") == "ajuda"


def test_assistente_usa_dados_do_usuario_e_mostra_limitacoes():
    r = responder("quanto gasta o chuveiro de 2 pessoas com banho de 10 minutos, tarifa 0,90")
    assert "2 pessoas" in r and "10 min" in r and "0,90" in r
    assert "Condições" in r and "Fontes" in r


@pytest.mark.parametrize("frase,esperado", [
    ("minha conta veio cara", "dicas"),
    ("polui?", "ambiente"),
    ("quanto gasto de luz com 5 pessoas", "consumo"),
    ("tenho tarifa social", "regras"),
    ("como funciona o fio b?", "regras"),
])
def test_frases_encontradas_nos_testes_internos(frase, esperado):
    assert detectar_intencao(frase) == esperado


def test_extrai_somos_em_3():
    assert "3 pessoas" in responder("somos em 3 morando aqui, banho de 12 minutos")


def test_formato_brasileiro_e_meses():
    r = responder("qual compensa mais? tarifa 0,95")
    assert "0,95" in r and "cerca de 2 meses" in r and "0.95" not in r


def test_planeta_vai_para_ambiente_e_tarifa_social_combina_com_alternativas():
    assert detectar_intencao("energia solar ajuda o planeta?") == "ambiente"
    r = responder("tenho tarifa social, compensa o aquecedor solar?")
    assert "Tarifa Social" in r and "aquecedor solar de água" in r
