"""
Custom exception used by Local Lambda execution
"""


class FunctionNotFound(Exception):
    """
    Raised when the requested CFC function is not found
    """

class LayerNotFound(Exception):
    """
    Raised when the requested CFC layer is not found
    """
