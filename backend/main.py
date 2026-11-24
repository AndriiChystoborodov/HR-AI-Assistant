import argparse
from agent import run_main_flow


def main():
    parser = argparse.ArgumentParser(description="LeafAI terminal chatbot")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print source/debug logs from backend flow"
    )
    args = parser.parse_args()

    print("LeafAI terminal chat")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSee you later!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("See you later!")
            break

        try:
            answer = run_main_flow(user_input, debug=args.debug)
            print(f"\nLeafAI: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()