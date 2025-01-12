#!./venv/bin/python
from models.map import Map


if __name__ == "__main__":
    map = Map()
    map.save("map.html")
