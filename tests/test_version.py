"""
Tests for the Version class.
"""

from __future__ import annotations

import pytest
from madonna import Version
from madonna.version import VersionDict, VersionTuple


def test_version_init() -> None:
    v = Version(1, 2, 4, "rc.1", "build.123")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 4
    assert v.prerelease == "rc.1"
    assert v.buildmetadata == "build.123"


def test_version_repr() -> None:
    v = Version(1, 2, 4, "rc.1", "build.123")
    want = "Version(major=1, minor=2, patch=4, prerelease='rc.1', buildmetadata='build.123')"
    assert repr(v) == want


def test_version_hash() -> None:
    v = Version(1, 2, 4, "rc.1", "build.123")
    want = hash(v.to_tuple())
    assert hash(v) == want


@pytest.mark.parametrize(
    ("major", "minor", "patch"),
    [
        (-1, 2, 4),
        (1, -2, 4),
        (1, 2, -4),
    ],
)
def test_version_raises_less_than_zero(major: int, minor: int, patch: int) -> None:
    with pytest.raises(ValueError):
        Version(major, minor, patch)


@pytest.mark.parametrize(
    ("version", "string"),
    [
        (Version(1, 2, 4, None, None), "v1.2.4"),
        (Version(1, 2, 4), "v1.2.4"),
        (Version(2, 6, 8, "rc.2", None), "v2.6.8-rc.2"),
        (Version(2, 6, 8, "rc.2"), "v2.6.8-rc.2"),
        (Version(7, 6, 2, None, "build.123"), "v7.6.2+build.123"),
        (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1+build.123"),
    ],
)
def _(version: Version, string: str) -> None:
    assert str(version) == string


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
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
def test_version_eq(v1: Version, v2: Version, want: bool) -> None:
    assert (v1 == v2) is want


def test_eq_notimplemented() -> None:
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        assert v == "a string"


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
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
def _(v1: Version, v2: Version, want: bool) -> None:
    assert (v1 != v2) == want


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
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
def test_lt(v1: Version, v2: Version, want: bool) -> None:
    assert (v1 < v2) is want


def test_lt_notimplemented() -> None:
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        assert v < "a string"


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
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
def test_le(v1: Version, v2: Version, want: bool) -> None:
    assert (v1 <= v2) is want


def test_le_notimplemented() -> None:
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        assert v <= "a string"


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
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
def test_gt(v1: Version, v2: Version, want: bool) -> None:
    assert (v1 > v2) is want


def test_gt_notimplemented() -> None:
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        assert v > "a string"


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
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
def test_ge(v1: Version, v2: Version, want: bool) -> None:
    assert (v1 >= v2) is want


def test_ge_notimplemented() -> None:
    v = Version(1, 2, 4)

    with pytest.raises(TypeError):
        assert v >= "a string"


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
    [
        (Version(1, 0, 0, "equal"), Version(1, 0, 0, "equal"), 0),
        (Version(1, 0, 0, "pre1"), Version(1, 0, 0, "hello1"), 0),
        (Version(1, 0, 0, "pre"), Version(1, 0, 0), -1),
        (Version(1, 0, 0), Version(1, 0, 0, "pre"), 1),
        (Version(1, 0, 0, "pre1"), Version(1, 0, 0, "pre2"), -1),
        (Version(1, 0, 0, "pre2"), Version(1, 0, 0, "pre1"), 1),
    ],
)
def test_compare_prerelease(v1: Version, v2: Version, want: int) -> None:
    assert v1._compare_prerelease(v2) == want


def test_cmp_prerelease_raises_on_non_numeric() -> None:
    v1 = Version(1, 0, 0, "pre")
    v2 = Version(1, 0, 0, "prepre")

    with pytest.raises(ValueError):
        v1._compare_prerelease(v2)


def test_cmp_prerelease_raises_on_multiple_digits() -> None:
    v1 = Version(1, 0, 0, "pre3")
    v2 = Version(1, 0, 0, "pre3version4")

    with pytest.raises(ValueError):
        v1._compare_prerelease(v2)


