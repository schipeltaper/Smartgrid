
from classes.Battery import Battery
from classes.House import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from visualization.Algorithms import Combining_algorithms

# calculate costs for list of batteries Get rid of this!!!!!!!!!!!!!!!!!!!
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs

def main():

    # Houses and battery locations are static and no cable sharing

    # ------------ Greedy_house allocation & Astar cable drawing ------------

    # results1 = Combining_algorithms(1)

    # print("make variable")

    # results1.greedy_house_astar_cable()

    # print("Greedy done")

    # print("Refresh done")

    # print("The Greedy_house allocation & Astar cable drawing: ")

    # ------------ simulated annealing house allocation & Astar cable drawing ------------

    results2 = Combining_algorithms(1)

    results2.simulated_annealing_house_astar_cable()

    # ------------ Random_Greedy_house allocation & Astar cable drawing ------------

    #results3 = Combining_algorithms(1)
    #print(results3.random_greedy_astar_cable(10))

    # ------------ Random_Greedy_house allocation & Astar cable drawing ------------

    #results4 = Combining_algorithms(1)
    #print(results4.sa_cable_share_astar())

    #print(cable_line.cable_network[0])
    #print()


if __name__ == "__main__":
    main()
