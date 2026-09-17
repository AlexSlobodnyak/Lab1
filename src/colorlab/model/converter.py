from .cmyk import (
    cmyk_to_rgb as _cmyk_to_rgb01,
    rgb_to_cmyk_gcr,
    rgb_to_cmyk_ucr,
)
from .gamut import clip_rgb, scale_rgb
from .rgb_xyz import (
    build_rgb_to_xyz_matrix,
    build_xyz_to_rgb_matrix,
    rgb_to_xyz,
    xyz_to_rgb,
)
from .xyz_lab import lab_to_xyz, xyz_to_lab


class ColorConverter:
    def __init__(
        self,
        illuminant: str = "D65",
        cmyk_algo: str = "GCR",
        gamut_strategy: str = "clip",
    ):
        self.cmyk_algo = cmyk_algo
        self.gamut_strategy = gamut_strategy
        self._illuminant = None
        self.m = None
        self.m_inv = None
        self.set_illuminant(illuminant)

    @property
    def illuminant(self) -> str:
        return self._illuminant

    def set_illuminant(self, name: str):
        self._illuminant = name
        self.m = build_rgb_to_xyz_matrix(name)
        self.m_inv = build_xyz_to_rgb_matrix(name)

    def rgb_to_xyz(self, r, g, b):
        return rgb_to_xyz(r, g, b, self.m)

    def xyz_to_rgb(self, x, y, z):
        return xyz_to_rgb(x, y, z, self.m_inv)

    def rgb_to_lab(self, r, g, b):
        x, y, z = self.rgb_to_xyz(r, g, b)
        return xyz_to_lab(x, y, z, self._illuminant)

    def lab_to_rgb(self, l, a, b):
        x, y, z = lab_to_xyz(l, a, b, self._illuminant)
        rgb01 = self.xyz_to_rgb(x, y, z)
        rgb01, warn = self._apply_gamut(rgb01)
        return tuple(v * 255.0 for v in rgb01), warn

    def rgb_to_cmyk(self, r, g, b):
        r01, g01, b01 = r / 255.0, g / 255.0, b / 255.0
        if self.cmyk_algo == "GCR":
            c, m, y, k = rgb_to_cmyk_gcr(r01, g01, b01)
        else:
            c, m, y, k = rgb_to_cmyk_ucr(r01, g01, b01)
        return c * 100.0, m * 100.0, y * 100.0, k * 100.0

    def cmyk_to_rgb(self, c, m, y, k):
        c01, m01, y01, k01 = c / 100.0, m / 100.0, y / 100.0, k / 100.0
        r, g, b = _cmyk_to_rgb01(c01, m01, y01, k01)
        return r * 255.0, g * 255.0, b * 255.0

    def _apply_gamut(self, rgb01):
        if self.gamut_strategy == "clip":
            return clip_rgb(*rgb01)
        return scale_rgb(*rgb01)