from cryptography.fernet import Fernet


key = Fernet.generate_key()

print("Adicione essa key no seu arquivo .env:\n\n", key, "\n\n")

