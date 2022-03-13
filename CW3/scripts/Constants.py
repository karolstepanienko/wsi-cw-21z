# Autor: Karol Stepanienko


class Constants:
    def __init__(self):
        ### Game settings ###
        # Size of the game board
        self.game_size = 2
        # How many steps forward will the algorithm check
        self.depth = 2
        ### Game settings ###

        # Allow random choice on same score paths
        self.allow_random_choice = False
        # self.allow_random_choice = True
        
        # Number of rotations for Statistics.py
        self.rotations = 100
        
        # Allow custom state
        self.allow_custom_state = False
        # self.allow_custom_state = True

        ### Proposed custom states ###

        # # State favoring Min (3)
        # self.game_size = 3
        # self.moves_index_list = [5, 5, 15, 15, 0, 0, 8, 10, 8]

        # # Square in the middle (3)
        # self.game_size = 3
        # self.moves_index_list = [5, 5, 15, 15]
        
        # # Square in top-left (3)
        # self.game_size = 3
        # self.moves_index_list = [0, 0, 10, 10]
        
        # # Square in bottom-right (3)
        # self.game_size = 3
        # self.moves_index_list = [10, 10, 20, 20]
        
        # # Square in the left-smiddle (4)
        # self.game_size = 4
        # self.moves_index_list = [6, 6, 24, 24]

        ### Proposed custom states ###

    def __str__(self):
        return "\n".join(["Game size: " + str(self.game_size), "Depth: " + str(self.depth)])
