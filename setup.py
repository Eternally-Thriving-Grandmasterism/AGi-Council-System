from setuptools import setup, find_packages

setup(
    name="agi-council-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "torch>=2.0.0",
        "chess>=1.10.0",
        "qutip>=4.7.0",
        "astropy>=5.0",
        "ecdsa"
    ],
)