def test_cmp_prerelease_rasies_if_cant_compare() -> None:
    v1 = Version(1, 0, 0, "cantcompareme")
    v2 = Version(1, 0, 0, "orme")

    with pytest.raises(ValueError):
        v1._compare_prerelease(v2)


@pytest.mark.parametrize(
    ("v1", "v2", "want"),
    [
        (Version(1, 0, 0, None, "equal"), Version(1, 0, 0, None, "equal"), 0),
        (Version(1, 0, 0, None, "build1"), Version(1, 0, 0, None, "hello1"), 0),
        (Version(1, 0, 0, None, "build"), Version(1, 0, 0), -1),
        (Version(1, 0, 0), Version(1, 0, 0, None, "build"), 1),
        (Version(1, 0, 0, None, "build1"), Version(1, 0, 0, None, "build2"), -1),
        (Version(1, 0, 0, None, "build2"), Version(1, 0, 0, None, "build1"), 1),
    ],
)
def test_compare_build(v1: Version, v2: Version, want: int) -> None:
    assert v1._compare_build(v2) == want


def test_cmp_build_raises_on_non_numeric() -> None:
    v1 = Version(1, 0, 0, None, "build")
    v2 = Version(1, 0, 0, None, "buildybuild")

    with pytest.raises(ValueError):
        v1._compare_build(v2)


def test_cmp_build_raises_on_multiple_digits() -> None:
    v1 = Version(1, 0, 0, None, "build3")
    v2 = Version(1, 0, 0, None, "build1ver4")

    with pytest.raises(ValueError):
        v1._compare_build(v2)


def test_cmp_build_raises_if_cant_compare() -> None:
    v1 = Version(1, 0, 0, None, "cantcompareme")
    v2 = Version(1, 0, 0, None, "orme")

    with pytest.raises(ValueError):
        v1._compare_build(v2)


@pytest.mark.parametrize(
    ("original", "bumped"),
    [
        (Version(1, 2, 4), Version(2, 0, 0)),
        (Version(0, 0, 1), Version(1, 0, 0)),
        (Version(0, 0, 0), Version(1, 0, 0)),
        (Version(0, 7, 6, "pre"), Version(1, 0, 0)),
        (Version(0, 7, 6, "pre", "build"), Version(1, 0, 0)),
        (Version(999999, 999, 9999, "holy_crap"), Version(1000000, 0, 0)),
    ],
)
def test_bump_major(original: Version, bumped: Version) -> None:
    assert original.bump_major() == bumped


@pytest.mark.parametrize(
    ("original", "bumped"),
    [
        (Version(1, 2, 4), Version(1, 3, 0)),
        (Version(0, 0, 1), Version(0, 1, 0)),
        (Version(0, 0, 0), Version(0, 1, 0)),
        (Version(0, 7, 6, "pre"), Version(0, 8, 0)),
        (Version(0, 7, 6, "pre", "build"), Version(0, 8, 0)),
        (Version(999999, 999, 9999, "holy_crap"), Version(999999, 1000, 0)),
    ],
)
def test_bump_minor(original: Version, bumped: Version) -> None:
    assert original.bump_minor() == bumped


@pytest.mark.parametrize(
    ("original", "bumped"),
    [
        (Version(1, 2, 4), Version(1, 2, 5)),
        (Version(0, 0, 1), Version(0, 0, 2)),
        (Version(0, 0, 0), Version(0, 0, 1)),
        (Version(0, 7, 6, "pre"), Version(0, 7, 7)),
        (Version(0, 7, 6, "pre", "build"), Version(0, 7, 7)),
        (Version(999999, 999, 9999, "holy_crap"), Version(999999, 999, 10000)),
    ],
)
def test_bump_patch(original: Version, bumped: Version) -> None:
    assert original.bump_patch() == bumped


