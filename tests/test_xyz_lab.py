import pytest

from src.colorlab.model.converter import ColorConverter


@pytest.fixture
def conv():
    return ColorConverter("D65")


def test_black(conv):
    l, a, b = conv.rgb_to_lab(0, 0, 0)
    assert abs(l - 0.0) < 0.1
    assert abs(a - 0.0) < 0.1
    assert abs(b - 0.0) < 0.1


def test_white(conv):
    l, a, b = conv.rgb_to_lab(255, 255, 255)
    assert abs(l - 100.0) < 0.1
    assert abs(a - 0.0) < 0.5
    assert abs(b - 0.0) < 0.5


def test_gray(conv):
    l, a, b = conv.rgb_to_lab(128, 128, 128)
    assert abs(l - 53.59) < 0.2
    assert abs(a) < 0.5
    assert abs(b) < 0.5


def test_red(conv):
    l, a, b = conv.rgb_to_lab(255, 0, 0)
    assert abs(l - 53.24) < 0.2
    assert abs(a - 80.09) < 0.5
    assert abs(b - 67.20) < 0.5


def test_green(conv):
    l, a, b = conv.rgb_to_lab(0, 255, 0)
    assert abs(l - 87.74) < 0.2
    assert abs(a + 86.18) < 0.5
    assert abs(b - 83.18) < 0.5


def test_blue(conv):
    l, a, b = conv.rgb_to_lab(0, 0, 255)
    assert abs(l - 32.30) < 0.2
    assert abs(a - 79.19) < 0.5
    assert abs(b + 107.86) < 0.5


def test_lab_idempotent(conv):
    for xyz in [(0, 0, 0), (95.05, 100.0, 108.88), (41.24, 21.26, 1.93)]:
        rgb = conv.xyz_to_rgb(*xyz)
        l1, a1, b1 = conv.rgb_to_lab(*rgb)
        l2, a2, b2 = conv.rgb_to_lab(*conv.xyz_to_rgb(*xyz))
        assert abs(l1 - l2) < 1e-9
        assert abs(a1 - a2) < 1e-9
        assert abs(b1 - b2) < 1e-9