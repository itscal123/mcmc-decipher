import numpy as numpy
from collections import defaultdict
import pickle
import os.path

def generateFreqCounts(textFile):
    """
    Takes a .txt file and generates a dictionary with the frequencies of
    every two letter pairs in the given text file.
    ---------
    parameters:
        textFile (str): path to text file
    ---------
    returns:
        freq_dict (dict): frequency of all bigram character pairs
    """
    freq_dict = defaultdict(int)
    chars = set(['A','B','C','D','E','F','G','H','I','J','K','L','M',
                 'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])

    f = open(textFile)

    for line in f:
        # Conver to upper case
        line = str.upper(line)

        # Remove '\n' characters
        line = line[0:len(line)-1]

        # Count the frequency of bigram characters
        for i in range(len(line)-1):
            bigram = line[i] + line[i+1]

            # Non-letter + letter
            if (line[i] not in chars) and (line[i+1] in chars):
                bigram = ' ' + line[i+1]

            # Letter + non-letter
            elif (line[i] in chars) and (line[i+1] not in chars):
                bigram = line[i] + ' '

            # Two non-letters
            elif (line[i] not in chars) and (line[i+1] not in chars):
                bigram = '  '
            
            freq_dict[bigram] += 1

    # Pickle freq_dict
    with open('freq_dict.pkl', 'wb') as f:
        pickle.dump(freq_dict, f)
        

if __name__ == "__main__":
    if not os.path.exists('freq_dict.pkl'):
        generateFreqCounts('war_and_peace.txt')