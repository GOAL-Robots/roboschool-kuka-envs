import os.path, time, gym
from OpenGL import GLU
import numpy as np
import roboschool
import time

def demo_run():

    env = gym.make("RoboschoolKuka-v0")
    
    while 1:
        obs = env.reset()    
        for t in range(1000):
            if t%200==0: actions = np.random.uniform(-1,1,[9]) * np.pi/2.0 
            obs, r, done, _ = env.step(actions)
            still_open = env.render("human")

        


if __name__=="__main__":

    demo_run()
