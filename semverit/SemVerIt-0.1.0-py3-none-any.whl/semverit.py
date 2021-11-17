"""Manipulate semantic versioning (SemVer)

Manipulate semantic version numbers.  Create a new version number,
initialize it with an, existing number or alternatively read it from an
existing project setup.py file.

See also https://semver.org/
"""

import configparser
import logging
from pathlib import Path
import tempfile
import beetools.beeutils
from beetools.beearchiver import Archiver

_PROJ_DESC = __doc__.split("\n")[0]
_PROJ_PATH = Path(__file__)
_PROJ_NAME = _PROJ_PATH.stem
_PROJ_VERSION = "0.0.1"


class SemVerIt:
    """Manipulate semantic versioning (SemVer)"""

    def __init__(
        self, p_version=None, p_setup_cfg_pth=None, p_parent_log_name="", p_verbose=True
    ):
        """Initialize the class

        Parameters
        ----------
        p_version : str, default = None
            Initial version to start with.
        p_setup_py_pth : Path default = None
            setup.py file from where the version number can be read.
        p_parent_log_name : str
            Name of the parent.  In combination witt he class name it will
            form the logger name.
        p_verbose: bool, default = True
            Write messages to the console.

        Examples
        --------
        """
        self.success = True
        if p_parent_log_name:
            self._log_name = "{}.{}".format(p_parent_log_name, _PROJ_NAME)
            self.logger = logging.getLogger(self._log_name)
        self.verbose = p_verbose

        self.version = "0.0.1"
        if p_setup_cfg_pth:
            if p_setup_cfg_pth.exists():
                self.version = self.get_from_setup_cfg(p_setup_cfg_pth)
        elif p_version:
            self.version = p_version
        major, minor, patch = self.version.split(".")
        self.maj = int(major)
        self.min = int(minor)
        self.patch = int(patch)
        pass

    def bump_maj(self):
        """Bump the major version.

        The major version will be increased by 1. In the process the minor
        and patch versions will be reset to 0 i.e.
        0.0.1 -> 1.0.0.
        0.1.2 -> 1.0.0

        Returns
        -------
        version : str
            Complete version string

        Examples
        --------

        """
        self.maj += 1
        self.min = 0
        self.patch = 0
        self.version = "{}.{}.{}".format(self.maj, self.min, self.patch)
        return self.version

    def bump_min(self):
        """Bump the minor version.

        The minor version will be increased by 1. The major version will
        stay the same, but the patch version will be reset to 0 i.e.
        0.0.1 -> 0.1.0.
        0.1.2 -> 0.2.0

        Returns
        -------
        version : str
            Complete version string

        Examples
        --------

        """
        self.min += 1
        self.patch = 0
        self.version = "{}.{}.{}".format(self.maj, self.min, self.patch)
        return self.version

    def bump_patch(self):
        """Bump the patch version.

        The patch version will be increased by 1. The major- and the minor
        version will stay the same.
        0.0.1 -> 0.0.2.
        0.1.2 -> 0.1.3

        Returns
        -------
        version : str
            Complete version string

        Examples
        --------

        """
        self.patch += 1
        self.version = "{}.{}.{}".format(self.maj, self.min, self.patch)
        return self.version

    def get_from_setup_cfg(self, p_pth):
        """Read the version number from the setup.py file.

        The setup.py file (should) contain the version number for the
        current module and package.  Most projects already has a setup.py
        file and is most probably also the correct version currently pushed
        to git.  It makes sense to read it from there.

        Parameters
        ----------
        p_pth : Path
            Path to the setup.cfg file

        Returns
        -------
        version : str
            Complete version string

        Examples
        --------

        """
        # content = p_pth.read_text()
        # dist = run_setup(p_pth, stop_after="init")
        # self.version = dist.get_version()
        setup_cfg = configparser.ConfigParser(inline_comment_prefixes="#")
        setup_cfg.read([p_pth])
        if setup_cfg.has_option("metadata", "version"):
            version = setup_cfg.get("metadata", "version")
            major, minor, patch = version.split(".")
            self.maj = int(major)
            self.min = int(minor)
            self.patch = int(patch)
            self.version = version
        else:
            version = self.version
        return version


