import pygame
from checkers.view import View
from checkers.game import Game

class App:
    ROWS = 8
    COLS = 8

    def __init__(self, window_size):
        pygame.init()

        self.view = View(window_size, self.COLS, self.ROWS)
        self.game = Game(self.COLS, self.ROWS)

        self.square_size = window_size / self.ROWS

        self.run = True
        pygame.display.set_caption("checkers")

        self.mouse_pos = pygame.mouse.get_pos()

    def _update_mouse_pos(self):
        self.mouse_pos = pygame.mouse.get_pos()
        col, row = int(self.mouse_pos[0] // self.square_size), int(self.mouse_pos[1] // self.square_size)
        return col, row

    def _update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                col, row = self._update_mouse_pos()
                #self.game.on_mouse_pressed(col, row)
                self.game.change_turn()

        self.game.check_winner()

    def main(self):
        while self.run:
            self._update_events()
            self.view.draw(self.game.board)
