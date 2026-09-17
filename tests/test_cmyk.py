import pytest

from src.colorlab.model.converter import ColorConverter


@pytest.fixture
def conv_gcr():
    return ColorConverter("D65", "GCR")


@pytest.fixture
def conv_ucr():
    return ColorConverter("D65", "UCR")


def test_gcr_red(conv_gcr):
    c, m, y, k = conv_gcr.rgb_to_cmyk(255, 0, 0)
    assert abs(c - 0) < 0.5
    assert abs(m - 100) < 0.5
    assert abs(y - 100) < 0.5
    assert abs(k - 0) < 0.5


def test_gcr_white(conv_gcr):
    c, m, y, k = conv_gcr.rgb_to_cmyk(255, 255, 255)
    assert abs(c) < 0.5
    assert abs(m) < 0.5
    assert abs(y) < 0.5
    assert abs(k) < 0.5


def test_gcr_black(conv_gcr):
    c, m, y, k = conv_gcr.rgb_to_cmyk(0, 0, 0)
    assert abs(c) < 0.5
    assert abs(m) < 0.5
    assert abs(y) < 0.5
    assert abs(k - 100) < 0.5


def test_gcr_gray(conv_gcr):
    c, m, y, k = conv_gcr.rgb_to_cmyk(128, 128, 128)
    assert abs(c) < 0.5
    assert abs(m) < 0.5
    assert abs(y) < 0.5
    assert abs(k - 49.8) < 0.5


def test_ucr_black(conv_ucr):
    c, m, y, k = conv_ucr.rgb_to_cmyk(0, 0, 0)
    assert abs(k - 70.0) < 0.5
    assert abs(c - 100) < 0.5
    assert abs(m - 100) < 0.5
    assert abs(y - 100) < 0.5


def test_ucr_vs_gcr_differ(conv_gcr, conv_ucr):
    assert conv_gcr.rgb_to_cmyk(0, 0, 0) != conv_ucr.rgb_to_cmyk(0, 0, 0)


def test_cmyk_rgb_roundtrip(conv_gcr):
    for rgb in [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 255),
        (0, 0, 0),
        (128, 64, 32),
    ]:
        c, m, y, k = conv_gcr.rgb_to_cmyk(*rgb)
        r, g, b = conv_gcr.cmyk_to_rgb(c, m, y, k)
        assert abs(r - rgb[0]) < 1.5
        assert abs(g - rgb[1]) < 1.5
        assert abs(b - rgb[2]) < 1.5


def test_cmyk_to_rgb_in_range(conv_gcr):
    for cmyk in [
        (0, 0, 0, 0),
        (100, 100, 100, 100),
        (50, 50, 50, 50),
        (0, 100, 100, 0),
        (100, 0, 100, 0),
        (0, 0, 0, 100),
    ]:
        r, g, b = conv_gcr.cmyk_to_rgb(*cmyk)
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255


def test_cmyk_no_negative_rgb(conv_gcr):
    r, g, b = conv_gcr.cmyk_to_rgb(100, 100, 100, 0)
    assert r >= 0
    assert g >= 0
    assert b >= 0