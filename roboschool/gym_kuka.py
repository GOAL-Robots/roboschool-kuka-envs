from myroboschool.gym_urdf_robot_env import RoboschoolUrdfEnv
from roboschool.scene_abstract import cpp_household
from roboschool.scene_stadium import SinglePlayerStadiumScene
import numpy as np

class RoboschoolKuka(RoboschoolUrdfEnv):
    def create_single_player_scene(self):
        return SinglePlayerStadiumScene(gravity=9.8, timestep=0.0165/8, frame_skip=8)   # 8 instead of 4 here

    def __init__(self):
        RoboschoolUrdfEnv.__init__(self,
            "kuka_description/urdf/kuka.urdf",
            "pelvis",
            action_dim=30, obs_dim=70,
            fixed_base=False,
            self_collision=True)
    
    def reset(self, close=False):
        super(RoboschoolKuka, self).reset()

    def render(self, mode, close=False):
        super(RoboschoolKuka, self).render(mode, close)

    def step(self, a):
        return None, None, False, None
    
    def robot_specific_reset(self):
        pass
    
    def calc_state(self):
        return None
