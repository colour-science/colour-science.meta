"""
Class Docstring Examples
========================

Demonstrate class-level docstring patterns used in colour-science.

This module showcases different class types and their documentation patterns,
including regular classes, dataclasses, enumerations, and class attributes.
"""

from __future__ import annotations

import typing
from dataclasses import dataclass
from enum import Enum

if typing.TYPE_CHECKING:
    from colour.hints import Real

__author__ = "Colour Developers"
__copyright__ = "Copyright 2025 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "ExampleEnum",
    "ExampleClass", 
    "DataclassExample",
]


# =============================================================================
# Enumerations
# =============================================================================

class ExampleEnum(Enum):
    """
    Define enumeration for categorizing example types in colour-science
    workflows.

    Provide a type-safe mechanism to specify and enforce consistent
    categorization of examples used throughout the colour-science library.
    This enumeration ensures standardized classification and usage patterns
    across all modules and subsystems.

    Attributes
    ----------
    BASIC : :class:`str`
        Basic example type for simple use cases.
    ADVANCED : :class:`str`
        Advanced example type for complex scenarios.
    EXPERIMENTAL : :class:`str`
        Experimental features under development.
    """

    BASIC = "basic"
    ADVANCED = "advanced"
    EXPERIMENTAL = "experimental"


# =============================================================================
# Regular Classes
# =============================================================================

class ExampleClass:
    """
    Define a comprehensive example class demonstrating various docstring
    patterns.

    This class showcases different types of method and property docstrings
    commonly used in the colour-science codebase. It includes regular methods,
    properties, static methods, and class methods.

    Parameters
    ----------
    name
        Name identifier for the instance.
    value
        Initial value to store.
    description
        Optional description of the instance.

    Attributes
    ----------
    name : :class:`str`
        The name identifier.
    description : :class:`str`
        The description text.
    DEFAULT_CONFIG : :class:`dict`
        Default configuration for all instances.

    Methods
    -------
    -   :meth:`~colour.utilities.ExampleClass.__init__`
    -   :meth:`~colour.utilities.ExampleClass.__str__`
    -   :meth:`~colour.utilities.ExampleClass.process`
    -   :meth:`~colour.utilities.ExampleClass.validate`
    -   :meth:`~colour.utilities.ExampleClass.from_dict`
    -   :meth:`~colour.utilities.ExampleClass.create_default`

    Examples
    --------
    >>> example = ExampleClass("test", 42.0)
    >>> example.name
    'test'
    >>> example.value
    42.0
    >>> print(example)
    ExampleClass(name='test', value=42.0)
    """

    DEFAULT_CONFIG: dict = {"enabled": True, "threshold": 0.5}
    """
    Default configuration dictionary for all class instances.
    
    This class attribute provides default settings that can be shared
    across all instances of the ExampleClass.
    """

    def __init__(
        self,
        name: str,
        value: float,
        description: str = "No description provided"
    ) -> None:
        """
        Initialize the ExampleClass instance.

        Set up the initial state of the example object with the specified
        parameters.

        Parameters
        ----------
        name
            Name identifier for the instance.
        value
            Numerical value associated with the instance.
        description
            Textual description of the instance. Default is "No description
            provided".
        """

        self._name = name
        self._value = value
        self.description = description

    def __str__(self) -> str:
        """
        Return a formatted string representation of the instance.

        Returns
        -------
        :class:`str`
            Formatted representation showing name and value.
        """

        return f"{self.__class__.__name__}(name='{self._name}', value={self._value})"

    def __repr__(self) -> str:
        """
        Return an evaluable string representation of the instance.

        Returns
        -------
        :class:`str`
            Evaluable string representation that can be used to recreate the
            instance.
        """

        return (
            f"{self.__class__.__name__}("
            f"name={self._name!r}, "
            f"value={self._value!r}, "
            f"description={self.description!r})"
        )

    @property
    def name(self) -> str:
        """
        Getter property for the instance name.

        Returns
        -------
        :class:`str`
            Name identifier of the instance.
        """

        return self._name

    @property
    def value(self) -> float:
        """
        Return the instance value.

        Parameters
        ----------
        value
            Value to set. Must be a positive float.

        Returns
        -------
        :class:`float`
            Current value of the instance.

        Raises
        ------
        ValueError
            If the specified value is negative.
        """

        return self._value

    @value.setter
    def value(self, value: float) -> None:
        """Setter for the **self.value** property."""

        if value < 0:
            raise ValueError("Value must be non-negative")
        self._value = value

    @classmethod
    def from_dict(cls, data: dict) -> ExampleClass:
        """
        Create an instance from a dictionary representation.

        This class method provides an alternative constructor for creating
        instances from dictionary data.

        Parameters
        ----------
        data
            Dictionary containing 'name', 'value', and optionally 'description'
            keys.

        Returns
        -------
        :class:`ExampleClass`
            New instance created from the dictionary data.

        Raises
        ------
        KeyError
            If required keys are missing from the dictionary.
        TypeError
            If the dictionary values have incorrect types.

        Examples
        --------
        >>> data = {"name": "test", "value": 42.0, "description": "Test instance"}
        >>> example = ExampleClass.from_dict(data)
        >>> example.name
        'test'
        """

        return cls(
            name=data["name"],
            value=data["value"],
            description=data.get("description", "No description provided")
        )

    @staticmethod
    def create_default() -> ExampleClass:
        """
        Create a default instance with predetermined values.

        This static method demonstrates factory pattern usage for creating
        standard instances.

        Returns
        -------
        :class:`ExampleClass`
            Default instance with name="default" and value=1.0.

        See Also
        --------
        from_dict : Alternative constructor from dictionary.
        """

        return ExampleClass("default", 1.0, "Default instance")


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class DataclassExample:
    """
    Demonstrate dataclass-specific docstring patterns for colour science
    applications.

    This dataclass exemplifies how to document fields and methods in modern
    Python dataclasses, which are commonly used throughout the colour-science
    library for representing structured data such as colour coordinates,
    spectral measurements, and transformation matrices.

    Attributes
    ----------
    x : :class:`float`
        X-coordinate value in the specified coordinate system.
    y : :class:`float`
        Y-coordinate value in the specified coordinate system.
    label : :class:`str`
        Optional descriptive label for the coordinate point. Defaults to an
        empty string.
    metadata : :class:`dict`
        Additional key-value pairs for storing supplementary information
        about the data point.
    """

    x: float
    y: float
    label: str = ""
    metadata: dict = None

    def __post_init__(self) -> None:
        """
        Post-initialization processing.

        Ensures metadata is properly initialized as an empty dict if None.
        """

        if self.metadata is None:
            self.metadata = {}

    def distance_from_origin(self) -> float:
        """
        Calculate Euclidean distance from the origin.

        Returns
        -------
        :class:`float`
            Distance from (0, 0) to (x, y).
        """

        return (self.x ** 2 + self.y ** 2) ** 0.5