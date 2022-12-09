/*beliefs:*/
at_start
at_end
current_position
adjacency_list
distances

/*goals*/
+build_path

/*actions*/
move


/*rules:*/
+build_path <-
    at_start,
    ?at_end,
    ?current_position,
    ?adjacency_list,
    ?distances,
    .dijkstra()

dijkstra() <-
    current_position = start,
    distances[start] = 0,
    .visit_neighbors(start)

visit_neighbors(node) <-
    current_position = node,
    adjacency_list[node],
    .update_distances(neighbor)

update_distances(neighbor) <-
    current_position = node,
    distances[neighbor] = min(distances[node] + distance(node, neighbor), distances[neighbor]),
    .visit_neighbors(neighbor)

move <-
    current_position = node,
    distances[node],
    distances[neighbor] = min(distances[node], distances[neighbor]),
    neighbor,
    .move(neighbor)