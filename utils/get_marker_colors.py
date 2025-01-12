#!./venv/bin/python
import folium


def get_marker_color_by_elevation(elevation: float) -> folium.CustomIcon:
    """
    Get the color of the icon based on the elevation.

    Args:
        elevation (float): The elevation of the volcano.

    Returns:
        folium.CustomIcon: A Folium CustomIcon object with the appropriate image.
    """

    if elevation is None:
        icon_image = "assets/icons/gray-volcano.png"
    elif elevation < 1000:
        icon_image = "assets/icons/green-volcano.png"
    elif elevation < 2000:
        icon_image = "assets/icons/orange-volcano.png"
    else:
        icon_image = "assets/icons/red-volcano.png"

    icon = folium.CustomIcon(
        icon_image,
        icon_size=(30, 30),
        icon_anchor=(15, 15),
        popup_anchor=(0, -10),
    )

    return icon
