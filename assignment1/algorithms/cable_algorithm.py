
from classes.cable import Cable_instance
from classes.cable import Cable_line

class Cable():
    def __init__(self, district_instance):

        # all cables layed in object
        self.cable_network = []

        self.district_instance = district_instance
    
    def cable_list_batteries(self, batteries, cable_sharing):
        
        # adds list of cables to list of cables in every battery
        for battery in batteries:
            self.connect_battery_houses(battery, cable_sharing)
    
    def connect_battery_houses(self, battery, cable_sharing):

        if cable_sharing is True:
            self.list_houses = battery.houses_in_battery
            battery.list_cables.append(self.connecting_cables(self.list_houses, battery, 10))
            self.add_cable = self.connecting_cables(self.list_houses, battery, 10)

            for self.cable in self.add_cable:
                self.cable_network.append(self.cable)
                self.district_instance.all_cables.append(self.cable)
        
        else:
            # itterates through batteries and places a calbe
            for house in battery.houses_in_battery:
                battery.list_cables.append(self.connect_points_Astar(battery, house))
                self.add_cable = self.connect_points_Astar(battery, house)

                # adding cable list to nextwork
                self.cable_network.append(self.add_cable)
                self.district_instance.all_cables.append(self.add_cable)
    
    # lay cable between house and battery using best option
    def connect_points_Astar(self, start, end):

        self.current_point = Cable_instance(start.position_x, start.position_y)

        self.end_point = Cable_instance(end.position_x, end.position_y)

        self.former_point = Cable_instance(start.position_x, start.position_y)

        self.current_cable = Cable_line(self.current_point)

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
                self.current_cable.add_cable_instance(self.cable_options[0])
            else:
                # make next point current point
                self.current_point = self.cable_options[1]

                # lay cable
                self.current_cable.add_cable_instance(self.cable_options[1])

            # save current point to former point
            self.former_point.next_cable_inst = self.current_point

            # save former point to current point
            self.current_point.former_cable_inst = self.former_point
            
        return self.current_cable

    # calculates difference between two items
    def calculate_distance(self, obj_one, obj_two):

        return abs(obj_one.position_x - obj_two.position_x) + abs(obj_one.position_y - obj_two.position_y)

    # !!!!! Delete!!!!!?????!!!!!
    # calculating location of point inside self.configuration list
    def list_position(self, x_loc, y_loc):

        return (y_loc - 1) * (x_loc) + x_loc

    def connecting_cables(self, houses, end, range):
        
        # stores list with houses not yet connected
        self.houses_not_connected = houses.copy()

        # stores list that is in range of choosen house 
        self.too_connect = []

        # stores houses already connected with a battery
        self.houses_connected = []

        # stores a list of the cables layed to connect houses
        self.all_new_cables = []

        for self.a_house in houses:
                        
            if self.a_house not in self.houses_not_connected:
                continue

            # calculate the midpoint between cluster of houses
            self.x_min = self.a_house.position_x - range
            self.x_max = self.a_house.position_x + range
            self.y_min = self.a_house.position_y - range
            self.y_max = self.a_house.position_y + range

            self.too_connect.append(self.a_house)
            self.houses_not_connected.remove(self.a_house)
            self.average_x = self.a_house.position_x
            self.average_y = self.a_house.position_y

            for self.connect_house in self.houses_not_connected:
                if (self.x_min < self.connect_house.position_x < self.x_max) and (self.y_min < self.connect_house.position_y < self.y_max):
                    self.too_connect.append(self.connect_house)
                    self.houses_not_connected.remove(self.connect_house)
                    self.average_x += self.connect_house.position_x
                    self.average_y += self.connect_house.position_y
            self.average_x /= (len(self.too_connect))
            self.average_y /= (len(self.too_connect))
            self.mid_point = explore_node(int(self.average_x), int(self.average_y), end)
            
            self.main_cable = self.connect_points_Astar(self.mid_point, end)
            self.all_new_cables.append(self.main_cable)

            print(f"X: {int(self.average_x)} Y: {int(self.average_y)}")
            
            # connecting cables to main cable
            for self.connect_house_now in self.too_connect:
                self.new_cable = self.connect_points_Astar(self.connect_house_now, self.mid_point)
                self.new_cable.add_cable_instance(self.main_cable.cable_coordinates[0])
                self.all_new_cables.append(self.new_cable)
            
            self.houses_connected.append(self.too_connect)
            self.too_connect.clear()
        return self.all_new_cables

    
    
    
    
    
    
    
    def A_star(self, house, end, depth):
        
        # how far do we want to explore unefficient routes
        self.depth = depth

        self.current_cable_point = Cable_instance()
        self.current_cable_point.position_x = house.position_x
        self.current_cable_point.position_y = house.position_y
        
        # place to store cable
        self.the_cable = Cable_line(self.current_cable_point)

        # place to store nodes to explore
        self.nodes_to_explore = {}

        self.grid_to_explore = []

        # create grid
        for j in range(51):
            row = []
            for i in range(51):
                point = explore_node(j, i, end)
                row.append(point)
            self.grid_to_explore.append(row)

        # laying ze cable
        while self.current_cable_point.position_x is not end.position_x and self.current_cable_point.position_y is not end.position_y:

            # adding all options to nodes to explore dictionary
            self.list_of_options = []

            self.point_up = Cable_instance()
            self.point_up.position_x = self.current_cable_point.position_x
            self.point_up.position_y = self.current_cable_point.position_y - 1

            self.list_of_options.append(self.point_up)

            self.point_down = Cable_instance()
            self.point_down.position_x = self.current_cable_point.position_x
            self.point_down.position_y = self.current_cable_point.position_y + 1

            self.list_of_options.append(self.point_down)

            self.point_left = Cable_instance()
            self.point_left.position_x = self.current_cable_point.position_x - 1
            self.point_left.position_y = self.current_cable_point.position_y

            self.list_of_options.append(self.point_left)

            self.point_right = Cable_instance()
            self.point_right.position_x = self.current_cable_point.position_x + 1
            self.point_right.position_y = self.current_cable_point.position_y

            self.list_of_options.append(self.point_right)

            self.nodes_to_explore[self.current_cable_point] = self.list_of_options

        # adding options
        self.nodes_to_explore[self.cable_point]

        self.cable_point.x_coordinate
        
        # heurestiek is afstand
        self.calculate_distance()

class explore_node():


    def __init__(self, x_coordinate, y_coordinate, end):
        self.position_x = x_coordinate
        self.position_y = y_coordinate

        self.end_point = end

        #self.cal_for_cable = Cable(district_instance)
        
        #self.distance = self.cal_for_cable.calculate_distance(self, end)
        #self.costs = self.calculate_costs()

    #def calculate_costs(self):
        # self.cable = self.cal_for_cable.connect_points_Astar(self, self.end_point) <-- can't imput self
        #return self.cable.cal_cable_costs()

