# SokobanSolver 
First assignment in AI, COMP3702 at University of Queensland, which was a group project with Adrian, Nils-Gunnar and Christian. 
The task was to create a Sokoban solver using Uniform-Cost-Search and A*. I mostly worked on implementing deadlock-detection
as well as different helping methods. 

This folder consist of two python files.

node.py:

The node class represent a state of the puzzle. With variables as path, cost, boardstring and player position it calculates the next possible states
and create new successor nodes.

search_algorithms.py:

This is the file to run to check for solutions in a sokoban puzzle
In console you can write: python search_algorithms.py "filename_of_sokoban_puzzle" "outfile_for_solution"
search_algorithms.py has three methods.
manhattan_distance(Node): method used as a heuristic for the Amethod
A(boardstring, heuristic): Does A star search on the sokoban puzzle, using the given heuristic
uniform_cost_search(Node): Tries to solve the puzzle (boardstring) using uniform cost search approach.

