from .ert_adapter import ERT

try:
    from ert_shared.version import version as __version__
except ImportError:
    __version__ = "0.0.0"

# Other modules depend on the ert shared resources so we explicitly expose their path
from ert_shared.hook_implementations.jobs import (
    _resolve_ert_share_path as ert_share_path,
)


def clear_global_state():
    """Deletes the global ERT instance shared as a global variable in the
    ert_shared module. This is due to an exception that arrises when closing
    the ERT application when modules, Python objects and C-objects are removed.
    Over time the singleton instance of ERT should disappear and this function
    should be removed.
    """
    global ERT
    if ERT is None:
        return

    ERT._implementation = None
    ERT._enkf_facade = None
    ERT = None
