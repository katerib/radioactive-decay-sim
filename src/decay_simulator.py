import numpy as np 
import matplotlib.pyplot as plt
import random

from dataclasses import dataclass

@dataclass 
class DecaySimulation:
    init_amt: float 
    half_life: float
    time_pts: np.ndarray
    isotope_name: str 
    half_life_unit: str 
    noise_percentage: bool

    def __post_init__(self):
        self.decay_const = np.log(2) / self.half_life
    
    def calculate_decay(self):
        """
        Calculate the amount of radioactive material remaining and amount decayed at each of the time points in self.time_pts.

        Returns: 
            (np.ndarray) amount of decayed radioactive material at each time point `amt_decayed`
            (np.ndarray) amount of remaining radioactive material at each time point `amt_remaining`
        """
        exp_dt = self.decay_const * self.time_pts
        amt_remaining = self.init_amt * np.exp(-exp_dt)
        noise = random.uniform(-self.noise_percentage * amt_remaining, self.noise_percentage * amt_remaining)
        amt_remaining = amt_remaining + noise
        amt_decayed = self.init_amt - amt_remaining
    
        return amt_decayed, amt_remaining
    
    def calc_decay_rate(self):
        """
        Calculate decay rates for all time points.
        
        Returns:
            (np.ndarray) current decay rate at each time point
        """
        _, remaining = self.calculate_decay()
        return self.decay_const * remaining
    
    def conv_time(self, value:float, from_unit:str, to_unit:str):
        """
        Convert time between units (s, d, y)

        Returns:
            (float) time value
        """
        to_seconds = {
            's': 1,
            'd': 86400,
            'y': 31556926
        }

        seconds = value * to_seconds[from_unit]
        return seconds / to_seconds[to_unit]

    def plot_decay(self):
        """
        Plot the radioactive decay process showing both the amount of material remaining and the amount that has decayed over time.

        Plot should include:
            - two line plots (remaining and decayed material)
            - decay rate plot as secondary y-axis
            - labels, legend
            - half-life marker
            - grid lines (?)
        """
        # calculate decay values
        amt_decayed, amt_remaining = self.calculate_decay()

        # calculate decay rate for secondary y-axis
        decay_rate = self.calc_decay_rate()

        # create figure and primary axis
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # plot remaining and decayed values on primary y-axis
        ax1.plot(self.time_pts, amt_remaining, 'g-', label='Remaining Material')
        ax1.plot(self.time_pts, amt_decayed, 'r-', label='Decayed Material')
        ax1.set_xlabel(f'Time ({self.half_life_unit })')
        ax1.set_ylabel('Amount of Material')

        # add vertical line at half-life point
        half_life_time = self.half_life
        ax1.axvline(x=half_life_time, color='k', linestyle='--', label='Half-Life')
        ax1.legend(loc='lower right')

        # add: title and labels with units ; grid ; legend
        plt.title(f'Radioactive Decay Simulation for {self.isotope_name}')
        ax1.grid(True)
        fig.tight_layout()
        plt.show()

        # use different lines/colors, include labels 

        # create secondary y-axis for decay rate (diff color)

        pass