"""Handles simulation requests and returns decay data and plots as JSON."""

from flask import Blueprint, request, jsonify
import numpy as np, io, base64
import matplotlib.pyplot as plt

from app.utils.isotope_loader import load_unstable_isotopes
from app.utils.decay_simulator import DecaySimulation
from app.static.models.isotopes import Isotope
from app.utils.input_validation import is_input_valid

api_bp = Blueprint('api', __name__)
ISOTOPES = load_unstable_isotopes()

@api_bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    
    if data['isotope'] == 'custom':
        custom_isotope = Isotope(
            name=data['custom_name'],
            half_life=float(data['custom_half_life']),
            gamma_emission_probability=float(data['custom_gamma']),
            half_life_unit=data['custom_half_life_unit']
        )
        isotope = custom_isotope
    else:
        isotope = ISOTOPES[data['isotope']]
        
    initial_amount = float(data['initial_amount'])
    time_points = int(data['time_points'])
    noise = int(data['noise'])
    graph = data['checkedBoxes']

    max_time = isotope.half_life * 4
    time_pts = np.linspace(0, max_time, time_points)

    if not is_input_valid(initial_amount, time_points, noise):
        return None
    
    sim = DecaySimulation(
        init_amt=initial_amount,
        half_life=isotope.half_life,
        time_pts=time_pts,
        isotope_name=isotope.name,
        half_life_unit=isotope.half_life_unit,
        noise_percentage=noise,
        gamma_emission_probability=isotope.gamma_emission_probability / 100,
        graph=graph
    )
    
    amt_decayed, decay_rate, amt_remaining, gamma_emissions = sim.plot_decay()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    data_points = []
    for i in range(len(time_pts)):
        data_points.append({
            'time': f"{time_pts[i]:.2f}",
            'remaining': f"{amt_remaining[i]:.2f}",
            'decayed': f"{amt_decayed[i]:.2f}",
            'rate': f"{decay_rate[i]:.2f}",
            'gamma': f"{gamma_emissions[i]}"
        })
    
    return jsonify({
        'plot': plot_url,
        'data': data_points,
        # 'datasets': parsed_data
    })
