#!./venv/bin/python
import folium

INITIAL_LOCATION = [0, 0]
TILES_STYLE = "Cartodb Positron"
FALLBACK_TILES_STYLE = "OpenStreetMap"

MARKERS = [
    {
        "location": [38.2, -99.1],
        "popup": "green Marker",
        "icon": folium.Icon(color="green"),
    },
    {
        "location": [37.2, -98.1],
        "popup": "blue Marker",
        "icon": folium.Icon(color="blue"),
    },
]


class Map:
    """
    A class to represent a map.

    Attributes:
        location (list): The center of the map.
        zoom_start (int): The initial zoom level.
        tiles (str): The style of the map tiles.
        markers (list): A list of markers to add to the map.

    Methods:
        create_map(): Create a map with the given location, zoom level, and tiles style. Add markers to the map.
        create_marker(location: list, popup: str, icon: folium.Icon): Create a marker with the given location, popup, and icon.
        save(filename: str): Save the map to a file.
    """

    def __init__(
        self,
        location: list = INITIAL_LOCATION,
        zoom_start: int = 3,
        tiles: str = TILES_STYLE,
        markers: list = [],
    ):
        self.location = location
        self.zoom_start = zoom_start
        self.tiles = tiles
        self.markers = markers

    def create_map(self) -> folium.Map:
        """
        Create a map with the given location, zoom level, and tiles style. Add markers to the map.

        Args:
            location (list): The center of the map.
            zoom_start (int): The initial zoom level.
            tiles (str): The style of the map tiles.
            markers (list): A list of markers to add to the map.

        Returns:
            folium.Map: A map object with the given location, zoom level, tiles style, and markers.
        """
        try:
            map = folium.Map(
                location=self.location, zoom_start=self.zoom_start, tiles=self.tiles
            )
        except:
            print(
                f"Failed to load {self.tiles} tiles. Loading {FALLBACK_TILES_STYLE} tiles instead."
            )
            map = folium.Map(
                location=INITIAL_LOCATION, zoom_start=3, tiles=FALLBACK_TILES_STYLE
            )

        # FeatureGroup is a container for multiple features
        # TODO: Add a feature group for each type of marker (??)
        # TODO: check naming conventions for feature groups
        markers_fg = folium.FeatureGroup(name="My Map")

        for marker in self.markers:
            markers_fg.add_child(
                self.create_marker(
                    location=marker["location"],
                    popup=marker["popup"],
                    icon=marker["icon"],
                )
            )

        map.add_child(markers_fg)

        # Add a layer control to the map
        map.add_child(folium.LayerControl())

        return map

    def create_marker(self, location: list, popup: str, icon: folium.Icon):
        """
        Create a marker with the given location, popup, and icon.

        Args:
            location (list): The location of the marker.
            popup (str): The text to display when the marker is clicked.
            icon (folium.Icon): The icon to use for the marker.

        Returns:
            folium.Marker: A marker object with the given location, popup, and icon.
        """

        marker = folium.Marker(location=location, popup=popup, icon=icon)

        # Create a marker
        return marker

    def save(self, filename: str):
        """
        Save the map to a file.

        Args:
            filename (str): The name of the file to save the map to.
        """

        self.create_map().save(filename)


map = Map(markers=MARKERS)
map.save("map.html")
