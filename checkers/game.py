from checkers.board import Board
from minimax.algorithm import minimax
import pygame

class Game:
    def __init__(self, cols, rows):
        self.board = Board(cols, rows)
        self.depth = 10
        self._init()

    def _init(self):
        self.player_turn = 2


        self.selected = []

    def check_winner(self):
        if self.board:
            self.board.check_winner()
        else:
            self.board = Board(8, 8)

    def ai_move(self, board):
        if board:
            self.board = board
        else:
            self.board = Board(8, 8)

    def change_turn(self):
        self.player_turn = 1 if self.player_turn == 2 else 2

        if self.player_turn == 1:
            self.depth = 1
        else:
            self.depth = 13

        value, new_board, = minimax(self.board, self.depth, self.player_turn, float("-inf"), float("inf"))
        self.ai_move(new_board)




    def _move(self, col, row):
        pawn = self.board.get_pawn(self.selected[0], self.selected[1])
        move_valid = False
        skipped = []

        for move, skip in pawn.valid_moves.items():
            if len(move) == 2 and move == (col, row):
                move_valid = True
                skipped = skip

                break

        if move_valid:
            self.board.move(col, row, pawn, skipped, self.player_turn)
            pawn.select(self.board)

        else:
            return

        pawn.selected = False
        self.selected = []
        self.change_turn()


    def on_mouse_pressed(self, col, row):
        if self.should_move(col, row):
            self._move(col, row)


    def should_move(self, col, row):
        pawn = self.board.get_pawn(col, row)

        if not self.selected:
            forced_attacks = self.board.is_possible_attack(self.player_turn)

            if not (col, row) in forced_attacks and forced_attacks:
                return

            if pawn != 0 and pawn.player == self.player_turn:
                self.selected = [col, row]
                pawn.select(self.board)
                return False

        else:
            if pawn != 0 and [col, row] == self.selected:
                self.selected.clear()
                pawn.select(self.board)
                return False

            elif pawn == 0:
                return True




