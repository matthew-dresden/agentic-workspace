"""Shared template-version fixtures for unit and functional tests.

Template compatibility is decided by comparing a template's ``cli_version``
major against the running CLI's own major version. Every value below is
derived from :data:`workspace_cli.__version__` so that no test hard-codes a
major version number and the suite stays correct across version bumps.
"""

import semver

from workspace_cli import __version__

_CURRENT = semver.VersionInfo.parse(__version__)

#: Version recorded by a template the running CLI just wrote — compatible.
CURRENT_CLI_VERSION = __version__

#: Same major as the CLI, higher minor — compatible.
COMPATIBLE_MINOR_VERSION = str(_CURRENT.bump_minor())

#: Same major as the CLI, higher patch — compatible.
COMPATIBLE_PATCH_VERSION = str(_CURRENT.bump_patch())

#: Same major as the CLI but ordered before it — compatible, and older, so
#: upgrade paths that only act on out-of-date templates are exercised.
OLDER_COMPATIBLE_VERSION = str(_CURRENT.replace(prerelease="alpha.1"))

#: One major above the CLI — deliberately incompatible.
NEWER_MAJOR_VERSION = str(_CURRENT.bump_major())

#: Two majors above the CLI. Patch this in as the CLI's version to make a
#: template stamped :data:`NEWER_MAJOR_VERSION` look like it came from an
#: older, incompatible major.
NEWER_MAJOR_CLI_VERSION = str(_CURRENT.bump_major().bump_major())
