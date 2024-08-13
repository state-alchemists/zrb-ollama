from typing import Annotated


def calculate(
    formula: Annotated[
        str,
        "A simple mathematical expression containing only numbers and basic operators (+, -, *, /).",
    ],  # noqa
) -> str:
    """Perform a calculation."""
    return str(eval(formula))
