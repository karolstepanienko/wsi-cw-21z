# Autor: Karol Stepanienko


class Constants:
    # Action types: Movement directions
    # LEFT = 0
    # DOWN = 1
    # RIGHT = 2
    # UP = 3

    # List of all actions
    # actions = np.array([LEFT, DOWN, RIGHT, UP])
    # Number of actions (needs to be redefined)
    num_actions = 0

    # Number of episodes devoted to learning
    learning_num_episodes = 10000

    # Number of episodes devoted to testing and gathering results
    test_num_episodes = 100
    
    # Discount factor for future rewards
    # Future rewards are less important than current reward 
    gamma = 0.99
    
    # Step size
    beta = 0.3

    # Epsilon (epsilon greedy policy)
    epsilon = 0.004

    # T (Bolzmann policy)
    T = 0.0015
    # Environment variables
    # size - Environment size. Environment is a square matrix of states. It can be 4 or 8.
    size = 4
    map_name = str(size) + "x" + str(size)

    # Determines how many times to run the statistical data gathering loop
    n = 25

    @staticmethod
    def get_action_list():
        action_list = []
        for action in range(Constants.num_actions):
            action_list.append(action)
        return action_list
