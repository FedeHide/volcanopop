#!./venv/bin/python
import folium
import pandas
from utils.format_popup import format_popup
from utils.get_marker_colors import get_marker_color_by_elevation


class Map:
    """
    A class to represent a map.

    Attributes:
        location (list): The center of the map.
        zoom_start (int): The initial zoom level.
        tiles (str): The style of the map tiles.
        fallback_tiles (str): The fallback style of the map tiles.
        volcanoes_data_csv_file (str): The path to the CSV file containing the volcano data.
        countries_geodata_json_file (str): The path to the JSON file containing the countries geodata.

    Methods:
        create_map(): Create a map with the given location, zoom level, and tiles style. Add markers to the map.
        create_volcanoes_markers(): Create a feature group with markers for volcanoes.
        create_countries_geodata(): Create a feature group with geodata for countries.
        save(filename: str): Save the map to a file.
    """

    def __init__(
        self,
        location: list[float] | None = None,
        zoom_start: int = 3,
        tiles: str = "Cartodb Positron",
        fallback_tiles: str = "OpenStreetMap",
        volcanoes_data_csv_file: str = "data/volcanoes-data.csv",
        countries_geodata_json_file: str = "data/countries-geodata.json",
    ):
        self.location = location if location is not None else [0, 0]
        self.zoom_start = zoom_start
        self.tiles = tiles
        self.fallback_tiles = fallback_tiles
        self.volcanoes_data_csv_file = volcanoes_data_csv_file
        self.countries_geodata_json_file = countries_geodata_json_file

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

        # Add volcanoes markers to the map
        map.add_child(self.create_volcanoes_markers())

        # Add geodata to the map
        map.add_child(self.create_countries_geodata())

        # Add a layer control to the map
        map.add_child(folium.LayerControl())

        return map

    def create_volcanoes_markers(self) -> folium.FeatureGroup:
        """
        Create a feature group with markers for volcanoes.

        Returns:
            folium.FeatureGroup: A feature group with markers for volcanoes.
        """

        # read the data from the CSV file
        data = pandas.read_csv(self.volcanoes_data_csv_file)

        # FeatureGroup is a container for multiple features
        # Create a fg for the markers
        volcanoes_markers_fg = folium.FeatureGroup(name="Volcanoes")

        # Add a marker for each volcano
        for row in data.itertuples():
            popup_html = format_popup(row.NAME, row.ELEV)

            # Create an iframe to embed the HTML content in the popup
            iframe = folium.IFrame(html=popup_html, width=180, height=80)

            # determine the color of the icon based on the elevation
            icon = get_marker_color_by_elevation(row.ELEV)

            # Add a marker to the feature group
            volcanoes_markers_fg.add_child(
                folium.Marker(
                    location=[row.LAT, row.LON],
                    popup=folium.Popup(iframe),
                    icon=icon,
                )
            )

        return volcanoes_markers_fg

    def create_countries_geodata(self) -> folium.FeatureGroup:
        """
        Create a feature group with geodata for countries.

        Returns:
            folium.FeatureGroup: A feature group with geodata for countries.
        """

        # Create a fg for the countries geodata
        countries_geodata_fg = folium.FeatureGroup(name="Population")

        # Add the countries geodata to the feature group
        countries_geodata_fg.add_child(
            folium.GeoJson(
                data=open(
                    self.countries_geodata_json_file, "r", encoding="utf-8-sig"
                ).read(),
                style_function=lambda x: {
                    "fillColor": (
                        "green"
                        if x["properties"]["POP2005"] < 10000000
                        else (
                            "orange"
                            if 10000000 <= x["properties"]["POP2005"] < 20000000
                            else "red"
                        )
                    )
                },
            )
        )

        return countries_geodata_fg

    def save(self, filename: str) -> None:
        """
        Save the map to a file.

        Args:
            filename (str): The name of the file to save the map to.
        """
        self.create_map().save(filename)
