import gym
import wumpus_env
import random
import time
from datetime import timedelta

def main():
    start_time = time.time()
    env = gym.make('wumpus-v0')

    #random environment
    episodes = 10
    for episode in range(1, episodes+1):
        state = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            action = random.choice(env.action_space)
            print(action)
            n_state, reward, done, info = env.step(action)
            score += reward
        print('Episode:{} Score:{}'.format(episode, score))

    elapsed_time_secs = time.time() - start_time
    msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
    with open('times.txt', 'a') as f:
        f.write(datetime.fromtimestamp(start_time))
        #for i in printargs:
        #    f.write(i + '\n')
        f.write(msg + '\n')
        f.write('end' + '\n')

if __name__ == '__main__':
    main()
