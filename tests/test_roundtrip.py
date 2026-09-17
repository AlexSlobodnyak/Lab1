import pytest

from src.colorlab.model.converter import ColorConverter


@pytest.fixture
def conv():
    return ColorConverter("D65", "GCR", "clip")


def test_rgb_lab_rgb(conv):
    for rgb in [
        (0, 0, 0),
        (255, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (128, 64, 32),
    ]:
        l, a, b = conv.rgb_to_lab(*rgb)
        rgb2, _ = conv.lab_to_rgb(l, a, b)
        assert abs(rgb2[0] - rgb[0]) <= 1.5
        assert abs(rgb2[1] - rgb[1]) <= 1.5
        assert abs(rgb2[2] - rgb[2]) <= 1.5


def test_rgb_cmyk_rgb(conv):
    for rgb in [
        (0, 0, 0),
        (255, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (128, 64, 32),
    ]:
        c, m, y, k = conv.rgb_to_cmyk(*rgb)
        rgb2 = conv.cmyk_to_rgb(c, m, y, k)
        assert abs(rgb2[0] - rgb[0]) <= 1.5
        assert abs(rgb2[1] - rgb[1]) <= 1.5
        assert abs(rgb2[2] - rgb[2]) <= 1.5


def test_rgb_lab_rgb_d50(conv):
    conv.set_illuminant("D50")
    for rgb in [(255, 0, 0), (128, 64, 32), (200, 100, 50)]:
        l, a, b = conv.rgb_to_lab(*rgb)
        rgb2, _ = conv.lab_to_rgb(l, a, b)
        assert abs(rgb2[0] - rgb[0]) <= 2.0
        assert abs(rgb2[1] - rgb[1]) <= 2.0
        assert abs(rgb2[2] - rgb[2]) <= 2.0


def test_illuminant_change_affects_lab(conv):
    l65, a65, b65 = conv.rgb_to_lab(255, 128, 0)
    conv.set_illuminant("D50")
    l50, a50, b50 = conv.rgb_to_lab(255, 128, 0)
    assert abs(b65 - b50) > 1.0


def test_illuminant_change_not_affect_gray(conv):
    l65, a65, b65 = conv.rgb_to_lab(128, 128, 128)
    conv.set_illuminant("D50")
    l50, a50, b50 = conv.rgb_to_lab(128, 128, 128)
    assert abs(l65 - l50) < 0.5
    assert abs(a65 - a50) < 0.5
    assert abs(b65 - b50) < 0.5