import numpy as np 
import matplotlib.pyplot as plt

from dataclasses import dataclass
from .static.css.plot_colors import *

@dataclass 
class DecaySimulation:
    init_amt: float 
    half_life: float
    time_pts: np.ndarray
    isotope_name: str 
    half_life_unit: str 
    noise_percentage: int 
    gamma_emission_probability: float

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
        noise = np.random.normal(0, (self.noise_percentage / 100) * amt_remaining, size=self.time_pts.size)
        amt_remaining = amt_remaining + noise
        amt_decayed = self.init_amt - amt_remaining
    
        return amt_decayed, amt_remaining
    
    def calc_activity(self):
        """
        Calculate decay rates for all time points.
        
        Returns:
            (np.ndarray) current decay rate at each time point
        """
        _, remaining = self.calculate_decay()
        return self.decay_const * remaining
    
    def calc_gamma_emissions(self):
        amt_decayed, _ = self.calculate_decay()
        amt_decayed_int = np.maximum(amt_decayed, 0).astype(int)            # ensure positive value
        gamma_probability = self.gamma_emission_probability

        gamma_emissions = np.random.binomial(n=amt_decayed_int, p=gamma_probability)

        return gamma_emissions

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
        """
        plt.style.use('dark_background')
        
        amt_decayed, amt_remaining = self.calculate_decay()
        gamma_decay = self.calc_gamma_emissions()
        activity = self.calc_activity()

        fig, ax1 = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(table_grey)
        ax1.set_facecolor(table_grey)
        
        ax1.plot(self.time_pts, amt_remaining, color=cyan, marker='.', linestyle='-', label='Remaining Material')
        ax1.plot(self.time_pts, amt_decayed, color=coral, marker='.', linestyle='--', label='Decayed Material')
        ax1.plot(self.time_pts, gamma_decay, color=yellow, marker='.', linestyle=':', label='Gamma Decay')

        ax1.set_xlabel(f'Time ({self.half_life_unit})', color=white)
        ax1.set_ylabel('Amount of Material', color=white)
        ax1.tick_params(colors=white)
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('Activity (Bq)', color=grey_400)
        ax2.tick_params(colors=grey_400)
        
        half_life_time = self.half_life
        ax1.axvline(x=half_life_time, color=white, 
                    linestyle='--', label='First Half-Life')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, 
                    loc='best', facecolor=table_grey, labelcolor=white)

        ax1.grid(True, color=grey_400, alpha=0.2)
        
        plt.title(f'Radioactive Decay Simulation for {self.isotope_name}', 
                    color=white)
        
        for spine in ax1.spines.values():
            spine.set_color(white)
        for spine in ax2.spines.values():
            spine.set_color(grey_400)
                
        plt.tight_layout()

        return amt_decayed, activity, amt_remaining, gamma_decay  