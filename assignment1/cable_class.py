
class Cable():
    def __init__(self, battery, house):
        
        self.start_battery = battery

        self.end_house = house

        self.cable = []

        self.cable_costs = 0

    # lay cable between house and battery using best option
    def (self, self.battery, self.house, self.grid):
        
        self.potential_moves = []
        
        # former point location in configuration list
        self.former_point = self.list_position(self.battery.position_x, self.battery.position_y)

        self.new_point = self.list_position(self.battery.position_x, self.battery.position_y)
        
        # former distance
        self.former_distance = calculate_distance(self.battery, self.house)
        
        # next location
        self.x_next = 0
        self.y_next = 0
        
        # repeat untill cable ends at house location
        while self.house.position_x is not ... and self.house.position_y is not ...:

            # starting with heading the right way x axis
            if battery.position_x - house.position_x < 0:
                
                x_next = 1
            else:

                x_next = -1

            # starting with heading the right way y axis
            if battery.position_y - house.position_y < 0
                
                y_next = 1
            else:
                
                y_next = -1

            # calculate new position of point on grid

            # calculate distance with x_next & y 0
            self.new_point = self.list_position(self.x_next, self.battery.position_y)

            # compare distance with former point
            calculate_distance(self.grid.configuration.self.new_point, self.house)
            
            # x possition new_point - 
            self.list_position()

            self.calculate_distance()
            potential_moves.append({})

            # try with y_next & x 0


            ////////

            # starting with heading the right way x axis
            if battery.position_x - house.position_x < 0:
                
                x_range = range(-1, 0)

            else:

                x_range = range(0, 1)

            # starting with heading the right way y axis
            if battery.position_y - house.position_y < 0
                
                y_range = range(-1, 0)
            
            else:
                
                y_range = range(0, 1)
            
            # itterating through x option
            for x_options in x_range:
                
                # itterating through y option
                for y_opsitions in y_range:

                    if potential_moves = []:
                    
                    

    # calculates difference between two items
    def calculate_distance(self, obj_one, obj_two):

        return abs(obj_one.position_x - obj_two.position_x) + abs(obj_one.position_y - obj_two.position_y)

    # calculating location of point inside self.configuration list
    def list_position(self, x_loc, y_loc):
        
        return (y_loc - 1) * (x_loc) + x_loc


    




