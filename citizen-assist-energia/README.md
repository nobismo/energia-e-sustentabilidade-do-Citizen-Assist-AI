# Citizen Assist AI · Módulo de Energia e Sustentabilidade
**Global Solution 2026 · Soluções em Energias Renováveis e Sustentáveis · Ciência da Computação (1CC)**

> **Contribuição desta disciplina:** pasta `src/energia/` + `data/` + `docs/`.
> Se o repositório for compartilhado com outras disciplinas, mantenha tudo da disciplina dentro destes caminhos.

## Integrantes
| Nome completo | RM |
|---|---|
| Rodrigo Zambelle | 570425 |
| Rodrigo Santana | 572454 |
| Nickolas Emanuel | 573483 |

## Público e problema
**Público:** famílias de casas na Grande São Paulo (ex.: Cotia/SP), de baixa a média renda, que querem reduzir a conta de luz e têm dúvida se vale investir em energia solar.
**Necessidade energética:** o **banho quente com chuveiro elétrico** (~5 kW), um dos usos que mais pesam na conta residencial. Para uma família de 4 pessoas com banho de 8 min, são ~80 kWh/mês (~R$ 88/mês, estimativa).
**Como ajudamos:** o assistente responde, em linguagem simples, *quanto se gasta*, *quais alternativas existem*, *quanto custam*, *em quanto tempo se pagam* e *o que isso muda para o meio ambiente*, sempre com fontes e limitações.

## Funcionalidades de energia
1. Calcula consumo e custo do banho a partir de **pessoas, minutos de banho e tarifa** informados pelo usuário (ou valores padrão).
2. Compara alternativas para a **mesma necessidade e o mesmo período (10 anos)**:
   - **A** – Eficiência (banho mais curto + restritor de vazão)
   - **B** – **Renovável térmica:** aquecedor solar de água
   - **C** – **Renovável elétrica:** energia solar fotovoltaica
   - **A+B** e **A+C** – combinações
3. Mostra investimento, economia, retorno (payback), VPL, custo por kWh evitado e CO₂.
4. Explica limitações e referências em toda resposta.

## Como executar
```bash
# Python 3.10+ (sem dependências externas)
python src/main.py                         # chat no terminal
python src/gerar_relatorio.py              # gera docs/resultados.md e data/resultados.csv
pip install pytest && python -m pytest -q  # testes automáticos
```
**Integração com o Citizen Assist AI (outras disciplinas):**
```python
from energia.assistente import responder
resposta = responder("Quanto gasta o chuveiro de 4 pessoas?")   # devolve texto pronto
```
O assistente principal só precisa chamar `responder()` quando detectar tema de energia/conta de luz/banho.

## Exemplos para testar
- `Quanto gasta o chuveiro de 4 pessoas com banho de 10 minutos?`
- `Qual compensa mais: aquecedor solar ou placa solar? tarifa 0,95`
- `Isso ajuda o meio ambiente?`
- `Quais os limites dessas estimativas?`

## Estrutura
```
data/premissas.json      dados, unidades, origem, tipo (público/físico/estimado) e flag "verificar"
data/resultados.csv      resultados da comparação (gerado)
src/energia/calculos.py  física (E=m·c·ΔT), fluxo de caixa, payback, VPL, CO2
src/energia/assistente.py respostas do assistente baseadas nos cálculos
src/main.py              chat de terminal
src/gerar_relatorio.py   gera relatório
tests/                   testes automáticos
docs/resultados.md       cálculos e comparação (gerado)
docs/justificativas.md   recomendações: custo, viabilidade, ambiente
docs/referencias.md      fontes
docs/testes_usuarios.md  registro dos testes com usuários e ajustes
docs/roteiro_video.md    roteiro do vídeo de 3 min
```

## Principais resultados (valores estimados; ver `docs/resultados.md`)
Resultados do cenário padrão (4 pessoas, 8 min, tarifa estimada R$ 1,10/kWh, horizonte de 10 anos). Para o seu caso, informe sua tarifa/consumo no assistente. A fabricação do aquecedor solar não foi quantificada.

| Alt. | Investimento | Economia 1º ano | Retorno | CO₂ evitado em 10 anos |
|---|---|---|---|---|
| A · Eficiência | R$ 40 | R$ 263 | 0,2 ano | 92 kg |
| B · Aquecedor solar | R$ 4.500 | R$ 692 | 5,6 anos | 258 kg |
| C · Fotovoltaico | R$ 3.200 | R$ 895 | 3,3 anos | 360 kg (saldo c/ fabricação: −71 kg) |
| A+C | R$ 2.440 | R$ 935 | 2,5 anos | 360 kg (líquido +37 kg) |

## Limitações
Tarifa, custos e produção solar são **estimativas**; não há garantia de economia. Regras de compensação (Fio B, Lei 14.300), telhado, sombreamento e Tarifa Social alteram o resultado. Consulte orçamentos e profissional habilitado.
