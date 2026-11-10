# Testes com usuários (PREENCHER COM TESTES REAIS)

> ⚠️ Os campos abaixo são um modelo. **Não invente resultados**: aplique o teste com 3 a 5 pessoas do público-alvo (família, vizinhos, colegas) e registre o que aconteceu. Não coloque nome/endereço/CPF; use "Usuário 1", faixa etária e tipo de moradia.

## Roteiro de teste (5 min por pessoa)
1. Pedir que a pessoa pergunte, com suas palavras, quanto gasta o chuveiro dela.
2. Pedir que compare aquecedor solar e placa solar.
3. Perguntar: "Você entendeu? O que você faria agora?" e "Algum termo ficou difícil?" (kWh, payback, Fio B).
4. Nota de clareza (1 a 5) e utilidade (1 a 5).

## Registro
| # | Perfil (anônimo) | Situação testada | Comentário recebido | Nota clareza | Nota utilidade | Ajuste feito |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

## Ajustes realizados (histórico)
| Data | Problema observado | Mudança no código/texto | Commit |
|---|---|---|---|
| | | | |

## Ideias de ajuste prováveis (confirme se apareceram nos testes antes de citar)
- Explicar "kWh" com exemplo (um banho = X kWh).
- Trocar "payback" por "em quanto tempo se paga".

---

# Testes internos do grupo (REAIS, realizados com o assistente)

> **Importante:** estes foram testes feitos pela própria equipe, com frases variadas, **e não por usuários externos**. Se vocês conseguirem testar com pessoas de fora, registre na tabela acima e mantenha esta seção como complemento.

Foram testadas 20 frases com formas diferentes de perguntar (informais, curtas, maiúsculas, com número de moradores escrito de outro jeito).

## Falhas encontradas
| Frase testada | Problema | Ajuste feito |
|---|---|---|
| "minha conta veio cara" | Não reconheceu; mostrou só o menu de ajuda | Adicionadas palavras-chave ("cara", "conta alta") na intenção de dicas |
| "polui?" | Não reconheceu | Adicionada a palavra-chave "polui" na intenção de ambiente |
| "quanto gasto de luz com 5 pessoas" | Não reconheceu ("gasto" não estava mapeado) | Adicionada "gasto" na intenção de consumo |
| "tenho tarifa social" / "como funciona o fio b?" | Sem resposta específica | Criada a intenção "regras" com explicação de Tarifa Social e Fio B |
| "somos em 3 morando aqui, banho de 12 minutos" | Assistente usou 4 pessoas (padrão) e ignorou o "3" | Extração de pessoas passou a entender "somos em N" e "moramos N" |

Cada falha virou teste automático em `tests/test_calculos.py`, para não voltar a acontecer.

## Frases que já funcionavam
"quanto gasta o chuveiro de 2 pessoas, banho de 15 min, tarifa 0,80", "QUANTO GASTA O BANHO???", "vale a pena instalar painel solar?", "quanto custa o aquecedor solar", "qual a fonte desses dados?", "chuveiro 6 pessoas 5 minutos".

## Limitações conhecidas (não resolvidas)
- "energia solar compensa em casa alugada?" é tratada como comparação geral; não avisa que imóvel alugado exige autorização do proprietário.
- O assistente funciona por palavras-chave, então frases muito diferentes das previstas caem no menu de ajuda.

---

# Simulação com personas (SEM usuários reais)

> ⚠️ **Isto NÃO são testes com usuários reais.** Foram 5 personas fictícias, criadas a partir do público-alvo, cujas perguntas foram rodadas no assistente e avaliadas quanto à clareza (termos técnicos, formato de números, adequação da resposta). Serve como verificação de usabilidade; não substitui o teste com pessoas.

| Persona (fictícia) | Pergunta | Problema observado | Ajuste feito |
|---|---|---|---|
| Marta, 58, pouca familiaridade com tecnologia | "minha conta de luz veio muito cara, o que eu faço?" | Respondeu bem, mas usava a palavra "premissas" e "1.10" (ponto decimal) | Troca por "suposições"; números em formato brasileiro (1,10) |
| João, 22, mora de aluguel | "quanto gasta o chuveiro? somos em 3, banho de 15 minutos" | "kWh" sem explicação | Frase explicando que kWh é a unidade da conta de luz |
| Carla, 35, casa própria | "vale a pena instalar placa solar? tarifa 0,95" | "retorno: 0.2 anos" confuso e ponto decimal | Retornos menores que 1 ano aparecem em meses ("cerca de 2 meses"); vírgula decimal |
| Pedro, 67, CadÚnico | "tenho tarifa social, compensa o aquecedor solar?" | Só explicou as regras e não respondeu se o aquecedor compensa | Resposta passou a combinar a explicação das regras com a comparação das alternativas |
| Lucas, 17, curioso | "energia solar ajuda o planeta?" | Recebeu resposta financeira em vez de ambiental | Palavras "planeta" e "clima" adicionadas à intenção de ambiente |

Também: "kWp" ganhou explicação ("potência das placas") e "Fio B" passou a ser descrito como "taxa de uso da rede".
Cada ajuste tem teste automático em `tests/test_calculos.py` (17 testes no total).

## Como descrever isso na entrega e no vídeo
Diga a verdade: "além de testes internos, simulamos 5 perfis de usuários fictícios e ajustamos a linguagem; **ainda não testamos com pessoas reais**". Se conseguir uma pessoa real depois, registre na primeira tabela deste arquivo.
