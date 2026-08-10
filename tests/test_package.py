"""Baseline package smoke tests."""

from market_analysis import __version__


def test_package_exposes_version() -> None:
    """The installed package reports the version declared in project metadata."""
    assert __version__ == "0.1.0"
