"""
Waterloo Building Map Graph Representation
Based on floor plan showing all paths, junctions, and rooms.
Each path represents a corridor/walkway; each junction is a turning point.
"""

from graphSearch import find_path


class MapPath():
    """Represents a path/corridor in the building map."""

    def __init__(self, pathid: str, rooms: list[str] = None):
        self.id = pathid
        self.junction1 = None
        self.junction2 = None
        self.rooms = rooms if rooms is not None else []

    def __repr__(self):
        return f"MapPath(id={self.id},\njunction1={self.junction1},\njunction2={self.junction2},\nrooms={self.rooms})"


class MapJunction():
    """Represents a turning point/junction where paths meet."""

    def __init__(self, junId: str, connections: list["MapConnection"]):
        self.id = junId
        self.connections = connections

        for connection in connections:
            if connection.path.junction1 is None:
                connection.path.junction1 = self
            elif connection.path.junction2 is None:
                connection.path.junction2 = self
            else:
                raise ValueError(f"Path {connection.path.id} already has two junctions.")

    def __repr__(self):
        return f"MapJunction(id={self.id},\nconnections={self.connections})"


class MapConnection():
    """Represents a connection between a path and a junction with turn angle."""

    def __init__(self, path: "MapPath", angle: int):
        self.path = path
        self.angle = angle % 360

    def __repr__(self):
        return f"MapConnection(path={self.path.id}, angle={self.angle})"


class Map():
    """Represents the entire building map graph."""

    def __init__(self, paths: list["MapPath"] = None, junctions: list["MapJunction"] = None):
        self.paths = []
        self.junctions = []
        self.paths_dict = {}
        self.junctions_dict = {}
        self.roomPaths = {}

        if paths:
            for p in paths:
                self.addPath(p)
        if junctions:
            for j in junctions:
                self.addJunction(j)

    def addPath(self, path: MapPath):
        self.paths.append(path)
        self.paths_dict[path.id] = path
        for room in path.rooms:
            if room not in self.roomPaths:
                self.roomPaths[room] = []
            self.roomPaths[room].append(path)

    def addJunction(self, junction: MapJunction):
        self.junctions.append(junction)
        self.junctions_dict[junction.id] = junction

    def findPath(self, start: str, end: str):
        # Find the path of the start and end rooms
        start_paths = self.roomPaths.get(start, [])
        end_paths = self.roomPaths.get(end, [])

        if not start_paths or not end_paths:
            return []

        # Use the first path containing the start and end rooms for simplicity
        start_path = start_paths[0]
        end_path = end_paths[0]

        return find_path(start_path, end_path)

# Corridor numbers follow the floor plan. Suffixes distinguish straight
# segments of the same corridor on opposite sides of a junction.
paths = {
    path.id: path
    for path in [
        MapPath("1504", ["1101", "1102", "1103", "1104", "1105", "1106",
                         "1107", "1108", "1109", "1110"]),
        MapPath("1517", ["1513", "1518", "1519"]),
        MapPath("1515", ["1205"]),
        MapPath("1516-west", ["1218"]),
        MapPath("1516-east", ["1219", "1220"]),
        MapPath("1508", ["1201", "1202", "1203", "1204", "1205"]),
        MapPath("1507", []),
        MapPath("1509", ["1206", "1207", "1216"]),
        MapPath("1514-west", ["1207", "1217"]),
        MapPath("1514-east", ["1217", "1209"]),
        MapPath("1510", ["1208"]),
        MapPath("1511-west", ["1214", "1215", "1216", "1213", "1212"]),
        MapPath("1511-east", ["1211", "1209"]),
        MapPath("1512", ["1210"]),
        MapPath("1521", ["1220", "1221", "1218"]),
        MapPath("1522", ["1222", "1223"]),
        MapPath("1523-west", ["1222", "1226", "1227"]),
        MapPath("1523-east", ["1231", "1236"]),
        MapPath("1527", ["1228", "1229", "1230"]),
        MapPath("1531", ["1236", "1238", "1239"]),
        MapPath("1533", ["101", "103", "104", "1237", "1239", "137"]),
        MapPath("east-north", ["111", "110A", "112", "113", "115", "137"]),
        MapPath("east-west", ["102", "108", "109", "110"]),
    ]
}

# Angles point outward from each junction, clockwise from north.
junctions = [
    MapJunction(junction_id, [
        MapConnection(paths[path_id], angle) for path_id, angle in connections
    ])
    for junction_id, connections in [
        ("1504-1517", [("1504", 270), ("1517", 180)]),
        ("1515-1516", [("1516-west", 90), ("1515", 180)]),
        ("1516-1517", [("1517", 0), ("1516-east", 90), ("1516-west", 270)]),
        ("1507-1508-1509", [("1508", 0), ("1509", 135), ("1507", 270)]),
        ("1509-1514", [("1509", 315), ("1514-west", 90)]),
        ("1510-1514", [("1514-west", 270), ("1514-east", 90), ("1510", 180)]),
        ("1510-1511", [("1510", 0), ("1511-east", 90), ("1511-west", 270)]),
        ("1511-1512", [("1511-east", 270), ("1512", 180)]),
        ("1514-1515", [("1515", 0), ("1514-east", 270)]),
        ("1516-1521", [("1516-east", 270), ("1521", 180)]),
        ("1521-1522-1523", [("1521", 0), ("1523-west", 90), ("1522", 180)]),
        ("1523-1527", [("1527", 0), ("1523-east", 90), ("1523-west", 270)]),
        ("east-corridor", [("east-north", 0), ("east-west", 90)]),
    ]
]

building_map = Map(list(paths.values()), junctions)
