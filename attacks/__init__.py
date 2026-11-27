"""
attacks/__init__.py
Owner: Rayan
Purpose: Registry: the list of attacks the runner calls.
"""
from attacks import bad_modulus, fermat, phi_leak, pollard_rho, shared_prime, trial_division, wiener

SINGLE_ATTACKS = [
    ("trial_division", 3, trial_division.run),
    ("fermat", 12, fermat.run),
    ("pollard_rho", 12, pollard_rho.run),
    ("wiener", 5, wiener.run),
    ("phi_leak", 7, phi_leak.run),
    ("bad_modulus", 11, bad_modulus.run),
]

BATCH_ATTACKS = [
    ("shared_prime", 2, shared_prime.run_batch),
]

ATTACK_REGISTRY = [
    {"attack": name, "week": week, "batch": False}
    for name, week, _ in SINGLE_ATTACKS
] + [
    {"attack": name, "week": week, "batch": True}
    for name, week, _ in BATCH_ATTACKS
]

__all__ = ["ATTACK_REGISTRY", "SINGLE_ATTACKS", "BATCH_ATTACKS"]
