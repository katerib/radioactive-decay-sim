import pytest 
import numpy as np

from src.decay_simulator import DecaySimulation
from src.isotopes import *

def test_carbon_14_one_half_life():
    """
    Test C-14 decay after one half-life.
    """
    initial_amount = 1000
    time_points = np.array([0, CARBON_14.half_life])

    sim = DecaySimulation(
        init_amt=initial_amount,
        half_life=CARBON_14.half_life,
        time_pts=time_points
    )

    decayed, remaining = sim.calculate_decay()

    # there should be about half remaining 
    assert np.isclose(remaining[1], initial_amount/2, rtol=0.01)
    assert np.isclose(decayed[1], initial_amount/2, rtol=0.01)

    # and total should == initial
    assert np.isclose(remaining[1] + decayed[1], initial_amount, rtol=0.01)


def test_iodine_131_two_half_lives():
    """
    Test I-131 decay after two half-lives.
    """
    initial_amount = 1000
    time_points = np.array([0, IODINE_131.half_life, 2 * IODINE_131.half_life])

    sim = DecaySimulation(
        init_amt=initial_amount, 
        half_life=IODINE_131.half_life,
        time_pts=time_points
    )

    _, remaining = sim.calculate_decay()

    # one half-life
    assert np.isclose(remaining[1], initial_amount/2, rtol=0.01)

    # two half-lives
    assert np.isclose(remaining[2], initial_amount/4, rtol=0.01)


def test_time_conversion():
    sim = DecaySimulation(
        init_amt=1000,
        half_life=1,
        time_pts=np.array([0,1])
    )

    # year -> day
    assert np.isclose(sim.conv_time(1, 'y', 'd'), 365.242, rtol=0.01)

    # day -> sec
    assert np.isclose(sim.conv_time(1, 'd', 's'), 86400, rtol=0.01)


def test_decay_rate():
    initial_amount = 1000
    half_life = 100
    time_points = np.array([0])

    sim = DecaySimulation(
        init_amt=initial_amount,
        half_life=half_life,
        time_pts=time_points
    )

    decay_rate = sim.calc_decay_rate()
    expected_rate = (np.log(2) / half_life) * initial_amount

    assert np.isclose(decay_rate[0], expected_rate, rtol=0.01)


def test_edge_cases():
    # zero initial amount
    sim = DecaySimulation(
        init_amt=0,
        half_life=100,
        time_pts=np.array([0, 50])
    )

    decayed, remaining = sim.calculate_decay()

    assert np.all(remaining == 0)
    assert np.all(decayed == 0)

    # zero time 
    sim = DecaySimulation(
        init_amt=1000,
        half_life=100,
        time_pts=np.array([0])
    )

    decayed, remaining = sim.calculate_decay()

    assert remaining[0] == 1000
    assert decayed[0] == 0
    

if __name__ == "__main__":
    pytest.main([__file__, '-v'])