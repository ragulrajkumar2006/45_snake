import pygame
import random

class Food:
    def __init__(self, grid_width, grid_height, cell_size):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.x = 0
        self.y = 0
        self.respawn([])

    def respawn(self, occupied_cells):
        while True:
            self.x = random.randint(0, self.grid_width - 1)
            self.y = random.randint(0, self.grid_height - 1)
            if (self.x, self.y) not in occupied_cells:
                break

    def rect(self):
        return pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size)
