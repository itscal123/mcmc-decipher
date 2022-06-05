import pickle
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, median, stdev
from collections import defaultdict


def loadFreqDict():
    """
    Loads the generated frequency dictionary, used later during MCMC
    --------
    params:
        None:
    returns:
        freq_dict (dict): Dictionary that contains the frequency counts of bigram character pairs
    """
    with open('./data/freq_dict.pkl', 'rb') as f:
        return pickle.load(f)


def mapKey(key):
    """
    Uses a given cipher to construct a dictionary that maps the letter from the key to the 
    corresponding letter in the alphabet
    --------
    params:
        key (str): An encryption or decryption cipher
    --------
    returns:
        mapping (dict): New mapping between cipher letters and alphabet letters
    """
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    # Return the mapping between the cipher and alphabet
    return {alphabet[i] : key[i] for i in range(len(key))}


def applyKey(key, text):
    """
    Encrypts/Decrypts the given text based on the provided cipher. Returns the
    encrypted or decrypted text.
    --------
    params:
        key (str): An encryption or decryption cipher
        text (str): Some string of text
    --------
    returns:
        transformed (str): The transformed text
    """
    transformed = ""

    # Convert the text to a list
    text = list(text)

    # Get the mapping from mapKey
    mapping = mapKey(key)

    # Apply the mapping to the input text
    for letter in text:
        letter = str.upper(letter)
        # Apply the switch
        if letter in mapping: 
            transformed += mapping[letter]
        # Otherwise add a space
        else:
            transformed += " "
    
    # Return the final transformed text
    return transformed


def score(key, text, freq_dict):
    """
    Calculates the score of a decryption cipher based on its log likelihood with the
    reference text transition
    ----------
    params:
        key (str): Decryption cipher
        text (str): Encrypted text
        freq_dict (dict): Dictionary of frequency counts generated from the reference text
    ----------
    returns:
        score (float): log likelihood of the decryption cipher based on the encrypted text
    """
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    # Decode the given text
    decoded = applyKey(key, text)

    # Initialize score and target frequencies
    score = 0
    targetFreq = defaultdict(int)
    
    # Strip the text
    stripped = decoded.strip()

    # Count the number of two letter pairs in the next target
    for i in range(len(stripped) - 1):
        bigram = stripped[i] + stripped[i+1]

        # Non-letter + letter
        if (stripped[i] not in alphabet) and (stripped[i+1] in alphabet):
            bigram = ' ' + stripped[i+1]

        # Letter + non-letter
        elif (stripped[i] in alphabet) and (stripped[i+1] not in alphabet):
            bigram = stripped[i+1] + ' '

        # Two non-letters
        elif (stripped[i] not in alphabet) and (stripped[i+1] not in alphabet):
            bigram = '  '

        targetFreq[bigram] += 1

    # Calculate the log likelihood score
    for key, value in targetFreq.items():
        if key in freq_dict:
            score += np.log(value) + np.log(freq_dict[key])

    return score


def proposeKey(key, rng):
    """
    Takes a decryption cipher, and generates a new proposal to it.
    Currently working with substitutions (may change later)
    -------------
    params:
        key (str): String representation of a cipher
        rng (generator): Seeded random number generator
    returns:
        proposal (str): new proposed cipher
    """
    proposal = ''
    chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
               'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    # Randomly swap two characters
    char1, char2 = rng.choice(chars, size=2, replace=False)

    # Create the new proposal
    new_key = list(key)

    # Mark the spots in the key that contained the proposed characters to swap
    for i in range(len(new_key)):
        if new_key[i] == char1:
            index1 = i
        if new_key[i] == char2:
            index2 = i

    # Swap the characters in the original key
    new_key[index1] = char2
    new_key[index2] = char1

    # Generate the new proposal based on the new key
    for letter in new_key:
        proposal += letter

    return proposal


def generateEncryptionCipher(rng):
    """
    Generate a random substitution cipher
    --------
    params:
        rng (generator): Seeded random number generator
    returns:
        cipher (str): An encryption cipher
    """
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    cipher = ''
    encryption = list(rng.choice(alphabet, size=26, replace=False))

    for char in encryption:
        cipher += char

    return cipher


def testCipher(encrypt_key, base, decrypt_key):
    """
    Test function that evaluates the quality of the decryption cipher. Based on the number of correct letter assignments
    --------
    params:
        encrypt_key (str): String representation of the encryption cipher used
        
        base (str): String representation of what we are trying to decipher

        decrypt_key (str): String representation of the decryption cipher 
                           generated during MCMC
    returns:
        (str, int, float): The decrypted base text and number 
                           percentage of correct letters
    """
    # Apply encode then decode the base text
    test = applyKey(encrypt_key, base)
    guess = applyKey(decrypt_key, test)
    correct, total = 0, 0

    # Count correct letters
    for i in range(len(base)):
        if base[i] == guess[i]:
            correct += 1
        total += 1
    
    # Return the total number of correct and percentage (as a tuple)
    return guess, correct, correct/total


# TODO: Convert decryption key to potential energy representation
def toPosition(decrypt_key):
    return 


# TODO: Convert potential energy representation to decrypt key
def toDecryptKey(potential):
    return


def summary(encrypt_key, base, ciphers):
    """
    Helper function that generates and prints some summary statistics based on the MCMC runs. Summary stats calculated 
    include:
        - Mean
        - Standard deviation
        - Median
        - Min
        - Max
    -----------
    params:
        histories (iterable): An iterable of MCMC scores corresponding to each run of the MCMC function.
    returns:
        None
    """
    # Generate normalized accuracy for each cipher
    data = [100 * (testCipher(encrypt_key, base, decrypt_key))[2] for decrypt_key, _ in ciphers]

    # Output summary stats
    print('Summary Stats')
    print('----------------')
    print(f'Mean: {mean(data):.2f}')
    print(f'Std Dev: {stdev(data):.2f}')
    print(f'Median: {median(data):.2f}')
    print(f'Max: {data[0]:.2f}')
    print(f'Min: {data[-1]:.2f}')


# Function that visualizes history curve
def plotHistories(histories):
    """
    Helper function that reads through some collection of histories (i.e., runs of different MCMC) and plots them 
    along iteration time. Function saves the plot in the plots folder
    params:
        histories (iterable): An iterable of history arrays that record the MCMC run's score at each iteration
    returns:
        None
    """
    plt.rcParams["figure.figsize"] = (10,6)
    plt.gcf().set_dpi(400)

    # Find number of iterations
    iters = [i for i in range(1, len(histories[0])+1)]

    # Plot lines
    for idx, history in enumerate(histories):
        plt.plot(iters, history, label=f'Run {idx+1}')
    
    # Set figure parameters
    plt.legend()
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Score across MCMC runs')
    plt.savefig('plots/plot.png')