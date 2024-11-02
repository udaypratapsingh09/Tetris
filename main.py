import pygame,sys,random
from pygame.locals import *
import game_variables as gv
from Block import *

pygame.init()
win = pygame.display.set_mode(gv.win_size)
win.fill((15,15,15))
clock = pygame.time.Clock()

fontObj = pygame.font.SysFont("Sans sarif",24,True,False)

class Cell:
    def __init__(self,row,col,color="white",is_filled=0):
        self.is_filled=is_filled
        self.color = color
        self.row = row
        self.col = col
    def draw(self):
        pygame.draw.rect(win,self.color,(gv.GRID_X+self.col*gv.TOTAL_WIDTH,gv.GRID_Y+self.row*gv.TOTAL_WIDTH,gv.WIDTH,gv.WIDTH))

def update_score(lines_cleared):
    gv.score += gv.score_add[lines_cleared-1]
# Saves a block to the grid once it can no longer move
def is_game_over(block,grid):
    if block.row>0:
        return False
    for i in range(block.l):
        for j in range(block.l):
            if block.shape[i][j]==1 and grid[block.row+i][block.col+j].is_filled:
                return True
    return False

def save_to_grid(block):
    for i in range(block.l):
        for j in range(block.l):
            if block.shape[i][j]==1:
                c = grid[block.row+i][block.col+j]
                c.is_filled = 1
                c.color = block.color

def create_cells():
    grid = []
    for i in range(gv.ROWS):
        grid.append([])
        for j in range(gv.COLS):
            cell = Cell(i,j)
            grid[i].append(cell)
    return grid

grid = create_cells()

def draw_grid():
    for row in grid:
        for cell in row:
            cell.draw()

def clear_line(index):
    for i in range(index,0,-1):
        for j in range(gv.COLS):
            grid[i][j].is_filled = grid[i-1][j].is_filled
            grid[i][j].color = grid[i-1][j].color

    for i in range(gv.COLS):
        grid[0][i].is_filled=0
        grid[0][i].color="white"

def check_clear():
    # Checks if there is a row on grid which has to be cleared
    # and returns the number of lines to clear
    # Also calls clear function for each row that is to be cleared
    lines_cleared = 0
    for i in range(gv.ROWS):
        for j in range(gv.COLS):
            if not grid[i][j].is_filled:
                break
        else:
            lines_cleared+=1
            clear_line(i)
    if lines_cleared:
        update_score(lines_cleared)

def draw_score():
    score_text = fontObj.render("Score: ",True,"White",(15,15,15))
    score_text_rect = score_text.get_rect()
    score_text_rect.bottomleft = (gv.SCORE_BOARD_X,gv.SCORE_BOARD_Y-20)
    win.blit(score_text,score_text_rect)

    score_value = fontObj.render(str(gv.score),True,"White",(15,15,15))
    score_value_rect = score_value.get_rect()
    score_value_rect.topleft = (gv.SCORE_BOARD_X,gv.SCORE_BOARD_Y)
    win.blit(score_value,score_value_rect)

def draw_next(next_block):
    text = fontObj.render("NEXT",True,"White",(15,15,15))
    text_rect = text.get_rect()
    text_rect.bottomleft = (gv.NEXT_X,gv.NEXT_Y-20)
    win.blit(text,text_rect)
    color = next_block.color
    # draws the container
    pygame.draw.rect(win,"black",(gv.NEXT_X,gv.NEXT_Y,gv.TOTAL_WIDTH*4,gv.TOTAL_WIDTH*4))
    for i in range(next_block.l):
        for j in range(next_block.l):
            if next_block.shape[i][j]==1:
                pygame.draw.rect(win,color,(gv.NEXT_X+j*gv.TOTAL_WIDTH,gv.NEXT_Y+i*gv.TOTAL_WIDTH,gv.WIDTH,gv.WIDTH))

block,next_block = get_blocks()

def draw_blocks(block):
    block.draw(win)
    # gv.frames can exceed fall rate while down key is held as it reduces fall rate to one-third
    if gv.frames >= gv.FALL_RATE:
        block.down(grid)
        gv.frames = 0

while True:
    if gv.game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        continue
    key = pygame.key.get_pressed()
    if key[K_DOWN]:
        gv.FALL_RATE = gv.DEF_FALL_RATE//gv.SPEED_FACTOR
    else:
        gv.FALL_RATE = gv.DEF_FALL_RATE
    if key[K_RIGHT]:
        gv.r_counter += 1
        if gv.r_counter == gv.SLIDE_RATE:
            block.right(grid)
            gv.r_counter = 0
    elif key[K_LEFT]:
        gv.l_counter += 1
        if gv.l_counter == gv.SLIDE_RATE:
            block.left(grid)
            gv.l_counter = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                block.rotate(grid)

    if not block.can_move:
        # to save block to grid once it can no longer move
        save_to_grid(block)
        check_clear()
        gv.game_over = is_game_over(block,grid)
        block,next_block = get_blocks()


    gv.frames+=1
    draw_grid()
    draw_blocks(block)
    draw_next(next_block)
    draw_score()
    pygame.display.update()
    clock.tick(gv.FPS)