from mcmc import mcmc
import utils
import numpy as np

# Set random seed (using new preferred practice)
rng = np.random.default_rng(0)

# English alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Dummy text
dummy_less = """
    There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some 
    form, by injected humour, or randomised words which don't look even slightly believable.
"""

dummy = """
    There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some 
    form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a 
    passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the 
    Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true 
    generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence 
    structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from 
    repetition, injected humour, or non-characteristic words etc.
"""

# List representation of the alphabet
chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
         'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# Generate a random encryption cipher
encrypt_key = utils.generateEncryptionCipher(rng)

# Prompt user if they want to use the predefined text or put in their own input
prompt = input('Would you like to use predefined text? [Y/N]\n')

# Use dummy text if user presses Y or y, otherwise use user input
if prompt == 'Y' or prompt == 'y':
    # Boolean flag indicating whether we used the full or reduced version
    full = True
    prompt = input('Would you like to use the full sample prompt? [Y/N]\n')
    if prompt == 'Y' or prompt == 'y':
        user_input = dummy
    else:
        user_input = dummy_less
        full = False
        
# Prompt user for some text to be encrypted
else:
    user_input = input("Type text you wish to be encrypted:\n")

# Apply the key
encoded_text = utils.applyKey(encrypt_key, user_input)

# Display user input and encrypted input
print(f'\nUnencrypted text: \n{user_input}\n')
print(f'Encrypted text:\n{encoded_text}\n')

# Initialize array to store decryption ciphers and history curves
ciphers, histories = [], []

# 10 Runs of MCMC
for _ in range(10):
    # Generate a random decryption key
    decrypt_list = list(rng.choice(chars, size=26, replace=False))
    decrypt_key = "".join(decrypt_list)

    # Convert decryption key to position representation
    position = utils.toPosition(decrypt_key)

    # Run MCMC
    decrypt_key, history, score = mcmc(decrypt_key, encoded_text, rng, 10000)

    # Record the decryption cipher and history
    ciphers.append((decrypt_key, score))
    histories.append(history)

# Output the history curve
if full:
    filepath = 'plots/plot_full.png'
else:
    filepath = 'plots/plot_reduce.png'
utils.plotHistories(histories, filepath)

# Print decrypted text after MCMC
ciphers.sort(key=lambda x: x[1])
decrypt_key = ciphers[0][0]
decoded_text = utils.applyKey(decrypt_key, encoded_text)
print('----------------------')
print(f'Original text:\n{user_input}\n')
print(f'Final decrypted text:\n{decoded_text}\n')

# Calculate the number of correct letters
guess, count, percent = utils.testCipher(encrypt_key, alphabet, decrypt_key)

# Print the true alphabet, decrypted alphabet, and correct decryptions
print(f'Correct alphabet:\n{alphabet}\n')
print(f'Encryption Key {encrypt_key}\n')
print(f'Decrypted alphabet:\n{guess}\n')
print(f'Number of correctly decoded letters:\n{count}\n')
print(f'Percentage of correctly decoded letters:\n{percent * 100:.2f}%\n')

# Generate summary statistics
utils.summary(encrypt_key, alphabet, ciphers)