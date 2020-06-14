
from classes.cable import Cable_instance

class Cable():
    def __init__(self, district_instance):

        # all cables layed in object
        self.cable_network = []

        self.district_instance = district_instance

        self.cable_costs = 0
    
    def cable_list_batteries(self, batteries):
        
        # adds list of cables to list of cables in every battery
        for battery in batteries:
            battery.list_cables.append(self.connect_battery_houses(battery))
    
    def connect_battery_houses(self, battery):
        
        # stores all cables connected to battery
        self.battery_cables = []

        # itterates through batteries and places a calbe
        for house in battery.houses_in_battery:
            self.battery_cables.append(self.connect_points_Astar(battery, house))

        # returns all cables connected to battery
        return self.battery_cables
    
    # lay cable between house and battery using best option
    def connect_points_Astar(self, start, end):
        
        self.current_point = Cable_instance(start.position_x, start.position_y)
        
        # add the starting point to the configuration
        self.district_instance.adding_calbe_class_calbe(self.current_point)

        self.end_point = Cable_instance(end.position_x, end.position_y)

        self.former_point = Cable_instance(start.position_x, start.position_y)

        self.current_cable = [self.current_point]
                
        # run while end point not found
        while (self.current_point.position_x != self.end_point.position_x) or (self.current_point.position_y != self.end_point.position_y):

            self.cable_options = []

            # save current point into former point
            self.former_point = self.current_point
            
            # making sure we head the right way
            if self.current_point.position_x - self.end_point.position_x < 0:
                # lay cable one to the right
                self.cable_options.append(Cable_instance(self.current_point.position_x + 1, self.current_point.position_y))
            else:
                # lay cable one to the right
                self.cable_options.append(Cable_instance(self.current_point.position_x - 1, self.current_point.position_y))

            if self.current_point.position_y - self.end_point.position_y < 0:
                # lay cable one up
                self.cable_options.append(Cable_instance(self.current_point.position_x, self.current_point.position_y + 1))

            else:
                # lay cable one down
                self.cable_options.append(Cable_instance(self.current_point.position_x, self.current_point.position_y - 1))
            
            # updating points
            if self.calculate_distance(self.cable_options[0], self.end_point) < self.calculate_distance(self.cable_options[1], self.end_point):
                
                # make next point current point
                self.current_point = self.cable_options[0]
                
                # lay cable
                self.current_cable.append(self.cable_options[0])
            else:
                # make next point current point
                self.current_point = self.cable_options[1]
                
                # lay cable
                self.current_cable.append(self.cable_options[1])
            
            # save current point to former point
            self.former_point.next_cable_inst = self.current_point
            
            # save former point to current point
            self.current_point.former_cable_inst = self.former_point

            # add costs
            self.cable_costs += 9

            # lay cables inside configuration
            self.district_instance.adding_calbe_class_calbe(self.current_point)
          
        # adding cable list to nextwork
        self.cable_network.append(self.current_cable)
        
        return self.current_cable

    # calculates difference between two items
    def calculate_distance(self, obj_one, obj_two):

        return abs(obj_one.position_x - obj_two.position_x) + abs(obj_one.position_y - obj_two.position_y)

    # calculating location of point inside self.configuration list
    def list_position(self, x_loc, y_loc):
        
        return (y_loc - 1) * (x_loc) + x_loc