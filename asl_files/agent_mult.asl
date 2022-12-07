!start.

+!start <-
    .call_my_plan("hello", "world").

+!my_plan(X, Y) <-
    .print("Called with:", X);
    .print("Called with:", Y).