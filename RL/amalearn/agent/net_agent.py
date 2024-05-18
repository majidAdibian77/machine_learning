import numpy as np
from amalearn.agent import AgentBase

class NetAgent(AgentBase):
    def __init__(self, id, environment, policy):
        super(NetAgent, self).__init__(id, environment)
        self.policy = policy
        self.qValues = list()
        self.counts = list()
        self.observation = list()
        self.h = list()
        self.eps = .5
        self.average_reward = 0
        self.lr = .01

    def setup(self):
        actions_n = self.environment.available_actions()
        self.qValues = [100.0 for i in range(actions_n)]
        self.counts = [0 for i in range(actions_n)]
        self.observation = [list() for i in range(actions_n)]
        self.h = [0 for i in range(actions_n)]


    def pick_arm(self):
        available_actions = self.environment.available_actions()
        if self.policy == 'eGreedy':
            p = np.random.random() 
            if p < self.eps:
                chosen_arm_index = np.random.choice(available_actions)
            else:
                chosen_arm_index = np.argmin(self.qValues)
            return chosen_arm_index
        else:
            probs = [np.exp(i)/sum(np.exp(self.h)) for i in self.h]
            chosen_arm_index = np.random.choice(np.arange(available_actions), p=probs)
            return chosen_arm_index

        
        
        
    def update_params(self, chosen_arm_index, reward):
        if self.policy == 'eGreedy':
            self.counts[chosen_arm_index] += 1
            n = self.counts[chosen_arm_index]
            value = self.qValues[chosen_arm_index]
            new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
            self.qValues[chosen_arm_index] = new_value
        else: 
            reward *= -1
            probs = [np.exp(i)/sum(np.exp(self.h)) for i in self.h]
            # print(probs)
            self.counts[chosen_arm_index] += 1
            n = sum(self.counts)
            for i in range(len(self.h)):
                if i == chosen_arm_index:
                    self.h[i] += self.lr * (reward - self.average_reward) * (1 - probs[i])
                else:
                    self.h[i] -= self.lr * (reward - self.average_reward) * probs[i]
            self.average_reward = (self.average_reward * (n-1) + reward ) / n
                
        


        


    def take_action(self):
        chosen_arm_index = self.pick_arm()
        observation, reward, done, info = self.environment.step(chosen_arm_index)
        self.observation[chosen_arm_index].append(reward)
        self.update_params(chosen_arm_index, reward)
        # print(self.h)
        if sum(self.counts) % 10 == 0:
            self.eps -= 0.0005 
        if self.policy == 'eGreedy':
            return self.counts, self.qValues, reward
        else: 
            return self.counts, self.h, reward
