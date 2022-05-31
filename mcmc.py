"""
File containing functions that run MCMC to find decryption cipher. 
"""
import utils
import math
import numpy as np


def mcmc(decrypt_key, encoded_text, iters=100000):
    """
    Function that uses the Metroplis-Hastings algorithm for our Markov Chain 
    Monte Carlo implementation.

    """
    # Get the character frequencies
    freqDict = utils.loadFreqDict()

    print('Running Markov Chain Monte Carlo')
    # Run the MCMC for the passed number of iterations
    for i in range(iters):
        # Make proposal
        proposal = utils.proposeKey(decrypt_key)
        # Calculate the quality of the current decryption cipher
        curr_score = utils.score(decrypt_key, encoded_text, freqDict)
        # Calculate the quality of the proposed decryption cipher
        new_score = utils.score(proposal, encoded_text, freqDict)

        # Calculate the acceptance probability (ratio between the current
        # score and proposed score)
        threshold = min(1, math.exp(new_score - curr_score))

        # Sample randomly from [0,1]
        accept = np.random.uniform()

        # Boolean flag denoting if we should accept the proposal
        acceptProposal = False if accept > threshold else True

        # Use new decryption cipher if we accept proposal
        if acceptProposal:
            decrypt_key = proposal

        # Print every 500th iteration
        if (i+1) == 1 or (i+1) % 500 == 0:
            decode = utils.applyKey(decrypt_key, encoded_text)
            score = utils.score(decrypt_key, encoded_text, freqDict)
            print(f'Iteration {i+1:>5} -> Score: {score:.2f}\n')
            print(f'Decrypted text:\n{decode}\n')
    
    # Return the final decryption cipher
    return decrypt_key