import gym
import wumpus_env
import random

env = gym.make('wumpus-v0')
#states = env.observation_space.shape[0]


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
