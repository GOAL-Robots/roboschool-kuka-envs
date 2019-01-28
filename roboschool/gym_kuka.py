from roboschool.gym_urdf_robot_env import RoboschoolUrdfEnv
from roboschool.scene_abstract import SingleRobotEmptyScene
import numpy as np

class RoboschoolKuka(RoboschoolUrdfEnv):
    def create_single_player_scene(self):
        return SingleRobotEmptyScene(gravity=0.0, timestep=0.0165, frame_skip=1)

    def __init__(self):
        RoboschoolUrdfEnv.__init__(self,
            "kuka_gripper_description/urdf/kuka_gripper.urdf",
            "pelvis",
            action_dim=30, obs_dim=70,
            fixed_base=False,
            self_collision=True)
    
    def reset(self, close=False):
        super(RoboschoolKuka, self)._reset()

    def render(self, mode, close=False):
        super(RoboschoolKuka, self)._render(mode, close)

    def apply_action(self, a):

        assert(len(a) == 9)

        kp = 0.1
        kd = 1.0
        vel = 400.0

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

    
    def step(self, a):
        assert(not self.scene.multiplayer)
        
        self.apply_action(a)
        
        self.scene.global_step()

        state = self.calc_state()
        state = np.zeros(1)
        self.rewards = []
        reward = None
        done = False
        info = {}

        self.HUD(state, a, done)

        return state, reward, done, info
    
    def robot_specific_reset(self):
        pass
    
    def calc_state(self):
        return None

    def camera_adjust(self):
        x, y, z = self.fingertip.pose().xyz()
        x *= 0.5
        y *= 0.5
        self.camera.move_and_look_at(0.3, 0.3, 0.3, x, y, z)
