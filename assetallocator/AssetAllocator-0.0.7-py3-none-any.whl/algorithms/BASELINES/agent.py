import pandas as pd
import numpy as np
from .mpt import MPT

class BaselineAgent():
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.action_space = self.env.action_space.shape[-1]
        self.env.random_start_range = 0
        
    def learn(self, timesteps = None, print_every = None):
        if self.name == 'MPT':
            self.model = MPT(self.env)
            daily_returns = self.env.reset()
            daily_returns = daily_returns.reshape(self.env.n, -1)
            daily_returns = pd.DataFrame(daily_returns).T
            self.model.learn(daily_returns)
        elif self.name == 'BuyAndHold':
            self.model = np.random.random(size = self.env.n)
            self.model = weights/weights.sum()
        else:
            self.env.reset()
    
    def predict(self, obs):
        if self.name == 'Uniform':
            weights = [1/self.env.n] * self.env.n
        elif self.name == 'Random':
            weights = np.random.random(size = self.env.n)
            weights = weights/weights.sum()
        elif self.name == 'BuyAndHold':
            weights =  self.model
        elif self.name == 'MPT':
            weights = self.model.predict(obs)
        else:
            assert False, 'Model name must be one of Uniform, Random, BuyAndHold, or MPT'        
        
        if self.action_space > self.env.n:
                weights = np.append(weights, 0)
        return weights
            
            
            