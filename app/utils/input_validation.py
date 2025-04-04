"""Validates user input values for decay simulation parameters."""

def is_input_valid(initial_amount, time_points, noise):
    return (
        initial_amount >= 1
        and 10 <= time_points <= 1000
        and 0 <= noise <= 20
    )
