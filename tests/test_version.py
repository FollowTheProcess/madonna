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


def test_version_eq():
    v1 = Version(1, 2, 3, "pre", "build")
    v2 = Version(1, 2, 3, "pre", "build")
    v3 = Version(6, 2, 4, "different", "build")

    assert (v1 == v2) is True
    assert (v1 == v3) is False


def test_version_eq_invalid_type():
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        v == "a string"


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(0, 7, 6), Version(1, 7, 6), True),
        (Version(1, 6, 6), Version(1, 7, 6), True),
        (Version(1, 7, 5), Version(1, 7, 6), True),
        (Version(1, 7, 6, "pre"), Version(1, 7, 6), True),
        (Version(1, 7, 6, "pre", "build"), Version(1, 7, 6), True),
        (Version(1, 7, 6, "pre1"), Version(1, 7, 6, "pre2"), True),
        (Version(1, 7, 6, "pre1", "build1"), Version(1, 7, 6, "pre1", "build2"), True),
        (Version(1, 7, 6, None, "build1"), Version(1, 7, 6, None, "build2"), True),
        (Version(1, 7, 6), Version(0, 7, 6), False),
        (Version(1, 7, 6), Version(1, 6, 6), False),
        (Version(1, 7, 6), Version(1, 7, 5), False),
        (Version(1, 7, 6), Version(1, 7, 6, "pre"), False),
        (Version(1, 7, 6), Version(1, 7, 6, "pre", "build"), False),
        (Version(1, 7, 6, "pre2"), Version(1, 7, 6, "pre1"), False),
        (Version(1, 7, 6, "pre2", "build2"), Version(1, 7, 6, "pre1", "build1"), False),
        (Version(1, 7, 6, None, "build2"), Version(1, 7, 6, None, "build1"), False),
    ],
)
def test_version_lt(v1: Version, v2: Version, want: bool):
    assert (v1 < v2) is want


def test_version_lt_invalid_type():
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        v < "a string"


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(0, 7, 6), Version(1, 7, 6), True),
        (Version(1, 6, 6), Version(1, 7, 6), True),
        (Version(1, 7, 5), Version(1, 7, 6), True),
        (Version(1, 7, 6), Version(1, 7, 6), True),
        (Version(1, 7, 6, "pre"), Version(1, 7, 6), True),
        (Version(1, 7, 6, "pre", "build"), Version(1, 7, 6), True),
        (Version(1, 7, 6, "pre1"), Version(1, 7, 6, "pre2"), True),
        (Version(1, 7, 6, "pre1", "build1"), Version(1, 7, 6, "pre1", "build2"), True),
        (Version(1, 7, 6, None, "build1"), Version(1, 7, 6, None, "build2"), True),
        (Version(1, 7, 6), Version(0, 7, 6), False),
        (Version(1, 7, 6), Version(1, 6, 6), False),
        (Version(1, 7, 6), Version(1, 7, 5), False),
        (Version(1, 7, 6), Version(1, 7, 6, "pre"), False),
        (Version(1, 7, 6), Version(1, 7, 6, "pre", "build"), False),
        (Version(1, 7, 6, "pre2"), Version(1, 7, 6, "pre1"), False),
        (Version(1, 7, 6, "pre2", "build2"), Version(1, 7, 6, "pre1", "build1"), False),
        (Version(1, 7, 6, None, "build2"), Version(1, 7, 6, None, "build1"), False),
    ],
)
def test_version_le(v1: Version, v2: Version, want: bool):
    assert (v1 <= v2) is want


def test_version_le_invalid_type():
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        v <= "a string"


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(0, 7, 6), Version(1, 7, 6), False),
        (Version(1, 6, 6), Version(1, 7, 6), False),
        (Version(1, 7, 5), Version(1, 7, 6), False),
        (Version(1, 7, 6, "pre"), Version(1, 7, 6), False),
        (Version(1, 7, 6, "pre", "build"), Version(1, 7, 6), False),
        (Version(1, 7, 6, "pre1"), Version(1, 7, 6, "pre2"), False),
        (Version(1, 7, 6, "pre1", "build1"), Version(1, 7, 6, "pre1", "build2"), False),
        (Version(1, 7, 6, None, "build1"), Version(1, 7, 6, None, "build2"), False),
        (Version(1, 7, 6), Version(0, 7, 6), True),
        (Version(1, 7, 6), Version(1, 6, 6), True),
        (Version(1, 7, 6), Version(1, 7, 5), True),
        (Version(1, 7, 6), Version(1, 7, 6, "pre"), True),
        (Version(1, 7, 6), Version(1, 7, 6, "pre", "build"), True),
        (Version(1, 7, 6, "pre2"), Version(1, 7, 6, "pre1"), True),
        (Version(1, 7, 6, "pre2", "build2"), Version(1, 7, 6, "pre1", "build1"), True),
        (Version(1, 7, 6, None, "build2"), Version(1, 7, 6, None, "build1"), True),
    ],
)
def test_version_gt(v1: Version, v2: Version, want: bool):
    assert (v1 > v2) is want


