[Actions.MOVE_E,Actions.MOVE_N,
                                          Actions.MOVE_S,Actions.MOVE_W,
                                          Actions.MOVE_NW,Actions.MOVE_NE,
                                          Actions.MOVE_SW,Actions.MOVE_SE]
                                          
                                          
                                          
    def FindRandomPath(self, view):
        viewLen = len(view)


                                          
def avoidObstacles(self, direction):
    if direction == S:
        new = Actions.MOVE_SW
        if (view[viewLen//2+1][viewLen//2-1][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, SW)
    elif direction == SW:
        new = Actions.MOVE_W
        if (view[viewLen//2][viewLen//2-1][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, W)
    elif direction == W:
        new = Actions.MOVE_NW
        if (view[viewLen//2-1][viewLen//2-1][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, NW)
    elif direction == NW:
        new = Actions.MOVE_N
        if (view[viewLen//2-1][viewLen//2][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, N)
    elif direction == N:
        new = Actions.MOVE_NE
        if (view[viewLen//2-1][viewLen//2+1][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, NE)
    elif direction == NE:
        new = Actions.MOVE_E
        if (view[viewLen//2][viewLen//2+1][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, E)
    elif direction == E:
        new = Actions.MOVE_SE
        if (view[viewLen//2+1][viewLen//2+1][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, SE)
    else:
        new = Actions.MOVE_S
        if (view[viewLen//2+1][viewLen//2][0].CanMove()):
            return new
        else:
            return avoidObstacles(self, S)
        
