def rgb_to_cmyk_gcr(r: float, g: float, b: float):
    k = min(1.0 - r, 1.0 - g, 1.0 - b)
    if k >= 1.0 - 1e-9:
        return 0.0, 0.0, 0.0, 1.0
    c = (1.0 - r - k) / (1.0 - k)
    m = (1.0 - g - k) / (1.0 - k)
    y = (1.0 - b - k) / (1.0 - k)
    return c, m, y, k


def rgb_to_cmyk_ucr(r: float, g: float, b: float, factor: float = 0.7):
    k = min(1.0 - r, 1.0 - g, 1.0 - b) * factor
    if k >= 1.0 - 1e-9:
        return 0.0, 0.0, 0.0, 1.0
    c = (1.0 - r - k) / (1.0 - k)
    m = (1.0 - g - k) / (1.0 - k)
    y = (1.0 - b - k) / (1.0 - k)
    c = max(0.0, min(1.0, c))
    m = max(0.0, min(1.0, m))
    y = max(0.0, min(1.0, y))
    return c, m, y, k


def cmyk_to_rgb(c: float, m: float, y: float, k: float):
    r = (1.0 - c) * (1.0 - k)
    g = (1.0 - m) * (1.0 - k)
    b = (1.0 - y) * (1.0 - k)
    return r, g, b