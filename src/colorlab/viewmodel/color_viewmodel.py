from PyQt6.QtCore import QObject, pyqtSignal

from ..model.converter import ColorConverter


class ColorViewModel(QObject):
    color_changed = pyqtSignal(dict)
    warning_raised = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.converter = ColorConverter()
        self._rgb = (255.0, 0.0, 0.0)
        self._source_model = "RGB"

    def model_to_rgb(self, model_name, values):
        if model_name == "RGB":
            return tuple(self._clamp255(v) for v in values)
        if model_name == "LAB":
            rgb, _ = self.converter.lab_to_rgb(*values)
            return tuple(self._clamp255(v) for v in rgb)
        if model_name == "CMYK":
            rgb = self.converter.cmyk_to_rgb(*values)
            return tuple(self._clamp255(v) for v in rgb)
        raise ValueError(model_name)

    @staticmethod
    def _clamp255(v):
        return max(0, min(255, int(round(v))))

    def set_from_rgb(self, r, g, b):
        self._source_model = "RGB"
        self._rgb = (float(r), float(g), float(b))
        self._emit_all()

    def set_from_lab(self, l, a, b):
        self._source_model = "LAB"
        rgb, warn = self.converter.lab_to_rgb(l, a, b)
        self._rgb = rgb
        if warn:
            self.warning_raised.emit(
                f"Цвет вне охвата sRGB — применено: "
                f"{self.converter.gamut_strategy}"
            )
        self._emit_all()

    def set_from_cmyk(self, c, m, y, k):
        self._source_model = "CMYK"
        self._rgb = self.converter.cmyk_to_rgb(c, m, y, k)
        self._emit_all()

    def set_illuminant(self, name):
        self.converter.set_illuminant(name)
        self._source_model = None
        self._emit_all()

    def set_cmyk_algo(self, algo):
        self.converter.cmyk_algo = algo
        self._emit_all()

    def set_gamut_strategy(self, strategy):
        self.converter.gamut_strategy = strategy

    @property
    def source_model(self):
        return self._source_model

    def emit_current(self):
        self._emit_all()

    def _emit_all(self):
        r, g, b = self._rgb
        data = {
            "RGB": (r, g, b),
            "LAB": self.converter.rgb_to_lab(r, g, b),
            "CMYK": self.converter.rgb_to_cmyk(r, g, b),
        }
        self.color_changed.emit(data)