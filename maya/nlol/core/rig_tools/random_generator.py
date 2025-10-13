"""Functions for random generation."""

import colorsys
import hashlib
import random


def random_color(seed_string: str) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Get a consistent random color between sessions.
    For shelf backgrounds, curve colors, etc.

    Args:
        seed_string: String to generate consistent hash. String does not matter. It's just a seed.
            Changing the seed_string will change the random color.

    Returns:
        RGB values and RGB values with reduced brightness.

    """
    # create md5 hash object
    # convert string hash_key to bytes
    # get hexidecimal string representation of the hash
    # interpet hex string as base-16 (hexadecimal -> decimal)
    seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16)

    random.seed(seed)
    max_value = 0.70
    decimal_limit = 3

    # consistent random rgb values
    r_clr = round(random.random(), decimal_limit)
    g_clr = round(random.random(), decimal_limit)
    b_clr = round(random.random(), decimal_limit)

    # convert to hsv and back to tone down color via value
    h, s, v = colorsys.rgb_to_hsv(r_clr, g_clr, b_clr)
    h_clr = h
    s_clr = s
    v_clr = v * max_value
    r_dull, g_dull, b_dull = colorsys.hsv_to_rgb(h_clr, s_clr, v_clr)

    return (r_clr, g_clr, b_clr), (r_dull, g_dull, b_dull)


def random_colors_dull(seed_string_prefix: str = "") -> list[tuple]:
    """Create list of consistent random dull colors.
    Useful for shelf button colors.

    Args:
        seed_string_prefix: Optional seed string prefix to vary random colors
            from another group of random colors.

    Returns:
        Output list of consistent random dull colors.

    """
    random_colors_dull = []
    for i in range(30):
        color_dull = random_color(seed_string=f"{seed_string_prefix}{i}")[1]
        random_colors_dull.append(color_dull)

    return random_colors_dull
