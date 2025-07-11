"""
Function Docstring Examples
============================

Demonstrate function-level docstring patterns used in colour-science.

This module focuses on various function types and their documentation
patterns, including synchronous functions, asynchronous functions,
and special cases like deprecation notices and mathematical notation.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from colour.hints import ArrayLike, NDArrayFloat, Real

__author__ = "Colour Developers"
__copyright__ = "Copyright 2025 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "function_example",
    "async_function_example",
    "function_with_warnings_and_deprecation",
    "function_with_math_notation",
]


# =============================================================================
# Standard Functions
# =============================================================================

def function_example(
    data: ArrayLike,
    scale: Real = 1.0,
    method: str = "linear",
    **kwargs
) -> NDArrayFloat:
    """
    Process array data with specified scaling and method.

    This function demonstrates comprehensive parameter documentation including
    positional, keyword, and arbitrary keyword arguments.

    Parameters
    ----------
    data
        Input array data to process. Can be list, tuple, or numpy array.
    scale
        Scaling factor to apply. Must be positive.
    method
        Processing method to use.

    Other Parameters
    ----------------
    threshold : :class:`float`, optional
        {:func:`colour.function_example`},
        Threshold value for filtering. Default is 0.5.
    normalize : :class:`bool`, optional
        {:func:`colour.function_example`},
        Whether to normalize the output. Default is True.

    Returns
    -------
    :class:`numpy.ndarray`
        Processed array with applied scaling and method.

    Raises
    ------
    ValueError
        If scale is not positive or method is not recognized.

    Warnings
    --------
    Large input arrays may require significant memory.

    Notes
    -----
    -   The function is optimized for float64 arrays.
    -   Performance may vary based on the chosen method.
    -   The following methods are supported:

        - ``linear``: Linear interpolation
        - ``cubic``: Cubic spline interpolation
        - ``nearest``: Nearest neighbor

    References
    ----------
    :cite:`Doe2019` : Doe, J. (2019). Advanced Array Processing. Tech Report.

    Examples
    --------
    Basic usage with default parameters:

    >>> import numpy as np
    >>> data = np.array([1.0, 2.0, 3.0])
    >>> result = function_example(data)
    >>> result
    array([1., 2., 3.])

    Using scaling and method parameters:

    >>> result = function_example(data, scale=2.0, method="cubic")
    >>> result
    array([2., 4., 6.])

    With additional keyword arguments:

    >>> result = function_example(
    ...     data, scale=1.5, method="linear", threshold=0.8, normalize=False
    ... )
    >>> result
    array([1.5, 3. , 4.5])
    """

    # Implementation would go here
    pass


# =============================================================================
# Asynchronous Functions
# =============================================================================

async def async_function_example(
    url: str,
    timeout: float = 30.0
) -> dict:
    """
    Asynchronously fetch data from a URL.

    This async function demonstrates documentation for asynchronous operations
    commonly used in modern Python applications.

    Parameters
    ----------
    url
        The URL to fetch data from.
    timeout
        Request timeout in seconds.

    Returns
    -------
    :class:`dict`
        Parsed JSON response data.

    Raises
    ------
    asyncio.TimeoutError
        If the request exceeds the timeout.
    aiohttp.ClientError
        If there's a network or HTTP error.

    See Also
    --------
    function_example : Synchronous processing function.

    Examples
    --------
    >>> import asyncio
    >>> async def main():
    ...     data = await async_function_example("https://api.example.com/data")
    ...     return data
    >>> # asyncio.run(main())  # doctest: +SKIP
    """

    # Async implementation would go here
    pass


# =============================================================================
# Special Cases
# =============================================================================

def function_with_warnings_and_deprecation(old_param: float) -> float:
    """
    Legacy function demonstrating deprecation notices.

    .. deprecated:: 0.4.0
        This function will be removed in colour-science 0.5.0.
        Please use :func:`colour.function_example` instead.

    Parameters
    ----------
    old_param
        Legacy parameter that will be removed.

    Returns
    -------
    :class:`float`
        Processed value.

    Warnings
    --------
    This function uses outdated algorithms and should not be used in new code.
    """

    import warnings

    warnings.warn(
        "function_with_warnings_and_deprecation is deprecated, "
        "use function_example instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return old_param * 0.5


def function_with_math_notation(
    x: ArrayLike,
    y: ArrayLike,
    z: ArrayLike
) -> NDArrayFloat:
    r"""
    Compute vector cross product with mathematical notation.

    This function computes the cross product of two 3D vectors using the
    standard mathematical definition:

    .. math::

        \\mathbf{u} \\times \\mathbf{v} = \\begin{bmatrix}
            u_2 v_3 - u_3 v_2 \\\\
            u_3 v_1 - u_1 v_3 \\\\
            u_1 v_2 - u_2 v_1
        \\end{bmatrix}

    Parameters
    ----------
    x
        First vector component.
    y
        Second vector component.
    z
        Third vector component.

    Returns
    -------
    :class:`numpy.ndarray`
        Cross product result.

    Notes
    -----
    -   The vectors must be 3-dimensional.
    -   The result is perpendicular to both input vectors.
    -   The magnitude equals :math:`|\\mathbf{u}||\\mathbf{v}|\\sin\\theta`.
    """

    # Implementation would go here
    pass