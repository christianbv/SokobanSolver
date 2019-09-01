import copy
import queue


"""Class to repsent a given boardstate. 
   It has an unique ID to represent all boardstates with the same rock formation
   and where the players has access to the same free space """
class Node:
    
    #Check if node is a goal_state
    def goal_state(self):
        return 'B' not in self.boardstring
    
        
    # Functions to pregenerate standard deadlockpatterns   
    @staticmethod  
    def simple_deadlocks(board):
        targetList = []
        positionSet = set(())
        deadLockSet = set(())

        def freeDeadLockMoves(board,boxMove,playerMove):
            try:
                box = board[boxMove[0]][boxMove[1]]
                player = board[playerMove[0]][playerMove[1]]
                return box != '#' and player != '#'
            except IndexError:
                return False

        for row in range(1,len(board)-1):
            for col in range(1,len(board[row])-1):
                c = board[row][col]
                if (c == 'T' or c == 'b' or c == 'p'):
                    targetList.append((row,col))
                if c != '#':
                    deadLockSet.add((row,col))

        for target in targetList:
            positionSet.add(target)

            tempQueue = queue.Queue(maxsize=0)
            tempQueue.put(target)
            while not tempQueue.empty():
                currPos = tempQueue.get()

                playerDir = [(-2, 0), (2, 0), (0, 2), (0, -2)]  # The directions to explore
                boxDir = [(-1, 0), (1, 0), (0, 1), (0, -1)]

                for dir in range(0,len(boxDir)):
                    boxPos = (currPos[0]+boxDir[dir][0],currPos[1]+boxDir[dir][1])
                    playerPos = (currPos[0]+playerDir[dir][0],currPos[1]+playerDir[dir][1])

                    if(freeDeadLockMoves(board,boxPos,playerPos) and boxPos not in positionSet):
                        tempQueue.put(boxPos)
                        positionSet.add(boxPos)
                    

        deadLockSet = deadLockSet.difference(positionSet)
        return deadLockSet
        
   
    # self.cost
    # self.path 
    # self.ID
    # self.board
    # self.boardstring 
    # self.deadlocks
    def __init__(self, boardstring, path, simple_deadlocks=set()):
        
        # Hashes a board [['char']] --> ID 11B11B131B111B22B11B11
        def boardToID(self,board):
            pos = self.player_position
            IDstring = "{}{}".format(pos[0],pos[1])
            for r,row in enumerate(board):
                for c, char in enumerate(row):
                    if char == 'b' or char == 'B':
                        IDstring = IDstring + "B" + str(r) + str(c)

            return IDstring

        # Finds the players position    
        def find_player_position(self):
            for v,row in enumerate(self.board):
                for c,char in enumerate(row):
                    if char == 'p' or char =='P':
                        return (v,c)

        #Initialize the board [[]]
        self.boardstring = boardstring
        self.board = []
        for line in boardstring.split('\n'):
            self.board.append(list(line.strip()))
        
        # Variables             
        self.path = path                                    
        self.cost = len(path)
        self.player_position = find_player_position(self) 
        self.ID = boardToID(self, self.board)
        self.deadlocks = simple_deadlocks # Set of deadlock positions
    
   
    # Returns a dictionary with all possible player posistions --> {(x,y):"path" , (x,y):"path"}
    def getPossiblePlayerPositions(self):

        positions = {}                              # Collection of discovered positions
        q = queue.Queue(maxsize=0)                  # creates an empty queue
        q.put(self.player_position)                 # adds the startposition to the queue
        positions.update({self.player_position:""}) # adds the startposition to the dict

        while not q.empty():
            currPos = q.get()

            dir = {(-1,0):"u",(1,0):"d",(0,1):"r",(0,-1):"l"}

            for k,v in dir.items():
                dirVal = (k[0]+currPos[0],k[1]+currPos[1])

                if self.is_free_cell(dirVal) and (dirVal not in positions):
                    foo = str(positions.get(currPos))
                    path = foo + v
                    if foo == None:
                        path = v
                    newPos = {dirVal:path}
                    positions.update(newPos)
                    q.put(dirVal)
                else:
                    continue

        return positions

    # Takes in a given cordniate (x,y) and checks if there is an obstacle 
    def is_free_cell(self,move):
        c = self.board[move[0]][move[1]]
        return c != '#' and c != 'B' and c != 'b'

    # Check if square is a #
    def is_blocked(self,x,y):
        c = self.board[x][y]
        return c == '#'

    # Returns a set of all new states(nodes) which can be reached, filters on deadlocks
    def next_state(self):
        directions = {(-1,0):'u',(0,1):'r',(1,0):'d',(0,-1):'l'} 
        states = set()                                                                         # Dictionary { next_state:cost_to_get_there, .... }
        ppp = self.getPossiblePlayerPositions()
        for r,row in enumerate(self.board):                                                 # Iterate through the board 
            for c,char in enumerate(row):
                if char == 'b' or char == 'B':                                              # If we found a box 
                    for dir in directions.keys():
                        player_side = (r + dir[0]*-1, c + dir[1]*-1)                        # Put player on one side
                        opposite_side = (r + dir[0], c + dir[1])                            # Define the opposite_side of player
                        if opposite_side in self.deadlocks:                          
                            continue                            
                        if player_side in ppp and self.is_free_cell(opposite_side):         # If player can get to player_side and opposite_side is free 
                            new_boardstring = self.alter_board((r,c), dir)                  # Alter_board pushes the box and returns a new boardstring        
                            new_path = self.path + ppp.get(player_side) + directions.get(dir)
                            new_node = Node(new_boardstring,new_path, self.deadlocks)
                            if not new_node.is_double_deadlock(opposite_side[0], opposite_side[1]):                           # Does a search for typical double deadlock
                                states.add(new_node)    
                                                                  
        return states                    
   
    
    #Takes the current board and moves stone on 'pos' in direction 'dir' --> returns a new boardstring                      
    def alter_board(self, box_pos, dir):
        new_board = copy.deepcopy(self.board) # Deepcopy so we dont alter the original board 

        # Check which symbol was on original board and based on this decides new symbol (for example if the stone was on a target the player is now on a target)
        new_board[self.player_position[0]][self.player_position[1]] =  ' ' if self.board[self.player_position[0]][self.player_position[1]] == 'P' else 'T' 
        new_board[box_pos[0]][box_pos[1]] = 'P'                            if self.board[box_pos[0]][box_pos[1]] == 'B' else 'p'
        new_board[box_pos[0] + dir[0]][box_pos[1]+ dir[1]] = 'b'           if self.board[box_pos[0] + dir[0]][box_pos[1] + dir[1]] in {'T','p'}  else 'B'

        # Join the rows to a string
        for i in range(len(new_board)):
            new_board[i] = "".join(new_board[i])

        # Join the collums
        new_boardstring = '\n'.join(new_board)
        return new_boardstring 

    # Tostring function for path, cost and boardstring
    def __repr__(self):
        return "\n\nPath from start: {} (lenght = {}, cost = {})\nBoardstirng:{}\n{}\n ".format(self.path, len(self.path),self.cost, self.ID, self.boardstring)
    
    # For selfcomparing, used in priority queue
    def __lt__(self, other):
        return (self.cost  < (other.cost ))

    # Detect if doubble stone deadlock after push
    def is_double_deadlock(self,x,y):
        directions = {(-1,0), (1,0), (0,-1),(0,1)}
        for dir in directions:
            c = self.board[x + dir[0]][y + dir[1]]
            # If we find a stone
            if c == 'B' or (c == 'b' and self.board[x][y] != 'b'):
                # Check sides
                if dir[1] == 0: #The stones are in the vertical plane
                    pos1 = (x,y+1)
                    pos2 = (x+dir[0],y+1)
                    pos3 = (x,y-1)
                    pos4 = (x+dir[0],y-1)
                    if not (self.is_free_cell(pos1) or self.is_free_cell(pos2)):
                        return True
                    if not (self.is_free_cell(pos3) or self.is_free_cell(pos4)):
                        return True

                elif dir[0] == 0: # The stones are in the horisontal plane
                    pos1 = (x+1,y)
                    pos2 = (x+1, y+dir[1])
                    pos3 = (x-1,y)
                    pos4 = (x-1,y+dir[1])
                    if not (self.is_free_cell(pos1) or self.is_free_cell(pos2)):
                        return True
                    if not (self.is_free_cell(pos3) or self.is_free_cell(pos4)):
                        return True
        return False               


