from knapsack import KnapsackProblem
from TSP import TSP_Problem
import math

witch_problem = input('witch problem: 1) knapsack  2) TSP')
if witch_problem == '1':
    witch_input_file = input('witch input file: 1) knapsack_1.txt  2) knapsack_2.txt 3) knapsack_3.txt')
    a = KnapsackProblem('knapsack_{}.txt'.format(witch_input_file))
    print('running...')
    best_fitness = -math.inf
    result, items_value_wight = a.solve()
    print('best result:')
    print(result)
    sum_value = 0
    sum_weight = 0
    chromosome = result['chromosome']
    for i in range(len(chromosome)):
        sum_value += chromosome[i] * items_value_wight[i][0]
        sum_weight += chromosome[i] * items_value_wight[i][1]
    print('sum_value: '+ str(sum_value) + '    sum_weight: '+ str(sum_weight))   

elif witch_problem == '2':
    b = TSP_Problem('tsp_data.txt')
    print('running..')
    result = b.solve()
    print('best result:')
    print(result)
    print('distance: ' + str(result['fitness']))
else: 
    print('wrong answer!')
# 'D:\education\semester6\Computational intelligence\HWs\HW2\code'