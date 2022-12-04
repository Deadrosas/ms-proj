beliefs:
    - at_destination
    - at_origin


goals:
    - +arrive_at_destination


actions:
    - drive
    - turn
    - stop

rules:
    - +at_destination <- .stop
    - +at_intersection <- .turn(destination)
    - +arrive_at_destination <- .drive

