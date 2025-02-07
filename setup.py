from setuptools import setup, find_packages

setup(
    name="decay_simulator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=2.2.2',
        'pandas>=2.2.3',
        'matplotlib>=3.10.0',
    ],
    extras_require={
        'dev': [
            'pytest>=8.3.4',
        ],
    }
)