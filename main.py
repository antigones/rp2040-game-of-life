import time
from machine import Pin



class GameOfLife:

    def __init__(self, grid, n_gen):
        self.grid = grid
        self.n_gen = n_gen
        self.size_y = len(grid)
        self.size_x = len(grid[0])


    def count_alive_neighbours(self, on_grid, i, j):
        neighbors = [
            (i-1, j),   # n
            (i-1, j-1), # nw
            (i, j-1),   # w
            (i+1, j-1), # sw
            (i+1, j),   # s
            (i+1, j+1), # se
            (i, j+1),   # e
            (i-1, j+1)  # ne
            ]

        return sum(on_grid[x][y] == 1 for x, y in neighbors
                if 0 <= x < self.size_x and 0 <= y < self.size_y)


    def next_generation(self, on_grid):
        next_grid = [[0 for col in range(self.size_y)] for row in range(self.size_x)]
        for (i, j) in [(i, j) for i in range(self.size_y) for j in range(self.size_x)]:
            alive_n = self.count_alive_neighbours(on_grid, i, j)

            cur_cell = on_grid[i][j]
            if cur_cell == 1:
                if alive_n < 2:
                    next_grid[i][j] = 0
                if alive_n > 3:
                    next_grid[i][j] = 0
                if alive_n ==  2 or alive_n == 3:
                    next_grid[i][j] = 1
            else:
                if cur_cell == 0:
                    if alive_n == 3:
                        # current cell come alive
                        next_grid[i][j] = 1
                else:
                    next_grid[i][j] = 0
        return next_grid


    def generate_steps(self):
        steps = []
        step = self.grid
        steps.append(step)
        for _ in range(self.n_gen):
            step = self.next_generation(step)
            steps.append(step)
        return steps



def draw_glider(on_grid):
    on_grid[3][1] = 1
    on_grid[3][2] = 1
    on_grid[3][3] = 1
    on_grid[2][3] = 1
    on_grid[1][2] = 1


r5 = Pin(17, Pin.OUT)
r7 = Pin(18, Pin.OUT)
c2 = Pin(5, Pin.OUT)
c3 = Pin(7, Pin.OUT)
r8 = Pin(19, Pin.OUT)
c5 = Pin(4, Pin.OUT)
r6 = Pin(20, Pin.OUT)
r3 = Pin(21, Pin.OUT)

c8 = Pin(13, Pin.OUT)
c7 = Pin(12, Pin.OUT)
r2 = Pin(25, Pin.OUT)
c1 = Pin(29, Pin.OUT)
r4 = Pin(15, Pin.OUT)
c6 = Pin(28, Pin.OUT)
c4 = Pin(27, Pin.OUT)
r1 = Pin(16, Pin.OUT)

ordered_rows_pins = [r1, r2, r3, r4, r5, r6, r7, r8]
ordered_cols_pins = [c1, c2, c3, c4, c5, c6, c7, c8]

def clear_cols():
    for p in ordered_cols_pins:
        p.on()
def clear_rows():
    for p in ordered_rows_pins:
        p.off()

def clear():
    clear_cols()
    clear_rows()


clear()

size = 8
n_gen = 50
grid = [[0 for col in range(size)] for row in range(size)]
draw_glider(grid)
gol = GameOfLife(grid, n_gen)
steps = gol.generate_steps()
rows = len(grid)
cols = len(grid[0])

"""
# simpler but heavier, leds lightly lit
for step in steps:
    frame_start_time = time.ticks_ms()
    while time.ticks_ms() - frame_start_time < 1000:
        for x in range(rows):
             for y in range(cols):
                clear()
                if step[x][y] == 1:
                    p_row = ordered_rows_pins[x]
                    p_col = ordered_cols_pins[y]
                    p_row.on()
                    p_col.off()

"""

rows_and_cols_in_step = []
for step in steps:
    d = {}
    for x in range(rows):
        for y in range(cols):
            if step[x][y] == 1:
                if x in d.keys():
                    d[x].append(y)
                else:
                    d[x] = [y]
    rows_and_cols_in_step.append(d)

for row_and_col in rows_and_cols_in_step:
    clear()
    frame_start_time = time.ticks_ms()
    while time.ticks_ms()-frame_start_time < 1000:
        for x in row_and_col.keys():
            p_row = ordered_rows_pins[x]
            clear()
            p_row.on()
            cols = row_and_col[x]
            for y in cols:
                p_col = ordered_cols_pins[y]
                p_col.off()
