# Autor: Karol Stepanienko


from Constants import Constants


class Functions:
    def __init__(self, constants=Constants()):
        self.c = constants

    ## Simplest h
    # def h(self, state):
    #     """"Returns -1, 0, 1."""
    #     winner = state.get_winner()
        
    #     if winner is None:
    #         value = 0
    #     elif winner.char == '1':
    #         value = 1
    #     else:
    #         value = -1    
        
    #     return value

    # Counting current number of points (boxes)
    def h(self, state):
        max_score = self.get_player_score(state, '1')
        min_score = self.get_player_score(state, '2')
        maximum_possible_score = self.c.game_size**2
        empty_boxes = maximum_possible_score - max_score - min_score
        # Normalisation to <-1; 1>
        normalised_h = (max_score - min_score)/maximum_possible_score
        if empty_boxes != 0:
            # Prefer paths with higher amount of already taken boxes
            result = normalised_h/empty_boxes
        else:
            result = normalised_h
        return result

    @staticmethod
    def get_player_score(state, player_name):
        player_score = None
        scores = state.get_scores()
        for player, score in scores.items():
            if player.char == player_name:
                player_score = score
        return player_score
