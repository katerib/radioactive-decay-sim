from flask import Blueprint, render_template, request, jsonify
import numpy as np
import io
import base64
import matplotlib
import re 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .api_client import SearchIsotope

from .decay_simulator import DecaySimulation
from .isotopes import CARBON_14, RADIUM_226, COBALT_60, IODINE_131, URANIUM_238, CESIUM_137, Isotope

main_bp = Blueprint('main', __name__)

ISOTOPES = {
    'carbon-14': CARBON_14,
    'radium-226': RADIUM_226,
    'cobalt-60': COBALT_60,
    'iodine-131': IODINE_131,
    'uranium-238': URANIUM_238,
    'cesium-137': CESIUM_137,
    'custom': None
}

@main_bp.route('/')
def index():
    return render_template('index.html', isotopes=ISOTOPES)

@main_bp.route('/simulate', methods=['POST'])
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

@main_bp.route('/search', methods=['POST'])
def search():
    data = request.json
    parsed_data = {}

    if data:
        isotope_data = SearchIsotope(data)

        for i, entry in enumerate(isotope_data):
            dataset_id = entry['dataset']
    
            hl_unit_array = re.split(r'\+|\-|\s+', entry['isotope_data'][i]['half-life'])

            if hl_unit_array[1][0].isnumeric():
                hl_unit_array[0] += f'^{hl_unit_array[1][0]}'
                hl_unit_array[0] = hl_unit_array[0].replace('×10^', 'e')
                hl_unit_array[0] = int(hl_unit_array[0])
                hl_unit_array[1] = hl_unit_array[1].replace(hl_unit_array[1][0], '')

            hl = hl_unit_array[0]
            unit = ''.join(filter(lambda x: x.isalpha(), hl_unit_array[1]))

            parsed_data[dataset_id] = {
                'gamma_emissions': [
                    {
                        'type': emission['type'],
                        'energy': emission['energy'],
                        'intensity': emission['intensity'],
                        'dose': emission['dose'],
                    }
                    for emission in entry['gamma_emissions']
                ],
                'isotope_data': [
                    {
                        'half_life': hl,
                        'unit': unit,
                        'decay_mode': entry['isotope_data'][i]['Decay Mode'],
                    }
                ]
            }

    return jsonify({'datasets': parsed_data})
    

@main_bp.route('/about')
def about():
    return render_template('about.html')