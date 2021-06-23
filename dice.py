# coding: utf-8
"""
File: dice.py

Methods for "rolling dice", printing out a list of 
possible outcomes when dice are rolled, or a probability 
distribution for a given collection of dice.  

Last updated 23 June 2021.  RAM
"""

import matplotlib.pyplot as plt
from fractions import Fraction
import random
random.seed()

def _mergeDiceDicts(d1, d2):
    """  
    A helper method, generally to be used with the "diceDict"
    method defined elsewhere.
    """
    assert isinstance(d1, dict) and isinstance(d2, dict), "Invalid argument to mergeDiceDicts!"
    if len(d1) == 0:
        return d2
    if len(d2) == 0:
        return d1
    newDict = dict()
    for k1 in d1.keys():
        for k2 in d2.keys():
            newK = k1 + k2          # new key
            newV = d1[k1] * d2[k2]  # number of ways of making newK 
                                    # from the two given keys
            newDict[newK] = newDict.get(newK, 0) + newV  #  create/update 
                                                         # the new key in 
                                                         # the result
    return newDict

def diceDict(diceList):
    """
    A "merge sort" type of procedure to generate a dictionary of 
    outcomes of a list of dice numbers that describe the number of 
    sides on each side.  
    
    Each element of diceList is a positive number, or another list.  
    If it's a positive number n, it's for a die with that many 
    sides with numbers {1, ..., n}.  If it's a list, it's for a 
    die where the list describes the numbers on the sides of the 
    die (which could be positive, zero, or negative, and could 
    have repetitions).   
    """
    assert isinstance(diceList, list), "Invalid argument to diceDict!"
    if len(diceList) == 0:
        return dict()
    elif len(diceList) == 1:
        #  Check if the "die" element itself is a list.  If so,
        #  interpret it as a single die where the values of the sides
        #  are the elements of that list.  (Allows for dice with the 
        #  same values on sides, Sicherman dice, negative numbers, etc.)
        if isinstance(diceList[0], list):
            newDict = dict()
            for x in set(diceList[0]):
                newDict[x] = diceList[0].count(x)
            return newDict
        #  Otherwise, if it's a single integer, we assume it's positive,
        #  and is representing a die with that many sides, numbered
        #  with the labels { 1, ..., n } where n is that integer.
        else:
            assert diceList[0] > 0, "Negative number supplied as number of sides of die!"
            return { x : 1 for x in range(1, diceList[0]+1) }
    #  Otherwise, there are at least two elements in the list, so 
    #  split and recurse.
    random.shuffle(diceList)
    L = int(len(diceList)/2)
    leftDict = diceDict( diceList[:L] )
    rightDict = diceDict( diceList[L:] )
    final = _mergeDiceDicts(leftDict, rightDict)
    return { k: v for k, v in sorted(final.items()) }

def diceProb(diceList, exact=False):
    """ 
    Returns a dictionary of probabilities, where the keys are 
    the possible values obtainable with the set of dice in 
    diceList.  diceList is either a single integer (in which
    case it's recast into a list with one element, see below), 
    or is a list.

    Each element of diceList is a positive number, or another list.  
    If it's a positive number n, it's for a die with that many 
    sides with numbers {1, ..., n}.  If it's a list, it's for a 
    die where the list describes the numbers on the sides of the 
    die (which could be positive, zero, or negative, and could 
    have repetitions).   
    
    The parameter "exact" controls whether floating point numbers are
    returned, or if exact values are returned using the Fraction
    class from the fractions module.
    """
    assert isinstance(diceList, (list, int)), "Invalid argument to diceProb!"
    if isinstance(diceList, int):
        diceList = [ diceList ]    #  recast a single number to a list
    result = diceDict(diceList)
    s = sum(result.values())
    if exact:
        return { x : Fraction(result[x],s) for x in sorted(result.keys()) }
    else:
        return { x : result[x]/s for x in sorted(result.keys()) }

def roll(diceList):
    """ 
    Returns a "roll" of the dice described in diceList.  diceList
    is either a single integer (in which case it's assumed to be
    positive and will be recast into a list of a single item, 
    see below), or a list.  
    
    Each element of diceList is a positive number, or another list.  
    If it's a positive number n, it's for a die with that many 
    sides with numbers {1, ..., n}.  If it's a list, it's for a 
    die where the list describes the numbers on the sides of the 
    die (which could be positive, zero, or negative, and could 
    have repetitions).
    """ 
    assert isinstance(diceList, (list, int)), "Invalid argument to roll!"
    if isinstance(diceList, int):
        diceList = [ diceList ]     #  recast a single number as a list
    result = 0
    for dice in diceList:
        if isinstance(dice, int):
            assert dice > 0, "Negative number supplied as number of sides of die!"
            result += random.choice(range(1, dice+1))
        elif isinstance(dice, list):
            result += random.choice(dice)
    return result

def diceBarPlot(diceList):
    """
    A method to draw a histogram to illustrate the probability 
    distribution for a given set of dice described in diceList.
    """
    assert isinstance(diceList, (list, int)), "Invalid argument to diceHist!"
    hist = diceDict(diceList)
    plt.bar(hist.keys(), hist.values())
    