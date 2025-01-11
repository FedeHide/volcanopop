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
        location: list[float] | None = None,
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

        Returns:
            folium.FeatureGroup: A feature group with markers for volcanoes.
        """

        # read the data from the CSV file
        data = pandas.read_csv(self.data_csv_file)

        # FeatureGroup is a container for multiple features
        volcanoes_markers_fg = folium.FeatureGroup(name="Volcanoes")

        # HTML template for the popup
        html_template = """
                        <div class="popup-content">
                            <p><strong>Name:</strong> <a href="https://www.google.com/search?q={query}" target="_blank">{name}</a></p>
                            <p><strong>Elevation:</strong> {elev} mts</p>
                        </div>
                        <style>
                            body {{
                                margin: 0;
                                padding: 0;
                                box-sizing: border-box;
                                font-family: Arial, sans-serif;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                            }}
                            .popup-content {{
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                justify-content: center;
                                min-width: 150px;
                                gap: 0.5rem;
                            }}
                            .popup-content p {{
                                margin: 0;
                                font-size: 0.8rem;
                            }}
                            .popup-content p a {{
                                color: #007bff;
                                text-decoration: none;
                                position: relative;
                            }}
                            .popup-content p a::after {{
                                content: "";
                                position: absolute;
                                left: 0;
                                bottom: 0;
                                width: 0;
                                height: 1px;
                                background-color: #007bff;
                                transition: width 0.1s ease;
                            }}
                            .popup-content p a:hover::after {{
                                width: 100%;
                            }}
                        </style>
                        """

        def format_popup(name: str, elev: float) -> str:
            """
            Format the popup content.

            Args:
                name (str): The name of the volcano.
                elev (float): The elevation of the volcano.

            Returns:
                str: The formatted popup content.
            """

            name = name or "Unknown"
            elev = f"{int(elev)}" if elev is not None else "N/A"
            query = f"{name} volcano" if name != "Unknown" else ""
            return html_template.format(name=name, elev=elev, query=query)

        def get_icon_color_by_elevation(elev: float) -> str:
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

        # Add a marker for each volcano
        for row in data.itertuples():
            popup_html = format_popup(row.NAME, row.ELEV)

            # Create an iframe to embed the HTML content in the popup
            iframe = folium.IFrame(html=popup_html, width=180, height=80)

            # determine the color of the icon based on the elevation
            icon_color = get_icon_color_by_elevation(row.ELEV)

            # Add a marker to the feature group
            volcanoes_markers_fg.add_child(
                folium.Marker(
                    location=[row.LAT, row.LON],
                    popup=folium.Popup(iframe),
                    icon=folium.Icon(color=icon_color),
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
