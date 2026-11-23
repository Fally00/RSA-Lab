"""
audit/parser.py
Owner: Rayan
Purpose: Turn PEM public keys and raw 'n, e' text into (n, e) pairs.
"""

import json 

def parse_key(data):
    if isinstance(data , str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    if not isinstance(data, dict):
        raise ValueError("Public key must be a dictionary")

    if "n" not in data or "e" not in data:
        raise ValueError("Public key must contain 'n' and 'e' fields")

    
    n = data["n"]
    e = data["e"]

    if type(n) is not int or type(e) is not int:
        raise ValueError("n and e must be integers")

    if n <= 1 or e <= 1:
        raise ValueError("Modulus n and public exponent e must be greater than 1")

    return n, e