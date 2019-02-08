from roboschool.gym_urdf_robot_env import RoboschoolUrdfEnv
from roboschool.scene_abstract import SingleRobotEmptyScene
from roboschool.scene_abstract import cpp_household
import pyglet, pyglet.window as pw, pyglet.window.key as pwk
from pyglet import gl


import numpy as np
import copy
import sys
import os

# ------------------------------------------------------------------------------------

#
# This opens a third-party window (not test window), shows rendered 
# chase camera, allows to control humanoid using keyboard (in a different way)
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

# ------------------------------------------------------------------------------------


class RoboschoolKuka(RoboschoolUrdfEnv):
    
    def create_single_player_scene(self):
        return SingleRobotEmptyScene(gravity=9.8, 
                timestep=0.0165, frame_skip=1)

    def __init__(self):
        super(RoboschoolKuka, self).__init__(
            "kuka_gripper_description/urdf/kuka_gripper.urdf",
            "pelvis",
            action_dim=30, obs_dim=70,
            fixed_base=False,
            self_collision=True)
        
        self.rgb_window = None
        
    def get_contacts(self):
        
        contact_dict = {}

        for part in self.urdf.parts:
            name = part.name
            contacts = [contact for contact 
                    in part.contact_list()
                    if not contact.name in self.robot_parts_names]
            
            if len(contacts)>0:
                contact_dict[name] = [contact.name 
                        for contact in contacts]
        return contact_dict
   
    def _reset(self):
        s = super(RoboschoolKuka, self)._reset()
        self.robot_parts_names = [part.name for part 
                in self.urdf.parts]
        return s

    def _render(self, mode, close):    
        self.rgb_image = super(RoboschoolKuka, self).\
            _render("rgb_array", close)
        if mode=="human":
            if self.rgb_window is None:
                self.rgb_window = PygletInteractiveWindow(self)

            self.rgb_window.imshow(self.rgb_image)
            self.rgb_window.each_frame()
            
            return self.rgb_window.still_open
        return True

    def robot_specific_reset(self):
         
        pose_robot = cpp_household.Pose()
        pose_robot.set_xyz(-0.8, 0, 0)
        self.cpp_robot.set_pose_and_speed(pose_robot, 0,0,0)

        # add table
        pose_table = cpp_household.Pose()
        self.urdf_table  = self.scene.cpp_world.load_urdf(
            os.path.join(os.path.dirname(__file__), "models_robot",
                "kuka_gripper_description/urdf/table.urdf"),
            pose_table, True, True)
        
        # add cube
        pose_cube = cpp_household.Pose()
        pose_cube.set_xyz(0.0, 0, 0.482)
        self.urdf_cube  = self.scene.cpp_world.load_urdf(
            os.path.join(os.path.dirname(__file__), "models_robot",
                "kuka_gripper_description/urdf/cube.urdf"),
            pose_cube, False, True)
                
    def apply_action(self, a):

        assert(len(a) == 9)

        kp = 0.1
        kd = 1.0
        vel = 400
    
        a[-1] = np.minimum(a[-1], np.pi/2 - a[-2])
        
        for i,j in enumerate(a[:-2]):
            self.jdict["lbr_iiwa_joint_%d"%(i+1)].set_servo_target(
                    j, kp, kd, vel)
        self.jdict["base_to_finger00_joint"].set_servo_target(
                a[-2],  kp, kd, vel)
        self.jdict["base_to_finger10_joint"].set_servo_target(
                 a[-2],  kp, kd, vel)
        self.jdict["finger00_to_finger01_joint"].set_servo_target(
                 -a[-1],  kp, kd, vel)
        self.jdict["finger10_to_finger11_joint"].set_servo_target(
                 -a[-1],  kp, kd, 0.01*vel)

    
    def _step(self, a):
        assert(not self.scene.multiplayer)
        
        self.apply_action(a)
        
        self.scene.global_step()

        state = self.calc_state()
        self.rewards = []
        reward = None
        done = False
        info = {}

        return state, reward, done, info
    
    def calc_state(self):
        return (self.get_contacts(), )

    def camera_adjust(self): 
        x, y, z = self.cpp_robot.root_part.pose().xyz()
        y += 0.5
        z += 0.3
        self.camera.move_and_look_at(.7, -.7, .8, x, y, z)
