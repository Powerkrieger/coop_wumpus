
import gym
import numpy as np

import argparse
import configparser
import datetime
import os

import random
import time

import stable_baselines3

import wumpus_env
from datetime import timedelta

from stable_baselines3.common import env_checker
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from wumpus_env.envs import WumpusWorld

# Outuput visible?
rend = 1

# Mode? (0 -> Make new model; 1 -> Use existing model; steps -> Number of training steps to take)
m_mode = 1
steps = 500000

def main():
    # for saving timestamp and elapsed time
    now = datetime.datetime.now()
    start_time = time.time()

    print("Main started")
    # evaluate arguments
    parser = argparse.ArgumentParser('Parse configuration file')
    parser.add_argument('--env_config', type=str, default='config/env.config')
    parser.add_argument('--train_config', type=str, default='config/env.config')
    parser.add_argument('--output_dir', type=str, default='data/output')
    args = parser.parse_args()
    # read config
    train_config = configparser.RawConfigParser()
    train_config.read(args.train_config)

    env = gym.make("wumpus-v0")
    env.configure(args.env_config)
    stable_baselines3.common.env_checker.check_env(env, warn=True, skip_render_check=True)
    
    print("Made environment")

    if m_mode == 0:
        print("[ModelMaker]: Rebuilding Model from scratch")
        model = DQN("MultiInputPolicy", env, verbose=1)  # Changed to MultiInputPolicy for Dict obs space compatibility
        print("[ModelMaker]: Made Model")
        print("[ModelMaker]: Training model in", steps, "steps.")
        model.learn(total_timesteps=steps, log_interval=100)
        print("[ModelMaker]: Training completed.")
        model.save("dqn_test")
        print("[ModelMaker]: Model saved.")
        print("[ModelMaker]: Done!")

    if m_mode == 1:
        print("[ModelTester]: Using old model for testing purposes")

        model = DQN.load("dqn_test")
        print("[ModelTester]: Successfully loaded Model")

        obs = env.reset()
        print("[ModelTester]: Environment reset.")

        # random environment
        print("[ModelTester]: Start testing..")
        a = ['MoveUp', 'MoveDown', 'MoveLeft', 'MoveRight', 'PickUp', 'PutDown', 'Climb', 'Scream', 'Nothing']
        # episodes = train_config.getint('train', 'train_episodes')
        episodes = 2
        for episode in range(1, episodes + 1):
            state = env.reset()
            done = False
            score = 0

            while not done:
                if rend == 1: env.render()
                action, _states = model.predict(obs, deterministic=True)
                if rend == 1: print(a[action])
                obs, rewards, done, info = env.step(action)
                if rend == 1: print(obs)
                score += rewards
                if rend == 1: print(score)
            if rend == 1: print('Episode:{} Score:{}'.format(episode, score))

        elapsed_time_secs = time.time() - start_time
        msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))

        with open('times.txt', 'a') as f:
            f.write(str(now) + '\n')
            # for i in printargs:
            #    f.write(i + '\n')
            f.write(msg + '\n')
            f.write('end' + '\n')


if __name__ == '__main__':
    main()
