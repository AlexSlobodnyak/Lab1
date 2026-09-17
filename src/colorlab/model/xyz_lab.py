from .illuminants import white_point_xyz

_DELTA = 6.0 / 29.0
_DELTA3 = _DELTA ** 3
_THREE_DELTA2 = 3.0 * _DELTA ** 2


def _f(t: float) -> float:
    if t > _DELTA3:
        return t ** (1.0 / 3.0)
    return t / _THREE_DELTA2 + 4.0 / 29.0


def _f_inv(t: float) -> float:
    if t ** 3 > _DELTA3:
        return t ** 3
    return _THREE_DELTA2 * (t - 4.0 / 29.0)


def xyz_to_lab(x: float, y: float, z: float, illuminant_name: str):
    xn, yn, zn = white_point_xyz(illuminant_name)
    fx = _f(x / xn)
    fy = _f(y / yn)
    fz = _f(z / zn)
    l = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return l, a, b


def lab_to_xyz(l: float, a: float, b: float, illuminant_name: str):
    xn, yn, zn = white_point_xyz(illuminant_name)
    fy = (l + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    return _f_inv(fx) * xn, _f_inv(fy) * yn, _f_inv(fz) * zn