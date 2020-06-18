
from classes.Battery import Battery
from classes.House import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from Algorithms import Combining_algorithms

# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs

def main():

    # Houses and battery locations are static and no cable sharing
    
    # ------------ Greedy_house allocation & Astar cable drawing ------------
    
    results1 = Combining_algorithms(1)

    results1.greedy_house_astar_cable()

    results1.the_district.refresh_config()

    print("The Greedy_house allocation & Astar cable drawing: ")

    # ------------ Greedy_house allocation & Astar cable drawing ------------
    
    results2 = Combining_algorithms(1)

    results2.simulated_annealing_house_astar_cable()

    results2.the_district.refresh_config()
    
    
    #print(cable_line.cable_network[0])
    #print()

    #prox_greedy_solution_1 = Greedy()
    #prox_greedy_solution_1.proximity_sort()
    #print(totalCosts(prox_greedy_solution_1.batteries))

    """greedy_solution = Greedy()

    greedy_solution.adding_houses()

    # print amout of items in battery 1
    print(len(greedy_solution.batteries[0].houses_in_battery))

    # removes second house from first battery
    greedy_solution.batteries[0].remove_house(greedy_solution.batteries[0].houses_in_battery[1])
    
    # print amout of items in battery 1 after item removed
    print(len(greedy_solution.batteries[0].houses_in_battery))

    print(greedy_solution.batteries[0].houses_in_battery[1].production)
    print(greedy_solution.batteries[0].houses_in_battery[1].production)
    print(greedy_solution.batteries[0].houses_in_battery[2].production)
    print(greedy_solution.batteries[0].houses_in_battery[3].production)
    print(greedy_solution.batteries[1].houses_in_battery[0].production)
    print(greedy_solution.batteries[2].houses_in_battery[0].production)

    print(totalCosts(greedy_solution.batteries))
"""
    # house1 = House(1, 2, 3)
    # house2 = House(1, 3, 2)
    # house3 = House(1, 6, 9)
    # house4 = House(1, 4, 0)
    # houses = [house1, house2, house3, house4]
    # print(house1.capacity)
    # print(house2.capacity)
    # print(house3.capacity)
    # print(house4.capacity)

    # print(sortHouse(houses)[0].capacity)
    # print(sortHouse(houses)[1].capacity)
    # print(sortHouse(houses)[2].capacity)
    # print(sortHouse(houses)[3].capacity)

if __name__ == "__main__":
    main()
