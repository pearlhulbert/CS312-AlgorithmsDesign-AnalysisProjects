import random
import math


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):
    #This is an implementation of modular exponentiation
    #Time complexity: O(n^3)
    #Space complexity: O(n^2)
    if y == 0:
        return 1
    z = mod_exp(x, math.floor(y/2), N)
    if y % 2 == 0:
        return (z**2) % N
    else:
        return (x * z**2) % N
	

def fprobability(k):
    return 1 - (1/2)**k


def mprobability(k):
    return 1 - (1/4)**k

def createTestVals(k, N):
    #This is simply a function I wrote to make a random array of k a values
    testVals = []
    for a in range(0, k):
        val = random.randint(1, N-1)
        testVals.append(val)
    return testVals

def fermat(N,k):
    #Time complexity: O(kn^3)
    #Space complexity: O(n^2)
    testVals = createTestVals(k, N)
    #Taking multiple values increases the chances of accuracy
    for a in testVals:
        #This is a python implementation of Fermat's theorem. Mod_exp is the modular exponentiation part
        if mod_exp(a, N-1, N) != 1:
            return 'composite'
    return 'prime'


def miller_rabin(N,k):
    #Time complexity: O(kn^4)
    #Space complexity: O(n^2)
    testVals = createTestVals(k, N)
    #Miller rabin applies the modular exponentiation found in Fermat's theorem
    for a in testVals:
        n = N - 1
        if mod_exp(a, n, N) != 1:
            return 'composite'
        #If the first check fails, it keeps on using modular exponentiation, taking the square root of the result each time, until the exponent becomes odd and that is no longer possible
        while (n % 2 == 0):
            if mod_exp(a, n, N) == N - 1:
                break
            elif mod_exp(a, n, N) != 1:
                return 'composite'
            n = n/2
    return 'prime'
