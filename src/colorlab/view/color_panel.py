from PyQt6.QtCore import Qt, pyqtSignal, QSignalBlocker
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .gradient_slider import GradientSlider


class ColorPanel(QWidget):
    values_edited = pyqtSignal(tuple)

    def __init__(self, title: str, ranges: list):
        super().__init__()
        self.title = title
        self.ranges = ranges
        self.fields = []
        self.sliders = []

        self._current_values = [float(lo) for lo, _ in ranges]
        self._to_rgb = None

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        outer.setSpacing(0)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        outer.addWidget(frame)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        header = QLabel(title)
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        layout.addWidget(header)

        labels = {
            "RGB": ["R", "G", "B"],
            "LAB": ["L", "a", "b"],
            "CMYK": ["C", "M", "Y", "K"],
        }[title]

        for i, (lo, hi) in enumerate(ranges):
            block = QWidget()
            block.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            block_layout = QVBoxLayout(block)
            block_layout.setContentsMargins(0, 0, 0, 0)
            block_layout.setSpacing(2)

            row = QHBoxLayout()
            row.setSpacing(6)

            lbl = QLabel(labels[i] + ":")
            lbl.setFixedWidth(24)
            le = QLineEdit()
            le.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )
            le.setMinimumHeight(24)
            le.setMaximumHeight(28)
            row.addWidget(lbl)
            row.addWidget(le)
            block_layout.addLayout(row)

            slider = GradientSlider(
                gradient_provider=lambda idx=i: self._build_gradient_for(idx)
            )
            slider.setRange(int(lo), int(hi))
            slider.setMinimumHeight(24)
            slider.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            block_layout.addWidget(slider, 1)

            le.editingFinished.connect(self._on_edit)
            slider.valueChanged.connect(self._on_slider)

            self.fields.append(le)
            self.sliders.append(slider)

            layout.addWidget(block, 1)

        self._apply_to_widgets(self._current_values)

    def set_rgb_converter(self, fn):
        self._to_rgb = fn

    def set_values(self, values, block_signals=True):
        for i, (f, s, v) in enumerate(zip(self.fields, self.sliders, values)):
            new_text = self._fmt(v)
            if f.text() != new_text:
                f.blockSignals(True)
                f.setText(new_text)
                f.blockSignals(False)

            new_int = int(round(v))
            if s.value() != new_int:
                s.blockSignals(True)
                s.setValue(new_int)
                s.blockSignals(False)

            self._current_values[i] = float(v)

    def refresh_gradients(self):
        for s in self.sliders:
            s.update()

    def _on_edit(self):
        try:
            vals = tuple(
                float(f.text().replace(",", ".")) for f in self.fields
            )
        except ValueError:
            self._apply_to_widgets(self._current_values)
            return
        for i, v in enumerate(vals):
            self._current_values[i] = v
        self.values_edited.emit(vals)

    def _on_slider(self):
        vals = tuple(float(s.value()) for s in self.sliders)
        for i, v in enumerate(vals):
            self._current_values[i] = v
        for f, v in zip(self.fields, vals):
            f.blockSignals(True)
            f.setText(self._fmt(v))
            f.blockSignals(False)
        self.values_edited.emit(vals)

    def _apply_to_widgets(self, values):
        blockers = [QSignalBlocker(f) for f in self.fields]
        blockers += [QSignalBlocker(s) for s in self.sliders]
        for f, s, v in zip(self.fields, self.sliders, values):
            f.setText(self._fmt(v))
            s.setValue(int(round(v)))

    def _build_gradient_for(self, changed_index: int):
        if self._to_rgb is None:
            return []

        lo, hi = self.ranges[changed_index]
        span = hi - lo
        if span <= 0:
            return []

        steps = 64
        step = span / steps
        colors = []
        for k in range(steps + 1):
            v = lo + k * step
            values = list(self._current_values)
            values[changed_index] = v
            try:
                r, g, b = self._to_rgb(self.title, values)
            except Exception:
                r = g = b = 0
            r = max(0, min(255, int(round(r))))
            g = max(0, min(255, int(round(g))))
            b = max(0, min(255, int(round(b))))
            colors.append(QColor(r, g, b))
        return colors

    @staticmethod
    def _fmt(v: float) -> str:
        if abs(v - round(v)) < 1e-4:
            return str(int(round(v)))
        return f"{v:.2f}"