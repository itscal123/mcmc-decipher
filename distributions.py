import autograd.numpy as np
from autograd.scipy.special import logsumexp


def log_normal_mvnormal(mu, sigma):
    """
    Cholesky decomposition. Fill in details later
    """
    def logp(x):
        k = mu.shape[0]
        return (
            k * np.log(2 * np.pi) + 
            np.log(np.linalg.det(sigma)) + 
            np.dot(np.dot(x-mu).T, np.linalg.inv(sigma), x-mu)
        ) * 0.5

    return logp