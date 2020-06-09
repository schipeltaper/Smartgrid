'''
* house class
*
* Programmeertheorie
* Optimum Prime
*
* house class for smartgrid problem
*
'''
class House():
    def __init__(self, x_coordinate, y_coordinate, production):
        self.production = production
        self.position_x = x_coordinate
        self.position_y = y_coordinate
