
from classes.Battery import Battery
from classes.House import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from classes.Configuration import Configuration
from algorithms.hill_climber import Hill_climber
from algorithms.simulated_annealing import simulated_annealing

class Combining_algorithms():



    def __init__(self, district_numb):
        self.the_district = Configuration(district_numb)
        self.the_district.create_district()

    # Greedy_house allocation & Astar cable drawing - assumption 1 cable 1 house
    def greedy_house_astar_cable(self):

        # creating an instant to save greedy object
        self.greedy_house_devide = Greedy(self.the_district)

        # deviding houses amoung batteries using proximity
        self.greedy_house_devide.proximity_sort()

        # save the cable algorithm object
        self.astar_cable = Cable(self.the_district)

        # laying cables for every battery between its own houses
        self.astar_cable.cable_list_batteries(self.the_district.all_batteries, False)




        self.the_district.print_the_dam_thing()

        print(f"The total costs of greedy astar: {self.the_district.cal_costs()}")




        self.the_district.cal_costs()
        print(f"The total costs of greedy astar: {self.the_district.total_costs}")

    # simulated annealing hill climber
    def annealing_hill_climber(self):
        # creating an instant to save greedy object
        self.annealing_house_devide1 = simulated_annealing(self.the_district)

        # deviding houses among batteries using
        self.annealing_house_devide1.creating_starting_possition()
        self.annealing_house_devide1.running_simulated_annealing()

        self.hill = Hill_climber(self.the_district)

        self.hill.climb_the_hill()

        print(f"Final total costs of simulated annealing hill climber: {self.the_district.cal_costs()}")


    # simulated anealing house distribution & Astar cable drawing - assumption 1 cable 1 house
    def simulated_annealing_house_astar_cable(self):
        self.sa_distribution = simulated_annealing(self.the_district)
        self.sa_distribution.creating_starting_possition()
        self.sa_distribution.running_simulated_annealing()
        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, False)

        self.the_district.print_the_dam_thing()




        self.the_district.cal_costs()

        while self.the_district.total_costs > 60000:
            self.simulated_annealing_house_astar_cable()

        print(f"The total costs simulated annealing astar: {self.the_district.cal_costs()}")

    def random_greedy_astar_cable(self, rounds):
        self.random_greedy = Greedy(self.the_district)
        self.random_greedy.random_greedy(rounds)

        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, False)

        return self.the_district.cal_costs()

    # simulated anealing house distribution & Astar cable sharing drawing - assumption cable sharing
    def sa_cable_share_astar(self):
        self.sa_distribution = simulated_annealing(self.the_district)
        self.sa_distribution.creating_starting_possition()
        self.sa_distribution.running_simulated_annealing(True)
        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, True)
        self.the_district.print_the_dam_thing()

        print(f"The total costs simulated annealing astar: {self.the_district.cal_costs()}")

# calculate costs for list of batteries Get rid of this!!!!!!!!!!!!!!!!!!!
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs
