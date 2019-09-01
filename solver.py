from node import Node
import heapq
import queue
import time
import sys


# Heuristic functions 
def manhattan_distance_basic(node):

    total_distance = 0
    target_positions = set()    # Set to hold all target positions
    box_positions = set()       # Set to hold all box positions 

    # Iterate the board and fill position sets
    for r,row in enumerate(node.board): 
        for c, char in enumerate(row):
            if char == 'p' or char == 'T' or char == 'b':
                target_positions.add((r,c))
            if char == 'B' or char == 'b':
                box_positions.add((r,c))

    for box in box_positions:                                   # For each box
        distances = []                                          # List for distances to all targets for a given box
        for target in target_positions:
            distances.append(abs(box[0] - target[0]) + abs(box[1] - target[1]))
        total_distance = total_distance + min(distances)        # Add the shorest possible distance to total_distance

    return total_distance

# Search algorithms to traverse the graph
def a_star(boardstring, heuristic):
    start_time = time.time()
    explored = set()
    pq = []

    # Initialize start_node
    start_node = Node(boardstring, "")
    start_node.deadlocks = Node.simple_deadlocks(start_node.board) # Set a predetermined set of basic deadlocks
    heapq.heappush(pq, start_node)

    while pq:
        node = pq.pop(0)

        # Already checked an equal node    
        if(node.ID in explored):
          continue

    
        # Break if we find a solution
        if node.goal_state():
            break

        explored.add(node.ID)    
        # Add all child nodes to the graph
        for n in node.next_state():
            if not (n.ID in explored):
                n.cost = n.cost + heuristic(node) # Add an estimated cost 
                pq.append(n)

        heapq.heapify(pq)

    # Calculate and print the time used 
    endtime = time.time()
    minutes, seconds = divmod(endtime - start_time, 60)
    print("Generated: {}\nFringe: {}\nExplored: {}\nTime: {:0>2} minutes and {:0>2.3f} seconds".format(len(explored)+len(pq), len(pq), len(explored),int(minutes), seconds))

    # Return the path to the goal_state
    path = ','.join([i for i in node.path])
    return path

def uniform_cost_search(boardstring):
    start_time = time.time()
    start_node = Node(boardstring, "")
    explored = set()
    start_node.deadlocks = Node.simple_deadlocks(start_node.board)
    pq = []
    heapq.heappush(pq, start_node)
    counter = 0

    while pq:
        heapq.heapify(pq)
        node = heapq.heappop(pq)
        if node.goal_state():
            break

        explored.add(node.ID)
        for node in node.next_state():
            if  node not in pq and node.ID not in explored and node not in start_node.deadlocks:
                heapq.heappush(pq,node)
                counter += 1

    # Calculate and print the time used 
    endtime = time.time()
    minutes, seconds = divmod(endtime - start_time, 60)
    print("Generated: {}\nFringe: {}\nExplored: {}\nTime: {:0>2} minutes and {:0>2.3f} seconds".format(len(explored)+len(pq), len(pq), len(explored),int(minutes), seconds))

    # Return the path to the goal_state
    path = ','.join([i for i in node.path])
    return path



if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    f = open(inputfile, 'r')
    boardstring = f.read()
    solution = a_star(boardstring,manhattan_distance_basic)
    #solution = uniform_cost_search(boardstring)

    f.close

    f2 = open(outputfile,'w')
    f2.write(solution)
    f2.close