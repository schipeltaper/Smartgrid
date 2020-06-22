'''
* Cable_instance and Cable_line
*
* Programmeertheorie
* Optimum Prime
*
* The Cable_instance is one point inside a cable line, the Cable_line class saves a
* list of cable_instance's to form a calbe.
*
'''

class Cable_instance():
    '''
    A Cable_instance contants the coordinates, the next and former cable instance in 
    a cable and other information of one point inside a cable. Furthermore, the
    Cable_instance contains a function concering the cable point. Initialisation requires
    the x and y coordinates within a district.
    '''
    
    def __init__(self, x, y):

        # saves information for a cable instance
        self.position_x = x
        self.position_y = y
        self.next_cable_inst = None
        self.former_cable_inst = None
        self.potential_nodes = None
    
    def determine_direction_cable(self):
        '''
        Determines the drection of the cable from current point, heading towards the battery,
        or end or cable reached.

        Returns: String, indicating the direction
        '''

        if self.next_cable_inst is None:
            return "EMPTY"
        
        elif self.position_y > self.next_cable_inst.position_y:
            return "UP"

        elif self.position_y < self.next_cable_inst.position_y:
            return "DOWN"

        elif self.position_x > self.next_cable_inst.position_x:
            return "LEFT"
        
        elif self.position_x < self.next_cable_inst.position_x:
            return "RIGHT" 

class Cable_line():
    '''
    A Cable_instance contants the starting cable_instance, ending cable_instance and a list
    of all cable_instance's in a cable, and further information about the cable, and a collection
    of function concering cables in the configuration. Requires a starting instance to initialise.
    '''

    def __init__(self, start):
        # saves information on the cable line
        self.start = start
        self.end = None
        self.cable_coordinates = []
        self.costs = 0
        self.connected_house = None        
        self.add_cable_instance(start)

    def cal_cable_costs(self):
        '''
        Calculates the costs of the cable.

        Returns: Int of the costs of the cable. 
        '''

        self.costs = len(self.cable_coordinates) * 9
        return self.costs

    def add_cable_instance(self, cable_instance):
        '''
        Adds cable instance too the cable line and updates the end of the cable line and costs.
        '''        

        self.cable_coordinates.append(cable_instance)
        self.costs += 9
        self.end = cable_instance


