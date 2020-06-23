'''
* Main
*
*
* Programmeertheorie
* Optimum Prime
*
*
* This file contains the __main__ file of the Smartgrid optimization project.
*
*
*
'''
import json
import os.path

from algorithms.cable_algorithm import Cable
from algorithms.greedy_algorithm import Greedy
from algorithms.optimum_deluxe import optimum_deluxe
from algorithms.random_algorithms import Random_house_sort, Battery_capacity_hill_decent
from classes.battery import Battery
from classes.cable import Cable_instance
from classes.house import House
from classes.map_lists import district_1, district_2, district_3, district_test
from visualization.algorithms import Combining_algorithms
from visualization.check50_to_visualization import Check50_to_visualization

def main():
    '''
    Ask user which optimization algorithm to run with which district.
    '''

    # Get user input.
    district_id = input("Choose district (1,2 or 3):")
    district_id = int(district_id)
    cable_rule = input("Choose cable rule: \n 1. own-costs\n 2. shared-costs\n")
    cable_rule = int(cable_rule)
    cable_sharing = False
    if cable_rule == 2:
        cable_sharing = True
    check50_result = ''
    input_text = ''
    if cable_rule == 1:
         input_text = "Choose algorithm: \n 1. Random \n 2. Greedy \n 3. Random hill descent \n \
        4. Random Greedy \n 5. Simulated Annealing \n 6. Hill Climber followed by Simulated Annealing \n"
    if cable_rule == 2:
        input_text = "Choose algorithm: \n 1. Optimum Deluxe \n 2. Greedy \n 3. Random Greedy \n \
            4. Simulated Annealing \n"
    algorithm_id = input(input_text)
    algorithm_id = int(algorithm_id) + 6 * (cable_rule - 1)

    # Run algorithm.
    if algorithm_id == 1:
        optimization = Random_house_sort(district_id)
        check50_result = optimization.run()
    if algorithm_id == 2:
        # greedy
        optimization = Combining_algorithms(district_id)
        check50_result = optimization.greedy_house_manhatten_cable(cable_sharing)
    if algorithm_id == 3:
        optimization = Battery_capacity_hill_decent(district_id)
        check50_result = optimization.run()
        pass
    if algorithm_id == 4:
        # random Greedy
        step_num = input("How many steps would you like to take during you climb on the hill?")
        optimization = Combining_algorithms(district_id)
        check50_result = optimization.random_greedy_astar_manhatten_cable(int(step_num), cable_sharing)
    if algorithm_id == 5:
        #run Simulated Annealing
        optimization = Combining_algorithms(district_id)
        check50_result = optimization.simulated_annealing_house_manhatten_cable(cable_sharing)
    if algorithm_id == 6:
        #run Hill Climber followed by Simulated Annealing
        step_num = input("How many steps would you like to take during you climb on the hill?")
        config = Combining_algorithms(district_id)
        check50_result = config.annealing_hill_climber(int(step_num), False)
    if algorithm_id == 7:
        #run Optimum Deluxe
        optimization = optimum_deluxe(district_id)
        check50_result = optimization.run()
    if algorithm_id == 8:
        # greedy
        optimization = Combining_algorithms(district_id)
        check50_result = optimization.greedy_house_manhatten_cable(cable_sharing)
    if algorithm_id == 9:
        # random Greedy
        step_num = input("How many steps would you like to take during you climb on the hill?")
        optimization = Combining_algorithms(district_id)
        check50_result = optimization.random_greedy_astar_manhatten_cable(int(step_num), cable_sharing)
    if algorithm_id == 10:
        #run Simulated Annealing
        optimization = Combining_algorithms(district_id)
        check50_result = optimization.simulated_annealing_house_manhatten_cable(cable_sharing)


    # show result in check50 format
    print(check50_result[0])
    
    # print result in json file (inspired by Spectras on Stackoverflow)
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "results/output.json")
    with open(path, 'w') as f:
        f.seek(0)
        json.dump(check50_result, f)
        f.truncate()

    Check50_to_visualization("../results/output.json")


if __name__ == "__main__":
    main()
