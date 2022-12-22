!main.

+!main
<- !processList([1,2,3,4,5]);
    !processList2([1,2,3,4,5,6,7,8,9,10]).


+!processList([H|T])
<- .print(H);
    .print(T).

+!processList2(L)
<- .print(L).
