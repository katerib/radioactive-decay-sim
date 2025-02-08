# Radioactive Decay Simulator

## Table of Contents
- [Introduction](#introduction)
- [Overview](#overview)
- [Key Features](#key-features)
- [Todo](#todo)
- [Installation](#installation)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
  - [Running Tests](#running-tests)
- [Development Notes](#development-notes)
- [Technologies](#technologies)
- [Formulas](#formulas)
  - [Decay Constant](#decay-constant)
  - [Rate of Decay](#rate-of-decay)
  - [Decay Chains](#decay-chains)
- [Unit Conversions](#unit-conversions)
- [Resources](#resources)

## Introduction

### Modeling Half-Life and Nuclear Decay

A web-based tool for simulating radioactive decay through half-life calculations and statistical modeling.

## Overview

Radioactive decay is a fundamental process in nuclear physics where unstable atomic nuclei transform into more stable forms. While the exact moment of decay for any single atom is unpredictable, large populations of atoms follow mathematical patterns that can be modeled using statistical methods. This simulator models those patterns, allowing users to visualize decay curves, calculate remaining material over time, and explore the half-life behavior of different isotopes.

![I-131 Simulation](https://i.ibb.co/ccg4pLkT/Figure-1.png)
*I-131 decay simulation done over 20 time-steps*

## Key Features

*Some ideas, to review--*

- **Half-Life Calculator:** predicts the remaining amount of radioactive substance at any given time
- **Interactive Decay Curves:** visualizes how radioactive materials change over time
- **User-Friendly Interface:** makes complex decay calculations simple to understand
- **Unit Conversion:** supports conversion between common time units

- ? **Decay Chain Modeling:** would be cool to add a visualization of the parent to daughter isotope transformation. Need to figure out how we would even do that though. Can be a later goal.

## Todo

- [X] Calculate decayed and undecayed nuclei using half-life (s)
- [X] Plot the number of decayed and undecayed nuclei on a graph
- [ ] Potential feature: specific isotope selection and decay chain modeling
- [ ] Potential feature: simulate gamma radiation

## Installation

### Cloning the Repository

```sh
git clone https://github.com/katerib/radioactive-decay-sim.git
```

### Setting Up the Virtual Environment

Navigate to the project directory:

```sh
cd ./radioactive-decay-sim/
```

Create a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

*Note: You have to activate the venv for each instance of your shell*

- **Windows:**

```ps
venv/Scripts/activate
```

- **macOS:**

```sh
source venv/bin/activate
```

### Installing Dependencies

Install the required packages:

```sh
pip install -r requirements.txt
```

Install the package in development mode:

```sh
pip install -e .
```

*If you want to install with development dependencies, run:*

```sh
pip install -e ".[dev]"
```

### Running Tests

```sh
pytest tests/
```

## Development Notes

- The package is installed in editable mode (`-e` flag), so code changes will be reflected immediately without reinstallation.
- When adding new dependencies, add them to both `requirements.txt` and `setup.py`.

## Technologies

TODO: dependencies/libraries used

- Python

## Formulas

### Decay Constant

The rate that characterizes radioactive decay. Represents how quickly a specific radioactive material decays over time. Each isotope has its own unique decay constant calculated from its half-life.

$$
λ = \frac{\ln(2)}{t_{1/2}}
$$

- λ = decay constant of radioactive isotope
- ln(2) ≈ 0.693
- t₁/₂ = half-life

### Rate of Decay

The exponential decay equation that models how the amount of radioactive material changes over time. This describes the relationship between the initial amount, decay constant, and time elapsed.

$$
N(t) = N_0 * e^{-\lambda t}
$$

Where:
- N(t) = amount remaining at time t
- N₀ = initial amount
- λ = decay constant of radioactive isotope
- t = time elapsed

Derived quantities:

- λN(t) = current decay rate
- N(t) = amount remaining
- N₀ - N(t) = amount decayed

### Decay Chains

*We can remove/ignore this if we aren't going to show how a specific isotope decays into another. Just putting here to save it for now.*

Describes how one radioactive isotope transforms into another through sequential decay steps.

$$
N_2(t) = N_{10} \left[ \frac{λ_1}{λ_2 - λ_1} \right] \left[e^{-λ_1 t} - e^{-λ_2 t} \right]
$$

Where:

- N₂(t) = amount of daughter isotope at time t
- N₁₀ = initial amount of parent isotope
- λ₁ = decay constant of parent
- λ₂ = decay constant of daughter

## Unit Conversions

### Time Conversions

- 1 year = 31,556,926 seconds
- 1 day = 86,400 seconds

## Resources

- [Department of Chemistry, Federal University of Technology - Decay Equation Derivation](https://www.researchgate.net/profile/Chidi-Duru/publication/321018215_DERIVATION_OF_A_SIMPLIFIED_RADIOACTIVE_DECAY_EQUATION/links/5a083cf3aca272ed279f18da/DERIVATION-OF-A-SIMPLIFIED-RADIOACTIVE-DECAY-EQUATION.pdf)
- [HyperPhysics - Radioactive Decay Fundamentals](http://hyperphysics.phy-astr.gsu.edu/hbase/Nuclear/radact.html)
- Khan Academy - Nuclear Physics Educational Content:
  - [Radioactive Decay Types](https://www.khanacademy.org/science/in-in-class-12th-physics-india/nuclei/in-in-nuclear-physics/a/radioactive-decay-types-article)
  - [Nuclear Physics: Half-Life](https://www.khanacademy.org/science/highschool-physics/x6679aa2c65c01e53:nuclear-physics/x6679aa2c65c01e53:half-life/v/half-life-radiometric-dating)
  - [Radioactive Decay](https://www.khanacademy.org/science/highschool-physics/x6679aa2c65c01e53:nuclear-physics/x6679aa2c65c01e53:radioactive-decay/v/intro-to-radioactive-decay)

