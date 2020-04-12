'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv

# The function return a dictionary containing the desired information
def map_statistics(roads):
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions' : len(roads.junctions()),
        'Number of links' : sum_of_links(roads),
        'Outgoing branching factor' : Stat(max = find_max_son(roads), min = find_min_son(roads), avg = find_avg_son(roads)),
        'Link distance' : Stat(max = find_distance(roads, 2), min = find_distance(roads, 1), avg = find_distance(roads, 3)),
        'Link type histogram' : sum_of_types(roads),
    }



# The functio calculate the Link type histogram
def sum_of_types(roads) :
    # initalize a dictionary
    types_dic = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
        9 : 0,
        10 : 0,
        11 : 0,
        12 : 0
    }
    # run over all the junction and count the types
    for j in roads.junctions():
        for l in j.links:
            types_dic[l.highway_type] = types_dic[l.highway_type] + 1
    # return the update dictionary
    return types_dic



# The funcrion find the link distance
def find_distance(roads, option):
    min_d = roads.junctions()[0].links[0].distance
    max_d = 0
    # calculate minimum
    if option == 1:
        for j in roads.junctions():
            for l in j.links:
                if l.distance < min_d:
                    min_d = l.distance
        return min_d
    # calculate mazimum
    elif option == 2:
        for j in roads.junctions():
            for l in j.links:
                if l.distance > max_d:
                    max_d = l.distance
        return max_d
    # calculate average
    elif option == 3:
        avg_d = 0
        for j in roads.junctions():
            for l in j.links:
                avg_d = avg_d + l.distance
        avg_d = avg_d / sum_of_links(roads)
        return avg_d



# The function calculate the average of the sons
def find_avg_son(roads):
    return sum_of_links(roads) / len(roads.junctions())



# The function calculate the maximum of the sons
def find_max_son(roads):
    maximum = 0
    for son in roads.junctions():
        size_of_link = len(son.links)
        if size_of_link > maximum:
            maximum = size_of_link
    return maximum



# The function calculate the minimum of the sons
def find_min_son(roads):
    minimum = len(roads.junctions()[0])
    for son in roads.junctions():
        size_of_link = len(son.links)
        if size_of_link < minimum:
            minimum = size_of_link
    return minimum



# The function calculate sum of the links
def sum_of_links(roads):
    size_of_link = 0
    for j in roads.junctions():
        size_of_link = size_of_link + len(j.links)
    return size_of_link



def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))



if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
