
from classes.battery import Battery
from classes.house import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from algorithms.optimum_deluxe import optimum_deluxe
from classes.cable import Cable_instance
from visualization.algorithms import Combining_algorithms

def main():

    district_id = input("Choose district (1,2 or 3):")
    district_id = int(district_id)
    cable_rule = input("Choose cable rule: \n 1. own-costs\n 2. shared-costs\n")
    cable_rule = int(cable_rule)
    check50_result = ''
    input_text = ''
    if cable_rule == 1:
         input_text = "Choose algorithm: \n 1. Random\n 2. Greedy\n 3. Random hill descent\n \
        4. Random Greedy\n 5. Simulated Annealing\n 6. Hill Climber\n"
    if cable_rule == 2:
        input_text = "Choose algorithm: \n 1. A-star cable sharing\n 2. Optimum Deluxe\n"
    algorithm_id = input(input_text)
    algorithm_id = int(algorithm_id) + 6 * (cable_rule - 1)
    # run algorithm
    if algorithm_id == 1:
        #run Random
        check50_result = None
        pass
    if algorithm_id == 2:
        #run Greedy
        check50_result = None
        pass
    if algorithm_id == 3:
        #run Random hill descent
        check50_result = None
        pass
    if algorithm_id == 4:
        #run Random Greedy
        check50_result = None
        pass
    if algorithm_id == 5:
        #run Simulated Annealing
        check50_result = None
        pass
    if algorithm_id == 6:
        #run Hill Climber
        check50_result = None
        pass
    if algorithm_id == 7:
        #run A-star cable sharing
        check50_result = None
        pass
    if algorithm_id == 8:
        #run Optimum Deluxe
        optimization = optimum_deluxe(district_id)
        check50_result = optimization.run()

    # show result in check50 format
    print(check50_result)

# ------------ simulated annealing house allocation & Astar cable drawing ------------

    results2 = Combining_algorithms(4)

    results2.simulated_annealing_house_manhatten_cable(True)
#    results2.simulated_annealing_house_astar_cable()

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
