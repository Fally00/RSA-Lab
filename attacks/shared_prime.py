"""
attacks/shared_prime.py
Owner: Member 6
Purpose: W2: batch gcd across many keys to find shared primes.
Follows the shared contract: run_batch(keys) -> list[dict] (see README section 7).
"""
import math 
def find_gcd(A,B):
    if (A>B):
        result=math.gcd(A,B)
        print("GCD = ", result)
    elif (B>A):
        A, B = B, A
        result=math.gcd(A,B)
        print("GCD = ", result)
    else:
        print("Please inter valid numbers")

        


A=int(input("Enter your greatest num = "))
B=int(input("Enter your secound  num = "))

find_gcd(A,B)
