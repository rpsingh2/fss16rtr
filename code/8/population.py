class Population(object):
    def __init__(self):
        self.population = []
        self.fronts = []
        
    def __len__(self):
        return len(self.population)
        
    def __iter__(self):
        return self.population.__iter__()
        
    def extend(self, new_individuals):
        self.population.extend(new_individuals)
