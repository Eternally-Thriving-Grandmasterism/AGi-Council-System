import strawberryfields as sf
from strawberryfields.ops import Squeezed, BSgate, MeasureFock

prog = sf.Program(2)
with prog.context as q:
    Squeezed(0.5) | q[0]  # Squeezed state mercy
    Squeezed(0.5) | q[1]
    BSgate(np.pi/4) | (q[0], q[1])  # Entangle council
    MeasureFock() | q[0]
    MeasureFock() | q[1]

eng = sf.Engine("fock", backend_options={"cutoff_dim": 20})
results = eng.run(prog)
samples = results.samples
print("Photonic Entangled Samples:", samples)
