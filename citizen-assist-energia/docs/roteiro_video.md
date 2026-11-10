# Roteiro do vídeo técnico (máx. 3 min, YouTube não listado)

**Meta:** ~2:45 de vídeo. Grave a tela (OBS, Zoom ou Game Bar do Windows) com a câmera dos integrantes opcional. Fale devagar; ensaie 1 vez com cronômetro.
**Antes de gravar:** abrir `docs/resultados.md` (ou o CSV), um terminal com `python src/main.py` pronto e a pasta do repositório no GitHub.

| Tempo | Tela | Fala (leia ou adapte com suas palavras) |
|---|---|---|
| **0:00–0:15** (abertura) | Slide/título com nome do projeto e integrantes | "Olá! Somos [nomes], da turma 1CC. Este é o módulo de **energia e sustentabilidade** do Citizen Assist AI, nosso assistente digital para cidadãos." |
| **0:15–0:35** (público e necessidade) | Slide: casa, chuveiro, conta de luz | "Nosso público são **famílias de casas na Grande São Paulo** que querem reduzir a conta de luz. O alvo é o **banho quente com chuveiro elétrico**, que usa cerca de 5 quilowatts e pesa bastante na conta. Nosso assistente ajuda essa família a entender quanto gasta e qual alternativa compensa." |
| **0:35–1:05** (análise de consumo) | `docs/resultados.md`, seção 1 (fórmula e tabela) | "Calculamos a energia pela física da água: **massa vezes calor específico vezes variação de temperatura**. Para uma família de 4 pessoas, banho de 8 minutos, dá **0,66 kWh por banho**, cerca de **80 kWh por mês**, ou **88 reais por mês**. A tarifa de R$ 1,10 por kWh é **estimada** a partir da Enel SP e deve ser trocada pelo valor da conta do usuário. A emissão usa o fator do MCTI: 38,5 gramas de CO₂ por kWh." |
| **1:05–1:40** (comparação das alternativas) | Tabela da seção 2 de `resultados.md` | "Comparamos a **mesma necessidade em 10 anos**. **A:** banho mais curto e restritor de vazão: R$ 40, retorno em poucos meses, mas depende de hábito, por isso usamos 70% de adesão. **B, renovável térmica:** aquecedor solar, R$ 4.500, retorno de 5,6 anos. **C, renovável elétrica:** energia solar fotovoltaica, R$ 3.200, retorno de 3,3 anos. A **combinação A mais C** tem o melhor retorno: 2,5 anos. Quando reduzimos o consumo antes, o sistema solar fica menor e mais barato." |
| **1:40–1:55** (ambiente) | Seção 3 (impacto ambiental) | "Um achado importante: como a rede brasileira já é limpa, a solar evita pouco CO₂. Descontando a fabricação das placas, o saldo é próximo de zero. O ganho é **financeiro e de autonomia**, e o assistente explica isso com honestidade." |
| **1:55–2:25** (demo do assistente) | Terminal com `python src/main.py` | Digite e deixe a resposta aparecer: **1)** "Quanto gasta o chuveiro de 4 pessoas com banho de 10 minutos?" **2)** "Qual compensa mais: aquecedor solar ou placa solar? tarifa 0,95" Fale: "O assistente lê pessoas, minutos e tarifa da pergunta, recalcula e responde em linguagem simples. Toda resposta termina com **condições e fontes**." |
| **2:25–2:50** (recomendações e limitações) | Última resposta (limites) ou slide de resumo | "Nossa recomendação: **comece pela alternativa A**; se tiver telhado e capital, compare B e C com a sua tarifa. **Limitações:** custos, tarifa e geração são estimativas, não garantia; regras como o Fio B, o telhado e a Tarifa Social mudam o resultado. Validamos com [N] usuários e ajustamos [o que mudou, de `testes_usuarios.md`]." |
| **2:50–3:00** (encerramento) | Repositório GitHub | "Código, dados, cálculos, referências e testes estão no nosso GitHub. Obrigado!" |

## Dicas
- Se estourar 3:00, corte a parte de ambiente para 1 frase ou reduza a leitura de números; **o limite é duro**.
- **Troque** os números da fala se mudar premissas (rode `python src/gerar_relatorio.py` e releia a tabela).
- A frase sobre testes com usuários só pode ser dita **depois que você fizer os testes reais**.
- Cada integrante deve falar em alguma parte (mostra compreensão).
- Publicar no YouTube como **Não listado** e testar o link em aba anônima.
