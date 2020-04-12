from ways import graph
from random import randrange
import csv
import sys


# The function create the problem file choose 2 number in random
# check if they have path between them and write to the file
def create_problem_csv(roads):
    # initalize the number of the problem to 0
    count_problems = 0
    with open('problems.csv', 'w', newline='') as file:
        max_size = sys.maxsize
        write_to_file = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index in range(max_size):
            random_range = randrange(len(roads))
            # check if 100 problem and break
            if count_problems == 100:
                break
            # find a source and target in random
            source = randrange(random_range - 10, random_range)
            target = randrange(random_range - 10, random_range)
            # calculate bfs result by the best_first_search function
            close = best_first_search(source, roads)
            # Check for a path between the two junction
            goal_is = close[target]
            # if they have write to the file this source and target
            if goal_is:
                count_problems = count_problems + 1
                write_to_file.writerow([str(source), str(target)])


# The function create the path between two junction
def create_the_path(roads, node):
    result = []
    link = roads.get(node).links
    # run over all the child of junction and add to the result
    for index in link:
        temp = index[1]
        result.append(temp)
    return result


# The function implement a best first search algorithim
def best_first_search(source, roads):
    # initialize a counter for the len of the path between two junction
    count = 0
    # initialize a list for the result
    res_bfs = []
    res_bfs.append(source)
    # update the close_list by bool parameters
    close_list = [False] * (len(roads))
    close_list[source] = True
    # run over all the res_bfs list
    while res_bfs:
        count +=1
        # if the len of the path bigger then 30 break
        if count == 30:
            break
        new_node = res_bfs.pop(0)
        result = create_the_path(roads, new_node)
        # run over the resilt
        for node in result:
            # check if node not in close_list
            temp = close_list[node]
            if not temp:
                # add to the path and close_list
                close_list[node] = True
                res_bfs.append(node)
    # return the close_list
    return close_list


roads = graph.load_map_from_csv()
create_problem_csv(roads)