ILLUMINANTS = {
    "D65": (0.3127, 0.3290),
    "D50": (0.3457, 0.3585),
    "E": (1.0 / 3.0, 1.0 / 3.0),
}


def white_point_xyz(name: str, y: float = 100.0):
    if name not in ILLUMINANTS:
        raise ValueError(f"Unknown illuminant: {name}")
    x, y_chroma = ILLUMINANTS[name]
    xn = x / y_chroma * y
    yn = y
    zn = (1.0 - x - y_chroma) / y_chroma * y
    return xn, yn, zn