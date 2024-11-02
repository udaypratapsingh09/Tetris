import pygame
from game_variables import *
from random import randint

class Block:
    def __init__(self,row,col,shape,color):
        self.row=row
        self.col=col
        self.shape = shape
        self.color = color
        self.can_move = True
        self.l = len(shape)
        self.offset = self.l-1
    def draw(self,surface):
        for i in range(self.l):
            for j in range(self.l):
                if self.shape[i][j]==1:
                    pygame.draw.rect(surface,self.color,(GRID_X+(self.col+j)*TOTAL_WIDTH,GRID_Y+(self.row+i-self.offset)*TOTAL_WIDTH,WIDTH,WIDTH))
    
    def down(self,grid):
        for i in range(self.l):
            for j in range(self.l):
                if self.shape[i][j]==1:
                    r = self.row+i+1
                    if r-self.offset>0:
                        r-=self.offset
                    if self.row+i==ROWS-1:
                        self.can_move = False
                        return 0
                    elif grid[r][self.col+j].is_filled:
                        self.can_move = False
                        return 0
        if self.offset:
            self.offset-=1
        else:
            self.row += 1
        return 1
    

    def right(self,grid):
        if not self.can_move:
            return 0
        # Wall jump
        flag = 1
        for i in range(self.l):
            if self.shape[i][self.l-1] == 1:
                flag = 0
                break
        if flag:
            self.col-=1
            for i in range(self.l):
                self.shape[i].pop(self.l-1)
                self.shape[i].insert(0,0)
        # 
        for i in range(self.l):
            for j in range(self.l):
                if self.shape[i][j]==1:
                    if self.col+j==COLS-1:
                        return 0
                    elif grid[self.row+i][self.col+j+1].is_filled:
                        return 0
        self.col += 1
        return 1
    

    def left(self,grid):
        if not self.can_move:
            return 0
        
        # Wall push
        flag = 1
        for i in range(self.l):
            if self.shape[i][0] == 1:
                flag = 0
                break
        if flag:
            self.col+=1
            for i in range(self.l):
                self.shape[i].pop(0)
                self.shape[i].append(0)
        # 
        for i in range(self.l):
            for j in range(self.l):
                if self.shape[i][j]==1:
                    if self.col+j==0:
                        return 0
                    elif grid[self.row+i][self.col+j-1].is_filled:
                        return 0
        self.col -= 1
        return 1
    
    def rotate(self,grid):
        rotated = [[0 for i in range(self.l)] for j in range(self.l)]
        for i in range(self.l):
            for j in range(self.l):
                rotated[self.l-j-1][i] = self.shape[i][j]
        # check if rotation is valid
        for i in range(self.l):
            for j in range(self.l):
                if grid[self.row+i][self.col+j].is_filled and rotated[i][j]:
                    return 0
        self.shape = rotated


shapes = [
[[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]],
[[1,1,0],[1,1,0],[0,0,0]],
[[0,1,0],[1,1,1],[0,0,0]],
[[1,0,0],[1,0,0],[1,1,0]],
[[0,1,0],[0,1,0],[1,1,0]],
[[1,0,0],[1,1,0],[0,1,0]],
[[0,1,0],[1,1,0],[1,0,0]]
]

def shuffle(b):
    for i in range(len(b)):
        j = randint(0,len(b)-1)
        b[i],b[j]=b[j],b[i]

colors = ("cyan","yellow","purple","orange","blue","green","red")
blocks = list(zip(shapes,colors))
b = blocks.copy()
shuffle(b)
next = b[0]
def get_blocks():
    global b,next,blocks
    current = next
    if len(b)==1:
        b = blocks.copy()
        shuffle(b)
        next = b[0]
    else:
        next = b[1]
    b.pop(0)
    block = Block(start_row,start_col,current[0],current[1])
    next_block = Block(start_row,start_col,next[0],next[1])
    return (block,next_block)
