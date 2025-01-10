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

        for marker in self.markers:
            map.add_child(
                self.create_marker(
                    location=marker["location"],
                    popup=marker["popup"],
                    icon=marker["icon"],
                )
            )

        return map

    def create_marker(self, location: list, popup: str, icon: folium.Icon):
        # FeatureGroup is a container for multiple features
        # TODO: Add a feature group for each type of marker (??)
        # TODO: check naming conventions for feature groups
        markers_fg = folium.FeatureGroup(name="My Map")

        # Create a marker
        marker = folium.Marker(location=location, popup=popup, icon=icon)

        # Add marker to the feature group
        markers_fg.add_child(marker)

        return markers_fg

    def save(self, filename: str):
        self.create_map().save(filename)


map = Map(markers=MARKERS)
map.save("map.html")
