import pygame

class Snake:
    def __init__(self, x, y, cell_size):
        self.cell_size = cell_size
        # body is a list of (x, y) grid-cell positions, head is body[0]
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = (1, 0)  # moving right
        self._pending_direction = None
        self.grow_pending = False

    def set_direction(self, dx, dy):
        new_direction = (dx, dy)
        if self._pending_direction is not None:
            return
        if new_direction not in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            return
        if new_direction == self.direction:
            return
        if new_direction == (-self.direction[0], -self.direction[1]):
            return
        self._pending_direction = new_direction

    def move(self):
        if self._pending_direction is not None:
            self.direction = self._pending_direction
            self._pending_direction = None

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def head_rect(self):
        x, y = self.body[0]
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def segment_rects(self):
        return [
            pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            for (x, y) in self.body
        ]

    def collides_with_self(self):
        head = self.body[0]
        return head in self.body[1:]

    def collides_with_wall(self, grid_width, grid_height):
        x, y = self.body[0]
        return x < 0 or y < 0 or x >= grid_width or y >= grid_height
