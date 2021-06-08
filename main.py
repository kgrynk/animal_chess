import random

import numpy as np

height = 9
width = 7
animal_names = ('rat', 'cat', 'dog', 'wolf', 'leopard', 'tiger', 'lion', 'elephant')
animal_letters = ('r', 'c', 'd', 'w', 'j', 't', 'l', 'e')
animal_rank = {'r': 1, 'c': 2, 'd': 3, 'w': 4, 'j': 5, 't': 6, 'l': 7, 'e': 8}
directions = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Game:

    def __init__(self):
        self.board = np.array(list('..#*#.....#...........~~.~~..~~.~~..~~.~~...........#.....#*#..')).reshape(
            height, width)
        self.pawns = np.array(list('L.....T.D...C.R.J.W.E.....................e.w.j.r.c...d.t.....l')).reshape(
            height, width)
        self.pos = [[(2, 0), (1, 5), (1, 1), (2, 4), (2, 2), (0, 6), (0, 0), (2, 6)],
                    [(6, 6), (7, 1), (7, 5), (6, 2), (6, 4), (8, 0), (8, 6), (6, 0)]]
        self.den = ((0, 3), (8, 3))
        self.player = 0
        self.moves_form_last_beat = 0

    def valid_moves(self):
        is_first_player = self.player == 0
        moves = []
        for rank, pos in enumerate(self.pos[self.player], start=1):
            # print(rank, pos)
            if not pos:
                continue
            for direction in directions:
                field = self.board[tuple(pos)]
                new_pos = pos[0] + direction[0], pos[1] + direction[1]
                try:
                    pawn_to_beat = self.pawns[new_pos]
                    field_to_step = self.board[new_pos]
                    if pawn_to_beat == '.':
                        rank_to_beat = 0
                    else:
                        rank_to_beat = animal_rank[pawn_to_beat.lower()]
                    friendly_pawn = pawn_to_beat.isupper() == is_first_player
                except IndexError:
                    continue

                if field_to_step != '.' and field_to_step != '#':
                    if field_to_step == '*' and self.den[self.player] == new_pos:
                        continue
                    # cannot step into his own den

                    if field_to_step == '~' and rank != 1:
                        # only rat can step into water

                        if rank != 6 or rank != 7:
                            continue
                        # only lion and tiger can jump over water

                        else:
                            while field_to_step == '~':
                                if not friendly_pawn:
                                    break
                                field_to_step = self.board[new_pos]
                                pawn_to_beat = self.pawns[new_pos]
                                if pawn_to_beat == '.':
                                    rank_to_beat = 0
                                else:
                                    rank_to_beat = animal_rank[pawn_to_beat.lower()]
                                friendly_pawn = pawn_to_beat.isupper() == is_first_player
                            else:
                                jump_over_rat = False
                            jump_over_rat = True

                            if jump_over_rat:
                                continue
                            # cannot jump over enemy (rat)

                if pawn_to_beat != '.':
                    if friendly_pawn or field == '~':
                        continue
                    # cannot beat friendly pawn, cannot beat from water

                    if rank != 1 or rank_to_beat != 8:
                        if rank_to_beat > rank and field_to_step != '#':
                            continue
                    # cannot beat bigger animal except in trap, or rat->elephant

                moves.append((rank, tuple(pos), new_pos))

        return moves

    def do_move(self, move):
        rank, pos, new_pos = move
        my_animal_letter = self.pawns[pos]
        enemy_animal_letter = self.pawns[new_pos]
        self.pawns[pos] = '.'
        self.pawns[new_pos] = my_animal_letter
        self.pos[self.player][rank - 1] = new_pos
        self.player = 1 - self.player

        if enemy_animal_letter != '.':
            enemy_rank = animal_rank[enemy_animal_letter.lower()]
            self.pos[self.player][enemy_rank - 1] = None
            self.moves_form_last_beat = 0
        else:
            self.moves_form_last_beat += 1

    def terminal(self):
        if self.pawns[self.den[0]] != '.' or self.pawns[self.den[1]] != '.' or self.moves_form_last_beat >= 30:
            return True
        none_8 = [None] * 8
        return self.pos[0] == none_8 or self.pos[1] == none_8

    def result(self):
        if self.pawns[self.den[0]] != '.':
            return False
        elif self.pawns[self.den[1]] != '.':
            return True

        for i in reversed(range(8)):
            beaten_pawn0 = self.pos[0][i] is None
            beaten_pawn1 = self.pos[1][i] is None
            if beaten_pawn0 != beaten_pawn1:
                return beaten_pawn1
        return False
    # first player wins - returns True, else returns False


if __name__ == '__main__':
    for i in range(10000):
        main_game = Game()
        while not main_game.terminal():
            moves = main_game.valid_moves()
            # if not moves:
            #     break
            move = random.choice(moves)
            main_game.do_move(move)

        print(main_game.result())
    # print(main_game.board)
    # print(main_game.pawns)
    # print(main_game.pos[0])
    # print(main_game.valid_moves())
    # print(main_game.pos[0, 0])
    # print(main_game.board[tuple(main_game.pos[0, 0])])
