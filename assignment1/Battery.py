'''
* battery class
*
* Programmeertheorie
* Optimum Prime
*
* battery class for smartgrid problem
*
'''

class Battery():

    # initialises a battery with a location and capacity
    def __init__(self, float x_axis, float y_axis, float capacity):

        # saves battery location on grid
        self.position_x = x_axis
         
        self.position_y = y_axis

        # saves battery capacity
        self.capacity = capacity

        # total energy usage of all houses connected to battery
        self.energy_production

        # length of connected cables
        self.length_cables

        # total costs of cable length & battery
        self.costs = 5000

        # list of houses connected to battery
        self.houses_in_battery = []

    # check if house can be added & add house - Olaf
    # return true if house added and False if not
    def add_house(self, house):

        # make sure house fits in battery
        if self.capacity < self.energy_production + production:
            
            # battery not enought capacity
            return False
    
        # add battery
        self.capacity += production

        # add house to houses
        self.houses_in_battery.append(house)

        # add costs
        self.costs += add_cost(cable_length(house))

    # calculate how much cable has to layed to add house - Sam
    def cable_length(self, house):
        return abs(self.position_x - house.position_x) + abs(self.position_y - house.position_y)

    # calculate how much costs are added - Ruben
    def add_cost(self, cable_length):
            return cable_length * 9
