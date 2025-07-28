"""
Class Docstring Examples
========================

Demonstrate class-level docstring patterns used in the colour-science library.

This module showcases different class types and their documentation patterns,
including regular classes, dataclasses, enumerations, and class attributes.
The examples illustrate the standardized documentation approach for scientific
computing in the colour science domain.
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
    "SingleExampleClass",
    "MultiExampleClass",
    "DataclassExample",
]


# =============================================================================
# Enumerations
# =============================================================================

class ExampleEnum(Enum):
    """
    Define enumeration for categorizing example types in colour science
    workflows.

    Provide a type-safe mechanism to specify and enforce consistent
    categorization of examples used throughout the colour science library.
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

class SingleExampleClass:
    """
    Define a comprehensive single example class demonstrating various docstring
    patterns.

    This single example class showcases different types of method and property
    docstrings commonly used in the colour-science codebase. It includes regular
    methods, properties, static methods, and class methods for a single value.

    Parameters
    ----------
    name
        Name identifier for the single-instance.
    value
        Initial value to store.
    description
        Optional description of the single-instance.

    Attributes
    ----------
    name : :class:`str`
        The name identifier.
    description : :class:`str`
        The description text.
    DEFAULT_CONFIG : :class:`dict`
        Default configuration for all single-instances.

    Methods
    -------
    -   :meth:`~colour.utilities.SingleExampleClass.__init__`
    -   :meth:`~colour.utilities.SingleExampleClass.__str__`
    -   :meth:`~colour.utilities.SingleExampleClass.process`
    -   :meth:`~colour.utilities.SingleExampleClass.validate`
    -   :meth:`~colour.utilities.SingleExampleClass.from_dict`
    -   :meth:`~colour.utilities.SingleExampleClass.create_default`

    Examples
    --------
    >>> example = SingleExampleClass("test", 42.0)
    >>> example.name
    'test'
    >>> example.value
    42.0
    >>> print(example)
    SingleExampleClass(name='test', value=42.0)
    """

    DEFAULT_CONFIG: dict = {"enabled": True, "threshold": 0.5}
    """
    Default configuration dictionary for all single class single-instances.
    
    This class attribute provides default settings that can be shared
    across all single-instances of the SingleExampleClass.
    """

    def __init__(
        self,
        name: str,
        value: float,
        description: str = "No description provided"
    ) -> None:
        """
        Initialise the *SingleExampleClass* single-instance.

        Set up the initial state of the single example object with the specified
        parameters.

        Parameters
        ----------
        name
            Name identifier for the single-instance.
        value
            Numerical value associated with the single-instance.
        description
            Textual description of the single-instance. Default is "No description
            provided".
        """

        self._name = name
        self._value = value
        self.description = description

    def __str__(self) -> str:
        """
        Return a formatted string representation of the single-instance.

        Returns
        -------
        :class:`str`
            Formatted string representation displaying the single-instance's
            name and value.
        """

        return f"{self.__class__.__name__}(name='{self._name}', value={self._value})"

    def __repr__(self) -> str:
        """
        Return an evaluable string representation of the single-instance.

        Generate a string representation that, when evaluated, would recreate
        an equivalent single-instance with the same state.

        Returns
        -------
        :class:`str`
            Evaluable string representation that can recreate the single-instance.
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
        Getter for the single-instance name.

        Returns
        -------
        :class:`str`
            Name identifier of the single-instance.
        """

        return self._name

    @property
    def value(self) -> float:
        """
        Getter and setter for the single instance's numerical value.

        Provide access to the stored single numerical value with validation to
        ensure non-negative values. The getter retrieves the current single value
        while the setter validates and updates it.

        Parameters
        ----------
        value
            Numerical value to set. Must be a non-negative float.

        Returns
        -------
        :class:`float`
            Current numerical value of the single-instance.

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
    def from_dict(cls, data: dict) -> SingleExampleClass:
        """
        Create a single single-instance from a dictionary representation.

        This class method provides an alternative constructor for creating
        single single-instances from dictionary data.

        Parameters
        ----------
        data
            Dictionary containing 'name', 'value', and optionally
            'description' keys.

        Returns
        -------
        :class:`SingleExampleClass`
            New single single-instance created from the dictionary data.

        Raises
        ------
        KeyError
            If required keys are missing from the dictionary.
        TypeError
            If the dictionary values have incorrect types.

        Examples
        --------
        >>> data = {"name": "test", "value": 42.0, "description": "Test instance"}
        >>> example = SingleExampleClass.from_dict(data)
        >>> example.name
        'test'
        """

        return cls(
            name=data["name"],
            value=data["value"],
            description=data.get("description", "No description provided")
        )

    @staticmethod
    def create_default() -> SingleExampleClass:
        """
        Create a default single single-instance with predetermined values.

        This static method demonstrates factory pattern usage for creating
        standard single single-instances.

        Returns
        -------
        :class:`SingleExampleClass`
            Default single single-instance with name="default" and value=1.0.

        See Also
        --------
        from_dict : Alternative constructor from dictionary.
        """

        return SingleExampleClass("default", 1.0, "Default single single-instance")


class MultiExampleClass:
    """
    Define a comprehensive multi-example class demonstrating various docstring
    patterns.

    This multi-example class showcases different types of method and property
    docstrings commonly used in the colour-science codebase. It includes regular
    methods, properties, static methods, and class methods for multiple values.

    Parameters
    ----------
    name
        Name identifier for the multi-instance.
    value
        List of initial values to store.
    description
        Optional description of the multi-instance.

    Attributes
    ----------
    name : :class:`str`
        The name identifier.
    description : :class:`str`
        The description text.
    DEFAULT_CONFIG : :class:`dict`
        Default configuration for all multi-instances.

    Methods
    -------
    -   :meth:`~colour.utilities.MultiExampleClass.__init__`
    -   :meth:`~colour.utilities.MultiExampleClass.__str__`
    -   :meth:`~colour.utilities.MultiExampleClass.process`
    -   :meth:`~colour.utilities.MultiExampleClass.validate`
    -   :meth:`~colour.utilities.MultiExampleClass.from_dict`
    -   :meth:`~colour.utilities.MultiExampleClass.create_default`

    Examples
    --------
    >>> example = MultiExampleClass("test", [42.0, 24.0])
    >>> example.name
    'test'
    >>> example.value
    [42.0, 24.0]
    >>> print(example)
    MultiExampleClass(name='test', value=[42.0, 24.0])
    """

    DEFAULT_CONFIG: dict = {"enabled": True, "threshold": 0.5}
    """
    Default configuration dictionary for all multi-class multi-instances.
    
    This class attribute provides default settings that can be shared
    across all multi-instances of the MultiExampleClass.
    """

    def __init__(
        self,
        name: str,
        value: list[float],
        description: str = "No description provided"
    ) -> None:
        """
        Initialise the *MultiExampleClass* multi-instance.

        Set up the initial state of the multi-example object with the specified
        parameters.

        Parameters
        ----------
        name
            Name identifier for the multi-instance.
        value
            List of numerical values associated with the multi-instance.
        description
            Textual description of the multi-instance. Default is "No description
            provided".
        """

        self._name = name
        self._value = value
        self.description = description

    def __str__(self) -> str:
        """
        Return a formatted string representation of the multi-instance.

        Returns
        -------
        :class:`str`
            Formatted string representation displaying the multi-instance's
            name and value.
        """

        return f"{self.__class__.__name__}(name='{self._name}', value={self._value})"

    def __repr__(self) -> str:
        """
        Return an evaluable string representation of the multi-instance.

        Generate a string representation that, when evaluated, would recreate
        an equivalent multi-instance with the same state.

        Returns
        -------
        :class:`str`
            Evaluable string representation that can recreate the multi-instance.
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
        Getter for the multi-instance name.

        Returns
        -------
        :class:`str`
            Name identifier of the multi-instance.
        """

        return self._name

    @property
    def value(self) -> list[float]:
        """
        Getter and setter for the multi-instance's numerical value.

        Provide access to the stored multiple numerical values with validation to
        ensure non-negative values. The getter retrieves the current multiple values
        while the setter validates and updates them.

        Parameters
        ----------
        value
            List of numerical values to set. All must be non-negative floats.

        Returns
        -------
        :class:`list`
            Current list of numerical values of the multi-instance.

        Raises
        ------
        ValueError
            If any of the specified values are negative.
        """

        return self._value

    @value.setter
    def value(self, value: list[float]) -> None:
        """Setter for the **self.value** property."""

        if any(val < 0 for val in value):
            raise ValueError("All values must be non-negative")
        self._value = value

    @classmethod
    def from_dict(cls, data: dict) -> MultiExampleClass:
        """
        Create a multi multi-instance from a dictionary representation.

        This class method provides an alternative constructor for creating
        multi multi-instances from dictionary data.

        Parameters
        ----------
        data
            Dictionary containing 'name', 'value', and optionally
            'description' keys.

        Returns
        -------
        :class:`MultiExampleClass`
            New multi multi-instance created from the dictionary data.

        Raises
        ------
        KeyError
            If required keys are missing from the dictionary.
        TypeError
            If the dictionary values have incorrect types.

        Examples
        --------
        >>> data = {"name": "test", "value": [42.0, 24.0], "description": "Test instance"}
        >>> example = MultiExampleClass.from_dict(data)
        >>> example.name
        'test'
        """

        return cls(
            name=data["name"],
            value=data["value"],
            description=data.get("description", "No description provided")
        )

    @staticmethod
    def create_default() -> MultiExampleClass:
        """
        Create a default multi multi-instance with predetermined values.

        This static method demonstrates factory pattern usage for creating
        standard multi multi-instances.

        Returns
        -------
        :class:`MultiExampleClass`
            Default multi multi-instance with name="default" and value=[1.0, 2.0].

        See Also
        --------
        from_dict : Alternative constructor from dictionary.
        """

        return MultiExampleClass("default", [1.0, 2.0], "Default multi multi-instance")


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
        Additional key-value pairs for storing supplementary information about
        the data point.
    """

    x: float
    y: float
    label: str = ""
    metadata: dict = None

    def __post_init__(self) -> None:
        """
        Perform post-initialization processing for the dataclass instance.

        Ensure that the metadata attribute is properly initialized as an empty
        dictionary if None was specified during instantiation.
        """

        if self.metadata is None:
            self.metadata = {}

    def distance_from_origin(self) -> float:
        """
        Calculate the Euclidean distance from the origin.

        Compute the Euclidean distance from the origin point (0, 0) to the
        coordinate point (*x*, *y*) using the standard distance formula
        :math:`\\sqrt{x^2 + y^2}`.

        Returns
        -------
        :class:`float`
            Euclidean distance from the origin (0, 0) to the coordinate point
            (*x*, *y*).
        """

        return (self.x ** 2 + self.y ** 2) ** 0.5