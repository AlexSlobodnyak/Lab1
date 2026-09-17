from PyQt6.QtCore import Qt
from PyQt6.QtGui import QLinearGradient, QPainter
from PyQt6.QtWidgets import QSlider


class GradientSlider(QSlider):
    def __init__(self, gradient_provider, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self._provider = gradient_provider

    def paintEvent(self, event):
        painter = QPainter(self)
        colors = self._provider()
        if colors:
            grad = QLinearGradient(0, 0, self.width(), 0)
            n = max(1, len(colors) - 1)
            for i, c in enumerate(colors):
                grad.setColorAt(i / n, c)
            painter.fillRect(self.rect(), grad)
        super().paintEvent(event)