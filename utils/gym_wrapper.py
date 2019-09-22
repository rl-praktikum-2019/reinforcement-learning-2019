import gym
import numpy as np

BALL_RADIUS = 0.03

BALL_OBJECT_NAME = "object"
BALL_JOINT_NAME = "object:joint"


class ThrowEnvWrapper(gym.Wrapper):
    #
    #
    # Gym wrapper with features:
    # - new reward function
    # - detect ball collision with ground and reset
    #
    #
    def __init__(self, env):
        super(ThrowEnvWrapper, self).__init__(env)
        self.desired_ball_velocity = np.array([0, 0, 1])
        self.max_velocity = 0
        self.max_height = 0
        self.target_height = 0.4
        self.ball_velp = np.zeros((3,))
        self.ball_center_z = 0
        self.ball_center_vel_z = 0

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        return obs["observation"]

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        ball_center_pos = self.sim.data.get_joint_qpos(BALL_JOINT_NAME)
        self.ball_center_z = ball_center_pos[2]
        self.ball_velp = self.sim.data.get_joint_qvel(BALL_JOINT_NAME)[:3]
        self.ball_center_vel_z = self.ball_velp[2]

        self.ball_center_z = self.sim.data.get_joint_qpos(BALL_JOINT_NAME)[2]
        if self.ball_center_z <= BALL_RADIUS:
            print("Ball was dropped -> Reset Environment")
            done = True

        return observation["observation"], self.reward(reward), done, info

    def reward(self, reward):
        # reward = 0
        z_direction = np.sign(self.ball_center_vel_z)

        # if self.ball_center_z > self.target_height:
        #     print("Success. Ball in target region.")
        #     reward += 20
        #
        # if self.ball_center_z > self.target_height + 0.05:
        #     print("Success. Ball in target region.")
        #     reward += 40

        # if z_direction > 0:
        #     reward += (1 - self.ball_center_vel_z)

        # if abs(self.ball_center_vel_z) < 0.1:
        #     reward -= (1 - self.ball_center_vel_z) * 2

            # diff = np.absolute(self.dmp_action - self.ddpg_action)
            # correction = diff[diff < self.threshold] = 0
            # reward = sum(correction)

            # if z_direction > 0:
            #     reward += self.ball_center_vel_z * 10.
            #     reward += abs(self.ball_velp[0]) * -20.
            #     reward += abs(self.ball_velp[1]) * -20.

            # if self.ball_center_vel_z > self.max_velocity:
            #     velocity_reward = self.ball_center_vel_z * 10.
            #     reward += velocity_reward
            #     print("New achieved max velocity:", self.ball_center_vel_z)
            #     self.max_velocity = self.ball_center_vel_z

            # if self.ball_center_z > self.max_height:
            #     height_reward = self.ball_center_z * 20.
            #     reward += height_reward
            #     self.max_height = self.ball_center_z
            #     print("New achieved max height:", self.ball_center_z)

            # achieved = self.ball_velp / np.linalg.norm(self.ball_velp, ord=1)
            # delta_vel = self.desired_ball_velocity - achieved
            # d_vel = np.linalg.norm(delta_vel, axis=-1)
            # vel_reward = (10. * d_vel)
            # reward -= vel_reward

            # if self.ball_center_z <= BALL_RADIUS:
            #     print("Ball was dropped: -20 reward")
            #     return -100

            # if z_direction > 0:
            #     reward += (self.ball_center_z - self.target_height) * 10.
        return reward