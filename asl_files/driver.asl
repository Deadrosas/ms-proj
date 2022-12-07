!arrive_at_destination(destination)


+!drive(destination) 
    : not !at_destination(destination)
    <- drive_to(destination)


actions:
    - drive
    - turn
    - stop

rules:
    - +at_destination <- .stop
    - +at_intersection <- .turn(destination)
    - +arrive_at_destination <- .drive

