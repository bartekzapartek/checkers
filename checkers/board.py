import pygame
from checkers.pawn import Pawn

class Board:
    def __init__(self, cols, rows):
        self.rows = rows
        self.cols = cols

        self.player_one_pawns = 12
        self.player_two_pawns = 12

        self.player_one_kings = 0
        self.player_two_kings = 0

        self.board = []
        self._create_board()

    def _create_board(self):
        for row in range(self.rows):
            self.board.append([])

            for col in range(self.cols):
                if row < 3:
                    if (row + col) % 2 == 1:
                        self.board[row].append(Pawn(col, row, 2))
                    else:
                        self.board[row].append(0)

                elif row > 4:
                    if (col + row) % 2 == 1:
                        self.board[row].append(Pawn(col, row, 1))

                    else:
                        self.board[row].append(0)

                else:
                    self.board[row].append(0)

    def evaluate_ai(self):
        return 2 * (self.player_two_pawns - self.player_one_pawns) +  (self.player_two_kings - self.player_one_kings)

    def check_if_king(self, col, row):
        pawn = self.get_pawn(col, row)
        if row == 7 and pawn.player == 2:
            pawn.make_king()
            self.player_two_kings += 1
        elif row == 0 and pawn.player == 1:
            pawn.make_king()
            self.player_one_kings += 1

    def move(self, col, row, pawn, skipped, player_turn):
        self.board[row][col] = pawn
        self.board[pawn.row][pawn.col] = 0


        for skip in skipped:
            was_king = self.board[skip[1]][skip[0]].king
            self.board[skip[1]][skip[0]] = 0

            if player_turn == 1:
                self.player_two_pawns -= 1
                if was_king:
                    self.player_one_kings -= 1
            else:
                self.player_one_pawns -= 1
                if was_king:
                    self.player_two_kings -= 1

        pawn.move(col, row)
        self.check_if_king(col, row)

    def is_possible_attack(self, player):
        pawns_to_attack = []

        for row in range(8):
            for col in range(8):
                pawn = self.get_pawn(col, row)
                if pawn != 0 and player == pawn.player:
                    pawn.evaluate_moves(self)

                    for move, skipped in pawn.valid_moves.items():
                        if skipped:
                            pawns_to_attack.append((pawn.col, pawn.row))
                            break

                    pawn.valid_moves.clear()

        return pawns_to_attack



    def check_winner(self):
        print(self.player_one_pawns, self.player_two_pawns)
        if self.player_one_pawns == 0 or self.player_two_pawns == 0:
            return True
            # self.board = Board(8, 8)
        else:
            return False

    def get_pawn(self, col, row):
        return self.board[row][col]
