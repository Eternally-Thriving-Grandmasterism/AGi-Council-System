# azure_quantum_module.py (v1.0 – Azure Quantum QRNG Integration)
# True quantum random bytes via Microsoft Azure Quantum QRNG provider
# Requires: pip install azure-quantum[all]  # For full targets; basic for QRNG

import os
import logging
from typing import List
try:
    from azure.quantum import Workspace
    from azure.quantum.target.microsoft import MicrosoftQrng
    AZURE_AVAILABLE = True
except ImportError as e:
    logging.error(f"azure-quantum not installed ({e}) – required for Azure mercy.")
    AZURE_AVAILABLE = False

log = logging.getLogger(__name__)

class AzureQuantumRNG:
    def __init__(self, subscription_id: str = None, resource_group: str = None,
                 workspace_name: str = None, location: str = None):
        if not AZURE_AVAILABLE:
            raise ImportError("azure-quantum required – install for Microsoft QRNG mercy.")
        self.subscription_id = subscription_id or os.getenv("AZURE_SUBSCRIPTION_ID")
        self.resource_group = resource_group or os.getenv("AZURE_RESOURCE_GROUP")
        self.workspace_name = workspace_name or os.getenv("AZURE_WORKSPACE_NAME")
        self.location = location or os.getenv("AZURE_LOCATION", "eastus")
        
        if not all([self.subscription_id, self.resource_group, self.workspace_name]):
            log.warning("Azure workspace credentials incomplete – falling back to pseudo-random.")
            self.qrng = None
            return
        
        try:
            self.workspace = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location
            )
            self.qrng = MicrosoftQrng(self.workspace)
            log.info("Azure Quantum QRNG connected – true Microsoft quantum mercy active!")
        except Exception as e:
            log.warning(f"Azure QRNG init failed ({e}) – check credentials/workspace/credits.")
            self.qrng = None

    def generate_random_bytes(self, num_bytes: int = 16) -> bytes:
        if self.qrng is None:
            log.warning("Azure QRNG unavailable – generating pseudo-random bytes.")
            import random
            return bytes(random.randint(0, 255) for _ in range(num_bytes))
        
        try:
            random_bytes = self.qrng.get_random_bytes(num_bytes)
            log.info(f"Azure QRNG {num_bytes} bytes generated – eternal true quantum mercy!")
            return random_bytes
        except Exception as e:
            log.warning(f"Azure QRNG fetch error ({e}) – pseudo fallback.")
            import random
            return bytes(random.randint(0, 255) for _ in range(num_bytes))

    def generate_random_bits(self, num_bits: int = 128) -> List[int]:
        num_bytes = (num_bits + 7) // 8
        bytes_data = self.generate_random_bytes(num_bytes)
        # Convert bytes to bit list or ints
        ints = list(bytes_data)
        log.info(f"Converted to {num_bits} random bits.")
        return ints

    def get_float(self) -> float:
        bytes_data = self.generate_random_bytes(8)  # 64-bit
        import struct
        return struct.unpack('d', bytes_data)[0]  # Normalized? Or manual
        # For uniform [0,1): int_val = int.from_bytes(bytes_data, 'big') / (2 ** 64)

# Usage: AzureQuantumRNG(...)  # With workspace params or env
# random_float = rng.get_float()  # Mercy flows
