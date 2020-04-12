import heapq as hq
import math
from ways import graph
from ways import info
from ways import tools


# The function find the min between two parameters and return the small one
def find_min(a,b):
    if a < b:
        return a
    else:
        return b


# The function implement the ida_star algorithim
def ida_star(source, goal):
    global heuristic
    # load the map
    roads = graph.load_map_from_csv()
    # find the source and te goal junction
    source_junc = roads.junctions()[source]
    goal_junc = roads.junctions()[goal]
    # calculate the linit by the heuristic
    new_limit = tools.compute_distance(source_junc.lat, source_junc.lon, goal_junc.lat, goal_junc.lon) / 110
    heuristic = new_limit
    # create path result
    path = []
    f_limit = new_limit
    # run over infinity loop
    while True:
        # call dfs in al iteration by a limit and with the source
        solution,f_limit = dfs_counter(source,0,path,f_limit,goal,roads)
        if solution:
            # if the solution is true , create path and return
            path = create_succ(path)
            return tuple(path)
        # if the limit is inf return none - not a path between this junction
        if f_limit == math.inf:
            return None


global cost_to_print
global heuristic


# The function run dfs ,calculate the cost, heuristic and update the path
def dfs_counter(state, g, path, f_limit ,goal ,roads):
    global cost_to_print
    global heuristic
    # find the junction on map
    s_junction = roads.junctions()[state]
    t_junction = roads.junctions()[goal]
    # calculate the cost by g and h
    new_cost = g + tools.compute_distance(s_junction.lat, s_junction.lon,t_junction.lat, t_junction.lon) / 110
    # initalize the bound
    new_inf = math.inf
    # if the cost is bigger return none
    if new_cost > f_limit:
        return None, new_cost
    # if is the goal add to the path and return in recursive
    if state == goal:
        path.append(goal)
        cost_to_print = g
        return state,f_limit
    # run over all the child of the junction
    for link in roads.junctions()[state].links:
        # update the cost
        solution,new_f = dfs_counter(link.target, g + g_cost(link) ,path ,f_limit ,goal ,roads)
        # check if true and add to the path and return in recursive
        if solution:
            path.append(state)
            return solution,f_limit
        # check the new cost
        new_inf = find_min(new_inf,new_f)
    # if not find path
    return None,new_inf



# The function open problems file run over the 5 problem and write to the file the path and cost
def ida_star_res():
    # save the cost and heuristic of all path
    global cost_to_print
    global heuristic
    file_open = open('problems.csv', 'r')
    file_write = open('results/IDAStarRuns.txt', 'w')
    line = file_open.readline()
    # read from problem files and write to the result file all5 problem
    while line:
        split = line.split(',')
        start_index = int(split[0])
        split = split[1].split()
        goal_index = int(split[0])
        result = ida_star(start_index, goal_index)
        if result:
            file_write.write("source: " + str(start_index) + " ")
            file_write.write("goal: " + str(goal_index) + " ")
            file_write.write("cost: " + str(cost_to_print))
            file_write.write("heuristic: " + str(heuristic))
            file_write.write("\n")
        line = file_open.readline()


# The function calculate f
def f(link,roads):
    return h(link, roads) + g_cost(link)


# The function calculate G function by distance / velocity
# The function get link and calculate the cost
def g_cost(link):
    type = link.highway_type
    return (link.distance / 1000) / info.SPEED_RANGES[type][1]


# The heuristic function calculate the estimated time
# The function get start, goal and roads find the junction and calculate
def h(link, roads):
    max_speed = 110
    for j in roads.junctions():
        if j.index == link.source:
            s_junction = j
            break
    for j in roads.junctions():
        if j.index == link.target:
            t_junction = j
            break
    return (tools.compute_distance(s_junction.lat, s_junction.lon, t_junction.lat, t_junction.lon) / max_speed)


# The function create the path
# The function run over all the junction and create a list of the path
def create_succ(succ_list):
    result = []
    i = len(succ_list) - 1
    while i > 0:
        result.append(succ_list[i])
        i = i - 1
    result.append(succ_list[0])
    return result


# ida_star_res()