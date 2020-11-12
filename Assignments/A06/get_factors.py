# python3 Assignments/A06/get_factors.py input="Assignments/A06/numbers"
import sys
import math
import os
import csv
import array

def mykwargs(argv):
    '''
    Processes argv list into plain args (list) and kwargs (dict).
    Just easier than using a library like argparse for small things.
    '''
    args = []
    kargs = {}

    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs

def usage(message=None):
    """
    Display descriptive error messages if the keywords from .replit are incorrect
    """
    if message:
        print(message)
    name = os.path.basename(__file__)
    print(f"Usage: python {name} [input=string filename]")
    print(f"Example:\n\t python {name} input=in1\n")
    sys.exit()

def eratosthenes(n):
    """
    Sieve of Eratosthenes function finds all primes between 0 and some number n, stores them in a list, and returns the list
    """
    multiples = []
    primes = []
    for i in range(2, n+1):
        for j in range(i*i, n+1, i):
            multiples.append(int(j))
        if i not in multiples:
            primes.append(int(i))
    return primes

def getFactors(n, primes):
    """
    getFactors function stores and returns the factors of n in a list, factorList, for the (likely) composite number, n. 
    If n is a prime number and greater than 10,000 then the function will simply return an empty list
    """
    factorList = []
    # use the factored tree method
    for x in primes:
        if ((n % x) == 0):
            factorList.append(x)
    return factorList

if __name__=='__main__':
    required_params = 1 # adjust accordingly
    # get processed command line arguments 
    _,params = mykwargs(sys.argv[1:])

    # print usage if not called correctly
    if len(params) < required_params:
        usage()

    infile = params.get('input',None)
    if not infile:
      usage()
    
    numList = []
    primes = []

    with open(infile) as f:
      for line in f: # read rest of lines
          numList.append([int(x) for x in line.split()])

    # 10000 covers most prime numbers in file w/out breaking replit
    primes = eratosthenes(10000)
    factors = []

    # numList is a list of lists of integers with only one variable in the list
    for i in range(0,len(numList)):
      for j in numList[i]:
        # check for 0
        if (j == 0):
            print("Number", i+1, ": ", numList[i][0], " - Factors: 0")
        else:
            # factors will be a list of all factors for a number j
            factors = getFactors(j, primes)

            # checking for numbers too big for eratosthenes function
            if (len(factors) == 0):
              primes.append(j)

            if j not in primes:
              print("Number", i+1, ": ", numList[i][0], " - Factors:", factors)
            else:
              print("Number", i+1, ": ", numList[i][0], " - Prime!")
        