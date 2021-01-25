from __future__ import annotations
import re
from cowait.version import version

VERSION_FORMAT = re.compile('([0-9]+)\\.([0-9]+)\\.([0-9]+)')


class Version(object):
    def __init__(self, major: int, minor: int, revision: int):
        self.major = major
        self.minor = minor
        self.revision = revision

    def __str__(self) -> str:
        return f'{self.major}.{self.minor}.{self.revision}'

    def is_compatible(self):
        # 0.3 and below are not compatible.
        if self.minor < 4:
            return False
        return True

    @staticmethod
    def current():
        return Version.parse(version)

    @staticmethod
    def parse(version: str) -> Version:
        if re.match(VERSION_FORMAT, version) is None:
            raise ValueError(f'Illegal version string {version}')
        major, minor, rev = map(lambda v: int(v), version.split('.'))
        return Version(major, minor, rev)
