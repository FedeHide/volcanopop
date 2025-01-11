#!./venv/bin/python
def get_marker_color_by_elevation(elev: float) -> str:
    """
    Get the color of the icon based on the elevation.

    Args:
        elev (float): The elevation of the volcano.

    Returns:
        str: The color of the icon.
    """

    if elev is None:
        return "gray"
    elif elev < 1000:
        return "green"
    elif elev < 2000:
        return "orange"
    else:
        return "red"
