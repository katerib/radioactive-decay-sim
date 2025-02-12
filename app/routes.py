from flask import Blueprint, render_template, request, jsonify
import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .decay_simulator import DecaySimulation
from .isotopes import CARBON_14, IODINE_131, URANIUM_238, BISMUTH_193M

main_bp = Blueprint('main', __name__)

ISOTOPES = {
    'carbon-14': CARBON_14,
    'iodine-131': IODINE_131,
    'uranium-238': URANIUM_238,
    'bismuth-193m': BISMUTH_193M
}


@main_bp.route('/')
def index():
    return render_template('index.html', isotopes=ISOTOPES)


@main_bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    isotope = ISOTOPES[data['isotope']]
    initial_amount = float(data['initial_amount'])
    time_points = int(data['time_points'])
    noise = int(data['noise'])
    
    max_time = isotope.half_life * 4
    time_pts = np.linspace(0, max_time, time_points)
    
    sim = DecaySimulation(
        init_amt=initial_amount,
        half_life=isotope.half_life,
        time_pts=time_pts,
        isotope_name=isotope.name,
        half_life_unit=isotope.half_life_unit,
        noise_percentage=noise,
        gamma_emission_probability=isotope.gamma_emission_probability / 100             # convert percent to decimal
    )
    
    sim.plot_decay()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    amt_decayed, amt_remaining = sim.calculate_decay()
    decay_rate = sim.calc_activity()
    gamma_emissions = sim.calc_gamma_emissions()
    
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
        'data': data_points
    })