def test_version_gt_invalid_type():
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        v > "a string"


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(0, 7, 6), Version(1, 7, 6), False),
        (Version(1, 6, 6), Version(1, 7, 6), False),
        (Version(1, 7, 5), Version(1, 7, 6), False),
        (Version(1, 7, 6, "pre"), Version(1, 7, 6), False),
        (Version(1, 7, 6, "pre", "build"), Version(1, 7, 6), False),
        (Version(1, 7, 6, "pre1"), Version(1, 7, 6, "pre2"), False),
        (Version(1, 7, 6, "pre1", "build1"), Version(1, 7, 6, "pre1", "build2"), False),
        (Version(1, 7, 6, None, "build1"), Version(1, 7, 6, None, "build2"), False),
        (Version(1, 7, 6), Version(0, 7, 6), True),
        (Version(1, 7, 6), Version(1, 7, 6), True),
        (Version(1, 7, 6), Version(1, 6, 6), True),
        (Version(1, 7, 6), Version(1, 7, 5), True),
        (Version(1, 7, 6), Version(1, 7, 6, "pre"), True),
        (Version(1, 7, 6), Version(1, 7, 6, "pre", "build"), True),
        (Version(1, 7, 6, "pre2"), Version(1, 7, 6, "pre1"), True),
        (Version(1, 7, 6, "pre2", "build2"), Version(1, 7, 6, "pre1", "build1"), True),
        (Version(1, 7, 6, None, "build2"), Version(1, 7, 6, None, "build1"), True),
    ],
)
def test_version_ge(v1: Version, v2: Version, want: bool):
    assert (v1 >= v2) is want


def test_version_ge_invalid_type():
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        v >= "a string"


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(1, 0, 0, "equal"), Version(1, 0, 0, "equal"), 0),
        (Version(1, 0, 0, "pre1"), Version(1, 0, 0, "hello1"), 0),
        (Version(1, 0, 0, "pre"), Version(1, 0, 0), -1),
        (Version(1, 0, 0), Version(1, 0, 0, "pre"), 1),
        (Version(1, 0, 0, "pre1"), Version(1, 0, 0, "pre2"), -1),
        (Version(1, 0, 0, "pre2"), Version(1, 0, 0, "pre1"), 1),
    ],
)
def test_compare_prerelease(v1: Version, v2: Version, want: int):
    assert v1._compare_prerelease(v2) == want


def test_compare_prerelease_raises_if_no_digits():
    v1 = Version(1, 0, 0, "pre")
    v2 = Version(1, 0, 0, "prepre")

    with pytest.raises(ValueError):
        v1._compare_prerelease(v2)


def test_compare_prerelease_raises_if_multiple_digits():
    v1 = Version(1, 0, 0, "pre3")
    v2 = Version(1, 0, 0, "pre3version4")

    with pytest.raises(ValueError):
        v1._compare_prerelease(v2)


def test_compare_prerelease_raises_at_the_end():
    v1 = Version(1, 0, 0, "cantcompareme")
    v2 = Version(1, 0, 0, "orme")

    with pytest.raises(ValueError):
        v1._compare_prerelease(v2)


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(1, 0, 0, None, "equal"), Version(1, 0, 0, None, "equal"), 0),
        (Version(1, 0, 0, None, "build1"), Version(1, 0, 0, None, "hello1"), 0),
        (Version(1, 0, 0, None, "build"), Version(1, 0, 0), -1),
        (Version(1, 0, 0), Version(1, 0, 0, None, "build"), 1),
        (Version(1, 0, 0, None, "build1"), Version(1, 0, 0, None, "build2"), -1),
        (Version(1, 0, 0, None, "build2"), Version(1, 0, 0, None, "build1"), 1),
    ],
)
def test_compare_build(v1: Version, v2: Version, want: int):
    assert v1._compare_build(v2) == want


def test_compare_build_raises_if_no_digits():
    v1 = Version(1, 0, 0, None, "build")
    v2 = Version(1, 0, 0, None, "buildybuild")

    with pytest.raises(ValueError):
        v1._compare_build(v2)


def test_compare_build_raises_if_multiple_digits():
    v1 = Version(1, 0, 0, None, "build3")
    v2 = Version(1, 0, 0, None, "build1ver4")

    with pytest.raises(ValueError):
        v1._compare_build(v2)


def test_compare_build_raises_at_the_end():
    v1 = Version(1, 0, 0, None, "cantcompareme")
    v2 = Version(1, 0, 0, None, "orme")

    with pytest.raises(ValueError):
        v1._compare_build(v2)
