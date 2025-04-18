#!./venv/bin/python
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


def format_popup(name: str, elev: int) -> str:
    """
    Format the popup content.

    Args:
        name (str): The name of the volcano.
        elev (int): The elevation of the volcano.

    Returns:
        str: The formatted popup content.
    """

    name = name or "Unknown"
    elev = f"{elev}" if elev is not None else "N/A"
    query = f"{name} volcano" if name != "Unknown" else ""
    return html_template.format(name=name, elev=elev, query=query)
