/* Beliefs */

publisher(wiley)

/* Goals */

/* Achievement goals */

!write(book)

/* Test goals */

?publisher(P)

/* Events and Plans */

/* triggering_event : context <- body. */

/* AgentSpeak triggering events */

/*  +b (belief addition)
    -b (belief deletion)
    +!g (achievement goal addition)
    -!g (achievement goal deletion)
    +?g (test goal addition)
    -?g (test goal deletion)
*/

/* Original AgentSpeak; JASON allows for more complex triggering events */



+green_patch(Rock) : not battery_charge(low)
    <- ?location(Rock, Coordinates);
    !at(Coordinates);
    !examine(Rock);

+!at(Coords) : not at(Coords) & safe_path(Coords)
    <- move_towards(Coords);
    !at(Coords).

/* +!at(Coords) ...*/


/* JASON reasoning cycle */

/* Reasoning Cycle (Steps)

1. Perceiving the Environment

2. Updating the Belief Base

3. Receiving Communication from Other Agents

4. Selecting Socially Acceptable Messages

5. Selecting an Event

6. Retrieving all Relevant Plans

7. Determining the Applicable Plans

8. Selecting one Applicable Plan

9. Selecting an Intention for Further Execution

10. Executing one step of an Intention

*/

/* Intention Execution */

/*

a. Environment Actions

b. Achievement Goals

c. Test Goals

d. Mental Notes

e. Internal Actions

f. Expressions

*/

/* Belief Annotations */

/* Annotated predicate: 
    ps(t1, ..., tn)[a1, ..., am] 
    where ai are first order terms

    all predicates in the belief base have a special annotation source(si)
    where si belongs to {self, percept} and AgId

    Example of annotations

    blue(box1)[source(ag1)].
    red(box1)[source(percept)].
    colourblind(ag1)[source(self), doc(0.7)].
    lier(ag1)[source(self), doc(0.2)].

*/


/* Annotated Plan Example

    @aPlan[
        chance_of_success(0.3),
        usual_payoff(0.9),
        any_other_property]
    +!g(X) : c(t) <- a(X).

*/



