import os.path, time, gym
from OpenGL import GLU
import numpy as np
import roboschool
import time

np.set_printoptions(formatter={"float": "{:4.2f}".format})

actions = np.array([
    [0,    0,    0,     0,    0,    0,    0,   .8,    .8],   
    [0,    0,    0,  -1.0,  1.0,    0,    0,   .8,    .8],   
    [0,  0.29,   0,  -0.95,  1.0,   0,    0,   .8,    .8],   
    [0,  0.29,   0,  -0.95,  1.0,   0,    0,   .15,    .9]])*np.pi/2.0

def demo_run():

    env = gym.make("RoboschoolKuka-v0")
    
    while 1:
        obs = env.reset()    
        still_open = env.render("human")
        c = 0
        for t in range(1000):
            if         t <  5:
                a = actions[0].copy()
            elif  5 < t <=20:
                a = actions[1].copy()
            elif 20 < t <=40:
                a = actions[2].copy()
            elif 40 < t <=400:
              a = actions[2].copy()
              a[7] = np.maximum(0.1,a[7] - (t-40)*0.01)
              a[8] = np.maximum(0.9,a[8] + (t-40)*0.001)
            elif t >400:
                a = actions[3].copy()
                a[1] = np.maximum(0.,a[1] - (t-60)*0.01)
            #     print(a[1])
            #     print( actions[3])
            #     print()
            
            obs, r, done, _ = env.step(a)
            
            
            still_open = env.render("human")
        


if __name__=="__main__":

    demo_run()
