import numpy as np
from scipy.special import erf

class Tracer:
    def n_of_z(self, z) -> np.ndarray:
        """
        Returns the normalized redshift distribution n(z) for the tracer.
        Parameters:
            z (np.ndarray): Array of redshift values.
        Returns:
            np.ndarray: Array of n(z) values corresponding to input redshifts.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def n_of_L(self, L) -> np.ndarray:
        """
        Returns the luminosity function n(L) for the tracer.
        Parameters:
            L (np.ndarray): Array of luminosity values.
        Returns:
            np.ndarray: Array of n(L) values corresponding to input luminosities.
        """        
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def sample_redshifts(self, n) -> np.ndarray:
        """
        Generates a sample of redshifts according to the tracer's n_of_z distribution using rejection sampling.
        Parameters:
            n (int): Number of redshift samples to generate.
        Returns:
            np.ndarray: Array of sampled redshifts.
        """
        samples = []
        z_min, z_max = 0.0, 5.0
        max_prob_estimate = self.max_prob_estimate

        while len(samples) < n:
            # Generate a batch of proposed redshifts and probabilities
            batch_size = (n - len(samples)) * 3 # Oversample to improve acceptance rate. Guess the efficiency is ~1/3
            z_proposal = np.random.uniform(z_min, z_max, size=batch_size) # Uniform random redshift proposals
            prob_proposal = np.random.uniform(0, max_prob_estimate, size=batch_size) # Uniform random probabilities

            # Determine which proposals are accepted by evaluating n_of_z at proposed redshifts
            accepted = prob_proposal < self.n_of_z(z_proposal) # Vectorised acceptance mask

            # Append accepted samples to the list of samples
            samples.extend(z_proposal[accepted]) # Append accepted samples

        return np.array(samples[:n]) # Return only the requested number of samples
    
    def sample_absolute_magnitudes(self, n) -> np.ndarray:
        """
        Generates a sample of absolute magnitudes for the tracer.
        Parameters:
            n (int): Number of absolute magnitude samples to generate.
        Returns:
            np.ndarray: Array of sampled absolute magnitudes.
        """        # Placeholder implementation: uniform distribution between -22 and -18
        return np.random.uniform(-22, -18, size=n)
    
    def sample_colors(self, n) -> np.ndarray:
        """
        Generates a sample of colors for the tracer.
        Parameters:
            n (int): Number of color samples to generate.
        Returns:
            np.ndarray: Array of sampled colors.
        """        # Placeholder implementation: uniform distribution between 0 and 2
        return np.random.uniform(0, 2, size=n)
    
    def sample_peculiar_velocity(self, n) -> np.ndarray:
        """
        Generates a sample of velocities for the tracer.
        Parameters:
            n (int): Number of velocity samples to generate.
        Returns:
            np.ndarray: Array of sampled velocities.
        """        # Placeholder implementation: normal distribution with mean 0 and stddev 300 km/s
        return np.random.normal(0, 300, size=n)
    
    def sample_halo_mass(self, n) -> np.ndarray:
        """
        Generates a sample of halo masses for the tracer.
        Parameters:
            n (int): Number of halo mass samples to generate.
        Returns:
            np.ndarray: Array of sampled halo masses.
        """        # Placeholder implementation: log-normal distribution with mean 12 and stddev 0.5 in log10(M/Msun)
        return 10 ** np.random.normal(12, 0.5, size=n)

# ------------------------------------------------------------------------------ Tracer Subclasses ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------ LRG Tracer ------------------------------------------------------------------------------

class LRG(Tracer): # Luminous Red Galaxy
    def __init__(self):
        """
        Initializes the LRG tracer with specific parameters.

        :param self: Instance of LRG class
        """
        self.z_min = 0.4
        self.z_max = 1.0
        self.sigma = 0.1
        self.norm = 1.0 / (self.z_max - self.z_min)

    def n_of_z(self, z) -> np.ndarray:
        """
        Gaussian tail top hat model for number density of LRG galaxies.

        :param self: Instance of LRG class
        :param z: Redshift array
        :return: Number density n(z) as a numpy array
        """
        n_of_z = 0.5 * (erf((z - self.z_min) / np.sqrt(2) * self.sigma) - erf((z - self.z_max) / np.sqrt(2) * self.sigma))
        return n_of_z
    
# ------------------------------------------------------------------------------ ELG Tracer ------------------------------------------------------------------------------

class ELG(Tracer): # Emission Line Galaxy
    def __init__(self):
        """
        Initializes the ELG tracer with specific parameters.
        
        :param self: Instance of ELG class
        """
        self.alpha = 2.0
        self.beta = 1.5
        self.z0 = 0.8
        self.max_prob_estimate = 1.0

    def n_of_z(self, z) -> np.ndarray:
        """
        Modified Schechter function model for number density of ELG galaxies.
        
        :param self: Instance of ELG class
        :param z: Redshift array
        :return: Number density n(z) as a numpy array
        """
        n_of_z = z ** self.alpha * np.exp(-(z / self.z0) ** self.beta)
        return n_of_z
    
# ------------------------------------------------------------------------------ QSO Tracer ------------------------------------------------------------------------------
    
class QSO(Tracer): # Quasi-Stellar Object (Quasar)
    def __init__(self):
        """
        Initializes the QSO tracer with specific parameters.

        :param self: Instance of QSO class
        """
        self.z_star = 2.0

    def n_of_z(self, z) -> np.ndarray:
        """
        Power law and exponential model for number density of quasars.
        
        :param self: Instance of QSO class
        :param z: Redshift array
        :return: Number density n(z) as a numpy array
        """
        n_of_z = z ** 2 * np.exp(-z / self.z_star)
        return n_of_z
    
# ------------------------------------------------------------------------------ BGS Tracer ------------------------------------------------------------------------------

class BGS(Tracer): # Bright Galaxy Survey (Main Sequence Galaxy)
    def __init__(self):
        """
        Initializes the BGS tracer with specific parameters.
        
        :param self: Instance of BGS class
        """
        self.alpha = 2.0
        self.beta = 1.5
        self.z0 = 0.2
        self.max_prob_estimate = 1.0

    def n_of_z(self, z) -> np.ndarray:
        """
        Modified Schechter function model for number density of BGS galaxies.
        
        :param self: Instance of BGS class
        :param z: Redshift array
        :return: Number density n(z) as a numpy array
        """
        n_of_z = z ** self.alpha * np.exp(-(z / self.z0) ** self.beta)
        return n_of_z