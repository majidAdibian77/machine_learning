import numpy as np
from amalearn.agent import AgentBase

class TenArmedBanditAgent(AgentBase):
    def __init__(self, id, environment):
        super(TenArmedBanditAgent, self).__init__(id, environment)
        self.qValues = list()
        self.counts = list()
        self.mu = list()
        self.pi = list()
        self.lr = 0.35
        self.observations = list()

    def setup(self):
        actions_n = self.environment.available_actions()
        self.qValues = [0.0 for i in range(actions_n)]
        self.counts = [0 for i in range(actions_n)]
        self.mu = [0.0 for i in range(actions_n)]
        self.pi = [1.0/9 for i in range(actions_n)]
        self.observations = [list() for i in range(actions_n)]

    def pick_arm(self):
        normal_values = zip(self.mu, self.pi)
        all_draws = [np.random.normal(i[0], np.sqrt(1.0/i[1])) for i in normal_values]
        chosen_arm_index = all_draws.index(max(all_draws))
        return chosen_arm_index

    def update_params(self, chosen_arm_index, reward):
        self.counts[chosen_arm_index] += 1
        n = self.counts[chosen_arm_index]
        self.mu[chosen_arm_index] += self.lr * (reward - self.mu[chosen_arm_index])
        if len(self.observations[chosen_arm_index]) > 1:
            self.pi[chosen_arm_index] += 1.0 / np.var(self.observations[chosen_arm_index])
    

    def take_action(self):
        chosen_arm_index = self.pick_arm()
        observation, reward, done, info = self.environment.step(chosen_arm_index)
        self.lr -= .3 / 1000
        self.observations[chosen_arm_index].append(reward)
        self.update_params(chosen_arm_index, reward)
        self.environment.render()
        return self.counts, self.mu, reward
