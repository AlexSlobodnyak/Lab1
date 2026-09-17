from .gamma import linear_to_srgb, srgb_to_linear
from .illuminants import white_point_xyz

_PRIMARIES = {
    "R": (0.6400, 0.3300),
    "G": (0.3000, 0.6000),
    "B": (0.1500, 0.0600),
}


def _invert_3x3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    if abs(det) < 1e-12:
        raise ValueError("Singular 3x3 matrix")
    return [
        [(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
        [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
        [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det],
    ]


def _matmul_vec(m, v):
    return [
        m[i][0] * v[0] + m[i][1] * v[1] + m[i][2] * v[2]
        for i in range(3)
    ]


def build_rgb_to_xyz_matrix(illuminant_name: str):
    xr, yr = _PRIMARIES["R"]
    xg, yg = _PRIMARIES["G"]
    xb, yb = _PRIMARIES["B"]
    zr, zg, zb = 1 - xr - yr, 1 - xg - yg, 1 - xb - yb

    p = [
        [xr, xg, xb],
        [yr, yg, yb],
        [zr, zg, zb],
    ]
    p_inv = _invert_3x3(p)
    xn, yn, zn = white_point_xyz(illuminant_name, y=1.0)
    s = _matmul_vec(p_inv, [xn, yn, zn])

    return [
        [xr * s[0], xg * s[1], xb * s[2]],
        [yr * s[0], yg * s[1], yb * s[2]],
        [zr * s[0], zg * s[1], zb * s[2]],
    ]


def build_xyz_to_rgb_matrix(illuminant_name: str):
    return _invert_3x3(build_rgb_to_xyz_matrix(illuminant_name))


def rgb_to_xyz(r: float, g: float, b: float, m):
    rl = srgb_to_linear(r / 255.0)
    gl = srgb_to_linear(g / 255.0)
    bl = srgb_to_linear(b / 255.0)
    x = (m[0][0] * rl + m[0][1] * gl + m[0][2] * bl) * 100.0
    y = (m[1][0] * rl + m[1][1] * gl + m[1][2] * bl) * 100.0
    z = (m[2][0] * rl + m[2][1] * gl + m[2][2] * bl) * 100.0
    return x, y, z


def xyz_to_rgb(x: float, y: float, z: float, m_inv):
    x01, y01, z01 = x / 100.0, y / 100.0, z / 100.0
    rl = m_inv[0][0] * x01 + m_inv[0][1] * y01 + m_inv[0][2] * z01
    gl = m_inv[1][0] * x01 + m_inv[1][1] * y01 + m_inv[1][2] * z01
    bl = m_inv[2][0] * x01 + m_inv[2][1] * y01 + m_inv[2][2] * z01
    return linear_to_srgb(rl), linear_to_srgb(gl), linear_to_srgb(bl)