"""
Tests for the core functionality.

Author: Tom Fleet
Created: 09/10/2021
"""


import pytest

from madonna import Version
from madonna.version import VersionDict, VersionTuple


def test_version_init():
    v = Version(1, 2, 4, "rc.1", "build.123")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 4
    assert v.prerelease == "rc.1"
    assert v.buildmetadata == "build.123"


def test_version_repr():
    v = Version(1, 2, 4, "rc.1", "build.123")
    want = (
        "Version(major=1, minor=2, patch=4, prerelease='rc.1',"
        " buildmetadata='build.123')"
    )
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
        (Version(7, 6, 2, None, "build.123"), "v7.6.2+build.123"),
        (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1+build.123"),
    ],
)
def test_version_str(version: Version, want: str):
    assert str(version) == want


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(1, 2, 3), Version(1, 2, 3), True),
        (Version(1, 2, 3, "pre"), Version(1, 2, 3, "pre"), True),
        (Version(1, 2, 3, "pre", "build"), Version(1, 2, 3, "pre", "build"), True),
        (Version(1, 2, 3, None, None), Version(1, 2, 3, None, None), True),
        (Version(0, 2, 3), Version(1, 2, 3), False),
        (Version(1, 1, 3), Version(1, 2, 3), False),
        (Version(1, 2, 2), Version(1, 2, 3), False),
        (Version(1, 2, 3, "pre"), Version(1, 2, 3), False),
        (Version(1, 2, 3, None, "build"), Version(1, 2, 3, None, None), False),
        (
            Version(1, 2, 3, "pre", "build"),
            Version(1, 2, 3, "diffpre", "diffbuild"),
            False,
        ),
    ],
)
def test_version_eq(v1: Version, v2: Version, want: bool):
    assert (v1 == v2) is want


def test_version_eq_invalid_type():
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        v == "a string"


@pytest.mark.parametrize(
    "v1, v2, want",
    [
        (Version(1, 2, 3), Version(1, 2, 3), False),
        (Version(1, 2, 3, "pre"), Version(1, 2, 3, "pre"), False),
        (Version(1, 2, 3, "pre", "build"), Version(1, 2, 3, "pre", "build"), False),
        (Version(1, 2, 3, None, None), Version(1, 2, 3, None, None), False),
        (Version(0, 2, 3), Version(1, 2, 3), True),
        (Version(1, 1, 3), Version(1, 2, 3), True),
        (Version(1, 2, 2), Version(1, 2, 3), True),
        (Version(1, 2, 3, "pre"), Version(1, 2, 3), True),
        (Version(1, 2, 3, None, "build"), Version(1, 2, 3, None, None), True),
        (
            Version(1, 2, 3, "pre", "build"),
            Version(1, 2, 3, "diffpre", "diffbuild"),
            True,
        ),
    ],
)
def test_version_ne(v1: Version, v2: Version, want: bool):
    assert (v1 != v2) is want


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


@pytest.mark.parametrize(
    "v, want",
    [
        (Version(1, 2, 4), Version(2, 0, 0)),
        (Version(0, 0, 1), Version(1, 0, 0)),
        (Version(0, 0, 0), Version(1, 0, 0)),
        (Version(0, 7, 6, "pre"), Version(1, 0, 0)),
        (Version(0, 7, 6, "pre", "build"), Version(1, 0, 0)),
        (Version(999999, 999, 9999, "holy_crap"), Version(1000000, 0, 0)),
    ],
)
def test_bump_major(v: Version, want: Version):
    assert v.bump_major() == want


@pytest.mark.parametrize(
    "v, want",
    [
        (Version(1, 2, 4), Version(1, 3, 0)),
        (Version(0, 0, 1), Version(0, 1, 0)),
        (Version(0, 0, 0), Version(0, 1, 0)),
        (Version(0, 7, 6, "pre"), Version(0, 8, 0)),
        (Version(0, 7, 6, "pre", "build"), Version(0, 8, 0)),
        (Version(999999, 999, 9999, "holy_crap"), Version(999999, 1000, 0)),
    ],
)
def test_bump_minor(v: Version, want: Version):
    assert v.bump_minor() == want


@pytest.mark.parametrize(
    "v, want",
    [
        (Version(1, 2, 4), Version(1, 2, 5)),
        (Version(0, 0, 1), Version(0, 0, 2)),
        (Version(0, 0, 0), Version(0, 0, 1)),
        (Version(0, 7, 6, "pre"), Version(0, 7, 7)),
        (Version(0, 7, 6, "pre", "build"), Version(0, 7, 7)),
        (Version(999999, 999, 9999, "holy_crap"), Version(999999, 999, 10000)),
    ],
)
def test_bump_patch(v: Version, want: Version):
    assert v.bump_patch() == want


