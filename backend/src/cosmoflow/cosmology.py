import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d

class Cosmology:
    def __init__(self):
        """
        Initializes the Cosmology class with Planck 2018 cosmological parameters.
        """
        self.h = 0.6737  # Dimensionless Hubble parameter
        self.H0 = 100 * self.h  # Hubble constant in km/s/Mpc
        self.Omega_m = 0.3147  # Matter density parameter
        self.Omega_lambda = 0.6853  # Dark energy density parameter
        self.c = 299792.458  # Speed of light in km/s
        self._build_lookups()

    def E(self, z: float) -> float:
        """
        Computes the dimensionless Hubble parameter E(z).

        :param z: Redshift
        :return: E(z)
        """
        return np.sqrt(self.Omega_m * (1 + z) ** 3 + self.Omega_lambda)
    
    def _builds_lookups(self):
        """
        Precomputes look-up tables for comoving distance and distance modulus.
        """
        z_vals = np.linspace(0, 5, 1000)
        d_c_vals = np.zeros_like(z_vals)
        for i, z in enumerate(z_vals):
            integral, _ = quad(lambda z_prime: self.c / self.H0 / self.E(z_prime), 0, z)
            d_c_vals[i] = integral
        self.comoving_distance_lookup = interp1d(z_vals, d_c_vals, kind='cubic', fill_value="extrapolate")
    
    def comoving_distance(self, z: float) -> float:
        """
        Computes the comoving distance to redshift z.

        :param z: Redshift
        :return: Comoving distance in Mpc
        """
        return self.comoving_distance_lookup(z)
        
    def luminosity_distance(self, z: float) -> float:
        """
        Computes the luminosity distance to redshift z.

        :param z: Redshift
        :return: Luminosity distance in Mpc
        """
        return (1 + z) * self.comoving_distance(z)  
     
    def distance_modulus(self, z: float) -> float:
        """
        Computes the distance modulus to redshift z.

        :param z: Redshift
        :return: Distance modulus
        """
        d_L = self.luminosity_distance(z)
        return 5 * np.log10(d_L * 1e6) - 5  # Convert Mpc to pc for distance modulus