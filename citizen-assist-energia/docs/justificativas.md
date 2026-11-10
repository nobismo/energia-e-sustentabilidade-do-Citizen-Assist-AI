# Justificativas das recomendações

Resultados numéricos: `docs/resultados.md`. Valores abaixo referem-se ao cenário padrão e são **estimativas**.

## Por que o banho?
O chuveiro elétrico converte eletricidade em calor com potência alta (~5 kW). Mesmo usado poucos minutos por dia, o produto **potência × tempo** (energia, kWh) é grande. Com base no balanço de energia da água (`E = m·c·ΔT/η`), obtivemos ~0,66 kWh por banho, coerente com um chuveiro de ~5 kW (teste automático em `tests/`).

## Alternativa A · Eficiência (banho curto + restritor)
- **Custo:** ~R$ 40. **Viabilidade:** alta, qualquer morador, inclusive quem aluga.
- **Ambiente:** reduz consumo de energia e de água.
- **Limite:** depende de hábito; usamos adesão de 70%.
- **Recomendação:** **primeiro passo para todos.**

## Alternativa B · Aquecedor solar (renovável térmico)
- **Custo:** ~R$ 4.500 (estimado, verificar). **Retorno:** ~5,6 anos no cenário padrão.
- **Viabilidade:** média; precisa de telhado ensolarado, reservatório e pressão adequada; exige imóvel próprio.
- **Ambiente:** usa calor do sol diretamente (alta eficiência), sem eletrônica; vida útil menor que a do FV.
- **Quando recomendar:** quem tem casa própria e quer independência das regras da distribuidora.

## Alternativa C · Energia solar fotovoltaica (renovável elétrico)
- **Custo:** ~R$ 3.200 para ~0,8 kWp (estimado). **Retorno:** ~3,3 anos no cenário padrão.
- **Viabilidade:** média; telhado, aprovação da distribuidora e regras de compensação (Fio B). Sistemas tão pequenos quase não existem no mercado; na prática o kit é maior e atende mais cargas da casa.
- **Ambiente:** como a rede brasileira já é limpa (~38,5 g/kWh), o CO₂ evitado é pequeno e, descontando a fabricação (~41 g/kWh), o saldo é próximo de zero. O benefício é principalmente **financeiro e de autonomia**.

## Combinações
**A+C** tem o menor investimento e melhor retorno no cenário padrão: reduzir a demanda antes diminui o tamanho do sistema solar.

## O que o assistente diz ao usuário
1. Comece pela A.
2. Se tem telhado e capital, compare B e C com seus dados (tarifa, pessoas).
3. Não prometa economia: use faixas e condições.
4. Não venda a solar como "salvadora do clima" no Brasil; seja honesto sobre o ganho ambiental.

## Análise de sensibilidade sugerida (fazer antes da entrega)
Rode o assistente com tarifa 0,70 / 1,10 / 1,50 e com `escalada_tarifa_aa = 0` e registre como o ranking muda.
