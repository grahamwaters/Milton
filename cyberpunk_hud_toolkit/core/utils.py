"""
core/utils.py

Utility functions and constants:
 - color definitions
 - easing functions
"""
import math

def lerp(a, b, t):
    """ Linear interpolation from a to b with parameter t in [0..1]. """
    return a + (b - a) * t

def ease_in_out(t):
    """ Simple ease in-out function. """
    return 3*t**2 - 2*t**3

# Additional color/easing utils if needed
