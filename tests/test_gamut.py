import pytest

from src.colorlab.model.converter import ColorConverter


@pytest.fixture
def conv_clip():
    return ColorConverter("D65", "GCR", "clip")


@pytest.fixture
def conv_scale():
    return ColorConverter("D65", "GCR", "scale")


def test_clip_out_of_gamut_returns_warning(conv_clip):
    rgb, warn = conv_clip.lab_to_rgb(90, -100, 80)
    assert warn is True
    assert all(0 <= v <= 255 for v in rgb)
    assert 0 in rgb or 255 in rgb


def test_clip_in_gamut_no_warning(conv_clip):
    rgb, warn = conv_clip.lab_to_rgb(50, 0, 0)
    assert warn is False
    assert all(0 <= v <= 255 for v in rgb)


def test_scale_out_of_gamut_returns_warning(conv_scale):
    rgb, warn = conv_scale.lab_to_rgb(90, -100, 80)
    assert warn is True
    assert all(0 <= v <= 255 for v in rgb)
    assert any(5 < v < 250 for v in rgb)


def test_scale_in_gamut_no_warning(conv_scale):
    rgb, warn = conv_scale.lab_to_rgb(50, 0, 0)
    assert warn is False


def test_clip_and_scale_differ_out_of_gamut(conv_clip, conv_scale):
    rgb_clip, _ = conv_clip.lab_to_rgb(90, -100, 80)
    rgb_scale, _ = conv_scale.lab_to_rgb(90, -100, 80)
    assert rgb_clip != rgb_scale


def test_extreme_lab_out_of_gamut_clip(conv_clip):
    rgb, warn = conv_clip.lab_to_rgb(50, -200, 0)
    assert warn is True


def test_extreme_lab_out_of_gamut_scale(conv_scale):
    rgb, warn = conv_scale.lab_to_rgb(50, -200, 0)
    assert warn is True
    assert all(0 <= v <= 255 for v in rgb)


def test_white_in_gamut(conv_clip):
    rgb, warn = conv_clip.lab_to_rgb(100, 0, 0)
    assert warn is False
    assert all(250 <= v <= 255 for v in rgb)


def test_black_in_gamut(conv_clip):
    rgb, warn = conv_clip.lab_to_rgb(0, 0, 0)
    assert warn is False
    assert all(v <= 5 for v in rgb)