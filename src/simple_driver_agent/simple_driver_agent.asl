!start.

+!start <-
    .call_my_plan("path1", "path2", 4, 5).

+!my_plan(X, Y, A, B) <-
    .print("Called with:", X);
    .print("Called with:", Y);
    .get_shortest_path(X, Y, A, B, Z);
    .print("Shortest path:", Z).

+!get_shortest_path <-
    .calc_shortest_path(3, 2, X);
