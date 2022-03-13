# Autor: Karol Stepanienko


from math import floor

from MiniMax import MiniMax


class Statistics:
    def __init__(self):
        self.mini_max = MiniMax()

        self.check_allow_random_choice()

        # Data
        self.max_scores = []
        self.min_scores = []
        self.draws = 0
        self.max_wins_num = 0
        self.min_wins_num = 0
        self.average_max_score = 0
        self.average_min_score = 0

    def check_allow_random_choice(self):
        if not self.mini_max.c.allow_random_choice:
            print("No sense running Statistics.py without random choice allowed.")
            exit()

    def cal_averages(self):
        self.average_max_score = sum(self.max_scores)/len(self.max_scores)
        self.average_min_score = sum(self.min_scores)/len(self.min_scores)

    def parse_state(self, state):
        # Count victories
        winner = state.get_winner()
        if winner is None:
            self.draws = self.draws + 1
        elif winner.char == '1':
            self.max_wins_num = self.max_wins_num + 1
        else:
            self.min_wins_num = self.min_wins_num + 1

        # Append scores
        self.max_scores.append(self.mini_max.f.get_player_score(state, '1'))
        self.min_scores.append(self.mini_max.f.get_player_score(state, '2'))

    def run(self):
        # Gather data
        for i in range(self.mini_max.c.rotations):
            if (i % 20 == 0):
                print(i)
            state = self.mini_max.run_basic(show_state=False)
            self.parse_state(state)

        self.cal_averages()
        self.print_data()

    def print_data(self):
        print("Average score values: (" +\
              str(floor(self.average_max_score)) + "," + str(round(self.average_max_score - int(self.average_max_score), 2))[2:] \
              + " ; " + str(floor(self.average_min_score)) + "," + str(round(self.average_min_score - int(self.average_min_score), 2))[2:] + ")")
        if self.min_wins_num != 0:
            print("Max wins to Min wins: " + str(floor(self.max_wins_num/self.min_wins_num)) + "," + str(round(self.max_wins_num/self.min_wins_num - int(self.max_wins_num/self.min_wins_num), 2))[2:] )
        print("Average Max score: " + str(self.average_max_score))
        print("Average Min score: " + str(self.average_min_score))
        print("Max to Min wins: " + "(" + str(self.max_wins_num) + " ; " + str(self.min_wins_num) + ")")
        print("Max wins: " + str(self.max_wins_num))
        print("Min wins: " + str(self.min_wins_num))
        print("Draws: " + str(self.draws))


if __name__ == "__main__":
    s = Statistics()
    s.run()
