import os.path, time, gym
from OpenGL import GLU
import numpy as np
import matplotlib.pyplot as plt
import roboschool
import time

plt.ion()

np.set_printoptions(formatter={"float": "{:4.2f}".format})

actions = np.array([
    [0,    0,    0,     0,    0,    0,    0,   .8,    .8],   
    [0,    0,    0,  -1.0,  1.0,    0,    0,   .8,    .8],   
    [0,  0.29,   0,  -0.95,  1.0,   0,    0,   .8,    .8],   
    [0,  0.29,   0,  -0.95,  1.0,   0,    0,   .15,    .9]])*np.pi/2.0


fig = plt.figure()
ax = fig.add_subplot(111)
img = ax.imshow(np.zeros([2,2]))

def demo_run():

    env = gym.make("RoboschoolKuka-v0")
    
    while 1:
        obs = env.reset()    
        c = 0
        input("trial")
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
            
            state, r, done, _ = env.step(a)
           
            contacts, = state
            if len(contacts)>0:
                for body_part, conts in contacts.items():
                    print("{} : {}".format(body_part, conts))
            else:
                print("--")
            
            #still_open = env.render("human")
            still_open = env.render("rgb_array")
            if t%3 == 0 or t == 999:
                img.set_array(still_open.reshape(400, 600, 3)) 
                plt.pause(0.1)


if __name__=="__main__":

    demo_run()
