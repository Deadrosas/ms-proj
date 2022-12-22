!start.

path1(1).

path2(2).

+!start <-
    .call_my_plan("path1", "path2").

+!my_plan(X, Y) <-
    .print("Called with:", X);
    .print("Called with:", Y).

+!get_shortest_path <-
    .calc_shortest_path(3, X).
