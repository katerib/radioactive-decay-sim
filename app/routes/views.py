"""Page-rendering routes for the main UI and static views."""

from flask import Blueprint, render_template
from ..utils.isotope_loader import load_unstable_isotopes

views_bp = Blueprint('views', __name__)

ISOTOPES = load_unstable_isotopes()

@views_bp.route('/')
def index():
    return render_template('index.html', isotopes=ISOTOPES)

@views_bp.route('/about')
def about():
    return render_template('about.html')
