import os.path, time, gym
from OpenGL import GLU
import numpy as np
import roboschool
import time


actions = np.array([
    [0,     0.25,    0,    0,     0.25,     0,    0,   .5,     .8],   
    [0,     0.25,    0,    0,     0.1,      0,    0,   .3,    0.8],
    [0,     0.25,    0,    0.25,  0.1,      0,    0,   .5,    0.8],
    [0,     0.25,    0,    0.25,  0.5,      0,    0,   .1,    0.1],
    [0.1,   0.25,    0,    0,     0.25,     0.3,  0,   .5,    0.8]])*np.pi/2.0

def demo_run():

    env = gym.make("RoboschoolKuka-v0")
    
    while 1:
        obs = env.reset()    
        c = 0
        for t in range(1000):
            if t%20==0: c += 1 
            obs, r, done, _ = env.step(actions[c%5])
            still_open = env.render("human")

        


if __name__=="__main__":

    demo_run()
