import sys
try:
    import gemma_client
except ImportError:
    sys.exit("❌ Could not import 'gemma_client'. Make sure you run this script from the root of the repo folder.")

def main():
    print("=" * 60)
    print("🚀 Gemma 4 Terminal Chat Interface")
    print("Type your message and press Enter. Type 'exit' or 'quit' to end.")
    print("=" * 60)

    # Optional system/context instructions if supported by your repo's client
    system_prompt = "You are a helpful and concise AI assistant."

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nExiting session. Goodbye!")
                break

            print("\n🤖 Gemma:", end=" ", flush=True)

            # Check available functions in gemma_client module
            if hasattr(gemma_client, "ask"):
                response = gemma_client.ask(user_input)
                print(response)
            elif hasattr(gemma_client, "generate"):
                response = gemma_client.generate(user_input)
                print(response)
            elif hasattr(gemma_client, "chat"):
                response = gemma_client.chat(user_input)
                print(response)
            else:
                # Direct fallback to standard client usage
                print("\n[Calling gemma_client...]")
                response = gemma_client.ask_with_image(None, user_input) if hasattr(gemma_client, "ask_with_image") else "No recognized query method in gemma_client."
                print(response)

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()