def do_examples(p_cls=True):
    """A collection of implementation examples for SemVerIt.

    A collection of implementation examples for SemVerIt. The examples
    illustrate in a practical manner how to use the methods.  Each example
    show a different concept or implementation.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the examples.

    See Also
    --------

    Notes
    -----

    Examples
    --------

    """
    success = do_example1(p_cls)
    success = do_example2(p_cls) and success
    success = do_example3(p_cls) and success
    return success


def do_example1(p_cls=True):
    """A working example of the implementation of SemVerIt.

    Example1 illustrate the following concepts:
    1. Create an abject with no parameters i.e. the default.
    2. Bump the patch version
    3. Bump the minor version.  The patch version is reset to 0.
    4. Bump the minor version.
    5. Bump the patch version
    6. Bump the major version.  The patch and minor version are reset to 0.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the example

    """
    success = True
    archiver = Archiver(_PROJ_NAME, _PROJ_VERSION, _PROJ_DESC, _PROJ_PATH)
    archiver.print_header(p_cls=p_cls)

    svit = SemVerIt()
    print("{} - Initialize".format(svit.version))
    print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    print("{} -> {} - Bump minor version".format(svit.version, svit.bump_min()))
    print("{} -> {} - Bump minor version again".format(svit.version, svit.bump_min()))
    print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    print("{} -> {} - Bump major version".format(svit.version, svit.bump_maj()))

    archiver.print_footer()
    return success


def do_example2(p_cls=True):
    """A working example of the implementation of SemVerIt.

    Example1 illustrate the following concepts:
    1.Initialize object with version = 3.2.1
    2. Bump the patch version
    3. Bump the minor version.  The patch version is reset to 0.
    4. Bump the minor version.git status
    5. Bump the patch version
    6. Bump the major version.  The patch and minor version are reset to 0.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the example

    """
    success = True
    archiver = Archiver(_PROJ_NAME, _PROJ_VERSION, _PROJ_DESC, _PROJ_PATH)
    archiver.print_header(p_cls=p_cls)

    svit = SemVerIt(p_version="3.2.1")
    print("{} - Initialize".format(svit.version))
    print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    print("{} -> {} - Bump minor version".format(svit.version, svit.bump_min()))
    print("{} -> {} - Bump minor version again".format(svit.version, svit.bump_min()))
    print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    print("{} -> {} - Bump major version".format(svit.version, svit.bump_maj()))

    archiver.print_footer()
    return success


def do_example3(p_cls=True):
    """A working example of the implementation of SemVerIt.

    Example1 illustrate the following concepts:
    1. Read the version from the setup.cfg file
    2. Bump the patch version
    3. Bump the minor version.  The patch version is reset to 0.
    4. Bump the minor version.
    5. Bump the patch version
    6. Bump the major version.  The patch and minor version are reset to 0.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the example

    """
    success = True
    archiver = Archiver(_PROJ_NAME, _PROJ_VERSION, _PROJ_DESC, _PROJ_PATH)
    archiver.print_header(p_cls=p_cls)

    setup_pth = _create_setup_cfg()
    svit = SemVerIt(p_setup_cfg_pth=setup_pth)
    print("{} - Initialize".format(svit.version))
    print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    print("{} -> {} - Bump minor version".format(svit.version, svit.bump_min()))
    print("{} -> {} - Bump minor version again".format(svit.version, svit.bump_min()))
    print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    print("{} -> {} - Bump major version".format(svit.version, svit.bump_maj()))

    beetools.beeutils.rm_tree(setup_pth.parents[0])
    archiver.print_footer()
    return success


_setup_cfg_contents = """\
[metadata]
version = 2.3.4
"""


def _create_setup_cfg():
    working_dir = Path(tempfile.mktemp())
    working_dir.mkdir()
    setup_py_pth = working_dir / "setup.cfg"
    setup_py_pth.write_text(_setup_cfg_contents)
    return setup_py_pth


if __name__ == "__main__":
    do_examples()
