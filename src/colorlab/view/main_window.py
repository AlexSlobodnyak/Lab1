from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..viewmodel.color_viewmodel import ColorViewModel
from .color_panel import ColorPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Lab — CMYK ↔ LAB ↔ RGB")
        self.resize(1100, 700)
        self.setMinimumSize(800, 550)

        self.vm = ColorViewModel()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        self.warning_label = QLabel("")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.setStyleSheet(
            "QLabel { background-color: #ffd6d6; color: #900; "
            "font-weight: bold; padding: 6px; border-radius: 4px; }"
        )
        self.warning_label.setVisible(False)
        root.addWidget(self.warning_label)

        self._warning_timer = QTimer(self)
        self._warning_timer.setSingleShot(True)
        self._warning_timer.timeout.connect(
            lambda: self.warning_label.setVisible(False)
        )

        top = QHBoxLayout()
        top.setSpacing(8)

        top.addWidget(QLabel("Источник света:"))
        self.cb_illum = QComboBox()
        self.cb_illum.addItems(["D65", "D50", "E"])
        self.cb_illum.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        top.addWidget(self.cb_illum)

        top.addSpacing(12)
        top.addWidget(QLabel("CMYK:"))
        self.cb_cmyk = QComboBox()
        self.cb_cmyk.addItems(["GCR", "UCR"])
        self.cb_cmyk.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        top.addWidget(self.cb_cmyk)

        top.addSpacing(12)
        top.addWidget(QLabel("Gamut:"))
        self.cb_gamut = QComboBox()
        self.cb_gamut.addItems(["clip", "scale"])
        self.cb_gamut.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        top.addWidget(self.cb_gamut)

        top.addStretch(1)
        root.addLayout(top)

        panels = QHBoxLayout()
        panels.setSpacing(12)
        self.panel_rgb = ColorPanel("RGB", [(0, 255), (0, 255), (0, 255)])
        self.panel_lab = ColorPanel(
            "LAB",
            [(0, 100), (-128, 127), (-128, 127)],
        )
        self.panel_cmyk = ColorPanel(
            "CMYK",
            [(0, 100), (0, 100), (0, 100), (0, 100)],
        )
        for p in (self.panel_rgb, self.panel_lab, self.panel_cmyk):
            p.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            panels.addWidget(p, 1)
        root.addLayout(panels, 1)

        bottom = QHBoxLayout()
        bottom.setSpacing(12)
        bottom.addWidget(QLabel("Текущий цвет:"))
        self.preview = QLabel()
        self.preview.setMinimumSize(140, 60)
        self.preview.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.preview.setAutoFillBackground(True)
        bottom.addWidget(self.preview, 1)
        self.btn_palette = QPushButton("Выбрать из палитры…")
        self.btn_palette.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )
        bottom.addWidget(self.btn_palette)
        root.addLayout(bottom)

        for panel in (self.panel_rgb, self.panel_lab, self.panel_cmyk):
            panel.set_rgb_converter(self.vm.model_to_rgb)

        self.panel_rgb.values_edited.connect(
            lambda v: self.vm.set_from_rgb(*v)
        )
        self.panel_lab.values_edited.connect(
            lambda v: self.vm.set_from_lab(*v)
        )
        self.panel_cmyk.values_edited.connect(
            lambda v: self.vm.set_from_cmyk(*v)
        )

        self.cb_illum.currentTextChanged.connect(self.vm.set_illuminant)
        self.cb_cmyk.currentTextChanged.connect(self.vm.set_cmyk_algo)
        self.cb_gamut.currentTextChanged.connect(self.vm.set_gamut_strategy)

        self.btn_palette.clicked.connect(self._pick_from_palette)

        self.vm.color_changed.connect(self._on_color_changed)
        self.vm.warning_raised.connect(self._on_warning)

        self.vm.emit_current()

    def _on_color_changed(self, data: dict):
        if self.vm.source_model != "RGB":
            self.panel_rgb.set_values(data["RGB"], block_signals=True)
        if self.vm.source_model != "LAB":
            self.panel_lab.set_values(data["LAB"], block_signals=True)
        if self.vm.source_model != "CMYK":
            self.panel_cmyk.set_values(data["CMYK"], block_signals=True)

        r, g, b = data["RGB"]
        r = max(0, min(255, int(round(r))))
        g = max(0, min(255, int(round(g))))
        b = max(0, min(255, int(round(b))))
        pal = self.preview.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(r, g, b))
        self.preview.setPalette(pal)

        self.panel_rgb.refresh_gradients()
        self.panel_lab.refresh_gradients()
        self.panel_cmyk.refresh_gradients()

    def _on_warning(self, msg: str):
        self.warning_label.setText("⚠ " + msg)
        self.warning_label.setVisible(True)
        self._warning_timer.start(3000)
        self.statusBar().showMessage(msg, 3000)

    def _pick_from_palette(self):
        col = QColorDialog.getColor(parent=self)
        if col.isValid():
            self.vm.set_from_rgb(col.red(), col.green(), col.blue())