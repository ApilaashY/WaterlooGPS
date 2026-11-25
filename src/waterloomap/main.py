from MapGraph import path1, path3


queue = [[path1]]
result = []

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

        if neighbor[0] == path3:
            result = current.copy() + [junction, neighbor[0]]
            break
        if neighbor[0] not in current and junction not in current:
            queue.append(current.copy() + [junction, neighbor[0]])

total = ""
for path in result:
    total += path.id + " -> "
    
total = total.rstrip(" -> ")
print(total)