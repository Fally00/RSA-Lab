"""
audit/contract.py
Owner: Rayan
Purpose: Build and validate the shared result dict that every attack returns.
"""
import math
import time 

REQUIRED = ("attack" , "week" , "broken" , "factors" , "private_key" , "steps" , "time_ms" )

#MBuild a contract dict. Failed attacks: leave broken=False, factors/private_key None
def make_result( attack , week , broken = False , factors = None 
                , private_key = None , steps = None , time_ms = None ):
    return{
        "attack": attack,
        "week": week,
        "broken": broken,
        "factors": factors,
        "private_key": private_key,
        "steps": steps if steps is not None else[],
        "time_ms": round(time_ms,3) if time_ms is not None else None
    }

#A steps entry that Explain mode renders as a table. Cells are stringified
def table(headers, rows):
    return {
        "table": {
            "headers": [str(h) for h in headers],
            "rows": [
                [str(cell) for cell in row]
                for row in rows
            ]
        }
    }

#Estimate the elapsed time in milliseconds since the start time.
def elapsed_time(start):
    return(time.perf_counter() - start) * 1000

#derive the private key from the public exponent and the factors of n.
def derive_private_key(e , p , q ):
    try:
        return pow(e , -1 , math.lcm(p - 1 , q - 1))
    except ValueError:
        return None

#Validate that the result dict has all required fields and that they are of the correct type.
def validate(r):
    missing = [k for k in REQUIRED if k not in r]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    if type(r["week"]) is not int or not 1 <= r["week"] <= 14:
        raise ValueError(f"Week must be an integer, got {type(r['week'])}")

    if not isinstance(r["steps"], list):
        raise ValueError("steps must be a list")

    if not isinstance(r["attack"], str) or not r["attack"].strip():
        raise ValueError("Invalid attack name")

    if type(r["broken"]) is not bool:
        raise ValueError("broken must be boolean")

    # Validate execution time
    if r["time_ms"] is not None and (
    isinstance(r["time_ms"], bool)
    or not isinstance(r["time_ms"], (int, float))
    or not math.isfinite(r["time_ms"])
    or r["time_ms"] < 0
    ):
        raise ValueError("Invalid execution time")

    if r["broken"]:
        f = r["factors"]

        if not (
            isinstance(f, (list, tuple))
            and len(f) == 2
            and all(type(x) is int and x > 1 for x in f)
            and f[0] != f[1]
        ):
            raise ValueError("broken result needs two distinct integer factors > 1")

        d = r["private_key"]
        if d is not None and (type(d) is not int or d <= 0):
            raise ValueError("Successful attack private_key must be a positive exact integer")

    elif r["factors"] is not None or r["private_key"] is not None:
        raise ValueError("Failed attack must have factors=None and private_key=None")

    return r

#Recheck that the factors and private key are correct for the given n and e.
def verify_breaking(n , e , r):
    if not r["broken"]:
        return True
    p , q = r["factors"]
    if p < 2 or q < 2 or p * q != n:
        return False
    d = r["private_key"]
    if d is not None:
        return (d * e) % math.lcm(p-1 , q-1) ==1 
    return True

def verdict(results):
    if not isinstance(results, list) or not results:
        return "invalid"

    try:
        for result in results:
            validate(result)
    except (ValueError, TypeError, KeyError):
        return "invalid"

    if any(result["broken"] for result in results):
        return "broken"

    return "safe"

#Convert results to a JSON-serializable format to be ready for josnify()
def jsonify(r):

    out = dict(r)
    if r["factors"] is not None:
        out["factors"] = [str(x) for x in r["factors"]]
    if r["private_key"] is not None:
        out["private_key"] = str(r["private_key"])
    return out
