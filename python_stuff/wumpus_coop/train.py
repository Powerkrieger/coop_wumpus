import gym
import wumpus_env
import random
import time
import datetime
from datetime import timedelta
import numpy as np

def main():
    # for saving timestamp and elapsed time
    now = datetime.datetime.now()
    start_time = time.time()

    env = gym.make('wumpus-v0')

    # Init QTable
    qTable = [[]] * 32

    for x in range(len(qTable)):
        qTable[x] = np.array(np.arange(9))

    for x in range(len(qTable)):
        for y in range(len(qTable[x])):
            qTable[x][y] = 0

    allscore = 0

    # random environment
    episodes = 1000
    for episode in range(1, episodes+1):
        state = env.reset()
        done = False
        score = 0

        actions = env.action_space
        action = 'Nothing'
        n_state, reward, done, info = env.step(action)

        agentactions = []
        agentconfigs = []
        fullreward = 0

        while not done:
            env.render()

            confignum = 0
            for x in range(len(n_state)):
                if n_state[x]:
                    confignum = confignum + np.power(2, x)

            rand = random.randint(0, 100)
            if rand < 50 or not episode > 900:
                action = random.choice(env.action_space)
            else:
                actnr = 0
                actmaxrew = 0
                for x in range(len(qTable[confignum])):
                    if actmaxrew <= qTable[confignum][x]:
                        actnr = x
                        actmaxrew = qTable[confignum][x]

                action = actions[actnr]

            agentconfigs.append([n_state])
            agentactions.append(action)

            print(action)

            n_state, reward, done, info = env.step(action)
            score += reward

            fullreward += reward

            if rand < 50 or not episode > 900:
                qTable[confignum][actions.index(action)] = (qTable[confignum][actions.index(action)] + reward) / 2
            else:
                qTable[confignum][actnr] = (qTable[confignum][actnr] + reward) / 2

        print('Episode:{} Score:{}'.format(episode, score))
        allscore += score

        '''for a in range(len(agentconfigs)):

            confignum = 0
            for x in range(len(agentconfigs[a])):
                if agentconfigs[a][x]:
                    confignum = confignum + np.power(2, x)

            laction = agentactions[a]
            qTable[confignum][actions.index(laction)] = (qTable[confignum][actions.index(laction)] + fullreward) / 2'''

    print(qTable)
    print(allscore)

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
