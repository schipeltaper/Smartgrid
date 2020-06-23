'''
* House class
*
*
* Programmeertheorie
* Optimum Prime
*
* The House class is for representing a house inside the configuration.
*
'''
class House():
    '''
    The House class saves all the information of a house in the configuration. The
    initialisation requires an x and y coordinate on the configuration and the
    energy production of the house.
    '''

    def __init__(self, x_coordinate, y_coordinate, production):
        # variables that save information of the house
        self.production = production
        self.position_x = x_coordinate
        self.position_y = y_coordinate
        self.battery = None
