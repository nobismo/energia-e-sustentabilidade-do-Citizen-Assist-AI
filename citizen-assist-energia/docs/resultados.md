# Resultados da análise (gerado automaticamente)

> Gerado por `python src/gerar_relatorio.py`. Valores ESTIMADOS; veja `data/premissas.json`.

## 1. Consumo de referência (situação atual)

Fórmulas:

- Energia por banho: `E = vazão × tempo × c × ΔT / η / 3600` (kWh)
- Potência equivalente: `P = E / tempo` (kW)
- Consumo mensal: `E × pessoas × banhos/dia × dias`
- Custo mensal: `kWh × tarifa`

| Grandeza | Valor |
|---|---|
| Energia por banho | 0.664 kWh |
| Potência equivalente do chuveiro | 4.98 kW |
| Banhos por mês | 120 |
| Consumo mensal do banho | 79.7 kWh |
| Custo mensal do banho | R$ 87.71 |
| Emissão mensal (rede) | 3.07 kgCO2 |

## 2. Comparação das alternativas (mesma necessidade, 10 anos)

| Alt. | Descrição | Renovável | Investimento | kWh evitados/mês | Economia 1º ano | Saldo líquido 10a | VPL | Retorno | R$/kWh evitado |
|---|---|---|---|---|---|---|---|---|---|
| A | Eficiência: banho mais curto + restritor de vazão | não | R$ 40 | 19.9 | R$ 263 | R$ 3,428 | R$ 1,996 | cerca de 2 meses | R$ 0.02 |
| B | Renovável térmica: aquecedor solar de água | sim | R$ 4,500 | 55.8 | R$ 692 | R$ 4,761 | R$ 925 | 5,6 anos | R$ 0.74 |
| C | Renovável elétrica: energia solar fotovoltaica | sim | R$ 3,200 | 79.7 | R$ 895 | R$ 8,402 | R$ 3,630 | 3,3 anos | R$ 0.38 |
| A+B | Combinação: eficiência (A) + aquecedor solar (B) | sim | R$ 4,540 | 61.8 | R$ 771 | R$ 5,761 | R$ 1,496 | 5,2 anos | R$ 0.67 |
| A+C | Combinação: eficiência (A) + fotovoltaico menor (C) | sim | R$ 2,440 | 79.7 | R$ 935 | R$ 9,644 | R$ 4,677 | 2,5 anos | R$ 0.29 |

*Saldo líquido = economia acumulada − investimento − manutenção (sem desconto). VPL com taxa de 10% a.a. Tarifa com reajuste de 6% a.a.*

## 3. Impacto ambiental

| Alt. | CO2 evitado (operação) | CO2 líquido com fabricação FV |
|---|---|---|
| A | 92 kg | n/d |
| B | 258 kg | n/d |
| C | 360 kg | -71 kg |
| A+B | 285 kg | n/d |
| A+C | 360 kg | 37 kg |

*A fabricação do aquecedor solar NÃO foi quantificada (sem fonte confiável).* 

## 4. Limitações por alternativa

- **A**: Depende de hábito (considerada adesão de 70%).
- **B**: Exige telhado com sol, reservatório e pressão adequada; o resto é apoio elétrico. Vida útil menor que o horizonte pode exigir reparo/troca.
- **C**: Sistemas muito pequenos podem não ser ofertados; kits comuns começam em ~1,5 a 2 kWp. A conta nunca zera: há o custo de disponibilidade (mínimo cobrado). Vale a pena considerar o Fio B (Lei 14.300) e a aprovação da distribuidora.
- **A+B**: Combina hábito e equipamento; a economia da parte B incide sobre a demanda já reduzida.
- **A+C**: Reduzir a demanda antes reduz o tamanho (e o custo) do sistema solar.

## 5. Premissas que o grupo ainda precisa verificar

- `duracao_banho_min` = 8 min (estimado): Premissa do grupo (banho médio).
- `vazao_l_min` = 3.5 L/min (estimado): Vazão típica de chuveiro elétrico (~3 a 5 L/min).
- `temp_agua_fria_c` = 19 °C (estimado): Média anual aproximada da água da rede na Grande São Paulo.
- `tarifa_kwh` = 1.1 R$/kWh (estimado): Estimada a partir da tarifa B1 da Enel SP (R$ 725,18/MWh sem tributos em 2025, Exame), reajuste médio de 10,18% em jul/2026 (ANEEL), mais ICMS, PIS/COFINS e bandeira.
- `escalada_tarifa_aa` = 0.06 a.a. (estimado): Premissa do grupo (reajustes recentes variaram de ~3% a ~14% ao ano).
- `A_vazao_l_min` = 3.0 L/min (estimado): Vazão com restritor/arejador (alternativa A).
- `A_custo_rs` = 40 R$ (estimado): Restritor de vazão/arejador (pesquisar preço em loja).
- `B_fracao_solar` = 0.7 fração (estimado): Fração solar anual típica de aquecedor solar em SP (~60 a 80%); o resto é apoio elétrico.
- `B_custo_rs` = 4500 R$ (estimado): Sistema compacto (coletores + reservatório) instalado; pedir 3 orçamentos.
- `C_produtividade_kwh_kwp_mes` = 112 kWh/kWp·mês (estimado): ~1.340 kWh/kWp/ano (irradiação ~4,6 kWh/m²/dia x desempenho 0,80). Conferir no CRESESB/SunData para o CEP.
- `C_custo_wp_rs` = 4.0 R$/Wp (publico): Média nacional R$ 2,45/Wp no 1T2026 (Solfácil/Cenário Energia); faixa instalada R$ 3,40 a 4,20/Wp (UAI, out/2026). Sistemas muito pequenos custam mais por Wp; adotado valor conservador.
- `C_degradacao_aa` = 0.005 a.a. (estimado): Perda típica de ~0,5%/ano dos módulos.
- `C_fator_credito` = 0.83 fração da tarifa (estimado): Energia injetada gera crédito, descontada a cobrança escalonada do Fio B (60% em 2026, Lei 14.300/2022, segundo Monitor do Mercado). Fio B assumido ~28% da tarifa.
- `emissao_ciclo_pv_g_kwh` = 41 gCO2e/kWh (publico): Mediana de ciclo de vida de FV de telhado (IPCC AR5, WGIII, Anexo III).
