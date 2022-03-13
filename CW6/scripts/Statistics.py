# Autor: Karol Stepanienko


from Constants import Constants
from Main import Qlearning


class Statistics:
    def __init__(self):
        self.q_learning = Qlearning()
        self.reward_average = 0.0

    def run(self):
        reward_sum = 0.0
        # Run learning for every new parameter value
        self.q_learning.run_learing()

        # Gathering test results
        for i in range(1, Constants.n + 1):
            self.q_learning.run_test()
            reward_sum += self.q_learning.stat_data.get_num_wins()

        self.reward_average = reward_sum / Constants.n
        print("Average reward value: " + str(self.reward_average/Constants.test_num_episodes * 100) + " in " + str(Constants.n) + " runs.")
        return self.reward_average

    def rotate_over_gamma(self):
        parameter_value_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 0.995, 1.0]
        best_gamma = 0.0
        best_reward = 0.0
        param_and_rewards = dict()
        for gamma in parameter_value_list:
            print("----------")
            print("Current gamma value: ", gamma)
            Constants.gamma = gamma # Overwrite current beta
            self.run()
            param_and_rewards[gamma] = self.reward_average
            if best_reward < self.reward_average:
                best_gamma = gamma
                best_reward = self.reward_average
        print("Best gamma value: ", best_gamma)
        print("Best reward value: ", best_reward/Constants.test_num_episodes * 100)
        Statistics.print_results_latex(param_and_rewards)

    def rotate_over_beta(self):
        parameter_value_list = [0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.0, 1.1]
        best_beta = 0.0
        best_reward = 0.0
        param_and_rewards = dict()
        for beta in parameter_value_list:
            print("----------")
            print("Current beta value: ", beta)
            Constants.beta = beta # Overwrite current beta
            self.run()
            param_and_rewards[beta] = self.reward_average
            if best_reward < self.reward_average:
                best_beta = beta
                best_reward = self.reward_average
        print("Best beta value: ", best_beta)
        print("Best reward value: ", best_reward/Constants.test_num_episodes * 100)
        Statistics.print_results_latex(param_and_rewards)

    def rotate_over_epsilon(self):
        parameter_value_list = [0.0002, 0.0004, 0.006, 0.008, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05]
        best_epsilon = 0.0
        best_reward = 0.0
        param_and_rewards = dict()
        for epsilon in parameter_value_list:
            print("----------")
            print("Current epsilon value: ", epsilon)
            Constants.epsilon = epsilon # Overwrite current epsilon
            self.run()
            param_and_rewards[epsilon] = self.reward_average
            if best_reward < self.reward_average:
                best_epsilon = epsilon
                best_reward = self.reward_average
        print("Best epsilon value: ", best_epsilon)
        print("Best reward value: ", best_reward/Constants.test_num_episodes * 100)
        Statistics.print_results_latex(param_and_rewards)

    @staticmethod
    def print_results_latex(param_and_rewards):
        print("Latex table format.")
        print("-------------------")
        for param, reward in param_and_rewards.items():
            print(param, "   &   ", reward, "  \\\\")


if __name__ == "__main__":
    statistics = Statistics()
    # statistics.run()
    statistics.rotate_over_gamma()
    statistics.rotate_over_beta()
    statistics.rotate_over_epsilon()
