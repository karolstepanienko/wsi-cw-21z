# Autor: Karol Stepanienko


import gym
import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp
import itertools

from Constants import Constants


class Qlearning:
    """
    Frozen lake sometimes does not fulfil moves as it was told to.
    It simulates slipping on a frozen ice.
    self.env.action_space.n - number of possible actions
    Q - action-value function
    """
    def __init__(self) -> None:
        self.stat_data = StatData()
        self.env = self.create_environment()
        Constants.num_actions = self.env.action_space.n
        Constants.actions = Constants.get_action_list()
        self.state = self.env.reset()
        self.next_state = None
        self.reward = 0
        self.is_terminal = False
        self.action = None
        self.Q = self.init_Q()
        self.policy = self.policy_epsilon_greedy
        # self.policy = self.policy_bolzmann

    def re_init(self):
        self.stat_data.reset()
        self.state = self.env.reset()
        self.next_state = None
        self.reward = 0
        self.is_terminal = False
        self.action = None

    @staticmethod
    def init_Q():
        """ Creates Q dictionary: {"state": {"action": action_value}}."""
        Q = dict()
        # Every state
        for state_num in range(pow(Constants.size, 2)):
            Q[state_num] = dict()
            for action in Constants.actions:
                Q[state_num][action] = 0.0
        return Q

    @staticmethod
    def create_environment():
        env = gym.make('FrozenLake-v1', map_name=Constants.map_name)
        return env.env

    @staticmethod
    def policy_epsilon_greedy(state, Q):
        """ Returns action probabilities dictionary. """
        # {"action": action_probability}
        action_probabilities_dict = dict()

        best_action, best_action_value, best_action_amount = Qlearning.get_best_action_amount(state, Q)

        # Iterate over all actions
        for action in Constants.actions:
            action_probability = Constants.epsilon / Constants.num_actions
            if action == best_action:
                action_probability += (1 - Constants.epsilon) / best_action_amount
            # Append action probability
            action_probabilities_dict[action] = action_probability

        action_probabilities_dict = Qlearning.normalise_probabilities(action_probabilities_dict)
        return action_probabilities_dict

    @staticmethod
    def policy_bolzmann(state, Q):
        """ Returns action probabilities dictionary. """
        # {"action": action_probability}
        action_probabilities_dict = dict()

        # Iterate over all actions
        sum_bz_action_val = 0.0
        for action in Constants.actions:
            sum_bz_action_val += mp.exp(Q[state][action] / Constants.T)
        average_bz_action_val = sum_bz_action_val / len(Constants.actions)

        # Iterate over all actions
        for action in Constants.actions:
            action_probabilities_dict[action] = mp.exp(Q[state][action] / Constants.T) / average_bz_action_val

        # print(action_probabilities_dict)
        action_probabilities_dict = Qlearning.normalise_probabilities(action_probabilities_dict)
        return action_probabilities_dict

    @staticmethod
    def normalise_probabilities(action_probabilities_dict):
        """ Normalise probabilities. """
        action_probability_sum = sum(action_probabilities_dict.values())
        for action, action_probability in action_probabilities_dict.items():
            action_probabilities_dict[action] = action_probability / action_probability_sum
        return action_probabilities_dict

    @staticmethod
    def count_number_of_actions(state, Q, action):
        """ Returns number of given actions in gi"""
        number_of_actions = 0
        for dict_action in Q[state].keys():
            if dict_action == action:
                number_of_actions += 1
        return  number_of_actions

    @staticmethod
    def get_best_action_amount(state, Q):
        best_action = None
        best_action_value = 0.0
        best_action_amount = 0
        for action, action_value in Q[state].items():
            if action_value > best_action_value:
                best_action = action
                best_action_value = action_value
                best_action_amount += 1
            elif action_value == best_action_value:
                best_action_amount += 1
        return best_action, best_action_value, best_action_amount

    @staticmethod
    def get_best_action_value(state, Q):
        """ Returns best action value for given state. """
        return max(Q[state].values())

    @staticmethod
    def get_policy_driven_action(action_probabilities_dict):
        """ Returns one randomly chosen action with probabilities calculated using policy."""
        return np.random.choice(list(action_probabilities_dict.keys()), p=list(action_probabilities_dict.values()))

    @staticmethod
    def set_values_to_zero(dictionary):
        """ Sets all values in a dictionary to zeros. """
        for key in dictionary.keys():
            dictionary[key] = 0
        return dictionary

    def run_episode(self):
        t = 1
        self.state = self.env.reset()
        self.is_terminal = False
        reward_sum = 0
        while not self.is_terminal:
            action_probabilities_dict = self.policy(self.state, self.Q)
            # Get action for current state
            self.action = Qlearning.get_policy_driven_action(action_probabilities_dict)

            # Make action and get environment response
            self.next_state, self.reward, self.is_terminal, _ = self.env.step(self.action)

            # If agent lost
            if self.is_terminal:
                best_action_value_next_state = 0
                # self.Q[self.next_state] = Qlearning.set_values_to_zero(self.Q[self.next_state])
            else:
                best_action_value_next_state = Qlearning.get_best_action_value(self.next_state, self.Q)

            # Update Q action-value function
            self.Q[self.state][self.action] = \
                + self.Q[self.state][self.action] \
                + Constants.beta * (self.reward + Constants.gamma * best_action_value_next_state
                                    - self.Q[self.state][self.action])

            self.state = self.next_state

            # Save rewards
            reward_sum += self.reward
            # self.stat_data.rewards[episode_num] += self.reward
            t += 1

            # if t > 100 and self.is_terminal:
            #     print(t)
            #     self.env.render()
        return reward_sum, t

    def run_learing(self):
        self.Q = self.init_Q()
        for episode_num in range(Constants.learning_num_episodes):
            self.run_episode()

    def run_test(self):
        self.re_init()
        for episode_num in range(1, Constants.test_num_episodes + 1):
            self.stat_data.rewards[episode_num], self.stat_data.lengths[episode_num] = self.run_episode()