@pytest.mark.parametrize(
    ("version", "want"),
    [
        (Version(1, 2, 4, None, None), "v1.2.4"),
        (Version(1, 2, 4), "v1.2.4"),
        (Version(2, 6, 8, "rc.2", None), "v2.6.8-rc.2"),
        (Version(2, 6, 8, "rc.2"), "v2.6.8-rc.2"),
        (Version(7, 6, 2, None, "build.123"), "v7.6.2+build.123"),
        (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1+build.123"),
    ],
)
def test_version_to_string(version: Version, want: str) -> None:
    assert version.to_string() == want


@pytest.mark.parametrize(
    ("version", "want"),
    [
        (Version(1, 2, 4), (1, 2, 4, None, None)),
        (Version(1, 2, 4, "rc.1"), (1, 2, 4, "rc.1", None)),
        (Version(1, 2, 4, "rc.3", "build.8"), (1, 2, 4, "rc.3", "build.8")),
    ],
)
def test_version_to_tuple(version: Version, want: VersionTuple) -> None:
    assert version.to_tuple() == want


@pytest.mark.parametrize(
    ("version", "want"),
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
def test_version_to_dict(version: Version, want: VersionDict) -> None:
    assert version.to_dict() == want


@pytest.mark.parametrize(
    ("version", "want"),
    [
        (
            Version(1, 2, 4),
            ('{"major": 1, "minor": 2, "patch": 4, "prerelease": null,' ' "buildmetadata": null}'),
        ),
        (
            Version(1, 2, 4, "rc.1", "build.2"),
            ('{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1",' ' "buildmetadata": "build.2"}'),
        ),
    ],
)
def test_version_to_json(version: Version, want: str) -> None:
    assert version.to_json() == want


@pytest.mark.parametrize(
    ("version", "want"),
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
def test_is_valid(version: Version, want: bool) -> None:
    assert version.is_valid() is want


@pytest.mark.parametrize(
    ("d", "want"),
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
def test_from_dict(d: VersionDict, want: Version) -> None:
    assert Version.from_dict(d) == want


@pytest.mark.parametrize(
    ("string", "want"),
    [
        ("v1.2.3", Version(1, 2, 3)),
        ("1.2.3", Version(1, 2, 3)),
        ("v1.2.3-rc.1", Version(1, 2, 3, "rc.1")),
        ("v1.2.3-rc.1+build.123", Version(1, 2, 3, "rc.1", "build.123")),
    ],
)
def _(string: str, want: Version) -> None:
    assert Version.from_string(string) == want


def test_from_string_raises_if_invalid() -> None:
    with pytest.raises(ValueError):
        Version.from_string("I'm not a version")


@pytest.mark.parametrize("string", ["v1.2.4", "v1.2.4-rc.1", "v1.2.4-rc.1+build.123"])
def test_to_string_from_string_round_trip(string: str) -> None:
    assert Version.from_string(string).to_string() == string


@pytest.mark.parametrize(
    (("tup", "want")),
    [
        ((1, 2, 4), Version(1, 2, 4)),
        ((1, 2, 4, "rc.1"), Version(1, 2, 4, "rc.1")),
        ((1, 2, 4, "rc.1", "build.123"), Version(1, 2, 4, "rc.1", "build.123")),
    ],
)
def test_from_tuple(tup: VersionTuple, want: Version) -> None:
    assert Version.from_tuple(tup) == want


@pytest.mark.parametrize(
    ("json_string", "want"),
    [
        ('{"major": 1, "minor": 2, "patch": 4}', Version(1, 2, 4)),
        (
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1"}',
            Version(1, 2, 4, "rc.1"),
        ),
        (
            ('{"major": 1, "minor": 2, "patch": 4, "prerelease":' ' "rc.1","buildmetadata": "build.2"}'),
            Version(1, 2, 4, "rc.1", "build.2"),
        ),
    ],
)
def test_from_json(json_string: str, want: Version) -> None:
    assert Version.from_json(json_string) == want
