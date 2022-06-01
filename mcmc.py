"""
File containing functions that run MCMC to find decryption cipher. 
"""
import utils
import math
import numpy as np


def mcmc(decrypt_key, encoded_text, rng, iters=50000):
    """
    Function that uses the Metroplis-Hastings algorithm for our Markov Chain 
    Monte Carlo implementation.

    ----------
    params:
        decrypt_key (str): String representation of the decryption cipher
        encoded_text (str): Passed encrypted text
        rng (generator): Seeded random number generator
        iters (int): Number of MCMC iterations, default 50,000
    returns:
        decrypt_key (str): Decryption cipher sampled from MCMC
    """
    # Get the character frequencies
    freqDict = utils.loadFreqDict()

    print('Running Markov Chain Monte Carlo')
    # Run the MCMC for the passed number of iterations
    for i in range(iters):
        # Make proposal
        proposal = utils.proposeKey(decrypt_key, rng)
        # Calculate the quality of the current decryption cipher
        curr_score = utils.score(decrypt_key, encoded_text, freqDict)
        # Calculate the quality of the proposed decryption cipher
        new_score = utils.score(proposal, encoded_text, freqDict)

        # Calculate the acceptance probability (ratio between the current
        # score and proposed score)
        accept_ratio = min(1, np.exp(new_score - curr_score))

        # Sample randomly from [0,1]
        randnum = rng.uniform()

        # Boolean flag denoting if we should accept the proposal
        acceptProposal = False if randnum > accept_ratio else True

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


def leapfrog(q, p, dVdq, path_len, step_size):
    """
    Helper function for Hamiltonian Monte Carlo that uses leapfrog integration to numerically integrate
    differential equations
    ----------
    params:
        q (np.float64): initial position
        p (np.float64): initial momentum
        dVdq (callable): gradient of the velocity
        path_len (float): how long to integrate for
        step_size (float): how long each integration step should be

    returns:
        q, p (np.float64, np.float64): updated position and momentum
    """
    # TODO

"""
Useful links:
HMC
https://pythonhosted.org/pyhmc/

https://towardsdatascience.com/python-hamiltonian-monte-carlo-from-scratch-955dba96a42d

https://colindcarroll.com/2019/04/11/hamiltonian-monte-carlo-from-scratch/
----------------------------------------
Metropolis Hastings
https://jfking50.github.io/decipher/
"""