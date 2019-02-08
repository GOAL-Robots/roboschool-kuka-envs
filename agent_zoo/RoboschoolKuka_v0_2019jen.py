import os.path, time, gym
from OpenGL import GLU
import numpy as np
import roboschool
import time
import pyglet, pyglet.window as pw, pyglet.window.key as pwk
from pyglet import gl


#
# This opens a third-party window (not test window), shows rendered chase camera, allows to control humanoid
# using keyboard (in a different way)
#

class PygletInteractiveWindow(pw.Window):
    def __init__(self, env):
        pw.Window.__init__(self, width=600, height=400, vsync=False, resizable=True)
        self.theta = 0
        self.still_open = True

        @self.event
        def on_close():
            self.still_open = False

        @self.event
        def on_resize(width, height):
            self.win_w = width
            self.win_h = height

        self.keys = {}
        self.human_pause = False
        self.human_done = False

    def imshow(self, arr):
        H, W, C = arr.shape
        assert C==3
        image = pyglet.image.ImageData(W, H, 'RGB', arr.tobytes(), pitch=W*-3)
        self.clear()
        self.switch_to()
        self.dispatch_events()
        texture = image.get_texture()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        texture.width  = W
        texture.height = H
        texture.blit(0, 0, width=self.win_w, height=self.win_h)
        self.flip()

    def on_key_press(self, key, modifiers):
        self.keys[key] = +1
        if key==pwk.ESCAPE: self.still_open = False

    def on_key_release(self, key, modifiers):
        self.keys[key] = 0

    def each_frame(self):
        self.theta += 0.05 * (self.keys.get(pwk.LEFT, 0) - self.keys.get(pwk.RIGHT, 0))



def demo_run():
   
    np.set_printoptions(formatter={"float": "{:4.2f}".format})

    actions = np.array([
        [0,    0,    0,     0,    0,    0,    0,   .8,    .8],   
        [0,    0,    0,  -1.0,  1.0,    0,    0,   .8,    .8],   
        [0,  0.29,   0,  -0.95,  1.0,   0,    0,   .8,    .8],   
        [0,  0.29,   0,  -0.95,  1.0,   0,    0,   .25,   .3]])*np.pi/2.0

    env = gym.make("RoboschoolKuka-v0")


    while 1:
        obs = env.reset()    
        for t in range(1000):
            if         t <  5:
                a = actions[0].copy()
            elif  5 < t <=20:
                a = actions[1].copy()
            elif 20 < t <=40:
                a = actions[2].copy()
            elif 40 < t <=600:
              a = actions[2].copy()
              a[7] = np.maximum(0.25,a[7] - (t-40)*0.01)
              a[8] = np.maximum(0.3,a[8] - (t-40)*0.001)
            elif t >600:
              a[1] = np.maximum(0.,a[1] - (t-60)*0.01)
            
            state, r, done, _ = env.step(a)
           
            contacts, = state
            if len(contacts)>0:
                for body_part, conts in contacts.items():
                    print("{} : {}".format(body_part, conts))
            else:
                print("--")
           
            still_open = env.render("human")
            if not still_open : return
        
if __name__=="__main__":

    demo_run()
