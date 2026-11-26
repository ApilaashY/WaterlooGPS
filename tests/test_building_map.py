import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "waterloomap"))

from MapGraph import MapJunction, building_map


class BuildingMapTests(unittest.TestCase):
    def test_routes_across_connected_corridors(self):
        for start, end in [("1207", "1219"), ("1105", "1227"), ("1206", "1210")]:
            with self.subTest(start=start, end=end):
                route = building_map.findPath(start, end)
                self.assertTrue(route)
                self.assertIn(start, route[0].rooms)
                self.assertIn(end, route[-1].rooms)

    def test_numbered_rooms_are_not_used_as_through_routes(self):
        self.assertEqual(building_map.findPath("1105", "1239"), [])

    def test_route_does_not_revisit_junctions(self):
        route = building_map.findPath("1207", "1219")
        self.assertEqual(
            [element.id for element in route],
            ["1509", "1509-1514", "1514-west", "1510-1514", "1514-east",
             "1514-1515", "1515", "1515-1516", "1516-west", "1516-1517",
             "1516-east"],
        )

    def test_junction_connections_and_angles(self):
        self.assertEqual(
            {connection.path.id: connection.angle
             for connection in building_map.junctions_dict["1516-1517"].connections},
            {"1517": 0, "1516-east": 90, "1516-west": 270},
        )
        self.assertEqual(
            {connection.path.id: connection.angle
             for connection in building_map.junctions_dict["1507-1508-1509"].connections},
            {"1508": 0, "1509": 135, "1507": 270},
        )
        for junction in building_map.junctions:
            self.assertIsInstance(junction, MapJunction)
            for connection in junction.connections:
                self.assertIn(junction, (connection.path.junction1, connection.path.junction2))

    def test_shared_segments_have_opposite_connection_angles(self):
        for path in building_map.paths:
            if path.junction1 is not None and path.junction2 is not None:
                angles = [
                    next(connection.angle for connection in junction.connections
                         if connection.path is path)
                    for junction in (path.junction1, path.junction2)
                ]
                with self.subTest(path=path.id):
                    self.assertEqual((angles[0] - angles[1]) % 360, 180)


if __name__ == "__main__":
    unittest.main()
