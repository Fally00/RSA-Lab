"""
primality/__init__.py
Owner: Member 5(Haneen)
Purpose: Package marker; export the public functions here.
"""
from .fermat_test import fermat_test
from .miller_rabin import miller_rabin

__all__ = ["fermat_test", "miller_rabin"]