
from classes.Battery import Battery
from classes.house import House
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

    district_id = input("Choose district (1,2 or 3):")
    cable_rule = input("Choose cable rule: \n 1. own-costs\n 2. shared costs\n")
    if cable_rule == 1:
        algorithm_id = input("Choose algorithm: \n 1. Random\n 2. Greedy\n 3. Random hill descent\n \
        4. Random Greedy\n 5. Simulated Annealing\n 6. Hill Climber\n")


if __name__ == "__main__":
    main()
