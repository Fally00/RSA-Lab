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

#=================BATCH GCD=============================#
import math 

def product_tree(x: list[int])-> list[list[int]]:
    tree=[x]
    while len(x)>1:
        x=[math.prod(x[i*2:(i+1)*2])for i in range((len(x)+1)//2)]#if x odd
        tree.append(x)
    return tree
def batch_gcd(x:list[int]) -> list[int]:
    if not x:
        return[]
    elif (len(x)==1):
        return[1]
    prod=product_tree(x)
    remove=prod.pop()
    while prod:
        level=prod.pop()
        remove=[remove[i//2]%(level[i]**2) for i in range(len(level))]
    return[math.gcd(r//n,n) for r,n in zip(remove,x)]

num=int(input("Enter how many numbers of key  = "))
key=[]

for i in range(num):
    n=int(input(f"Enter RSA key {i+1} = "))
    key.append(n)

result= batch_gcd(key)
print(result)