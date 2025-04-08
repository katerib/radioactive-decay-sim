"""Unit tests for the decay simulation logic and utility methods."""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.decay_simulator import DecaySimulation
from app.utils.isotope_loader import load_unstable_isotopes

ISOTOPES = load_unstable_isotopes()


def test_carbon_14_one_half_life():
    carbon_14 = ISOTOPES["c-14"]
    initial = 1000
    time = np.array([0, carbon_14.half_life])

    sim = DecaySimulation(
        init_amt=initial,
        half_life=carbon_14.half_life,
        time_pts=time,
        isotope_name=carbon_14.name,
        half_life_unit=carbon_14.half_life_unit,
        noise_percentage=0.0,
        gamma_emission_probability=0,
        graph=""
    )

    decayed, remaining = sim.calculate_decay()
    assert np.isclose(remaining[1], initial / 2, rtol=0.01)
    assert np.isclose(decayed[1], initial / 2, rtol=0.01)
    assert np.isclose(remaining[1] + decayed[1], initial, rtol=0.01)


def test_iodine_131_two_half_lives():
    iodine = ISOTOPES["i-131"]
    initial = 1000
    time = np.array([0, iodine.half_life, 2 * iodine.half_life])

    sim = DecaySimulation(
        init_amt=initial,
        half_life=iodine.half_life,
        time_pts=time,
        isotope_name=iodine.name,
        half_life_unit=iodine.half_life_unit,
        noise_percentage=0.0,
        gamma_emission_probability=0,
        graph=""
    )

    _, remaining = sim.calculate_decay()
    assert np.isclose(remaining[1], initial / 2, rtol=0.01)
    assert np.isclose(remaining[2], initial / 4, rtol=0.01)


def test_carbon_14_with_noise():
    carbon_14 = ISOTOPES["c-14"]
    initial = 1000
    time = np.array([0, carbon_14.half_life])

    sim = DecaySimulation(
        init_amt=initial,
        half_life=carbon_14.half_life,
        time_pts=time,
        isotope_name=carbon_14.name,
        half_life_unit=carbon_14.half_life_unit,
        noise_percentage=0.01,
        gamma_emission_probability=0,
        graph=""
    )

    _, remaining = sim.calculate_decay()
    assert np.isclose(remaining[1], initial / 2, rtol=0.05)


def test_time_conversion():
    sim = DecaySimulation(
        init_amt=1000,
        half_life=1,
        time_pts=np.array([0, 1]),
        isotope_name="test",
        half_life_unit="y",
        noise_percentage=0.0,
        gamma_emission_probability=0,
        graph=""
    )

    assert np.isclose(sim.conv_time(1, 'y', 'd'), 365.242, rtol=0.01)
    assert np.isclose(sim.conv_time(1, 'd', 's'), 86400, rtol=0.01)


def test_activity():
    sim = DecaySimulation(
        init_amt=1000,
        half_life=100,
        time_pts=np.array([0]),
        isotope_name="test",
        half_life_unit="s",
        noise_percentage=0.0,
        gamma_emission_probability=0,
        graph=""
    )

    activity = sim.calc_activity()
    expected = (np.log(2) / 100) * 1000
    assert np.isclose(activity[0], expected, rtol=0.01)
    assert activity.shape == (1,)


def test_edge_cases():
    sim = DecaySimulation(
        init_amt=0,
        half_life=100,
        time_pts=np.array([0, 50]),
        isotope_name="test",
        half_life_unit="s",
        noise_percentage=0.0,
        gamma_emission_probability=0,
        graph=""
    )
    d, r = sim.calculate_decay()
    assert np.all(r == 0)
    assert np.all(d == 0)

    sim = DecaySimulation(
        init_amt=1000,
        half_life=100,
        time_pts=np.array([0]),
        isotope_name="test",
        half_life_unit="s",
        noise_percentage=0.0,
        gamma_emission_probability=0,
        graph=""
    )
    d, r = sim.calculate_decay()
    assert r[0] == 1000
    assert d[0] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
