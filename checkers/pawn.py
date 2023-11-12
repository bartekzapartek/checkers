
class Pawn:

    def __init__(self, col, row, player):
        self.col = col
        self.row = row

        self.player = player

        self.selected = False
        self.king = False

        self.valid_moves = {}



    def evaluate_king_moves(self, board, prev_pawn = [], prev_dir = ()):
        directions = [(-1, -1), (1, -1), (1, 1), (-1 ,1)]

        if not prev_pawn:
            prev_pawn = [self.col, self.row]

        for direction in directions:
            if prev_dir and (prev_dir[0] * (-1), prev_dir[1] * (-1)) == direction:
                continue

            col_step, row_step = direction
            current_col, current_row = prev_pawn[0] + col_step, prev_pawn[1] + row_step

            while 0 <= current_row < 8 and 0 <= current_col < 8:
                pawn = board.get_pawn(current_col, current_row)

                if pawn == 0 and prev_pawn == [self.col, self.row]:
                    self.valid_moves[(current_col, current_row)] = []

                elif pawn != 0 and pawn.player == self.player:
                    break

                elif pawn != 0 and pawn.player != self.player:
                    behind_col, behind_row = current_col + col_step, current_row + row_step

                    if 0 <= behind_row < 8 and 0 <= behind_col < 8:
                        pawn_behind = board.get_pawn(behind_col, behind_row)

                        if pawn_behind != 0:
                            break

                        self.valid_moves[(behind_col, behind_row)] = [(current_col, current_row)]
                        skipped_list = self.valid_moves.get((prev_pawn[0], prev_pawn[1]))
                        if prev_pawn != [self.col, self.row]:
                            for skipped in skipped_list:
                                self.valid_moves.get((behind_col, behind_row)).append(skipped)
                        self.evaluate_king_moves(board, [behind_col, behind_row], direction)
                        break

                current_col, current_row = current_col + col_step, current_row + row_step







    def traverse_direction(self, board, direction, prev_move = [], first_move = True):
        x, y = direction
        if not prev_move:
            prev_move = [self.col, self.row]

        current_x = prev_move[0] + x
        current_y = prev_move[1] + y

        if not (0 <= current_x < 8) or not (0 <= current_y < 8):
            return

        pawn = board.get_pawn(current_x, current_y)
        if pawn != 0 and pawn.player == self.player:
            return

        elif (pawn == 0 and first_move and prev_move == [self.col, self.row]):
            if self.player == 1 and current_y < self.row:
                self.valid_moves[(current_x, current_y)] = []
            elif self.player == 2 and current_y > self.row:
                self.valid_moves[(current_x, current_y)] = []

        elif pawn != 0 and pawn.player != self.player:
            behind_x, behind_y = current_x + x, current_y + y

            if 0 <= behind_x < 8 and 0 <= behind_y < 8 and board.get_pawn(behind_x, behind_y) == 0:
                if not (behind_x, behind_y) in self.valid_moves:
                    self.valid_moves[(behind_x, behind_y)] = [(current_x, current_y)]

                    skipped_list = self.valid_moves.get((prev_move[0], prev_move[1]))
                    if prev_move != [self.col, self.row]:
                        for skipped in skipped_list:
                            self.valid_moves.get((behind_x, behind_y)).append(skipped)
                else:
                    return

                self.evaluate_moves(board, [behind_x, behind_y], False)

    def force_attack(self):
        force = False
        can_move = False
        remove_moves = []

        for move, skipped in self.valid_moves.items():
            if skipped:
                force = True
            else:
                can_move = True
                remove_moves.append(move)

        if force and can_move:
            for move in remove_moves:
                del self.valid_moves[move]




    def evaluate_moves(self, board, prev_move = [], first_move = True):

        if prev_move == []:
           self.valid_moves.clear()

        if self.king:
            self.evaluate_king_moves(board)
            return

        directions = [(-1, -1), (1, -1), (1, 1), (-1 ,1)]

        for i in range(0, 4):
            self.traverse_direction(board, directions[i], prev_move, True)

        # print(self.valid_moves)

    def move(self, col, row):
        self.col = col
        self.row = row

    def make_king(self):
        self.king = True

    def select(self, board):
        self.selected = True if self.selected == False else False
        if self.selected:
            self.evaluate_moves(board)
            self.force_attack()
        else:
            self.valid_moves.clear()
