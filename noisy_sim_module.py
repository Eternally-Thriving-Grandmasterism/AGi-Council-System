# noisy_sim_module.py (v1.0 – Cross-Provider Noisy Simulator Modes)
# Depolarizing/bit-flip noise for cosmic radiation mercy testing

# Example with Qiskit (extend to others)
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

def add_radiation_noise(circuit, error_rate=0.05):
    noise_model = NoiseModel()
    error = depolarizing_error(error_rate, 1)
    noise_model.add_all_qubit_quantum_error(error, ['h', 'cx'])
    # Run with noise_model for habitat radiation resilience testing
    log.info(f"Noisy mode active – {error_rate*100}% decoherence mercy test!")
