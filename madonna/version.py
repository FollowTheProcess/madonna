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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f"Cannot compare object of type Version and {type(other)}")

        return (
            self.major,
            self.minor,
            self.patch,
            self.prerelease,
            self.buildmetadata,
        ) == (
            other.major,
            other.minor,
            other.patch,
            other.prerelease,
            other.buildmetadata,
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f"Cannot compare object of type Version and {type(other)}")

        if (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        ):
            return True

        pre_release_comp = self._compare_prerelease(other)
        if pre_release_comp == -1:
            return True

        build_comp = self._compare_build(other)
        if build_comp == -1:
            return True

        return False

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f"Cannot compare object of type Version and {type(other)}")

        if (self.major, self.minor, self.patch) > (
            other.major,
            other.minor,
            other.patch,
        ):
            return True

        pre_release_comp = self._compare_prerelease(other)
        if pre_release_comp == 1:
            return True

        build_comp = self._compare_build(other)
        if build_comp == 1:
            return True

        return False

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f"Cannot compare object of type Version and {type(other)}")

        if self == other:
            return True

        if self < other:
            return True

        return False

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise TypeError(f"Cannot compare object of type Version and {type(other)}")

        if self == other:
            return True

        if self > other:
            return True

        return False

    def _compare_prerelease(self, other: Version) -> int:
        """
        Helper to try and compare the pre-release versions.

        It will check for string equality, whether or not
        the different versions have pre-releases, check
        for integers in the text and compare based on them,
        and if none of this works will raise a ValueError.

        Note: This is only called if the numeric version
        is equal.
        """
        if self.prerelease == other.prerelease:
            # The pre release strings are equal
            return 0
        elif self.prerelease and not other.prerelease:
            # Ours has a pre-release but the other doesn't
            # meaning ours is less
            return -1
        elif not self.prerelease and other.prerelease:
            # Ours doesn't have a pre-release but the other
            # does meaning ours is greater
            return 1

        # Try and extract a number to compare
        if self.prerelease and other.prerelease:
            ours = re.findall(pattern=r"\d+", string=self.prerelease)
            others = re.findall(pattern=r"\d+", string=other.prerelease)

            if not ours or not others:
                raise ValueError("Could not parse comparable pre-release version info.")

            if len(ours) > 1 or len(others) > 1:
                raise ValueError("Multiple integers found in pre-release version.")

            our_version = int(ours.pop())
            other_version = int(others.pop())

            if our_version == other_version:
                return 0
            elif our_version > other_version:
                return 1
            elif our_version < other_version:
                return -1

        # If we get here, we couldn't parse the pre-release
        raise ValueError(f"Could not compare {self.prerelease} and {other.prerelease}")

    def _compare_build(self, other: Version) -> int:
        """
        Helper to try and compare the build metadata versions.

        It will check for string equality, whether or not
        the different versions have pre-releases, check
        for integers in the text and compare based on them,
        and if none of this works will raise a ValueError.

        Note: This is only called if both the numeric version
        and the pre-release strings are equal.
        """
        if self.buildmetadata == other.buildmetadata:
            # The pre release strings are equal
            return 0
        elif self.buildmetadata and not other.buildmetadata:
            # Ours has a pre-release but the other doesn't
            # meaning ours is less
            return -1
        elif not self.buildmetadata and other.buildmetadata:
            # Ours doesn't have a pre-release but the other
            # does meaning ours is greater
            return 1

        # Try and extract a number to compare
        if self.buildmetadata and other.buildmetadata:
            ours = re.findall(pattern=r"\d+", string=self.buildmetadata)
            others = re.findall(pattern=r"\d+", string=other.buildmetadata)

            if not ours or not others:
                raise ValueError(
                    "Could not parse comparable build metadata version info."
                )

            if len(ours) > 1 or len(others) > 1:
                raise ValueError("Multiple integers found in build metadata version.")

            our_version = int(ours.pop())
            other_version = int(others.pop())

            if our_version == other_version:
                return 0
            elif our_version > other_version:
                return 1
            elif our_version < other_version:
                return -1

        # If we get here, we couldn't parse the pre-release
        raise ValueError(
            f"Could not compare {self.buildmetadata} and {other.buildmetadata}"
        )

    def bump_major(self) -> Version:
        """
        Return a new `Version` with the major version
        number bumped.

        Returns:
            Version: New bumped version.

        Examples:

        ```python
        >>> v1 = Version(1, 2, 4)
        >>> v1.bump_major()
        Version(major=2, minor=0, patch=0, prerelease=None, buildmetadata=None)
        ```

        ```python
        >>> v1 = Version(0, 7, 6, "rc.1", "build.123")
        >>> v1.bump_major()
        Version(major=1, minor=0, patch=0, prerelease=None, buildmetadata=None)
        ```
        """
        return Version(self.major + 1, 0, 0)

    def bump_minor(self) -> Version:
        """
        Return a new `Version` with the minor version
        number bumped.

        Returns:
            Version: New bumped version.

        Examples:

        ```python
        >>> v1 = Version(1, 2, 4)
        >>> v1.bump_minor()
        Version(major=1, minor=3, patch=0, prerelease=None, buildmetadata=None)
        ```

        ```python
        >>> v1 = Version(0, 7, 6, "rc.1", "build.123")
        >>> v1.bump_major()
        Version(major=0, minor=8, patch=0, prerelease=None, buildmetadata=None)
        ```
        """
        return Version(self.major, self.minor + 1, 0)

    def bump_patch(self) -> Version:
        """
        Return a new `Version` with the patch version
        number bumped.

        Returns:
            Version: New bumped version.

        Examples:

        ```python
        >>> v1 = Version(1, 2, 4)
        >>> v1.bump_patch()
        Version(major=1, minor=2, patch=5, prerelease=None, buildmetadata=None)
        ```

        ```python
        >>> v1 = Version(0, 7, 6, "rc.1", "build.123")
        >>> v1.bump_major()
        Version(major=0, minor=7, patch=7, prerelease=None, buildmetadata=None)
        ```
        """
        return Version(self.major, self.minor, self.patch + 1)
