"""Chat de terminal do módulo de energia do Citizen Assist AI.

Execute:  python src/main.py
Digite 'sair' para encerrar.
"""
from energia.assistente import ajuda, responder


def main() -> None:
    print("=== Citizen Assist AI · módulo Energia ===\n")
    print(ajuda(), "\n")
    while True:
        try:
            texto = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if texto.lower() in {"sair", "exit", "q"}:
            break
        if texto:
            print("\nAssistente:", responder(texto), "\n")


if __name__ == "__main__":
    main()
