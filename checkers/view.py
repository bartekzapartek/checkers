import pygame

class View:
    SQUARE_WHITE_COLOR = (255, 255, 255)
    SQUARE_BLACK_COLOR = (0, 0, 0)

    PAWN_PLAYER_ONE_COLOR = (208, 73, 0)
    PAWN_PLAYER_TWO_COLOR = (0, 73, 200)
    SELECTED_PAWN_COLOR = (100, 100, 100)
    VALID_MOVE_COLOR = (255, 255, 255)


    def __init__(self, window_size, rows, cols):
        self.window_size = window_size

        self.rows = rows
        self.cols = cols

        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.tick_rate = 120

        self.square_size = self.window_size // self.cols
        self.pawn_size = round(self.square_size / 2.5)

    def draw(self, board):
        self.clock.tick(self.tick_rate)

        self._draw_board()
        self._draw_pawns(board)

        pygame.display.update()
        self.window.fill(self.SQUARE_BLACK_COLOR)

    def _draw_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (col + row) % 2:
                    pygame.draw.rect(self.window, self.SQUARE_BLACK_COLOR, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
                elif (col + row + 1) % 2:
                    pygame.draw.rect(self.window, self.SQUARE_WHITE_COLOR, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def _draw_pawns(self, board):
        for row in range(self.rows):
            for col in range(self.cols):
                pawn = board.get_pawn(col, row)
                if pawn != 0:
                    x, y = self._calculate_pawn_pos(col, row)
                    if pawn.player == 1:
                        pygame.draw.circle(self.window, self.PAWN_PLAYER_ONE_COLOR, (x + self.square_size // 2, y + self.square_size // 2), self.pawn_size)

                    elif pawn.player == 2:
                        pygame.draw.circle(self.window, self.PAWN_PLAYER_TWO_COLOR, (x + self.square_size // 2, y + self.square_size // 2), self.pawn_size)

                    if pawn.selected:
                        pygame.draw.circle(self.window, self.SELECTED_PAWN_COLOR, (x + self.square_size // 2, y + self.square_size // 2), self.pawn_size + 5, 1)
                        self._draw_valid_moves(board, pawn)
                    if pawn.king:
                        for radius_dec in range (6):
                            pygame.draw.circle(self.window, self.SQUARE_BLACK_COLOR,
                                               (x + self.square_size // 2, y + self.square_size // 2), self.pawn_size - radius_dec**2, 2)

    def _draw_valid_moves(self, board, pawn):
        for move, _ in pawn.valid_moves.items():
            pygame.draw.circle(self.window, self.VALID_MOVE_COLOR, (move[0] * self.square_size + self.square_size // 2, move[1] * self.square_size + self.square_size // 2), self.pawn_size // 5)

    def _calculate_pawn_pos(self, col, row):
        x = col * self.square_size
        y = row * self.square_size

        return x, y