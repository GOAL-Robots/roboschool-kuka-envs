import os.path, time, gym
from OpenGL import GLU
import numpy as np
import roboschool
import time


actions = np.array([
    [0,     0.25,    0,    0,     0.25,     0,    0,   .15,    0.35],   
    [0,     0.25,    0,    0,     0.1,      0,    0,   .15,    0.35],
    [0,     0.25,    0,    0.25,  0.1,      0,    0,   .15,    0.1],
    [0,     0.25,    0,    0.25,  0.5,      0,    0,   .15,    0.1],
    [0.1,   0.25,    0,    0,     0.25,     0.3,  0,   .25,    0.0]])*np.pi

def demo_run():

    env = gym.make("RoboschoolKuka-v0")

    env1 = gym.make("RoboschoolKukaEnv-v0")
    
    t = 0
    while 1:
        obs = env.reset()    
        obs1 = env1.reset()    
        c = 0
        for t in range(100):
            if t%20==0: a = np.random.rand(9)*np.pi/2
            obs, r, done, _ = env.step(a)
            still_open = env.render("human")

        


if __name__=="__main__":

    demo_run()
