"""
Module-Level Docstring Examples
===============================

Demonstrate module-level docstring patterns used in colour-science.

This module focuses specifically on module-level documentation patterns,
encompassing module docstrings, constants, variables, and type aliases
that adhere to scientific documentation standards.

References
----------
:cite:`NumPy2022` : NumPy Documentation Guidelines for Scientific Python.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from colour.hints import ArrayLike, Real

__author__ = "Colour Developers"
__copyright__ = "Copyright 2025 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "CONSTANT_EXAMPLE",
    "MODULE_VARIABLE_EXAMPLE",
]


# =============================================================================
# Module Constants and Variables with Docstrings
# =============================================================================

CONSTANT_EXAMPLE: float = 1.0
CONSTANT_EXAMPLE.__doc__ = """
Demonstrate module-level constant documentation as a *float* example.

This constant represents a normalized value used throughout the module.

References
----------
:cite:`Smith2020` : Smith, J. (2020). Example Reference. Journal of Examples.
"""

MODULE_VARIABLE_EXAMPLE = {"key": "value", "another_key": 42}
MODULE_VARIABLE_EXAMPLE.__doc__ = """
Module-level variable example with complex structure.

Demonstrate documentation for module-level dictionaries or other data
structures that require detailed explanation.

Attributes
----------
key : :class:`str`
    Primary key with string value.
another_key : :class:`int`
    Secondary key with integer value.

Notes
-----
-   This variable is mutable and should be used with caution.
-   Values may be updated during runtime.
"""


# =============================================================================
# Type Aliases and Module Variables
# =============================================================================

Real = typing.Union[int, float]
"""Type alias for real numeric values accepting both int and float."""

ArrayLike = typing.Union[list, tuple, "numpy.ndarray"]
"""Type alias for array-like structures."""

_GLOBAL_VARIABLE: str = "example"
"""Module-level private variable with docstring (pattern from colour.algebra.common)."""