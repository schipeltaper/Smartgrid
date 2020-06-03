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
        self.position = {x_axis, y_axis}

        # saves battery capacity
        self.capacity = capacity
