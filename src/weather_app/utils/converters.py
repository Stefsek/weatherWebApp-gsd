"""Temperature conversion and formatting utilities."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        The equivalent temperature in degrees Fahrenheit.
    """
    return (celsius * 9 / 5) + 32


def format_temperature(celsius: float, unit: str = "C") -> str:
    """Format a Celsius temperature as a display string with a degree symbol.

    Args:
        celsius: Temperature in degrees Celsius.
        unit: Target unit, either "C" for Celsius or "F" for Fahrenheit.
            Case-insensitive. Defaults to "C".

    Returns:
        A formatted string such as "21.5°C" or "70.7°F".
    """
    if unit.upper() == "F":
        temp = celsius_to_fahrenheit(celsius)
        return f"{temp:.1f}°F"
    return f"{celsius:.1f}°C"
