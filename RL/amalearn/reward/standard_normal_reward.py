from amalearn.reward import RewardBase
import numpy as np

class StdNormalReward(RewardBase):
    def __init__(self):
        super(StdNormalReward, self).__init__()
        self.mean = np.random.normal(0, 1)
        self.std = 1
        # self.p = p

    def get_reward(self):
        return np.random.normal(loc=self.mean, scale=self.std)
        # if np.random.random() > self.p:
        #     return 0.0
        # else:
        #     return 1.0
    def get_info(self):
        return self.mean