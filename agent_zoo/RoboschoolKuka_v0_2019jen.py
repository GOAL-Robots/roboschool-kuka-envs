import os.path, time, gym
from OpenGL import GLU
import numpy as np
import roboschool


def demo_run():

    env = gym.make("RoboschoolKuka-v0")


    while 1:
        obs = env.reset()

        while 1:

            obs, r, done, _ = env.step((np.pi/2.0)*np.random.rand(7))

            still_open = env.render("human")

if __name__=="__main__":

    demo_run()
