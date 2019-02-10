from roboschool.gym_urdf_robot_env import RoboschoolUrdfEnv
from roboschool.scene_abstract import SingleRobotEmptyScene
from roboschool.scene_abstract import cpp_household


import numpy as np
import copy
import sys
import os

#------------------------------------------------------------------------------


class RoboschoolKuka(RoboschoolUrdfEnv):
    
    EYE_W = 60
    EYE_H = 40

    
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
        self.rendered_rgb_eye = np.zeros([self.EYE_H, self.EYE_W, 3], dtype=np.uint8)
        
        
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
        self.eye = self.scene.cpp_world.new_camera_free_float(self.EYE_W, self.EYE_H, "eye")
        return s

    def _render(self, mode, close):
        render_res = super(RoboschoolKuka, self)._render(mode, close)
        self.eye_adjust() 
        rgb_eye, _, _, _, _ = self.eye.render(False, False, False) # render_depth, render_labeling, print_timing)
        self.rendered_rgb_eye = np.fromstring(rgb_eye, dtype=np.uint8).reshape( (self.EYE_H,self.EYE_W,3) )
        
        return render_res

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
        return (self.get_contacts(), self.rendered_rgb_eye)

    def camera_adjust(self): 
        x, y, z = self.cpp_robot.root_part.pose().xyz()
        y += 0.5
        z += 0.3
        self.camera.move_and_look_at(.7, -.7, .8, x, y, z)
    
    def eye_adjust(self): 
        x, y, z = self.cpp_robot.root_part.pose().xyz()
        y += 0.5
        self.eye.move_and_look_at(.2, -.2, 1., x, y, z)
