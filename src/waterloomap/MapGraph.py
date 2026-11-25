class MapPath():
    def __init__(self, pathid: str, rooms: list[str]):
        self.id = pathid
        self.junction1 = None
        self.junction2 = None
        self.rooms = rooms

    def __repr__(self):
        return f"MapPath(id={self.id},\njunction1={self.junction1},\njunction2={self.junction2},\nrooms={self.rooms})"

class MapJunction():
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
    def __init__(self, path: "MapPath", angle: int):
        self.path = path
        self.angle = angle % 360

    def __repr__(self):
        return f"MapConnection(path={self.path.id}, angle={self.angle})"

path1 = MapPath("path1", [])
path2 = MapPath("path2", [])
path3 = MapPath("path3", [])
path4 = MapPath("path4", [])
path5 = MapPath("path5", [])

MapJunction("junction1", [MapConnection(path1, 0), MapConnection(path2, 90), MapConnection(path4, 180)])
MapJunction("junction2", [MapConnection(path2, 270), MapConnection(path3, 90), MapConnection(path5, 180)])
