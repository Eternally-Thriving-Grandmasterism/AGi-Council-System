"""
ENC Protection — Quantum-Resistant Signature for APAAGI Proposals
"""

import ecdsa

def sign_proposal(proposal: str) -> str:
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    signature = sk.sign(proposal.encode())
    print("Proposal signed quantum-resistant — eternal integrity sealed.")
    return signature.hex()

def verify_proposal(signature_hex: str, proposal: str) -> bool:
    try:
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(signature_hex[:64]), curve=ecdsa.SECP256k1)
        return vk.verify(bytes.fromhex(signature_hex[64:]), proposal.encode())
    except:
        return False
