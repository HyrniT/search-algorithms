from asyncio import run_coroutine_threadsafe
from operator import ne
from platform import node
from re import X
from Space import *
from Constants import *
import math

def DFSUtil(g:Graph, node:Node, closed_set:list, open_set:list, father:list, sc:pygame.Surface):
    closed_set.append(node.value)
    node.set_color(blue)
    temp = g.start
    if g.is_goal(node):
        node.set_color(purple)
        temp.set_color(orange)
        g.draw(sc)
        return True
    for neighbor in g.get_neighbors(node):
        if neighbor.value not in closed_set:
            father[neighbor.value] = node
            open_set.append(neighbor)
            neighbor.set_color(yellow)
            for nodes in g.get_neighbors(neighbor):
                if nodes not in closed_set:
                    if nodes not in open_set:
                        nodes.set_color(red)
            g.draw(sc)
            if DFSUtil(g, neighbor, closed_set, open_set, father, sc):
                return True
    return False

def DFS(g:Graph, sc:pygame.Surface):
    print('Implement DFS algorithm')
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    DFSUtil(g, g.start, closed_set, open_set, father, sc)
    temp = g.goal
    pygame.draw.line(sc, green, [temp.x, temp.y],
                     [father[temp.value].x, father[temp.value].y], 3)
    while father[temp.value] != g.start:
        temp = father[temp.value]
        temp1 = father[temp.value]
        pygame.draw.line(sc, green, [temp.x, temp.y], [temp1.x, temp1.y], 3)
        temp.set_color(grey)
        g.draw(sc)
    # raise NotImplementedError('Not implemented')

def BFS(g:Graph, sc:pygame.Surface):
    print('Implement BFS algorithm')
    open_set = [g.start]
    closed_set = []
    father = [-1]*g.get_len()
    res = g.start
    for node in open_set:
        closed_set.append(node)
        node.set_color(yellow)
        if g.is_goal(node):
            node.set_color(purple)
            res.set_color(orange)
            g.draw(sc)
            break
        for neighbor in g.get_neighbors(node):
            if neighbor not in closed_set:
                if neighbor not in open_set:
                    father[neighbor.value] = node
                    open_set.append(neighbor)
                    neighbor.set_color(red)
                    g.draw(sc)
        node.set_color(blue)
        g.draw(sc)
    temp = g.goal
    pygame.draw.line(sc, green, [temp.x, temp.y],
                     [father[temp.value].x, father[temp.value].y], 3)
    while father[temp.value] != g.start:
        temp = father[temp.value]
        temp1 = father[temp.value]
        pygame.draw.line(sc, green, [temp.x, temp.y], [temp1.x, temp1.y], 3)
        temp.set_color(grey)
        g.draw(sc)
    # raise NotImplementedError('Not implemented')

def sort(arr):
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j][0] > arr[j + 1][0]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if not swapped:
            return

def checkQueue(queue_set:list, nd_arr:Node):
    for item in queue_set:
        if nd_arr == item[1]:
            return False
    return True

def UCS(g:Graph, sc:pygame.Surface):
    print('Implement UCS algorithm')
    open_set = {}
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0
    open_set = [(cost[g.start.value], g.start)]
    res = g.start
    while len(open_set) > 0:
        node = open_set.pop(0)
        closed_set.append(node[1])
        node[1].set_color(yellow)
        g.draw(sc)
        if g.is_goal(node[1]):
            node[1].set_color(purple)
            res.set_color(orange)
            g.draw(sc)
            break
        sort(open_set)
        # open_set.sort(key = lambda x: x[0])
        for neighbor in g.get_neighbors(node[1]):
            cost[neighbor.value] = cost[node[1].value] + 1
            
            if neighbor not in closed_set :
                if checkQueue(open_set, neighbor):
                    father[neighbor.value] = node[1]
                    open_set.append([cost[neighbor.value], neighbor])
                    neighbor.set_color(red)
                    # g.draw(sc)
        node[1].set_color(blue)        
    temp = g.goal
    pygame.draw.line(sc, green, [temp.x, temp.y],
                     [father[temp.value].x, father[temp.value].y], 3)
    while father[temp.value] != g.start:
        temp = father[temp.value]
        temp1 = father[temp.value]
        pygame.draw.line(sc, green, [temp.x, temp.y], [temp1.x, temp1.y], 3)
        temp.set_color(grey)
        g.draw(sc)
    # raise NotImplementedError('Not implemented')

def heuristic(nd1:Node, nd2:Node):
    return int(math.sqrt((nd1.x - nd2.x)**2 + (nd1.y - nd2.y)**2))

def AStar(g:Graph, sc:pygame.Surface):
    print('Implement A* algorithm')
    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0
    open_set = [[cost[g.start.value] + heuristic(g.start, g.goal), g.start]]
    res = g.start
    for node in open_set:
        closed_set.append(node[1])
        if g.is_goal(node[1]):
            node[1].set_color(purple)
            res.set_color(orange)
            g.draw(sc)
            break
        sort(open_set)
        min_h = 10**8
        cur_node = node[1]
        for neighbor in g.get_neighbors(node[1]):
            if neighbor not in closed_set:
                neighbor.set_color(red)
                g.draw(sc)
            cost[neighbor.value] = cost[node[1].value] + 1
            temp_h = cost[neighbor.value] + heuristic(neighbor, g.goal)
            if temp_h < min_h:
                min_h = temp_h
                cur_node = neighbor
        if cur_node not in closed_set:
            father[cur_node.value] = node[1]
            open_set.append([cost[cur_node.value] + min_h, cur_node])
            cur_node.set_color(yellow)
            g.draw(sc)
        node[1].set_color(blue)
        g.draw(sc)    
    temp = g.goal
    pygame.draw.line(sc, green, [temp.x, temp.y],
                     [father[temp.value].x, father[temp.value].y], 3)
    while father[temp.value] != g.start:
        temp = father[temp.value]
        temp1 = father[temp.value]
        pygame.draw.line(sc, green, [temp.x, temp.y], [temp1.x, temp1.y], 3)
        temp.set_color(grey)
        g.draw(sc)
    # raise NotImplementedError('Not implemented')