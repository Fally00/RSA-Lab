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
def table(headers , rows):
    return {
        "table" : {
            "headers": [str(h) for h in headers],
            "rows": [str(c) for c in rows]
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
    missing = [ k for k in REQUIRED if k not in r]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    if not isinstance(r["week"], int) or not 1 <= r["week"] <=14:
        raise ValueError(f"Week must be an integer, got {type(r['week'])}")
    if not isinstance(r["steps"], list ):
        raise ValueError(f"steps must be a list")
    if r["broken"]:
        f = r["factors"]
        if not (isinstance(f, (list, tuple)) and len(f) == 2
                and all(isinstance(x, int) and x >= 2 for x in f)):
            raise ValueError("broken result needs factors = [p, q] with both ints >= 2")
    elif r["factors"] is not None or r["private_key"] is not None:
        raise ValueError("Failed attack must have Factors = None and Private key = None")
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
    """
    Given a list of result dicts, return a summary verdict.
    If any attack is broken, the verdict is broken.
    If all attacks are unbroken, the verdict is unbroken.
    If any attack is missing required fields, the verdict is invalid.
    """
    return "broken" if any(r["broken"] for r in results)  else "Safe"

#Convert results to a JSON-serializable format to be ready for josnify()
def jsonify(r):

    out = dict(r)
    if r["factors"] is not None:
        out["factors"] = [str(x) for x in r["factors"]]
    if r["private_key"] is not None:
        out["private_key"] = str(r["private_key"])
    return out