@pytest.mark.parametrize(
    "version, want",
    [
        (Version(1, 2, 4, None, None), "v1.2.4"),
        (Version(1, 2, 4), "v1.2.4"),
        (Version(2, 6, 8, "rc.2", None), "v2.6.8-rc.2"),
        (Version(2, 6, 8, "rc.2"), "v2.6.8-rc.2"),
        (Version(7, 6, 2, None, "build.123"), "v7.6.2+build.123"),
        (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1+build.123"),
    ],
)
def test_version_to_string(version: Version, want: str):
    assert version.to_string() == want


@pytest.mark.parametrize(
    "version, want",
    [
        (Version(1, 2, 4), (1, 2, 4, None, None)),
        (Version(1, 2, 4, "rc.1"), (1, 2, 4, "rc.1", None)),
        (Version(1, 2, 4, "rc.3", "build.8"), (1, 2, 4, "rc.3", "build.8")),
    ],
)
def test_version_to_tuple(version: Version, want: VersionTuple):
    assert version.to_tuple() == want


@pytest.mark.parametrize(
    "version, want",
    [
        (
            Version(1, 2, 4),
            {
                "major": 1,
                "minor": 2,
                "patch": 4,
                "prerelease": None,
                "buildmetadata": None,
            },
        ),
        (
            Version(1, 2, 4, "rc.1"),
            {
                "major": 1,
                "minor": 2,
                "patch": 4,
                "prerelease": "rc.1",
                "buildmetadata": None,
            },
        ),
        (
            Version(1, 2, 4, "rc.1", "build.123"),
            {
                "major": 1,
                "minor": 2,
                "patch": 4,
                "prerelease": "rc.1",
                "buildmetadata": "build.123",
            },
        ),
    ],
)
def test_version_to_dict(version: Version, want: VersionDict):
    assert version.to_dict() == want


@pytest.mark.parametrize(
    "version, want",
    [
        (
            Version(1, 2, 4),
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": null, "buildmetadata":'
            " null}",
        ),
        (
            Version(1, 2, 4, "rc.1", "build.2"),
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1",'
            ' "buildmetadata": "build.2"}',
        ),
    ],
)
def test_version_to_json(version: Version, want: str):
    assert version.to_json() == want


@pytest.mark.parametrize(
    "version, want",
    [
        (Version(1, 2, 4), True),
        (Version(1, 2, 3, "pre"), True),
        (Version(1, 2, 4, "pre", "build"), True),
        (Version(8, 2, 3, "rc.1", "build.123"), True),
        (Version(1, 0, 0, "alpha-a.b-c-somethinglong", "build.1-aef.1-its-okay"), True),
        (Version(1, 2, 3, "ajbas---28", "lnq==2987"), False),
        (Version(1, 2, 4, "blah198y_+-2-", "build---19790"), False),
    ],
)
def test_version_is_valid(version: Version, want: bool):
    assert version.is_valid() is want


@pytest.mark.parametrize(
    "d, want",
    [
        (
            {
                "major": 7,
                "minor": 2,
                "patch": 6,
            },
            Version(7, 2, 6),
        ),
        (
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "prerelease": "rc.1",
            },
            Version(1, 2, 3, "rc.1"),
        ),
        (
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "prerelease": "rc.1",
                "buildmetadata": "build.123",
            },
            Version(1, 2, 3, "rc.1", "build.123"),
        ),
    ],
)
def test_version_from_dict(d: VersionDict, want: Version):
    assert Version.from_dict(d) == want


@pytest.mark.parametrize(
    "string, want",
    [
        ("v1.2.3", Version(1, 2, 3)),
        ("1.2.3", Version(1, 2, 3)),
        ("v1.2.3-rc.1", Version(1, 2, 3, "rc.1")),
        ("v1.2.3-rc.1+build.123", Version(1, 2, 3, "rc.1", "build.123")),
    ],
)
def test_version_from_string(string: str, want: Version):
    assert Version.from_string(string) == want


def test_version_from_string_raises_on_bad_string():
    bad = "i'm not a version"

    with pytest.raises(ValueError):
        Version.from_string(bad)


@pytest.mark.parametrize("string", ["v1.2.4", "v1.2.4-rc.1", "v1.2.4-rc.1+build.123"])
def test_version_from_string_to_string_round_trip(string: str):
    assert Version.from_string(string).to_string() == string


@pytest.mark.parametrize(
    "tup, want",
    [
        ((1, 2, 4), Version(1, 2, 4)),
        ((1, 2, 4, "rc.1"), Version(1, 2, 4, "rc.1")),
        ((1, 2, 4, "rc.1", "build.123"), Version(1, 2, 4, "rc.1", "build.123")),
    ],
)
def test_version_from_tuple(tup: VersionTuple, want: Version):
    assert Version.from_tuple(tup) == want


@pytest.mark.parametrize(
    "json_string, want",
    [
        ('{"major": 1, "minor": 2, "patch": 4}', Version(1, 2, 4)),
        (
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1"}',
            Version(1, 2, 4, "rc.1"),
        ),
        (
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1","buildmetadata":'
            ' "build.2"}',
            Version(1, 2, 4, "rc.1", "build.2"),
        ),
    ],
)
def test_version_from_json(json_string: str, want: Version):
    assert Version.from_json(json_string) == want
