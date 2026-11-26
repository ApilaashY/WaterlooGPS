def find_path(start, end_path):
    if start == end_path:
        return [start]

    queue = [[start]]
    while len(queue) > 0:
        current = queue.pop(0)

        last_path = current[-1]

        # Find all neighboring paths connected to the last path
        neighbors = []
        if last_path.junction1:
            for connection in last_path.junction1.connections:
                if connection.path != last_path:
                    neighbors.append([connection.path, 1])
        if last_path.junction2:
            for connection in last_path.junction2.connections:
                if connection.path != last_path:
                    neighbors.append([connection.path, 2])

        for neighbor in neighbors:
            junction = last_path.junction1 if neighbor[1] == 1 else last_path.junction2

            if neighbor[0] == end_path:
                return current + [junction, neighbor[0]]
            if neighbor[0] not in current and junction not in current:
                queue.append(current.copy() + [junction, neighbor[0]])
    return []