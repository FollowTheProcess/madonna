"""
Core semantic version functionality.

Author: Tom Fleet
Created: 08/10/2021
"""

from __future__ import annotations

import re
from typing import Optional


class Version:
    def __init__(
        self,
        major: int,
        minor: int,
        patch: int,
        prerelease: Optional[str] = None,
        buildmetadata: Optional[str] = None,
    ) -> None:
        """
        A data container for a semantic version.

        Args:
            major (int): The major version, to be incremented when making
                backwards incompatible (breaking) changes.
            minor (int): The minor version, to be incremented when introducing
                backwards compatible features.
            patch (int): The patch version, to be incremented when making
                backwards compatible bug fixes.
            prerelease (Optional[str], optional): Any pre-release tags
                e.g. 'rc.1'. Defaults to None.
            buildmetadata (Optional[str], optional): Any build meta tags
                e.g. 'build.123'. Defaults to None.

        Raises:
            ValueError: If any numeric version part < 0.
        """
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.buildmetadata = buildmetadata

        if any(part < 0 for part in (self.major, self.minor, self.patch)):
            raise ValueError(
                f"Version {self!r} is invalid. Parts cannot be less than 0."
            )

    def __repr__(self) -> str:
        return (
            self.__class__.__qualname__
            + f"(major={self.major!r}, minor={self.minor!r}, patch={self.patch!r}, "
            + f"prerelease={self.prerelease!r}, buildmetadata={self.buildmetadata!r})"
        )

    def __str__(self) -> str:
        ver = f"v{self.major}.{self.minor}.{self.patch}"

        if self.prerelease:
            ver += f"-{self.prerelease}"

        if self.buildmetadata:
            ver += f"-{self.buildmetadata}"

        return ver

    def __lt__(self, v: Version) -> bool:
        if not isinstance(v, Version):
            raise NotImplementedError(
                f"Cannot compare object of type Version and {type(v)}"
            )

        diff = (self.major, self.minor, self.patch) < (v.major, v.minor, v.patch)
        if diff:
            # If the numeric versions are less, return True straight away
            return True

        # If our version has a pre-release and the other doesn't
        # ours is less
        if self.prerelease and not v.prerelease:
            return True

        # If our version has a build tag and the other doesn't
        # ours is less
        if self.buildmetadata and not v.buildmetadata:
            return True

        # If our version has a prerelease of e.g. 'rc.1' and other
        # has e.g. 'rc.2', ours is less
        if self.prerelease and v.prerelease:
            our_rc = re.match(pattern=r"rc.(?P<rc_ver>\d+)", string=self.prerelease)
            other_rc = re.match(pattern=r"rc.(?P<rc_ver>\d+)", string=v.prerelease)

            if not our_rc or not other_rc:

                return False

            our_rc_ver = int(our_rc.group("rc_ver"))
            other_rc_ver = int(other_rc.group("rc_ver"))

            if our_rc_ver < other_rc_ver:
                return True

        # If our version has a build of e.g. 'build.123' and other
        # has e.g. 'build.456', ours is less
        if self.buildmetadata and v.buildmetadata:
            our_build = re.match(
                pattern=r"build.(?P<build_ver>\d+)", string=self.buildmetadata
            )
            other_build = re.match(
                pattern=r"build.(?P<build_ver>\d+)", string=v.buildmetadata
            )

            if not our_build or not other_build:

                return False

            our_build_ver = int(our_build.group("build_ver"))
            other_build_ver = int(other_build.group("build_ver"))

            if our_build_ver < other_build_ver:
                return True

        # We've exhausted every scenario we know how to compare
        return False
