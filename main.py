import subprocess
import time
import requests
import ollama

def start_ollama():
    process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("Servidor Ollama inicializado....")
    return await_api(process)

def await_api(process):
    for _ in range(20):
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1)
            if r.status_code == 200:
                print("✅ Ollama está pronto para uso")
                return process
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    raise RuntimeError("Não foi possível conectar ao Ollama. Verifique a instalação.")

def main():
    ollama_process = start_ollama()

    print("Welcome :)")

    try:
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "quit":
                break

            print("\nAssistant (stream): ", end="")

            for chunk in ollama.chat(
                model="moondream",
                messages=[{"role": "user", "content": user_input}],
                stream=True,
                options={"num_predict": 50}
            ):
                print(chunk["message"]["content"], end="", flush=True)

            print()
    finally:
        ollama_process.terminate()
        print("\nFinalizando Ollama...")

if __name__ == "__main__":
    main()
