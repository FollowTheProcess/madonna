from ward import raises, test

from madonna import Version
from madonna.version import VersionDict, VersionTuple


@test("version instantiation")
def _():
    v = Version(1, 2, 4, "rc.1", "build.123")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 4
    assert v.prerelease == "rc.1"
    assert v.buildmetadata == "build.123"


@test("version repr is correct")
def _():
    v = Version(1, 2, 4, "rc.1", "build.123")
    want = (
        "Version(major=1, minor=2, patch=4, prerelease='rc.1',"
        " buildmetadata='build.123')"
    )
    assert repr(v) == want


@test("version hash is correct")
def _():
    v = Version(1, 2, 4, "rc.1", "build.123")
    want = hash(v.to_tuple())
    assert hash(v) == want


for major, minor, patch in [
    (-1, 2, 4),
    (1, -2, 4),
    (1, 2, -4),
]:

    @test("version raises if any numeric part < 0")
    def _(major: int = major, minor: int = minor, patch: int = patch):
        with raises(ValueError):
            Version(major, minor, patch)


for version, string in [
    (Version(1, 2, 4, None, None), "v1.2.4"),
    (Version(1, 2, 4), "v1.2.4"),
    (Version(2, 6, 8, "rc.2", None), "v2.6.8-rc.2"),
    (Version(2, 6, 8, "rc.2"), "v2.6.8-rc.2"),
    (Version(7, 6, 2, None, "build.123"), "v7.6.2+build.123"),
    (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1+build.123"),
]:

    @test("version string representation is correct")
    def _(version: Version = version, string: str = string):
        assert str(version) == string


for v1, v2, want in [
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
]:

    @test("version __eq__ is correct")
    def _(v1: Version = v1, v2: Version = v2, want: bool = want):
        assert (v1 == v2) is want


@test("version __eq__ returns NotImplemented on anything other than a Version")
def _():
    v = Version(1, 2, 4)

    with raises(TypeError):
        assert v == "a string"


for v1, v2, want in [
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
]:

    @test("version __ne__ is correct")
    def _(v1: Version = v1, v2: Version = v2, want: bool = want):
        assert (v1 != v2) == want


for v1, v2, want in [
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
]:

    @test("version __lt__ is correct")
    def _(v1: Version = v1, v2: Version = v2, want: bool = want):
        assert (v1 < v2) is want


@test("version __lt__ raises on anything other than a Version")
def _():
    v = Version(1, 2, 4)

    with raises(TypeError):
        assert v < "a string"


for v1, v2, want in [
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
]:

    @test("version __le__ is correct")
    def _(v1: Version = v1, v2: Version = v2, want: bool = want):
        assert (v1 <= v2) is want


@test("version __lt__ raises on anything other than a Version")
def _():
    v = Version(1, 2, 4)

    with raises(TypeError):
        assert v <= "a string"


for v1, v2, want in [
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
]:

    @test("version __gt__ is correct")
    def _(v1: Version = v1, v2: Version = v2, want: bool = want):
        assert (v1 > v2) is want


@test("version __gt__ raises on anything other than a Version")
def _():
    v = Version(1, 2, 4)

    with raises(TypeError):
        assert v > "a string"


for v1, v2, want in [
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
]:

    @test("version __ge__ is correct")
    def _(v1: Version = v1, v2: Version = v2, want: bool = want):
        assert (v1 >= v2) is want


@test("version __ge__ raises on anything other than a Version")
def _():
    v = Version(1, 2, 4)

    with raises(TypeError):
        assert v >= "a string"


for v1, v2, want in [
    (Version(1, 0, 0, "equal"), Version(1, 0, 0, "equal"), 0),
    (Version(1, 0, 0, "pre1"), Version(1, 0, 0, "hello1"), 0),
    (Version(1, 0, 0, "pre"), Version(1, 0, 0), -1),
    (Version(1, 0, 0), Version(1, 0, 0, "pre"), 1),
    (Version(1, 0, 0, "pre1"), Version(1, 0, 0, "pre2"), -1),
    (Version(1, 0, 0, "pre2"), Version(1, 0, 0, "pre1"), 1),
]:

    @test("compare prerelease is correct")
    def _(v1: Version = v1, v2: Version = v2, want: int = want):
        assert v1._compare_prerelease(v2) == want


@test("compare prerelease raises if it can't find numeric digits")
def _():
    v1 = Version(1, 0, 0, "pre")
    v2 = Version(1, 0, 0, "prepre")

    with raises(ValueError):
        v1._compare_prerelease(v2)


@test("compare prerelease raises if there are multiple digits")
def _():
    v1 = Version(1, 0, 0, "pre3")
    v2 = Version(1, 0, 0, "pre3version4")

    with raises(ValueError):
        v1._compare_prerelease(v2)


@test("compare prerelease raises if all checks were inconclusive")
def _():
    v1 = Version(1, 0, 0, "cantcompareme")
    v2 = Version(1, 0, 0, "orme")

    with raises(ValueError):
        v1._compare_prerelease(v2)


for v1, v2, want in [
    (Version(1, 0, 0, None, "equal"), Version(1, 0, 0, None, "equal"), 0),
    (Version(1, 0, 0, None, "build1"), Version(1, 0, 0, None, "hello1"), 0),
    (Version(1, 0, 0, None, "build"), Version(1, 0, 0), -1),
    (Version(1, 0, 0), Version(1, 0, 0, None, "build"), 1),
    (Version(1, 0, 0, None, "build1"), Version(1, 0, 0, None, "build2"), -1),
    (Version(1, 0, 0, None, "build2"), Version(1, 0, 0, None, "build1"), 1),
]:

    @test("compare build is correct")
    def _(v1: Version = v1, v2: Version = v2, want: int = want):
        assert v1._compare_build(v2) == want


@test("compare prerelease raises if it can't find numeric digits")
def _():
    v1 = Version(1, 0, 0, None, "build")
    v2 = Version(1, 0, 0, None, "buildybuild")

    with raises(ValueError):
        v1._compare_build(v2)


@test("compare build raises if there are multiple digits")
def _():
    v1 = Version(1, 0, 0, None, "build3")
    v2 = Version(1, 0, 0, None, "build1ver4")

    with raises(ValueError):
        v1._compare_build(v2)


@test("compare build raises if all checks were inconclusive")
def _():
    v1 = Version(1, 0, 0, None, "cantcompareme")
    v2 = Version(1, 0, 0, None, "orme")

    with raises(ValueError):
        v1._compare_build(v2)


for original, bumped in [
    (Version(1, 2, 4), Version(2, 0, 0)),
    (Version(0, 0, 1), Version(1, 0, 0)),
    (Version(0, 0, 0), Version(1, 0, 0)),
    (Version(0, 7, 6, "pre"), Version(1, 0, 0)),
    (Version(0, 7, 6, "pre", "build"), Version(1, 0, 0)),
    (Version(999999, 999, 9999, "holy_crap"), Version(1000000, 0, 0)),
]:

    @test("bump_major is correct")
    def _(original: Version = original, bumped: Version = bumped):
        assert original.bump_major() == bumped


for original, bumped in [
    (Version(1, 2, 4), Version(1, 3, 0)),
    (Version(0, 0, 1), Version(0, 1, 0)),
    (Version(0, 0, 0), Version(0, 1, 0)),
    (Version(0, 7, 6, "pre"), Version(0, 8, 0)),
    (Version(0, 7, 6, "pre", "build"), Version(0, 8, 0)),
    (Version(999999, 999, 9999, "holy_crap"), Version(999999, 1000, 0)),
]:

    @test("bump_minor is correct")
    def _(original: Version = original, bumped: Version = bumped):
        assert original.bump_minor() == bumped


for original, bumped in [
    (Version(1, 2, 4), Version(1, 2, 5)),
    (Version(0, 0, 1), Version(0, 0, 2)),
    (Version(0, 0, 0), Version(0, 0, 1)),
    (Version(0, 7, 6, "pre"), Version(0, 7, 7)),
    (Version(0, 7, 6, "pre", "build"), Version(0, 7, 7)),
    (Version(999999, 999, 9999, "holy_crap"), Version(999999, 999, 10000)),
]:

    @test("bump_patch is correct")
    def _(original: Version = original, bumped: Version = bumped):
        assert original.bump_patch() == bumped


for version, want in [
    (Version(1, 2, 4, None, None), "v1.2.4"),
    (Version(1, 2, 4), "v1.2.4"),
    (Version(2, 6, 8, "rc.2", None), "v2.6.8-rc.2"),
    (Version(2, 6, 8, "rc.2"), "v2.6.8-rc.2"),
    (Version(7, 6, 2, None, "build.123"), "v7.6.2+build.123"),
    (Version(7, 2, 1, "rc.1", "build.123"), "v7.2.1-rc.1+build.123"),
]:

    @test("version.to_string() is correct")
    def _(version: Version = version, want: str = want):
        assert version.to_string() == want


for version, want in [
    (Version(1, 2, 4), (1, 2, 4, None, None)),
    (Version(1, 2, 4, "rc.1"), (1, 2, 4, "rc.1", None)),
    (Version(1, 2, 4, "rc.3", "build.8"), (1, 2, 4, "rc.3", "build.8")),
]:

    @test("version.to_tuple() is correct")
    def _(version: Version = version, want: VersionTuple = want):
        assert version.to_tuple() == want


for version, want in [
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
]:

    @test("version.to_dict() is correct")
    def _(version: Version = version, want: VersionDict = want):
        assert version.to_dict() == want


for version, want in [
    (
        Version(1, 2, 4),
        (
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": null, "buildmetadata":'
            " null}"
        ),
    ),
    (
        Version(1, 2, 4, "rc.1", "build.2"),
        (
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1",'
            ' "buildmetadata": "build.2"}'
        ),
    ),
]:

    @test("version.to_json() is correct")
    def _(version: Version = version, want: str = want):
        assert version.to_json() == want


for version, want in [
    (Version(1, 2, 4), True),
    (Version(1, 2, 3, "pre"), True),
    (Version(1, 2, 4, "pre", "build"), True),
    (Version(8, 2, 3, "rc.1", "build.123"), True),
    (Version(1, 0, 0, "alpha-a.b-c-somethinglong", "build.1-aef.1-its-okay"), True),
    (Version(1, 2, 3, "ajbas---28", "lnq==2987"), False),
    (Version(1, 2, 4, "blah198y_+-2-", "build---19790"), False),
]:

    @test("version.is_valid() is correct")
    def _(version: Version = version, want: bool = want):
        assert version.is_valid() is want


for d, want in [
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
]:

    @test("version.from_dict() is correct")
    def _(d: VersionDict = d, want: Version = want):
        assert Version.from_dict(d) == want


for string, want in [
    ("v1.2.3", Version(1, 2, 3)),
    ("1.2.3", Version(1, 2, 3)),
    ("v1.2.3-rc.1", Version(1, 2, 3, "rc.1")),
    ("v1.2.3-rc.1+build.123", Version(1, 2, 3, "rc.1", "build.123")),
]:

    @test("version.from_string() is correct")
    def _(string: str = string, want: Version = want):
        assert Version.from_string(string) == want


@test("version.from_string() raises on an invalid semver string")
def _():
    with raises(ValueError):
        Version.from_string("I'm not a version")


for string in ["v1.2.4", "v1.2.4-rc.1", "v1.2.4-rc.1+build.123"]:

    @test("version.to_string() -> version.from_string() round trip")
    def _(string: str = string):
        assert Version.from_string(string).to_string() == string


for tup, want in [
    ((1, 2, 4), Version(1, 2, 4)),
    ((1, 2, 4, "rc.1"), Version(1, 2, 4, "rc.1")),
    ((1, 2, 4, "rc.1", "build.123"), Version(1, 2, 4, "rc.1", "build.123")),
]:

    @test("version.from_tuple() is correct")
    def _(tup: VersionTuple = tup, want: Version = want):
        assert Version.from_tuple(tup) == want


for json_string, want in [
    ('{"major": 1, "minor": 2, "patch": 4}', Version(1, 2, 4)),
    (
        '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1"}',
        Version(1, 2, 4, "rc.1"),
    ),
    (
        (
            '{"major": 1, "minor": 2, "patch": 4, "prerelease": "rc.1","buildmetadata":'
            ' "build.2"}'
        ),
        Version(1, 2, 4, "rc.1", "build.2"),
    ),
]:

    @test("version.from_json() is correct")
    def _(json_string: str = json_string, want: Version = want):
        assert Version.from_json(json_string) == want
