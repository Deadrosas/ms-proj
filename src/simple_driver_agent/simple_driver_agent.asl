!start.


+!start <-
    paths(N);
    .calc_shortest_path(N, X);
    .print(X).



+!starts <-
    .call_my_plan("path1", "path2").

+!my_plan(X, Y) <-
    paths(N);
    !print_list(N);
    .print("Called with:", X);
    .print("Called with:", Y).

+!get_shortest_path <-
    .calc_shortest_path(3, X).


+!print_list([H|T]) <-
    .print(H);
    !print_list(T).

+!print_list([]) <-
    .print("Done").
