
from classes.battery import Battery
from classes.house import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from visualization.algorithms import Combining_algorithms

def main():

    district_id = input("Choose district (1,2 or 3):")
    cable_rule = input("Choose cable rule: \n 1. own-costs\n 2. shared costs\n")
    if cable_rule == 1:
        algorithm_id = input("Choose algorithm: \n 1. Random\n 2. Greedy\n 3. Random hill descent\n \
        4. Random Greedy\n 5. Simulated Annealing\n 6. Hill Climber\n")

# ------------ simulated annealing house allocation & Astar cable drawing ------------

    # results2 = Combining_algorithms(1)
    results2 = Combining_algorithms(1)

    # results2.simulated_annealing_house_astar_cable()
    results2.simulated_annealing_house_astar_cable()

    # ------------ Random_Greedy_house allocation & Astar cable drawing ------------

    #resultaten = []
    #for x in range(10):
    #    results3 = Combining_algorithms(1)
    #    resultaten.append(results3.random_greedy_astar_cable(10))

    #print(resultaten)
    #results3 = Combining_algorithms(1)
    #print(results3.random_greedy_astar_cable(10))


if __name__ == "__main__":
    main()