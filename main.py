import pygame

size = (512,512)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Drawing Board. (PRESS ESC TO RUN) ")

drawing = True

column_count = 50
row_count = 50

cell_height = round(size[1]/row_count)
cell_width = round(size[0]/column_count)


grid = [[0 for x in range(column_count)] for y in range(row_count)]

def step_grid(old_grid):
    new_grid = []

    #input()
    for i in range(row_count):
        new_grid.append([])
        for j in range(column_count):
            total_neighbours = check_neighbours(old_grid,j,i)
            if old_grid[i][j]: # Alive
                if total_neighbours < 2:
                    new_grid[-1].append(0)
                elif total_neighbours == 2 or total_neighbours == 3:
                    new_grid[-1].append(1)
                elif total_neighbours > 3:
                    new_grid[-1].append(0)
                else:
                    new_grid[-1].append(0)
            else: # Dead
                if total_neighbours == 3:
                    new_grid[-1].append(1)
                else:
                    new_grid[-1].append(0)

    return new_grid

def render_grid(grid):
    for i in range(row_count):
        for j in range(column_count):
            if grid[i][j]:
                pygame.draw.rect(screen, (255,255,255), (cell_width*j,cell_height*i,cell_width,cell_height))
            else:
                pygame.draw.rect(screen, (0,0,0), (cell_width*j,cell_height*i,cell_width,cell_height))

def check_neighbours(grid,x,y):
    total_neighbours = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if (y+i < 0) or (y+i > row_count): continue
            if (x+j < 0) or (x+j > column_count): continue
            if (y+i == y) and (x+j == x): continue
            try:
                total_neighbours += grid[y+i][x+j]
            except:
                pass
    return total_neighbours

currentFPS = 800
while True:
    pygame.time.Clock().tick(currentFPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_caption("Running Game of Life... (UP AND DOWN CHANGE SPEED)")
                currentFPS = 10
                drawing = False

            if event.key == pygame.K_UP:
                currentFPS += 5
            if event.key == pygame.K_DOWN:
                currentFPS -= 5
                currentFPS = max(1,currentFPS)

    if (drawing):
        x_pos,y_pos = pygame.mouse.get_pos()
        
        x_index = int(x_pos//cell_width)
        y_index = int(y_pos//cell_height)

        if pygame.mouse.get_pressed()[0]: #LMB Down
            try:
                grid[y_index][x_index] = 1
            except:
                pass

        if pygame.mouse.get_pressed()[2]:
            try:
                grid[y_index][x_index] = 0
            except:
                pass
    else:
        grid = step_grid(grid)

    render_grid(grid)

    pygame.display.flip()
