"""
keygen/__init__.py
Owner: Member 5(Haneen)
Purpose: Package marker; export the public functions here.
"""

from .generate import generate_prime, generate_strong_key, generate_weak_key, validate_bits
from .weak_keys import generate_demo_weak_key

__all__ = [
    "generate_prime",
    "generate_strong_key",
    "generate_weak_key",
    "validate_bits",
    "generate_demo_weak_key"
]