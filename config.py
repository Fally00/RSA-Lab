"""
config.py
Owner: Rayan
Purpose: Settings: default key size, attack time limits.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Server settings

HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

#Data Source settings

USE_MOCK = False
MOCK_PATH = os.path.join(BASE_DIR, "docs" , "mock_results.json")

#Input settings

MAX_INPUT_CHARS = 200_00
MAX_KEYS = 50
MAX_MODULUS = 8192

#Key generation settings

DEFAULT_KEY_BITS = 1024
MIN_KEY_BITS = 12
MAX_KEY_BITS = 2048
PUBLIC_EXPONENT = 65537

# Attack settings

ATTACK_TIMEOUT_S = 5.0

TRAIL_DIVISION_LIMIT = 1_000_000
FERMAT_LIMIT = 100_000
POLLARD_RHO_MAX_ITER = 1_000_000
PHI_LEAK_SCAM = 10_000
