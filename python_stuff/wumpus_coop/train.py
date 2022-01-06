import gym
import numpy as np
import wumpus_env
import random
import time
import datetime
from datetime import timedelta

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

    env = DummyVecEnv([lambda: WumpusWorld()])

    print("Made environment")

    model = DQN("MlpPolicy", env, verbose=1)
    print("Made Model")
    model.learn(total_timesteps=10000, log_interval=4)
    print("Trained Model")
    model.save("dqn_test")
    print("Saved Model")

    del model

    model = DQN.load("dqn_test")
    print("Loaded Model")

    obs = env.reset()
    print("Reset Env")

    # random environment
    episodes = 10
    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        score = 0

        observations = env.observation_space
        print(observations)

        while not done:
            if rend == 1: env.render()
            action, _states = model.predict(obs, deterministic=True)
            if rend == 1: print(action)
            obs, reward, done, info = env.step(action)
            score += reward
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
