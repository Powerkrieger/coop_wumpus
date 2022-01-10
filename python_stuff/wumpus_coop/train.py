
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

# outuput visible?

rend = 1

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

    model = DQN("MultiInputPolicy", env, verbose=0)  # Changed to MultiInputPolicy for Dict obs space compatibility
    print("Made Model")
    model.learn(total_timesteps=500000, log_interval=100)
    print("Trained Model")
    model.save("dqn_test")
    print("Saved Model")

    del model

    model = DQN.load("dqn_test")
    print("Loaded Model")

    obs = env.reset()
    print("Reset Env")

    # random environment
    episodes = train_config.getint('train', 'train_episodes')
    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        score = 0

        a = ['MoveUp', 'MoveDown', 'MoveLeft', 'MoveRight', 'PickUp', 'PutDown', 'Climb', 'Scream', 'Nothing']
        while not done:
            if rend == 1: env.render()
            action, _states = model.predict(obs, deterministic=True)
            if rend == 1: print(a[action])
            obs, rewards, done, info = env.step(action)
            print(obs)
            score += rewards
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
