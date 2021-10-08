"""
Core semantic version functionality.


Author: Tom Fleet
Created: 08/10/2021
"""

from typing import Optional

from pydantic import BaseModel


class Version(BaseModel):
    major: int
    minor: int
    patch: int
    prerelease: Optional[str]
    buildmetadata: Optional[str]
