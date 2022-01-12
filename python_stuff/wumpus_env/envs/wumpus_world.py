import numpy as np
import copy
import gym
import configparser

from gym import error, spaces, utils
from gym.utils import seeding
import os
from wumpus_env.envs.utils.wumpus import Wumpus
from wumpus_env.envs.utils.robot import Robot

from collections import OrderedDict


def create_new_playing_field():
    # change this to be able to randomize the playing field
    board = []
    layout_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'layouts', 'wumpus_4x4_book.lay')
    # read the board file and construct the layout

    try:
        fin = open(layout_file, 'r', encoding='utf-8')
    except:
        print('Cannot read the layout file')

    for line in fin.readlines():
        if line.strip() == '':
            break
        tmp = line.strip().split(',')
        if '' in tmp:
            tmp.remove('')
        board.append(tmp)

    # check if board is valid
    # this is not a valid test, since it only checks for being rectangular but that doesnt even have to be a criterion
    # for i in range(len(board) - 1):
    #   assert len(board[i]) == len(board[i+1]), 'Board is not valid!'

    return board


class WumpusWorld(gym.Env):
    metadata = {'render.modes': ['text']}

    def __init__(self):

        self.exit_locs = None
        self.robots = None
        self.wumpus_awake = None
        self.robot_has_gold = None
        self.robot_has_arrow = None

        self.board = None
        self.base_reward = None
        self.high_reward = None
        self.config = None

        self.gold_loc = None
        self.robot_had_gold = None
        self.robot_was_exit = None

    def configure(self, config):
        self.robots = []
        self.num_robots = 0
        self.exit_locs = []
        self.board = create_new_playing_field()
        self.board = np.array(self.board, dtype=object)
        self.base_reward = 1
        self.high_reward = 1000
        self.config = config
        env_config = configparser.RawConfigParser()
        env_config.read(config)

        self.robot_had_gold = False
        self.robot_was_exit = False

        # self.final_num_robots = env_config.getint('env', 'num_robots')
        self.wumpus = None

        # set initial location of the agent
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row, col] == 'A':
                    self.robots.append(Robot(env_config, row, col, self.num_robots))
                    self.num_robots += 1
                    self.exit_locs.append((row, col))  # switched col, row to row, col
                elif self.board[row, col] == 'W':
                    self.wumpus = Wumpus(env_config, row, col)
                elif self.board[row, col] == 'G':
                    self.gold_loc = (row, col)
        assert len(self.robots) > 0, 'Agent not found :('

        # self.action_space = spaces.Discrete(['MoveUp', 'MoveDown', 'MoveLeft', 'MoveRight', 'PickUp', 'PutDown',
        # 'Climb', 'Scream', 'Nothing'])
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Dict({"stench": spaces.Discrete(2), "breeze": spaces.Discrete(2),
                                              "glitter": spaces.Discrete(2), "bump": spaces.Discrete(2),
                                              "scream": spaces.Discrete(2), "has_gold": spaces.Discrete(2),
                                              "gold_h": spaces.Discrete(10), "exit_h": spaces.Discrete(10)})
        self.robot_has_arrow = True
        self.robot_has_gold = False
        self.wumpus_awake = False

    def reset(self):
        self.configure(self.config)
        observations = []
        for robot in self.robots:
            observations.append(self._get_current_state(robot, False, False))
        # [stench, breeze, glitter, bump, scream, gold_h]

        obsdic = OrderedDict({"stench": observations[0][0], "breeze": observations[0][1],
                              "glitter": observations[0][2], "bump": observations[0][3],
                              "scream": observations[0][4], "has_gold": False,
                              "gold_h": observations[0][5], "exit_h": 0})

        return obsdic

    def exec_action(self, action_ind, robot):
        gameover = False
        scream = False

        gold_h_start = (abs(robot.loc[0] - self.gold_loc[0]) + abs(robot.loc[1] - self.gold_loc[1]))
        exit_h_start = (abs(robot.loc[0] - self.exit_locs[robot.num][0]) +
                        abs(robot.loc[1] - self.exit_locs[robot.num][1]))

        if action_ind == 0:
            # north
            if robot.loc[0] > 0:
                self.board[robot.loc] = '.' if self.board[robot.loc] == 'A' else self.board[robot.loc].replace('A&',
                                                                                                               '')
                robot.loc = (robot.loc[0] - 1, robot.loc[1])
            # Trying more complex reward calculation to emphazize stepping in the right dircetion
            if self.robot_has_gold:
                exit_h_end = (abs(robot.loc[0] - self.exit_locs[robot.num][0]) +
                              abs(robot.loc[1] - self.exit_locs[robot.num][1]))
                if exit_h_end == 0 and not self.robot_was_exit:
                    reward = self.high_reward / 10
                    self.robot_was_exit = True
                elif not self.robot_was_exit:
                    # reward = -self.base_reward + (2 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (2 * self.base_reward * (exit_h_start - exit_h_end))
                else:
                    # reward = -self.base_reward + (4 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (4 * self.base_reward * (exit_h_start - exit_h_end))
            else:
                gold_h_end = (abs(robot.loc[0] - self.gold_loc[0]) + abs(robot.loc[1] - self.gold_loc[1]))
                # reward = -self.base_reward + (2 * self.base_reward * (gold_h_start - gold_h_end))
                reward = -1 - self.base_reward * gold_h_end + (2 * self.base_reward * (gold_h_start - gold_h_end))

        elif action_ind == 1:
            # south
            if robot.loc[0] < len(self.board) - 1:
                self.board[robot.loc] = '.' if self.board[robot.loc] == 'A' else self.board[robot.loc].replace('A&',
                                                                                                               '')
                robot.loc = (robot.loc[0] + 1, robot.loc[1])
            # Trying more complex reward calculation to emphazize stepping in the right dircetion
            if self.robot_has_gold:
                exit_h_end = (abs(robot.loc[0] - self.exit_locs[robot.num][0]) +
                              abs(robot.loc[1] - self.exit_locs[robot.num][1]))
                if exit_h_end == 0 and not self.robot_was_exit:
                    reward = self.high_reward / 10
                    self.robot_was_exit = True
                elif not self.robot_was_exit:
                    # reward = -self.base_reward + (2 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (2 * self.base_reward * (exit_h_start - exit_h_end))
                else:
                    # reward = -self.base_reward + (4 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (4 * self.base_reward * (exit_h_start - exit_h_end))
            else:
                gold_h_end = (abs(robot.loc[0] - self.gold_loc[0]) + abs(robot.loc[1] - self.gold_loc[1]))
                # reward = -self.base_reward + (2 * self.base_reward * (gold_h_start - gold_h_end))
                reward = -1 - self.base_reward * gold_h_end + (2 * self.base_reward * (gold_h_start - gold_h_end))

        elif action_ind == 2:
            # west
            if robot.loc[1] > 0:
                self.board[robot.loc] = '.' if self.board[robot.loc] == 'A' else self.board[robot.loc].replace('A&',
                                                                                                               '')
                robot.loc = (robot.loc[0], robot.loc[1] - 1)
            # Trying more complex reward calculation to emphazize stepping in the right dircetion
            if self.robot_has_gold:
                exit_h_end = (abs(robot.loc[0] - self.exit_locs[robot.num][0]) +
                              abs(robot.loc[1] - self.exit_locs[robot.num][1]))
                if exit_h_end == 0 and not self.robot_was_exit:
                    reward = self.high_reward / 10
                    self.robot_was_exit = True
                elif not self.robot_was_exit:
                    # reward = -self.base_reward + (2 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (2 * self.base_reward * (exit_h_start - exit_h_end))
                else:
                    # reward = -self.base_reward + (4 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (4 * self.base_reward * (exit_h_start - exit_h_end))
            else:
                gold_h_end = (abs(robot.loc[0] - self.gold_loc[0]) + abs(robot.loc[1] - self.gold_loc[1]))
                # reward = -self.base_reward + (2 * self.base_reward * (gold_h_start - gold_h_end))
                reward = -1 - self.base_reward * gold_h_end + (2 * self.base_reward * (gold_h_start - gold_h_end))

        elif action_ind == 3:
            # east
            if robot.loc[1] < len(self.board[0]) - 1:
                self.board[robot.loc] = '.' if self.board[robot.loc] == 'A' else self.board[robot.loc].replace('A&',
                                                                                                               '')
                robot.loc = (robot.loc[0], robot.loc[1] + 1)
            # Trying more complex reward calculation to emphazize stepping in the right dircetion
            if self.robot_has_gold:
                exit_h_end = (abs(robot.loc[0] - self.exit_locs[robot.num][0]) +
                              abs(robot.loc[1] - self.exit_locs[robot.num][1]))
                if exit_h_end == 0 and not self.robot_was_exit:
                    reward = self.high_reward / 10
                    self.robot_was_exit = True
                elif not self.robot_was_exit:
                    # reward = -self.base_reward + (2 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (2 * self.base_reward * (exit_h_start - exit_h_end))
                else:
                    # reward = -self.base_reward + (4 * self.base_reward * (exit_h_start - exit_h_end))
                    reward = -1 - self.base_reward * exit_h_end + (4 * self.base_reward * (exit_h_start - exit_h_end))
            else:
                gold_h_end = (abs(robot.loc[0] - self.gold_loc[0]) + abs(robot.loc[1] - self.gold_loc[1]))
                # reward = -self.base_reward + (2 * self.base_reward * (gold_h_start - gold_h_end))
                reward = -1 - self.base_reward * gold_h_end + (2 * self.base_reward * (gold_h_start - gold_h_end))

        elif action_ind == 4:
            # pick up
            if self.board[robot.loc] == 'A&G':
                self.board[robot.loc] = 'A'
                self.robot_has_gold = True
                if self.robot_had_gold:
                    reward = -self.base_reward
                else:
                    reward = self.high_reward / 5
                    self.robot_had_gold = True
            else:
                reward = -self.base_reward * 10

        elif action_ind == 5:
            # put down
            if self.robot_has_gold and self.board[robot.loc] == 'A':
                self.board[robot.loc] = 'A&G'
                self.robot_has_gold = False
                reward = -self.base_reward
            else:
                reward = 10 * -self.base_reward

        elif action_ind == 6:
            # climb
            if robot.loc == self.exit_locs[robot.num] and self.robot_has_gold:
                reward = self.high_reward
                gameover = True
            elif robot.loc == self.exit_locs[robot.num]:
                reward = -self.high_reward
                gameover = True
            else:
                reward = -self.base_reward * (exit_h_start * 5)
                bump = True

        elif action_ind == 7:
            # scream
            scream = True
            reward = 9 * -self.base_reward
        elif action_ind == 8:
            # Nothing
            reward = 10 * -self.base_reward

        return reward, scream, gameover

    def step(self, actions, update=True):
        '''
        performs the exact action (not noisy!)
        '''
        bump = False
        observations = []
        rewards = []
        gameovers = []

        # set the agent on board! every agent??
        # new empty position
        for robot, action in zip(self.robots, [actions]):
            assert action in self.action_space, 'Unknown action! : ' + action
            # action_ind = self.action_space.index(action)
            action_ind = action
            old_robot_loc = copy.deepcopy(robot.loc)
            old_wumpus_loc = copy.deepcopy(self.wumpus.loc)

            # self.wumpus.check(old_robot_loc, robot.num)

            # stuff needs to happen here

            reward, scream, gameover = self.exec_action(action_ind, robot)

            # if wumpus moved, erase old position
            if old_wumpus_loc != self.wumpus.loc:
                self.board[old_wumpus_loc] = '.' if self.board[old_wumpus_loc] == 'W' else self.board[
                    old_wumpus_loc].replace('W&', '')

            # moved
            if old_wumpus_loc != self.wumpus.loc and self.board[self.wumpus.loc] == '.':
                self.board[self.wumpus.loc] = 'W'
            # caught by wumpus
            elif old_wumpus_loc != self.wumpus.loc and self.board[self.wumpus.loc] == 'A':
                self.board[robot.loc] = 'A&W'
            # standing on gold
            elif old_wumpus_loc != self.wumpus.loc and self.board[self.wumpus.loc] == 'G':
                self.board[self.wumpus.loc] = 'W&G'
            # walked against wall
            elif old_wumpus_loc == self.wumpus.loc:
                pass

            # moved
            if old_robot_loc != robot.loc and self.board[robot.loc] == '.':
                self.board[robot.loc] = 'A'
            # caught by wumpus
            elif old_robot_loc != robot.loc and self.board[robot.loc] == 'W':
                self.board[robot.loc] = 'A&W'
                reward = -self.high_reward
                gameover = True
            # fallen in pit
            elif old_robot_loc != robot.loc and self.board[robot.loc] == 'P':
                self.board[robot.loc] = 'A&P'
                reward = -self.high_reward
                gameover = True
            # standing on gold
            elif old_robot_loc != robot.loc and self.board[robot.loc] == 'G':
                self.board[robot.loc] = 'A&G'
            # walked against wall
            elif old_robot_loc == robot.loc and self.board[robot.loc] == 'A&W':
                reward = -self.high_reward
                gameover = True
            elif old_robot_loc == robot.loc:
                bump = True  # Removed -baseReward here because its not necessary and causing errors with climb

            state = self._get_current_state(robot, scream, bump)
            observations.append(state)
            rewards.append(reward)
            gameovers.append(gameover)

        done = True if sum(1 for x in gameovers if x) == self.num_robots else False

        # return state, reward, done, info

        stepdict = OrderedDict({"stench": state[0], "breeze": state[1],
                                "glitter": state[2], "bump": state[3],
                                "scream": state[4], "has_gold": self.robot_has_gold,
                                "gold_h": state[5], "exit_h": state[6]})

        return stepdict, rewards[0], done, {}

    def _get_current_state(self, robot, scream, bump):
        # robot.location and current position things!
        # [stench, breeze, glitter, bump, scream]
        # stench = [False] * self.num_robots -> Hotfix because one Bot WIP
        # breeze = [False] * self.num_robots -> Hotfix because one Bot WIP
        # glitter = [False] * self.num_robots -> Hotfix because one Bot WIP

        stench = False
        breeze = False
        glitter = False

        agent_fours = [
            # ob and location, ob for moving the wumpus therefor pointing in opposite direction
            (robot.loc[0] - 1, robot.loc[1]) if robot.loc[0] - 1 >= 0 else None,
            (robot.loc[0] + 1, robot.loc[1]) if robot.loc[0] + 1 < len(self.board) else None,
            (robot.loc[0], robot.loc[1] - 1) if robot.loc[1] - 1 >= 0 else None,
            (robot.loc[0], robot.loc[1] + 1) if robot.loc[1] + 1 < len(self.board[0]) else None,
            (robot.loc[0], robot.loc[1])
        ]

        for loc in agent_fours:
            if loc is not None:
                if 'P' in self.board[loc]:
                    breeze = True  # Hotfix, because List wasnt hepful -> breeze.append(True)
                if 'W' in self.board[loc]:
                    stench = True  # Hotfix, because List wasnt hepful -> stench.append(True)
                if 'G' in self.board[loc]:
                    glitter = True  # Hotfix, because List wasnt hepful -> glitter.append(True)

        gold_h = (abs(robot.loc[0] - self.gold_loc[0]) + abs(robot.loc[1] - self.gold_loc[1]))
        exit_h = (abs(robot.loc[0] - self.exit_locs[robot.num][0]) + abs(robot.loc[1] - self.exit_locs[robot.num][1]))

        obs = [stench, breeze, glitter, bump, scream, gold_h, exit_h]

        # Disabled to try Dict as obs space
        '''confignum = 0
        for x in range(len(obs)):
            if obs[x]:
                confignum = confignum + np.power(2, x)'''

        return obs

    def get_action_space(self):
        return self.action_space

    def render(self, mode='text'):
        print(self.print_env())

    def print_env(self):
        printer = ''.join(['########' for i in range(len(self.board[0]))]) + '#\n'

        for row in range(len(self.board)):
            printer += '#   '
            for col in range(len(self.board[0])):
                if 'A' not in self.board[row, col]:
                    printer += self.board[row, col] + '   |   '
                else:
                    # print agent
                    p = self.board[row, col]
                    if len(p) > 1:
                        p += ' |   '
                    else:
                        p += '   |   '
                    printer += p

            printer = printer[:-4] + '#\n'
            if row < len(self.board) - 1:
                printer += '#' + ''.join(['--------' for i in range(len(self.board[0]))])[:-1] + '#\n'
        printer += ''.join(['########' for i in range(len(self.board[0]))]) + '#\n'
        return printer

    def close(self):
        return
