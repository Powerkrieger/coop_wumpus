import argparse
import configparser
import datetime
import os
import random
import time
import wumpus_env
from datetime import timedelta

import gym


def main():
    # for saving timestamp and elapsed time
    now = datetime.datetime.now()
    start_time = time.time()

    parser = argparse.ArgumentParser('Parse configuration file')
    parser.add_argument('--env_config', type=str, default='config/env.config')
    parser.add_argument('--train_config', type=str, default='config/env.config')
    parser.add_argument('--output_dir', type=str, default='data/output')
    args = parser.parse_args()

    train_config = configparser.RawConfigParser()
    train_config.read(args.train_config)

    env = gym.make('wumpus-v0')
    env.configure(args.env_config)

    #random environment
    episodes = train_config.getint('train', 'train_episodes')



    for episode in range(1, episodes+1):
        state = env.reset()
        done = False
        score = 0
        a = ['MoveDown', 'MoveDown', 'MoveLeft', 'MoveLeft', 'MoveLeft', 'MoveDown', 'MoveUp']
        while not done:
            env.render()
            #action = random.choice(env.action_space)
            action = a.pop()
            print(action)
            n_state, reward, done, info = env.step(action)
            score += reward
        print('Episode:{} Score:{}'.format(episode, score))

    elapsed_time_secs = time.time() - start_time
    msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
    with open('times.txt', 'a') as f:
        f.write(str(now) + '\n')
        #for i in printargs:
        #    f.write(i + '\n')
        f.write(msg + '\n')
        f.write('end' + '\n')

if __name__ == '__main__':
    main()
