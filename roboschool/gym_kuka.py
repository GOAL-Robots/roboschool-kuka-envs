from roboschool.gym_urdf_robot_env import RoboschoolUrdfEnv
from roboschool.scene_abstract import SingleRobotEmptyScene
import numpy as np

class RoboschoolKuka(RoboschoolUrdfEnv):
    def create_single_player_scene(self):
        return SingleRobotEmptyScene(gravity=0.0, timestep=0.0165, frame_skip=1)

    def __init__(self):
        RoboschoolUrdfEnv.__init__(self,
            "kuka_description/urdf/kuka.urdf",
            "pelvis",
            action_dim=30, obs_dim=70,
            fixed_base=False,
            self_collision=True)
    
    def reset(self, close=False):
        super(RoboschoolKuka, self)._reset()

    def render(self, mode, close=False):
        super(RoboschoolKuka, self)._render(mode, close)

    def step(self, a):
        assert(not self.scene.multiplayer)
        #self.apply_action(a)
        self.jdict["lbr_iiwa_joint_1"].set_motor_torque(a[0])
        self.jdict["lbr_iiwa_joint_2"].set_motor_torque(a[1])
        self.jdict["lbr_iiwa_joint_3"].set_motor_torque(a[2])
        self.scene.global_step()

        #state = self.calc_state()  # sets self.to_target_vec
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