class StatData:
    def __init__(self):
        # {episode_num: reward_sum}
        self.rewards = dict()
        # {episode_num: episode_length}
        self.lengths = dict()

    def reset(self):
        self.rewards = dict()
        self.lengths = dict()

    def get_num_wins(self):
        return sum(self.rewards.values())

    def get_num_wins_every_thousand(self):
        wins_every_thousand = []
        for episode_num in range(1, Constants.test_num_episodes + 1, 1000):
            # print(episode_num, episode_num + 999)
            rewards_in_thousand = dict(itertools.islice(self.rewards.items(), episode_num, episode_num + 999))
            wins_every_thousand.append(sum(rewards_in_thousand.values()))
        return wins_every_thousand

    def print_wins_every_thousand(self):
        wins_every_thousand = self.get_num_wins_every_thousand()
        print(wins_every_thousand)
        for wins, episodes in zip(wins_every_thousand, range(1, 1000 * len(wins_every_thousand), 1000)):
            print("Wins percentages: ", wins/1000 * 100, " in episodes from", episodes,
                  " to ", episodes + 999)

    def make_plot(self):
        plt.bar(self.lengths.keys(), self.lengths.values())
        plt.title("Długości epizodów")
        plt.show()

        plt.bar(self.rewards.keys(), self.rewards.values())
        plt.title("Nagrody")
        plt.show()


if __name__ == "__main__":
    q_learning = Qlearning()
    q_learning.run_learing()
    q_learning.run_test()
    # q_learning.stat_data.print_wins_every_thousand()
    print("Percentage wins all:", q_learning.stat_data.get_num_wins() / Constants.test_num_episodes * 100)

    # q_learning.stat_data.make_plot()
