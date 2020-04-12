import heapq as hq
from ways import graph
from ways import info
from ways import tools
from ways import draw
import random

import matplotlib.pyplot as plot

# class node conntain a parents and index num
# The class updae the cost (g) all the time and compare by F function
# The class initialize a heuristic when create a node
class Node:
    def __init__(self, parent = None, index_num = None):
        self.parent = parent
        self.index_num = index_num
        self.cost = 0
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.cost == other.cost:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        else:
            return False


# The function run over all the node in the open list, find new_node and return him
def find_node(new_node, open):
    # create a new map
    copy_open = []
    # bool parameter if find the parameter
    is_find = False
    # pop a node from the lost and push to the copy list
    node = hq.heappop(open)
    hq.heappush(copy_open, node)
    # check if this is the node,push him to the list if yes and return the node
    if node.index_num == new_node.index_num:
        hq.heappush(open, node)
        return node
    # run over all the list and find the node
    while open:
        if node.index_num == new_node.index_num:
            is_find = True
            break
        node = hq.heappop(open)
        hq.heappush(copy_open, node)
    # run over al the copy list and push back the nodes
    while copy_open:
        to_push = hq.heappop(copy_open)
        hq.heappush(open, to_push)
    # if find return the node
    if is_find:
        return node


# The function find node in the cost and update the cost
def change_cost(new_node, open):
    # create new list
    copy_open = []
    # run over all the list, if find the node push the new_node back
    while open:
        node = hq.heappop(open)
        if node.index_num == new_node.index_num:
            hq.heappush(open,new_node)
            # run over all the copy and push back the nodes
            while copy_open:
                to_push = hq.heappop(copy_open)
                hq.heappush(open, to_push)
            return open
        hq.heappush(copy_open, node)
    # run over all the copy and push back the nodes
    while copy_open:
        to_push = hq.heappop(copy_open)
        hq.heappush(open, to_push)
    return open


# The function run over all the open list and check if contain the new_node and return True or False
def is_in_open(new_node, open):
    copy_open = []
    # if the list empty return false
    if open.__len__() == 0:
        return False
    # pop the new node and check if contain the node, if yes return True and push back
    first = hq.heappop(open)
    hq.heappush(copy_open,first)
    if first.index_num == new_node.index_num:
        hq.heappush(open, first)
        return True
    # run over all the open list and check if contain the new_node
    # if the list contain return true, if not return false in the end
    while open:
        if first.index_num == new_node.index_num:
            while copy_open:
                to_push = hq.heappop(copy_open)
                hq.heappush(open,to_push)
            return True
        first = hq.heappop(open)
        hq.heappush(copy_open, first)
    # run over all the copy open and push back all the nodes if not in open
    # return false
    while copy_open:
        to_push = hq.heappop(copy_open)
        hq.heappush(open,to_push)
    return False

global ret_h
global ret_cost

# The function  get source and goal and return the path by astar algorithm
def find_astar_route(source, goal):
    global ret_h
    global ret_cost
    roads = graph.load_map_from_csv()
    # initialize the first node
    start_node = Node(None, source)
    start_node.parent = None
    start_node.g = 0
    # find the junction of source and goal
    s_junction = roads.junctions()[source]
    t_junction = roads.junctions()[goal]
    # calculate the heuristic of source and goal
    heuristic = tools.compute_distance(s_junction.lat, s_junction.lon, t_junction.lat, t_junction.lon) / 110
    # initialize the start node paramenters
    start_node.h = heuristic
    start_node.cost = start_node.h + start_node.g
    # create visited and add the first node
    visited = set()
    visited.add(start_node.index_num)
    # create open heap and push the first node
    open = []
    hq.heappush(open, start_node)
    # while open not empty
    while open:
        # pop node and check if is the goal
        curr_node = hq.heappop(open)
        if curr_node.index_num == goal:
            # return the path
            ret_g = curr_node.g
            # create the result list
            ret_cost = ret_g
            ret_h = heuristic
            result = create_succ(curr_node)
            return tuple(result)
        # add the current node toe the visited list
        visited.add(curr_node.index_num)
        # run over all the links of the current node
        for link in roads.junctions()[curr_node.index_num].links:
            # create newNode and update the cost
            new_node = Node(curr_node.index_num, link.target)
            # the actually cost
            cost_g = curr_node.g + g(link)
            # if the new node not in visited and not in open push and update the parameters
            if is_in_open(new_node, open) is False and new_node.index_num not in visited:
                # update the path
                new_node.parent = curr_node
                new_node.g = cost_g
                new_node.h = h(link.target, goal, roads)
                new_node.cost = new_node.g + new_node.h
                hq.heappush(open, new_node)
            # if the new node in open check if the new cost < old cost
            elif is_in_open(new_node, open) is True:
                if cost_g < find_node(new_node, open).g:
                    # create new node to the junction ,update the cost function and the parameters
                    new_node = Node(curr_node.index_num, link.target)
                    new_node.g = cost_g
                    # update the heuristic of the new_node - not change
                    new_node.h = h(link.target, goal, roads)
                    # update the path
                    new_node.parent = curr_node
                    # update f by f = g + h
                    new_node.cost = new_node.g + new_node.h
                    # update the new cost
                    open = change_cost(new_node, open)



