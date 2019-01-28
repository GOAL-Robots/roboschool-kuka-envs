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

    obs = env.reset()
    
    t = 0
    c = 0
    while 1:
        if t%100 == 0:
             c += 1
        obs, r, done, _ = env.step(actions[c%5])
        still_open = env.render("human")
        t +=1
        


if __name__=="__main__":

    demo_run()
