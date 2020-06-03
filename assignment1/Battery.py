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

        # total costs of cable length & battery
        self.costs = 5000

        # list of houses connected to battery
        self.houses_in_batteries


    # check if house can be added & add house - Olaf

    # calculate how much cable has to layed to add house - Sam

    # calculate how much costs are added - Ruben
        def add_cost(self, cable_length):
            self.costs += cable_length * 9
            
        