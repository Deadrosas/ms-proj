class Edge:

    def __init__(self,name, cost=1):
        self.name = name
        self.cost = cost

        self.previous = []
        self.next = []
    
    def get_name(self):
        return self.name
        
    def set_cost(self, cost):
        self.cost = cost

    def add_previous(self, edge):
        self.previous.append(edge)
    
    def add_next(self, edge):
        self.next.append(edge)

    def set_next(self, edges):
        self.next = edges
    
    def set_previous(self, edges):
        self.previous = edges

    def get_next(self):
        return self.next

    def __repr__(self) -> str:
        return "Edge: " + self.name + " Cost: " + str(self.cost) + " Next: " + str(self.previous) + " Previous: " + str(self.next)
    
    def __str__(self) -> str:
        return "Edge: " + self.name + " Cost: " + str(self.cost) + " Next: " + str(self.previous) + " Previous " + str(self.next)