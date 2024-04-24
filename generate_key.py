from cryptography.fernet import Fernet

# Generate a Fernet key
key = Fernet.generate_key()

# Save the key to a file
with open('encrypt_key.txt', 'wb') as file:
    file.write(key)
