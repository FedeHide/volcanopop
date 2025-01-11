#!./venv/bin/python
import folium
import pandas


class Map:
    """
    A class to represent a map.

    Attributes:
        location (list): The center of the map.
        zoom_start (int): The initial zoom level.
        tiles (str): The style of the map tiles.
        fallback_tiles (str): The fallback style of the map tiles.
        data_csv_file (str): The path to the CSV file containing the volcano data.

    Methods:
        create_map(): Create a map with the given location, zoom level, and tiles style. Add markers to the map.
        create_volcanoes_markers(): Create a feature group with markers for volcanoes.
        save(filename: str): Save the map to a file.
    """

    def __init__(
        self,
        location: list = None,
        zoom_start: int = 3,
        tiles: str = "Cartodb Positron",
        fallback_tiles: str = "OpenStreetMap",
        data_csv_file: str = "volcanoes.csv",
    ):
        self.location = location if location is not None else [0, 0]
        self.zoom_start = zoom_start
        self.tiles = tiles
        self.fallback_tiles = fallback_tiles
        self.data_csv_file = data_csv_file

    def create_map(self) -> folium.Map:
        """
        Create a map with the given location, zoom level, and tiles style. Add markers to the map.

        Returns:
            folium.Map: A map with markers for volcanoes.
        """
        try:
            map = folium.Map(
                location=self.location, zoom_start=self.zoom_start, tiles=self.tiles
            )
        except Exception as e:
            print(
                f"Failed to load tiles '{self.tiles}' ({e}) tiles. Using fallback '{self.fallback_tiles}'."
            )
            map = folium.Map(
                location=self.location,
                zoom_start=self.zoom_start,
                tiles=self.fallback_tiles,
            )

        # Add markers to the map
        map.add_child(self.create_volcanoes_markers())

        # Add a layer control to the map
        map.add_child(folium.LayerControl())

        return map

    def create_volcanoes_markers(self) -> folium.FeatureGroup:
        """
        Create a feature group with markers for volcanoes.

        Args:
            data_csv_file (str): The path to the CSV file containing the volcano data.

        Returns:
            folium.FeatureGroup: A feature group with markers for volcanoes.
        """

        data = pandas.read_csv(self.data_csv_file)

        # FeatureGroup is a container for multiple features
        # TODO: Add a feature group for each type of marker (??)
        # TODO: check naming conventions for feature groups
        volcanoes_markers_fg = folium.FeatureGroup(name="volcanoes_markers")

        lat = list(data["LAT"])
        lon = list(data["LON"])

        for lt, ln in zip(lat, lon):
            volcanoes_markers_fg.add_child(
                folium.Marker(
                    location=[lt, ln], popup="volcano", icon=folium.Icon(color="red")
                )
            )

        return volcanoes_markers_fg

    def save(self, filename: str) -> None:
        """
        Save the map to a file.

        Args:
            filename (str): The name of the file to save the map to.
        """

        self.create_map().save(filename)


if __name__ == "__main__":
    map = Map()
    map.save("map.html")
