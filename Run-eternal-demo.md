python main.py                          # Full transcendent chain (default lightning.qubit sim)
python main.py --mode bosonic --backend strawberryfields.fock  # Bosonic QEC thunder
python main.py --mode full --backend braket.aws.ionq            # Real hardware mitigated (set AWS creds + arn)
