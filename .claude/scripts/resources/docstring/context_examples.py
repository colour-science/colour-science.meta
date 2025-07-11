"""
Context Manager and Special Pattern Examples
=============================================

Demonstrate context manager and special pattern docstrings used in colour-science.

This module focuses on context managers and other special patterns that
require specific documentation approaches, including __enter__/__exit__
methods and specialized classes.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from colour.hints import Self

__author__ = "Colour Developers"
__copyright__ = "Copyright 2025 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "VerboseContext",
]


# =============================================================================
# Context Managers
# =============================================================================

class VerboseContext:
    """
    Context manager for temporarily modifying verbose settings.

    This context manager allows temporarily changing the verbosity level
    for a block of code, similar to colour.utilities.verbose.

    Parameters
    ----------
    verbose
        Verbose setting to apply within the context.

    Examples
    --------
    >>> with VerboseContext(True):
    ...     # Code with verbose output enabled
    ...     pass  # doctest: +SKIP
    """

    def __init__(self, verbose: bool = True) -> None:
        """
        Initialize the verbose context manager.

        Parameters
        ----------
        verbose
            Verbose setting to apply.
        """

        self._verbose = verbose
        self._previous_verbose = None

    def __enter__(self) -> VerboseContext:
        """
        Enter the runtime context.

        Returns
        -------
        :class:`VerboseContext`
            Self reference for use in with statement.
        """

        # Store previous state and set new verbose level
        self._previous_verbose = getattr(self, '_global_verbose', False)

        # Set new verbose state
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the runtime context.

        Parameters
        ----------
        exc_type
            Exception type if an exception occurred.
        exc_val
            Exception value if an exception occurred.
        exc_tb
            Exception traceback if an exception occurred.

        Returns
        -------
        :class:`NoneType`
            None to propagate exceptions.
        """

        # Restore previous verbose state
        pass