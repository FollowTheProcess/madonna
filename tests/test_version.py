"""
Tests for the core functionality.

Author: Tom Fleet
Created: 09/10/2021
"""

import pytest

from madonna import Version


def test_version_init():
    v = Version(1, 2, 4, "rc.1", "build.123")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 4
    assert v.prerelease == "rc.1"
    assert v.buildmetadata == "build.123"


def test_version_repr():
    v = Version(1, 2, 4, "rc.1", "build.123")
    want = "Version(major=1, minor=2, patch=4, prerelease='rc.1', buildmetadata='build.123')"  # noqa: E501
    assert repr(v) == want


def test_version_less_than_zero_major():
    """
    Initialising a version with any part < 0 should raise
    a ValueError.
    """
    with pytest.raises(ValueError):
        Version(-1, 2, 4)


def test_version_less_than_zero_minor():
    """
    Initialising a version with any part < 0 should raise
    a ValueError.
    """
    with pytest.raises(ValueError):
        Version(1, -2, 4)


def test_version_less_than_zero_patch():
    """
    Initialising a version with any part < 0 should raise
    a ValueError.
    """
    with pytest.raises(ValueError):
        Version(1, 2, -4)


@pytest.mark.parametrize(
    "version, want",
    [
        (Version(1, 2, 4, None, None), "v1.2.4"),
        (Version(1, 2, 4), "v1.2.4"),
        (Version(2, 6, 8, "rc.2", None), "v2.6.8-rc.2"),
        (Version(2, 6, 8, "rc.2"), "v2.6.8-rc.2"),
        (Version(7, 6, 2, None, "build.123"), "v7.6.2-build.123"),
        (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1-build.123"),
    ],
)
def test_version_str(version: Version, want: str):
    assert str(version) == want


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(6, 4, 2), Version(6, 4, 3), True),  # Patch lt
        (Version(6, 4, 3), Version(6, 4, 2), False),  # Patch gt
        (Version(6, 4, 2), Version(6, 5, 2), True),  # Minor lt
        (Version(6, 5, 2), Version(6, 4, 2), False),  # Minor gt
        (Version(6, 4, 2), Version(7, 4, 2), True),  # Major lt
        (Version(7, 4, 2), Version(6, 4, 2), False),  # Major gt
        (Version(0, 0, 0), Version(9, 9, 9), True),  # Big diff true
        (Version(9, 9, 9), Version(0, 0, 0), False),  # Big diff false
        (Version(2, 2, 2), Version(2, 2, 2), False),  # Equal
        (Version(0, 0, 0), Version(0, 0, 0), False),  # Zeros
        (
            Version(1, 2, 4),
            Version(1, 2, 4, "rc.1"),
            False,
        ),
        (
            Version(1, 2, 4, "rc.1"),
            Version(1, 2, 4),
            True,
        ),
        (
            Version(1, 2, 4),
            Version(1, 2, 4, "rc.1", "build.123"),
            False,
        ),
        (
            Version(1, 2, 4, "rc.1", "build.123"),
            Version(1, 2, 4),
            True,
        ),
        (
            Version(1, 2, 4, "rc.1"),
            Version(1, 2, 4, "rc.2"),
            True,
        ),
        (
            Version(1, 2, 4, "rc.2"),
            Version(1, 2, 4, "rc.1"),
            False,
        ),
        (
            Version(1, 2, 4, None, "build.123"),
            Version(1, 2, 4, None, "build.456"),
            True,
        ),
        (
            Version(1, 2, 4, None, "build.456"),
            Version(1, 2, 4, None, "build.123"),
            False,
        ),
        (
            Version(1, 2, 4, "rc.1", "build.123"),
            Version(1, 2, 4, "rc.2", "build.123"),
            True,
        ),
        (
            Version(1, 2, 4, "rc.2", "build.123"),
            Version(1, 2, 4, "rc.1", "build.123"),
            False,
        ),
        (
            Version(1, 2, 4, "rc.1", "build.456"),
            Version(1, 2, 4, "rc.1", "build.123"),
            False,
        ),
        (
            Version(1, 2, 4, "rc.1", "build.123"),
            Version(1, 2, 4, "rc.1", "build.456"),
            True,
        ),
        (
            Version(1, 2, 4, "rc.1", "build.123"),
            Version(1, 2, 4, "rc.1"),
            True,
        ),
    ],
)
def test_version_less_than(v1: Version, v2: Version, want: bool):
    assert (v1 < v2) == want


def test_version_less_than_raises_if_invalid_object():
    v1 = Version(1, 2, 4)
    v2 = "I'm a string"

    with pytest.raises(NotImplementedError):
        v1 < v2


@pytest.mark.parametrize(
    "v1, v2",
    [
        (Version(5, 2, 4, "badrelease1"), Version(5, 2, 4, "badrelease2")),
        (Version(5, 2, 4, None, "badbuild1"), Version(5, 2, 4, None, "badbuild2")),
    ],
)
def test_version_less_than_raises_if_cannot_parse_pre_or_build(
    v1: Version, v2: Version
):
    with pytest.raises(ValueError):
        v1 < v2
