import gym
import numpy as np
import wumpus_env
import random
import time
import datetime
from datetime import timedelta

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam


def build_model(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1, states)))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(actions, activation="linear"))
    return model

# outuput visible?
rend = 0


def main():
    # for saving timestamp and elapsed time
    now = datetime.datetime.now()
    start_time = time.time()

    env = gym.make('wumpus-v0')

    states = np.arange(32)
    actions = env.action_space

    model = build_model(states, actions)
    model.summary()

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
            action = random.choice(env.action_space)
            if rend == 1: print(action)
            n_state, reward, done, info = env.step(action)
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
