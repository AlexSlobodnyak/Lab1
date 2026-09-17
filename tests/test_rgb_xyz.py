import pytest

from src.colorlab.model.converter import ColorConverter


@pytest.fixture
def conv():
    return ColorConverter("D65")


def test_black(conv):
    x, y, z = conv.rgb_to_xyz(0, 0, 0)
    assert abs(x) < 1e-6
    assert abs(y) < 1e-6
    assert abs(z) < 1e-6


def test_white_d65(conv):
    x, y, z = conv.rgb_to_xyz(255, 255, 255)
    assert abs(x - 95.05) < 0.1
    assert abs(y - 100.00) < 0.1
    assert abs(z - 108.88) < 0.1


def test_red_d65(conv):
    x, y, z = conv.rgb_to_xyz(255, 0, 0)
    assert abs(x - 41.24) < 0.1
    assert abs(y - 21.26) < 0.1
    assert abs(z - 1.93) < 0.1


def test_green_d65(conv):
    x, y, z = conv.rgb_to_xyz(0, 255, 0)
    assert abs(x - 35.76) < 0.1
    assert abs(y - 71.52) < 0.1
    assert abs(z - 11.92) < 0.1


def test_blue_d65(conv):
    x, y, z = conv.rgb_to_xyz(0, 0, 255)
    assert abs(x - 18.05) < 0.1
    assert abs(y - 7.22) < 0.1
    assert abs(z - 95.05) < 0.1


def test_white_d50(conv):
    conv.set_illuminant("D50")
    x, y, z = conv.rgb_to_xyz(255, 255, 255)
    assert abs(x - 96.42) < 0.2
    assert abs(y - 100.00) < 0.2
    assert abs(z - 82.52) < 0.2


def test_white_e(conv):
    conv.set_illuminant("E")
    x, y, z = conv.rgb_to_xyz(255, 255, 255)
    assert abs(x - 100.0) < 0.2
    assert abs(y - 100.0) < 0.2
    assert abs(z - 100.0) < 0.2


def test_rgb_xyz_roundtrip(conv):
    for rgb in [(0, 0, 0), (255, 255, 255), (255, 0, 0), (128, 64, 32)]:
        x, y, z = conv.rgb_to_xyz(*rgb)
        r, g, b = conv.xyz_to_rgb(x, y, z)
        assert abs(r * 255 - rgb[0]) < 1.0
        assert abs(g * 255 - rgb[1]) < 1.0
        assert abs(b * 255 - rgb[2]) < 1.0