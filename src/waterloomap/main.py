from MapGraph import building_map, MapJunction



result = building_map.findPath("1207", "1219")
# result = building_map.findPath("1105", "1227")

total = ""
for index, path in enumerate(result):
    if isinstance(path, MapJunction):
        # Get the junction angles of the two connected paths
        prev_path = result[index - 1]
        next_path = result[index + 1]
        prev_angle = list(filter(lambda x: x.path == prev_path, path.connections))[0].angle
        next_angle = list(filter(lambda x: x.path == next_path, path.connections))[0].angle

        total += str(next_angle - prev_angle) + "° turn at " + path.id + " -> "
    else:
        total += path.id + " -> "

total = total.rstrip(" -> ")
print(total)