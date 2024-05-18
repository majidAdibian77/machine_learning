import numpy as np
from amalearn.agent import AgentBase

class UniAgent(AgentBase):
    def __init__(self, id, environment, policy):
        super(UniAgent, self).__init__(id, environment)
        self.policy = policy
        self.lamda = -5
        self.alpha = .88
        self.beta = 1.5
        self.monetary_value = 8.5
        self.h = 1.5
        self.qValues = list()
        self.counts = list()
        self.observation = list()
        self.delay_border = 10
        self.eps = .5
        self.c = 10
        self.agg_counts = 1

    def setup(self):
        actions_n = self.environment.available_actions()
        self.qValues = [15.0 for i in range(actions_n)]
        self.counts = [1 for i in range(actions_n)]
        self.observation = [list() for i in range(actions_n)]


    def pick_arm(self):
        available_actions = self.environment.available_actions()
        if self.policy == 'eGreedy':
            p = np.random.random() 
            if p < self.eps:
                chosen_arm_index = np.random.choice(available_actions)
            else:
                chosen_arm_index = np.argmax(self.qValues)
            return chosen_arm_index
        else:   
            rewards = []
            for action in range(available_actions):
                action_reward = (self.qValues[action] + 
                    self.c * np.sqrt(np.log(self.agg_counts) / self.counts[action]))
                rewards.append(action_reward)
            self.agg_counts += 1
            return np.argmax(rewards)


        
        
        
    def update_params(self, chosen_arm_index, reward):
        self.counts[chosen_arm_index] += 1
        n = self.counts[chosen_arm_index]
        value = self.qValues[chosen_arm_index]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.qValues[chosen_arm_index] = new_value
        

    def apply_subjective(self, chosen_arm_index, reward):
        p = 0
        if chosen_arm_index > self.delay_border:
            p = (chosen_arm_index - self.delay_border)**self.h
        # you get bus
        if reward <= chosen_arm_index:
            if reward <= self.delay_border:
                return (self.delay_border - reward)**self.alpha + self.monetary_value
            else:
                return self.lamda * (reward - self.delay_border)**self.beta + self.monetary_value - p
        # you get taxi
        else:
            if chosen_arm_index <= self.delay_border:
                return (self.delay_border - chosen_arm_index)**self.alpha
            else:
                return self.lamda * (chosen_arm_index - self.delay_border)**self.beta


        


    def take_action(self):
        chosen_arm_index = self.pick_arm()
        observation, reward, done, info = self.environment.step(chosen_arm_index)
        self.observation[chosen_arm_index].append(reward)
        reward = self.apply_subjective(chosen_arm_index, reward)
        self.update_params(chosen_arm_index, reward)
        self.environment.render()
        if sum(self.counts) % 100 == 0:
            self.eps -= 0.005 
        return self.counts, self.qValues, reward
