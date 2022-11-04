!print_factorial(5).

+!print_factorial(N)
    <- !fact(N,F);
        .print("The factorial of ", N, " is ", F).

+!fact(N,1) : N == 0.

+!fact(N,F) : N > 0 
    <- !fact(N-1, F1);
    F = N * F1.