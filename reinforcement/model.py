
"""
Functions you should use.
Please avoid importing any other torch functions or modules.
Your code will not pass if the gradescope autograder detects any changed imports
"""

from torch.nn import Module
from torch.nn import  Linear
from torch import tensor, double, optim
from torch.nn.functional import relu, mse_loss



class DeepQNetwork(Module):
    """
    A model that uses a Deep Q-value Network (DQN) to approximate Q(s,a) as part
    of reinforcement learning.
    """
    def __init__(self, state_dim, action_dim):
        self.num_actions = action_dim
        self.state_size = state_dim
        super(DeepQNetwork, self).__init__()
        # Remember to set self.learning_rate, self.numTrainingGames,
        # and self.batch_size!
        "*** YOUR CODE HERE ***"
        self.learning_rate = 0.01
        self.numTrainingGames = 4000
        self.batch_size = 128
        # hidden1_size = 500
        # self.linear1 = Linear(state_dim, hidden1_size)
        # self.linear2 = Linear(hidden1_size, action_dim)
        hidden1_size = 500
        hidden2_size = 500
        hidden3_size = 500
        self.linear1 = Linear(state_dim, hidden1_size)
        self.linear2 = Linear(hidden1_size, hidden2_size)
        self.linear3 = Linear(hidden2_size, hidden3_size)
        self.linear4 = Linear(hidden3_size, action_dim)
        self.optimizer = optim.SGD(self.parameters(), lr=self.learning_rate)
        "**END CODE"""
        self.double()


    def get_loss(self, states, Q_target):
        """
        Returns the Squared Loss between Q values currently predicted 
        by the network, and Q_target.
        Inputs:
            states: a (batch_size x state_dim) numpy array
            Q_target: a (batch_size x num_actions) numpy array, or None
        Output:
            loss node between Q predictions and Q_target
        """
        "*** YOUR CODE HERE ***"
        return mse_loss(self.forward(states), Q_target)

    def forward(self, states):
        """
        Runs the DQN for a batch of states.
        The DQN takes the state and returns the Q-values for all possible actions
        that can be taken. That is, if there are two actions, the network takes
        as input the state s and computes the vector [Q(s, a_1), Q(s, a_2)]
        Inputs:
            states: a (batch_size x state_dim) numpy array
        Output:
            result: (batch_size x num_actions) numpy array of Q-value
                scores, for each of the actions
        """
        "*** YOUR CODE HERE ***"
        return self.linear4(relu(self.linear3(relu(self.linear2(relu(self.linear1(states)))))))
    
    def run(self, states):
        return self.forward(states)

    def gradient_update(self, states, Q_target):
        """
        Update your parameters by one gradient step with the .update(...) function.
        You can look at the ML project for an idea of how to do this, but note that rather
        than iterating through a dataset, you should only be applying a single gradient step
        to the given datapoints.

        Inputs:
            states: a (batch_size x state_dim) numpy array
            Q_target: a (batch_size x num_actions) numpy array, or None
        Output:
            None
        """
        "*** YOUR CODE HERE ***"
        self.optimizer.zero_grad()
        loss = self.get_loss(states, Q_target)
        loss.backward()
        self.optimizer.step()