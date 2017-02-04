from robot import Robot
from constants import Actions, TileType
import random
import time

##########################################################################
# One of your team members, Chris Hung, has made a starter bot for you.  #
# Unfortunately, he is busy on vacation so he is unable to aid you with  #
# the development of this bot.                                           #
#                                                                        #
# Make sure to read the README for the documentation he left you         #
#                                                                        #
# @authors: christoh, [TEAM_MEMBER_1], [TEAM_MEMBER_2], [TEAM_MEMBER_3]  #
# @version: 2/4/17                                                       #
#                                                                        #
# README - Introduction                                                  #
#                                                                        #
# Search the README with these titles to see the descriptions.           #
##########################################################################

# !!!!! Make your changes within here !!!!!
class player_robot(Robot):
    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        ##############################################
        # A couple of variables - read what they do! # 
        #                                            #
        # README - My_Robot                          #
        ##############################################
        self.time_turn_back = 500
        self.direction = self.random_dir()
        self.toHome = []
        self.turns_left = 1000
        self.numturns = 0            
        self.goinghome = False;      
        self.targetPath = None
        self.targetDest = (0,0)

    def random_dir(self):
        self.directions =[(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        return self.directions[random.randint(0, len(self.directions)-1)]

    # A couple of helper functions (Implemented at the bottom)
    def OppositeDir(self, direction):
        return # See below

    def ViewScan(self, view):
        return # See below

    def FindRandomPath(self, view):
        return # See below

    def UpdateTargetPath(self):
        return # See below

    ###########################################################################################
    # This function is called every iteration. This method receives the current robot's view  #
    # and returns a tuple of (move_action, marker_action).                                    #
    #                                                                                         #
    # README - Get_Move                                                                       #
    ###########################################################################################
    def get_move(self, view):
        self.turns_left -= 1

        if(self.storage_remaining() == 0):
            self.goinghome = True

        if(self.turns_left == 975):
            self.direction = self.random_dir()
        if(self.turns_left % 100 == 0):
            self.direction = self.random_dir()
        
        if(self.turns_left > self.time_turn_back):
            # Search for resources

            viewLen = len(view)
            score = 0
            # Run BFS to find closest resource
            
            # Updates self.targetPath, self.targetDest
            self.ViewScan(view)
            
            # If you can't find any resources...go in a random direction!
            actionToTake = None
            if(self.targetPath == None):
                #actionToTake = self.FindRandomPath(view)
                actionToTake = self.DirectionPath(view)

            # Congrats! You have found a resource
            elif(self.targetPath == []):
                self.targetPath = None
                return (Actions.MINE, Actions.DROP_NONE)
            else:
                # Use the first coordinate on the path as the destination , and action to move
                actionToTake = self.UpdateTargetPath()
            self.toHome.append(actionToTake)
            #markerDrop = random.choice([Actions.DROP_RED,Actions.DROP_YELLOW,Actions.DROP_GREEN,Actions.DROP_BLUE,Actions.DROP_ORANGE])
            markerDrop = Actions.DROP_NONE
            assert(isinstance(actionToTake, int))
            return (actionToTake, markerDrop)
        else:
            self.goinghome = True
        if(self.goinghome):
            #go home
            # You are home
            if(self.toHome == []):
                self.goinghome = False
                self.time_turn_back = self.turns_left / 2
                return (Actions.DROPOFF, Actions.DROP_NONE)
            # Trace your steps back home
            prevAction = self.toHome.pop()
            revAction = self.OppositeDir(prevAction)
            assert(isinstance(revAction, int))
            return (revAction, Actions.DROP_NONE)

    def avoidObstacles(self, view, direction): # avoids obstacles
        viewLen = len(view)
        if direction == (0, 1):
            new = Actions.MOVE_SW
            if (view[viewLen//2+1][viewLen//2-1][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (-1, 1))
        elif direction == (-1, 1):
            new = Actions.MOVE_W
            if (view[viewLen//2][viewLen//2-1][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (-1, 0))
        elif direction == (-1, 0):
            new = Actions.MOVE_NW
            if (view[viewLen//2-1][viewLen//2-1][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (-1, -1))
        elif direction == (-1, -1):
            new = Actions.MOVE_N
            if (view[viewLen//2-1][viewLen//2][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (0, -1))
        elif direction == (0, -1):
            new = Actions.MOVE_NE
            if (view[viewLen//2-1][viewLen//2+1][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (1, -1))
        elif direction == (1, -1):
            new = Actions.MOVE_E
            if (view[viewLen//2][viewLen//2+1][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (1, 0))
        elif direction == (1, 0):
            new = Actions.MOVE_SE
            if (view[viewLen//2+1][viewLen//2+1][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (1, 1))
        else:
            new = Actions.MOVE_S
            if (view[viewLen//2+1][viewLen//2][0].CanMove()):
                return new
            else:
                return self.avoidObstacles(view, (0, 1))
    
    def get_dir(self):
        actionToTake = Actions.MOVE_S
        if(self.direction == (1,0)):
            actionToTake = Actions.MOVE_E
        elif(self.direction == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.direction == (0,1)):
            actionToTake = Actions.MOVE_S
        elif(self.direction == (-1,1)):
            actionToTake = Actions.MOVE_SW
        elif(self.direction == (-1,0)):
            actionToTake = Actions.MOVE_W
        elif(self.direction == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.direction == (0,-1)):
            actionToTake = Actions.MOVE_N
        elif(self.direction == (1,-1)):
            actionToTake = Actions.MOVE_NE
        return actionToTake
    
    def DirectionPath(self, view):
        if(view[self.get_fov()//2 + self.direction[1]][self.get_fov()//2 + self.direction[0]][0].CanMove()):
            return self.get_dir()
        else:
            while(not view[self.get_fov()//2 + self.direction[1]][self.get_fov()//2 + self.direction[0]][0].CanMove()):
                self.direction = self.random_dir()
            return self.get_dir()
        #return self.avoidObstacles(view, self.direction)
    
    # Returns opposite direction
    def OppositeDir(self, prevAction):
        if(prevAction == Actions.MOVE_N):
            return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE):
            return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E):
            return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE):
            return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S):
            return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW):
            return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W):
            return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW):
            return Actions.MOVE_SE
        else:
            return Actions.MOVE_S

    def get_direction_from_bias(self, bias):
        actionToTake = Actions.MOVE_N
        if(bias == [1,0]):
            actionToTake = Actions.MOVE_S
        elif(bias == [1,1]):
            actionToTake = Actions.MOVE_SE
        elif(bias == [0,1]):
            actionToTake = Actions.MOVE_E
        elif(bias == [-1,1]):
            actionToTake = Actions.MOVE_NE
        elif(bias == [-1,0]):
            actionToTake = Actions.MOVE_N
        elif(bias == [-1,-1]):
            actionToTake = Actions.MOVE_NW
        elif(bias == [0,-1]):
            actionToTake = Actions.MOVE_W
        elif(bias == [1,-1]):
            actionToTake = Actions.MOVE_SW
        return actionToTake
            
    def sign(self, val):
        if(val > 0):
            return 1
        elif(val < 0):
            return -1
        else:
            return 0
        
    def disperse(self, view):
        bias = [0, 0]
        for x in range(0, self.get_fov()):
            for y in range(0, self.get_fov()):
                num_robots = view[x][y][1]
                vector = (-x + self.get_fov() // 2, -y + self.get_fov() // 2)
                if(num_robots > 1 and vector == (0, 0)):
                    bias[0] += random.randint(-10, 10)
                    bias[1] += random.randint(-10, 10)
                bias[0] += vector[0]# * num_robots
                bias[1] += vector[1]# * num_robots
        bias[0] = self.sign(bias[0])
        bias[1] = self.sign(bias[1])
        return self.get_direction_from_bias(bias)
                
    
    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))

        targetDepleted = (view[self.targetDest[0]][self.targetDest[1]][0].GetType() == TileType.Resource and
                         view[self.targetDest[0]][self.targetDest[1]][0].AmountRemaining() <= 0)

        # BFS TO find the next resource within your view
        if(self.targetPath == None or targetDepleted):
            while(len(queue)>0):
                path = queue[0]
                loc = path[0]
                queue = queue[1:]
                viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
                if (view[viewIndex[0]][viewIndex[1]][0].GetType() == TileType.Resource and
                    view[viewIndex[0]][viewIndex[1]][0].AmountRemaining() > 0):
                    # print(path)
                    self.targetPath = path[1:]
                    self.targetDest = path[0]
                    return
                elif(view[viewIndex[0]][viewIndex[1]][0].CanMove()):
                    for i in range(8):
                        x = loc[0] + deltas[i][0]
                        y = loc[1] + deltas[i][1]
                        if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                            if((x,y) not in visited):
                                queue.append([(x,y)] + path[1:] + [deltas[i]])
                                visited.add((x,y))

        return

    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        viewLen = len(view)

        while(True):
            actionToTake = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                                          Actions.MOVE_S,Actions.MOVE_W,
                                          Actions.MOVE_NW,Actions.MOVE_NE,
                                          Actions.MOVE_SW,Actions.MOVE_SE])
            if ((actionToTake == Actions.MOVE_N and view[viewLen//2-1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_S and view[viewLen//2+1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_E and view[viewLen//2][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_W and view[viewLen//2][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NW and view[viewLen//2-1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NE and view[viewLen//2-1][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SW and view[viewLen//2+1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SE and view[viewLen//2+1][viewLen//2+1][0].CanMove()) ):
               return actionToTake

        return None

    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]

        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW

        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path    
        self.targetPath = self.targetPath[1:]

        return actionToTake

