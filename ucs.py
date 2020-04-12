import heapq as hq
from ways import graph
from ways import info
from ways import tools


# class node contain the index of junction, the index pf the father and the cost
class Node:
    def __init__(self, parent = None, cost = None, index_num = None):
        self.parent = parent
        self.cost = cost
        self.index_num = index_num

    # compare < by cost
    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        else:
            return False

    # compare > by cost
    def __eq__(self, other):
        if self.cost == other.cost:
            return True
        else:
            return False

    # compare > by cost
    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        else:
            return False

# The function run over all the node in the open list, find new_node and return him
def find_node(new_node, open):
    copy_open = []
    is_find = False
    node = hq.heappop(open)
    hq.heappush(copy_open, node)
    if node.index_num == new_node.index_num:
        hq.heappush(open, node)
        return node
    # run over all the lost and check if is the node
    while open:
        if node.index_num == new_node.index_num:
            is_find = True
            break
        node = hq.heappop(open)
        hq.heappush(copy_open, node)
    # push back all the nodes to the open list
    while copy_open:
        hq.heappush(open, hq.heappop(copy_open))
    # return the node if found, and none if not
    if is_find:
        return node
    return None



# The function find node in the cost and update the new cost
def change_cost(new_node, open):
    copy_open = []
    # run over all the list and check if is open node replace between the node
    while open:
        node = hq.heappop(open)
        if node.index_num == new_node.index_num:
            hq.heappush(open,new_node)
            # push back all the node to open
            while copy_open:
                to_push = hq.heappop(copy_open)
                hq.heappush(open, to_push)
            # retrun the update open
            return open
        hq.heappush(copy_open, node)
    # push back all the node to open if not find the node in open
    while copy_open:
        to_push = hq.heappop(copy_open)
        hq.heappush(open, to_push)
    # retrun open
    return open


# The function run over all the open list and check if the list contain the new_node
# return True or False accordingly
def is_in_open(new_node, open):
    copy_open = []
    # if open is empty return false
    if open.__len__() == 0:
        return False
    # pop a node and check
    first = hq.heappop(open)
    hq.heappush(copy_open,first)
    if first.index_num == new_node.index_num:
        hq.heappush(open, first)
        return True
    # run over all the open list and check
    while open:
        if first.index_num == new_node.index_num:
            while copy_open:
                to_push = hq.heappop(copy_open)
                hq.heappush(open,to_push)
            return True
        first = hq.heappop(open)
        hq.heappush(copy_open, first)
    # push all the nodes back to the open list and return the result
    while copy_open:
        to_push = hq.heappop(copy_open)
        hq.heappush(open,to_push)
    return False


# The function implement uniform cost search algorithim
def find_ucs_rout(start, goal):
    # load the map
    roads = graph.load_map_from_csv()
    find_s = roads.junctions()[start]
    #initialize the first node
    start_node = Node(None, 0, start)
    start_node.parent = None
    # create list of visited nodes and add the first one
    visited = set()
    visited.add(start_node.index_num)
    # create list of open nodes and push the first one
    open = []
    hq.heappush(open, start_node)
    # while open is not empty
    while open:
        # pop the first one
        curr_node = hq.heappop(open)
        # check if this node is the goal
        if curr_node.index_num == goal:
            # return the path and  the cost
            cost = curr_node.cost
            result = create_succ(curr_node)
            return tuple(result)
        # add the node to the list
        visited.add(curr_node.index_num)
        # run over all the child of the node and check
        for link in roads.junctions()[curr_node.index_num].links:
            # create new node
            new_node = Node(curr_node.index_num, curr_node.cost + f(link), link.target)
            # if open and visited not contain this node, add and update the cost and the path
            if is_in_open(new_node, open) is False and new_node.index_num not in visited:
                new_node.parent = curr_node
                hq.heappush(open, new_node)
            # if this node in open and old cost < new cost
            elif is_in_open(new_node, open) is True:
                if new_node < find_node(new_node, open):
                    # create new node and replace between them , update the new cost function and the path
                    new_node = Node(curr_node.index_num, curr_node.cost + f(link), link.target)
                    new_node.cost = curr_node.cost + f(link)
                    new_node.parent = curr_node
                    open = change_cost(new_node, open)



# The function open problems file run over the 100 problem and write to the file the path and cost
def uniform_cost_search():
    file_open = open('problems.csv', 'r')
    file_write = open('results/UCSRuns.txt', 'w')
    line = file_open.readline()
    while line:
        split = line.split(',')
        start_index = int(split[0])
        split = split[1].split()
        goal_index = int(split[0])
        result = find_ucs_rout(start_index, goal_index)
        file_write.write(str(start_index) + " ")
        file_write.write(str(goal_index) + " ")
        file_write.write("cost is : " + str(result))
        file_write.write("\n")
        line = file_open.readline()


# The function get a link
# calculate and return the actually direction cost of a node by distance / max velocity in km
def f(link):
    type = link.highway_type
    return (link.distance / 1000) / info.SPEED_RANGES[type][1]


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


#uniform_cost_search()

