from copy import  deepcopy

player_one = 1
player_two = 2


def minimax(position, depth, maximalize_player, alpha, beta):
    if depth == 0 or position.check_winner():

        return position.evaluate_ai(), position

    if maximalize_player == 2:
        max_eval = float("-inf")
        best_move = None

        for move in get_all_moves(position, maximalize_player):
            evaluation = minimax(move, depth - 1, 1, alpha, beta)[0]

            alpha = max(evaluation, alpha)
            if alpha >= beta:
                break

            max_eval = max(max_eval, evaluation)

            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move

    else:
        min_eval = float("inf")
        best_move = None

        for move in get_all_moves(position, maximalize_player):
            evaluation = minimax(move, depth - 1, 2, alpha, beta)[0]

            beta = min(beta, evaluation)
            if alpha >= beta:
                break

            min_eval = min(min_eval, evaluation)

            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move


def simulate_move(piece, move, board, skip, player):
    board.move(move[0], move[1], piece, skip, player)
    return board

def get_all_moves(board, player):
    moves = []
    forced_moves = board.is_possible_attack(player)

    for row in board.board:
        for pawn in row:
            if pawn == 0:
                continue

            if pawn.player != player:
                continue

            if (pawn.col, pawn.row) not in forced_moves and forced_moves:
                continue

            pawn.evaluate_moves(board)

            pawn.force_attack()



            for move, skip in pawn.valid_moves.items():
                temp_board = deepcopy(board)
                temp_pawn = temp_board.get_pawn(pawn.col, pawn.row)
                new_board = simulate_move(temp_pawn, move, temp_board, skip, player)
                moves.append(new_board)

    return moves