"""
This file cointains our own definitions for the operators: <, >, >= and <=
This file is a subfile beloning to the GEPCLASS algorithm --> see: GEPCLASS_main_code.py
Author: Matthijs van Ede
Date: 04-12-2019 
"""

def own_lt(x, const):
    """
    arguments: 
        x:      the actual variable, in the GEPCLASS: a, b, c or d
        const:  the constant with which x has to be compared, e.g.: a|6 --> const = 6
    """
    return x < const


def own_gt(x, const):
    """
    arguments: 
        x:      the actual variable, in the GEPCLASS: a, b, c or d
        const:  the constant with which x has to be compared, e.g.: a|6 --> const = 6
    """
    return x > const


def own_le(x, const):
    """
    arguments: 
        x:      the actual variable, in the GEPCLASS: a, b, c or d
        const:  the constant with which x has to be compared, e.g.: a|6 --> const = 6
    """
    return x <= const


def own_ge(x, const):
    """
    arguments: 
        x:      the actual variable, in the GEPCLASS: a, b, c or d
        const:  the constant with which x has to be compared, e.g.: a|6 --> const = 6
    """
    return x >= const



