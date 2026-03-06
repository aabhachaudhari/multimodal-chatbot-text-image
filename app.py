import os
import sys
from dotenv import load_dotenv
from colorama import Fore, Style, init
from utils.gemini_helper import create_client, chat_text, chat_image
from utils.image_handler import load_image, is_valid_image

init(autoreset=True)

def load_key():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print(Fore.RED + "ERROR: No API key found in .env file!")
        sys.exit(1)
    return key

def banner():
    print(Fore.CYAN + """
╔══════════════════════════════════════╗
║      🤖 MULTI-MODAL CHATBOT 🤖       ║
╚══════════════════════════════════════╝
""")
    print("Commands:")
    print("  Type anything        → chat with AI")
    print("  /image photo.jpg     → analyze an image")
    print("  /clear               → clear history")
    print("  /quit                → exit")
    print(Fore.CYAN + "─" * 40 + "\n")

def main():
    key = load_key()
    client = create_client(key)
    history = []
    banner()

    while True:
        try:
            user = input(Fore.BLUE + "You: " + Fore.WHITE).strip()
            if not user:
                continue

            if user.lower() in ["/quit", "/exit"]:
                print(Fore.CYAN + "Goodbye! 👋")
                break

            elif user.lower() == "/clear":
                history = []
                print(Fore.YELLOW + "Chat history cleared!\n")

            elif user.lower().startswith("/image "):
                parts = user[7:].strip().split(" ", 1)
                path = parts[0]
                question = parts[1] if len(parts) > 1 else "Describe this image."

                if not is_valid_image(path):
                    print(Fore.RED + "Not a valid image! Use .jpg .png .webp\n")
                    continue

                img_bytes, mime, err = load_image(path)
                if err:
                    print(Fore.RED + f"Error: {err}\n")
                    continue

                print(Fore.GREEN + "Gemini is looking at your image...")
                reply, err = chat_image(client, img_bytes, mime, question, history)
                if err:
                    print(Fore.RED + f"Error: {err}\n")
                else:
                    print(Fore.GREEN + f"\n🤖 Gemini: {reply}\n")
                    history.append({"role": "user", "content": f"[image] {question}"})
                    history.append({"role": "model", "content": reply})

            else:
                print(Fore.GREEN + "Gemini is thinking...")
                reply, err = chat_text(client, user, history)
                if err:
                    print(Fore.RED + f"Error: {err}\n")
                else:
                    print(Fore.GREEN + f"\n🤖 Gemini: {reply}\n")
                    history.append({"role": "user", "content": user})
                    history.append({"role": "model", "content": reply})

        except KeyboardInterrupt:
            print(Fore.CYAN + "\nGoodbye! 👋")
            break

if __name__ == "__main__":
    main()