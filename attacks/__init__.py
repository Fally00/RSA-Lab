"""Registry of attacks run by :mod:`audit.runner`."""

from . import bad_modulus, fermat, phi_leak, pollard_rho, shared_prime, trial_division, wiener


ATTACKS = (
    {"name": "trial_division", "week": 3, "module": trial_division, "batch": False},
    {"name": "fermat", "week": 12, "module": fermat, "batch": False},
    {"name": "pollard_rho", "week": 12, "module": pollard_rho, "batch": False},
    {"name": "wiener", "week": 5, "module": wiener, "batch": False},
    {"name": "phi_leak", "week": 6, "module": phi_leak, "batch": False},
    {"name": "bad_modulus", "week": 11, "module": bad_modulus, "batch": False},
    {"name": "shared_prime", "week": 2, "module": shared_prime, "batch": True},
)

__all__ = ["ATTACKS"]
