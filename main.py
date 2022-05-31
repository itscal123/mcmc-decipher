import mcmc
import utils
import numpy as np

# English alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# List representation of the alphabet
chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
         'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# Generate a random encryption cipher
encrypt_key = utils.generateEncryptionCipher()

# Prompt user for some text to be encrypted
user_input = input("Type text you wish to be encrypted:\n")

# Apply the key
encoded_text = utils.applyKey(encrypt_key, user_input)

# Display user input and encrypted input
print(f'\nUnencrypted text: \n{user_input}\n')
print(f'Encrypted text:\n{encoded_text}\n')

# Generate a random decryption key
decrypt_list = list(np.random.choice(chars, size=26, replace=False))
decrypt_key = "".join(decrypt_list)

# Run MCMC
# TODO

# Print decrypted text after MCMC
decoded_text = utils.applyKey(decrypt_key, encoded_text)
print(f'Decrypted text:\n{decoded_text}\n')

# Calculate the number of correct letters
guess, count, percent = utils.testCipher(encrypt_key, alphabet, decrypt_key)

# Print the true alphabet, decrypted alphabet, and correct decryptions
print(f'Correct alphabet:\n{alphabet}\n')
print(f'Decrypted alphabet:\n{guess}\n')
print(f'Number of correctly decoded letters:\n{count}\n')
print(f'Percentage of correctly decoded letters:\n{percent:.2f}\n')