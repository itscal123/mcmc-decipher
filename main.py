import mcmc
import utils

# Generate a random encryption cipher
encrypt_key = utils.generateEncryptionCipher()

# Prompt user for some text to be encrypted
user_input = input("Type text you wish to be encrypted:\n")

# Apply the key
encoded_text = utils.applyKey(encrypt_key, user_input)

# Display user input and encrypted input
print(f'\nUnencrypted text: \n{user_input}')
print()
print(f'Encrypted text:\n{encoded_text}')