def clip_rgb(r: float, g: float, b: float):
    warn = (
        r < 0.0 or r > 1.0
        or g < 0.0 or g > 1.0
        or b < 0.0 or b > 1.0
    )
    return (
        max(0.0, min(1.0, r)),
        max(0.0, min(1.0, g)),
        max(0.0, min(1.0, b)),
    ), warn


def scale_rgb(r: float, g: float, b: float):
    mn = min(r, g, b)
    mx = max(r, g, b)

    if mn < 0.0:
        span = mx - mn
        if span < 1e-12:
            return (0.0, 0.0, 0.0), True
        return (
            (r - mn) / span,
            (g - mn) / span,
            (b - mn) / span,
        ), True

    if mx > 1.0:
        return (r / mx, g / mx, b / mx), True

    return (r, g, b), False