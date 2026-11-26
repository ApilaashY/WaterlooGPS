# Building map

`building_map` in `src/waterloomap/MapGraph.py` models the corridors shown in
the floor plan. Path names use corridor numbers where shown; suffixes split a
corridor into straight segments at junctions. Connection angles point outward
from the junction, clockwise from north.

Rooms are listed on corridors they open onto directly. Numbered rooms are not
used as through routes, so corridors separated by a room remain disconnected,
and rooms reachable only through another room are not included.