# The function open problems file run over the 100 problem and write to the file the path,g and h function
def a_star():
    global ret_h
    global ret_cost
    # open problem file
    file_open = open('problems.csv', 'r')
    # create new file
    file_write = open('results/AStarRuns.txt', 'w')
    # run over all the lines in the problems file and calculate the path
    line = file_open.readline()
    while line:
        split = line.split(',')
        start_index = int(split[0])
        split = split[1].split()
        goal_index = int(split[0])
        # calculate the path by start and goal index
        result = find_astar_route(start_index, goal_index)
        # write to the file g and h of all path
        file_write.write(str(start_index) + " ")
        file_write.write(str(goal_index) + " ")
        file_write.write("cost is: " + str(ret_cost) + " ")
        file_write.write("heuristic is: " + str(ret_h))
        file_write.write("\n")
        line = file_open.readline()


# The function calculate G function by distance / velocity
# The function get link and calculate the cost
def g(link):
    type = link.highway_type
    return (link.distance / 1000) / info.SPEED_RANGES[type][1]


# The heuristic function calculate the estimated time
# the function get start, goal and roads find the junction and calculate
def h(s,t,roads):
    max_speed = 110
    s_junction = roads.junctions()[s]
    t_junction = roads.junctions()[t]
    return (tools.compute_distance(s_junction.lat, s_junction.lon, t_junction.lat, t_junction.lon) / max_speed)



# The function create the path
# The function run over all the node and create a list of the path
def create_succ(goal_node):
    result = []
    while goal_node.parent is not None:
        result.append(goal_node.index_num)
        goal_node = goal_node.parent
    result.append(goal_node.index_num)
    reverse_res = []
    i = len(result) - 1
    while i > 0:
        reverse_res.append(result[i])
        i = i - 1
    reverse_res.append(result[0])
    return reverse_res

# The function create graph of path of 10 problem
def create_map(roads):
    count = 0
    # open the problem file and chose 10 problem in random
    file_open = open('problems.csv', 'r')
    read = file_open.readlines()
    while count != 10:
        line = random.choice(read)
        split = line.split(',')
        start_index = int(split[0])
        split = split[1].split()
        goal_index = int(split[0])
        # calculate by astar
        result = find_astar_route(start_index, goal_index, roads)
        path = list(result[2])
        # create the graph and show
        draw.plot_path(roads,path)
        plot.title("A_star-source: " + str(start_index) + "goal: " + str(goal_index))
        plot.show()
        count = count + 1


# The function create a graph of all the 100 problem by g and h value
def graph_G_and_H(roads):
    # open problem file and run over all the problem
    file_open = open('problems.csv', 'r')
    line = file_open.readline()
    while line:
        split = line.split(',')
        start_index = int(split[0])
        split = split[1].split()
        goal_index = int(split[0])
        result = find_astar_route(start_index, goal_index,roads)
        g = result[0]
        h = result[1]
        plot.plot(h,g,'o',color='black')
        line = file_open.readline()
    plot.xlabel("heuristic")
    plot.ylabel("cost")
    plot.title("graph")
    plot.show()


# roads = graph.load_map_from_csv()
# a_star()

