import math

# Linear Interpolation and Basic Easing
def lerp(a, b, t):
    """Linear interpolation from a to b with parameter t in [0..1]."""
    return a + (b - a) * t

def ease_in_out(t):
    """Simple ease in-out function: smooth acceleration and deceleration."""
    return 3*t**2 - 2*t**3

# Additional Easing Functions
def ease_in(t):
    """Easing function for gradual acceleration (quadratic)."""
    return t * t

def ease_out(t):
    """Easing function for gradual deceleration (quadratic)."""
    return t * (2 - t)

def cubic_ease_in(t):
    """Cubic ease-in function for a stronger start."""
    return t**3

def cubic_ease_out(t):
    """Cubic ease-out function for a stronger finish."""
    return 1 - (1 - t)**3

def exponential_ease_out(t):
    """Exponential ease-out for a very sharp deceleration (except at t==1)."""
    return 1 if t == 1 else 1 - math.pow(2, -10 * t)

# Color Utilities
def rgb_to_hex(r, g, b):
    """
    Convert RGB color values to hexadecimal string.

    Parameters:
      r, g, b: Integers in the range 0-255.

    Returns:
      Hexadecimal color string (e.g., "#ff8800").
    """
    return '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))

def hex_to_rgb(hex_color):
    """
    Convert a hexadecimal color string to an RGB tuple.

    Parameters:
      hex_color: String of the form "#rrggbb" or "#rgb".

    Returns:
      Tuple (r, g, b) with each component as an integer.
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        # Expand shorthand hex code to full form (e.g., "abc" becomes "aabbcc")
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def mix_colors(color1, color2, t):
    """
    Mix two colors together.

    Parameters:
      color1: A tuple (r, g, b) for the first color.
      color2: A tuple (r, g, b) for the second color.
      t:      A float in [0, 1] indicating the mixing ratio. 0 returns color1; 1 returns color2.

    Returns:
      A tuple (r, g, b) for the mixed color.
    """
    return tuple(int(lerp(c1, c2, t)) for c1, c2 in zip(color1, color2))

# Example predefined color constants
COLOR_PRIMARY   = (50, 150, 250)  # A sample blue
COLOR_SECONDARY = (250, 150, 50)  # A sample orange
COLOR_SUCCESS   = (76, 175, 80)   # A sample green
COLOR_ERROR     = (244, 67, 54)   # A sample red

if __name__ == '__main__':
    # Example usage of the easing functions and color utilities:

    # Easing function demonstration:
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        print(f"t: {t:.2f}, ease_in: {ease_in(t):.2f}, ease_out: {ease_out(t):.2f}, ease_in_out: {ease_in_out(t):.2f}")

    # Color conversion demonstration:
    rgb_color = (255, 100, 50)
    hex_color = rgb_to_hex(*rgb_color)
    print(f"RGB {rgb_color} -> Hex {hex_color}")

    # Convert back to RGB
    converted_rgb = hex_to_rgb(hex_color)
    print(f"Hex {hex_color} -> RGB {converted_rgb}")

    # Color mixing demonstration:
    mix = mix_colors(COLOR_PRIMARY, COLOR_SECONDARY, 0.5)
    print(f"Mix of {COLOR_PRIMARY} and {COLOR_SECONDARY} (50-50): {mix}")
