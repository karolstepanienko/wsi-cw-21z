# Autor: Karol Stepanienko


import random
from math import inf

from two_player_games.games.dots_and_boxes import DotsAndBoxes

from Functions import Functions
from Constants import Constants

class MiniMax:
    def __init__(self):
        self.c = Constants()
        self.f = Functions(self.c)

    def min_max_alpha_beta(self, state, depth, alfa, beta):
        if depth == 0 or state.is_finished():
            return self.f.h(state)

        successors = self.get_successors(state)

        current_player = state.get_current_player()
        
        # Max (1)
        if current_player.char == '1':
            for next_state in successors.keys():
                alfa = max(alfa, self.min_max_alpha_beta(next_state, depth - 1, alfa, beta))
                if alfa >= beta:
                    return beta
            return alfa
        # Min (2)
        else:
            for next_state in successors.keys():
                beta = min(beta, self.min_max_alpha_beta(next_state, depth - 1, alfa, beta))
                if alfa >= beta:
                    return alfa
            return beta

    @staticmethod
    def get_successors(state):
        moves = state.get_moves()
        successors = dict()
        
        for move in moves:
            successors[state.make_move(move)] = move
        
        return successors

    @staticmethod
    def get_indexes(list_of_values, value):
        indexes = []
        for i, val in enumerate(list_of_values):
            if val == value:
                indexes.append(i)
        return indexes

    def sum_up(self, state):
        winner = state.get_winner()
        scores = state.get_scores()
        if winner is None:
            string = 'Draw'
        elif winner.char == '1':
            string = "The winner is: Max (1)"
        elif winner.char == '2':
            string = "The winner is: Min (2)"
        print(string, "(" + str(self.f.get_player_score(state, '1')) + " : " + str(self.f.get_player_score(state, '2')) + ")")
        # Current algorithm settings
        print(self.c.__str__())

    # If there are more than one equal maximum heuristic values, choose_randomly from them
    def get_random_desired_index(self, heuristics, desired_h_val):
        if heuristics.count(desired_h_val) != 1:
            #  Get list of max indexes
            indexes = self.get_indexes(heuristics, desired_h_val)
            max_index = random.choice(indexes)
        else:
            # Returns the index of the largest value in heuristics
            max_index = max(range(len(heuristics)), key=heuristics.__getitem__)
        return  max_index

    def init_state(self):
        move_num = 1
        if self.c.allow_custom_state:
            self.game = DotsAndBoxes(size=self.c.game_size)
            self.game, move_num = self.get_custom_game_state()
        else:
            # Using initial, blank game state.
            self.game = DotsAndBoxes(size=self.c.game_size)
        return move_num

    def get_custom_game_state(self):
        for move_index in self.c.moves_index_list:
            moves = self.game.get_moves()
            self.game.make_move(moves[move_index])
        return self.game, len(self.c.moves_index_list) + 1

    def run_basic(self, show_state):
        move_num = self.init_state()
        # print(self.game.__str__())
        # input()
        alfa = -inf
        beta = inf
        while not self.game.is_finished():
            # Get possible moves and states
            successors = self.get_successors(self.game.state)

            heuristics = []
            # Calculate values for states
            for state in successors.keys():
                heuristics.append(self.min_max_alpha_beta(state, self.c.depth, alfa, beta))

            current_player = self.game.get_current_player()

            # Choose next move
            # Max (1) is choosing
            if current_player.char == '1':
                if self.c.allow_random_choice:
                    max_h_val = max(heuristics)
                    index = self.get_random_desired_index(heuristics, max_h_val)
                else:
                    # Returns the index of the largest value in heuristics
                    index = max(range(len(heuristics)), key=heuristics.__getitem__)

            # Min (2) is choosing
            else:
                if self.c.allow_random_choice:
                    min_h_val = min(heuristics)
                    index = self.get_random_desired_index(heuristics, min_h_val)
                else:
                    # Returns the index of the smallest value in heuristics
                    index = min(range(len(heuristics)), key=heuristics.__getitem__)

            # Get next move
            next_move = list(successors.values())[index]
            # Make move
            self.game.make_move(next_move)

            if show_state:
                # Print state
                strings = ["_" * (2 * self.c.game_size + 1), "Move number: " + str(move_num), self.game.state.__str__()]
                print("\n".join(strings))

            move_num = move_num + 1
        return self.game.state

    def run(self):
        last_state = self.run_basic(show_state=True)
        # Sum up
        self.sum_up(last_state)


if __name__ == "__main__":
    mini_max = MiniMax()
    mini_max.run()
    