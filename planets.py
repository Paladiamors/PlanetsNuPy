import math

class Planet:

    def __init__(self, temp, pop, supplies=0, mc=0, factories=0, mines=0, defences=0, supply=0, tax=0):
        self.temp = temp
        self.pop = pop
        self.supplies = supplies
        self.factories = factories
        self.mc = mc
        self.mines = mines
        self.defences = defences
        self.supply = supply
        self.tax = tax

    def pop_growth(self, pop=None):
        """
        computes the population growth
        """

        if not pop:
            pop = self.pop
        if 15 < self.temp < 85:
            growth = round(math.sin(3.14*(100-self.temp)/100) * pop/20*5/(self.tax+5))
        else:
            growth = 0

        return growth if self.pop <= 66000 else round(growth*0.5)

    def pop_grow(self):

        self.pop += self.pop_growth()
        return self.pop


    def pop_max(self):
        """
        returns the maximum population of a planet
        """

        if self.temp > 84:
            return int(20099.9 - (200*self.temp)/10)
        elif self.temp < 15:
            return int(299.9 - (200*self.temp)/10)
        else:
            return round(math.sin(3.14*(100-self.temp)/100)*100000)

    def struct_max(self, pop_bracket, pop=None):

        if pop is None:
            pop = self.pop

        if pop < pop_bracket:
            return pop

        else:
            return int(pop_bracket + (pop-pop_bracket)**0.5)

    def mines_max(self, pop=None):
        return self.struct_max(200, pop=pop)

    def factories_max(self, pop=None):
        return self.struct_max(100, pop=pop)

    def defences_max(self, pop=None):
        return self.struct_max(50, pop=pop)

    def build_structure(self, structure, mc_cost):
        """
        builds a structure at some cost
        """

        buildable = getattr(self, f"{structure}_max")() - getattr(self, structure)

        to_build = min([buildable, self.supplies, int((self.supplies + self.mc)/(mc_cost + 1))])
        new_total = getattr(self, structure) + to_build
        setattr(self, structure, new_total)

        total_cost = mc_cost*to_build
        if self.mc > total_cost:
            self.mc -= total_cost
            self.supplies -= to_build
        else:
            self.mc = 0
            self.supplies -= (total_cost - self.mc) + to_build

        if self.supplies < 0:
            print("supplies is negative")

    def build_structures(self):
        """
        builds as given by resources on the planet
        """
        self.build_structure("factories", 3)
        self.build_structure("mines", 4)
        self.build_structure("defences", 10)

    def advance(self):
        """
        advances the planet by one turn
        """

        self.supplies += self.factories
        self.pop_grow()
