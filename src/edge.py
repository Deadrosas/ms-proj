class Edge:

    def __init__(self,name, cost=1):
        self.name = name
        self.cost = cost

        self.previous = []
        self.next = []
    
    def set_cost(self, cost):
        self.cost = cost

    def add_previous(self, edge):
        self.previous.append(edge)
    
    def add_next(self, edge):
        self.next.append(edge)

    def __repr__(self) -> str:
        return "Edge: " + self.name + " Cost: " + str(self.cost) + " Next: " + str(self.previous) + " Previous: " + str(self.next)
    
    def __str__(self) -> str:
        return "Edge: " + self.name + " Cost: " + str(self.cost) + " Next: " + str(self.previous) + " Previous " + str(self.next)