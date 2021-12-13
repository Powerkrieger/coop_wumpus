import numpy as np
import copy
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os

class WumpusWorld(gym.Env):
    metadata = {'render.modes': ['text']}

    def __init__(self):

        self.agents = []
        self.board = self.create_new_playing_field()
        self.board = np.array(self.board, dtype=object)
        self.base_reward = 1
        self.high_reward = 1000

        # set initial location of the agent
        self.agent_loc = None
        self.wumpus_loc = None
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row, col] == 'A':
                    self.agent_loc = (row, col)
                elif self.board[row, col] == 'W':
                    self.wumpus_loc = (row, col)
        assert self.agent_loc != None, 'Agent not found :('

        # set the default heading as north -> 0: N, 1: E, 2: S, 3: W
        self.agent_head = 0
        self.exit_loc = copy.deepcopy(self.agent_loc)
        self.action_space = ['MoveUp','MoveDown','MoveLeft','MoveRight', 'PickUp', 'PutDown', 'Climb', 'Scream', 'Nothing']
        self.agent_has_arrow = True
        self.agent_has_gold = False

    def create_new_playing_field(self):
        #change this to be able to randomize the playing field
        board = []
        layout_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'layouts', 'wumpus_4x4_book.lay')
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
        # this is not a valid test, since it only checks for being rechteckig but that doesnt even have to be a criterion
        for i in range(len(board) - 1):
            assert len(board[i]) == len(board[i+1]), 'Board is not valid!'

        return board

    def reset(self):
        self.__init__()
        return self._get_current_state(False, False)

    def step(self, action, update=True):
        '''
        performs the excat action (not noisy!)
        '''
        assert action in self.action_space, 'Unknown action!'
        action_ind = self.action_space.index(action)
        gameover = False
        scream = False
        bump = False

        pas_loc = copy.deepcopy(self.agent_loc)
        if action_ind == 0:
            #north
            if self.agent_head == 0 and self.agent_loc[0] > 0:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0] - 1, self.agent_loc[1])
            self.agent_head = 0
            reward = -base_reward

        elif action_ind == 1:
            #south
            if self.agent_head == 2 and self.agent_loc[0] < len(self.board) - 1:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0] + 1, self.agent_loc[1])
            self.agent_head = 2
            reward = -base_reward

        elif action_ind == 2:
            #west
            if self.agent_head == 3 and self.agent_loc[1] > 0:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0], self.agent_loc[1] - 1)
            self.agent_head = 3
            reward = -base_reward

        elif action_ind == 3:
            #east
            if self.agent_head == 1 and self.agent_loc[1] < len(self.board[0]) - 1:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0], self.agent_loc[1] + 1)
            self.agent_head = 1
            reward = -base_reward

        elif action_ind == 4:
            #pick up
            if self.board[self.agent_loc] == 'A&G':
                self.board[self.agent_loc] = 'A'
                self.agent_has_gold = True
            reward = -base_reward
        elif action_ind == 5:
            #put down
            if self.agent_has_gold and self.board[self.agent_loc] == 'A':
                self.board[self.agent_loc] = 'A&G'
                self.agent_has_gold = False
            reward = -base_reward
        elif action_ind == 6:
            # climb
            if self.agent_loc == self.exit_loc and self.agent_has_gold:
                reward = high_reward
                gameover = True
            elif self.agent_loc == self.exit_loc:
                gameover = True
                reward = -high_reward
            else:
                reward = -base_reward
                bump = True

        elif action_ind == 7:
            # scream
            scream = True
            reward = -base_reward
        elif action_ind == 8:
            #Nothing
            reward = -base_reward

        # set the agent on board!
        if pas_loc != self.agent_loc and self.board[self.agent_loc] == '.':
            self.board[self.agent_loc] = 'A'
        elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'W':
            self.board[self.agent_loc] = 'A&W'
            reward = -high_reward
            gameover = True
        elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'P':
            self.board[self.agent_loc] = 'A&P'
            reward = -high_reward
            gameover = True
        elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'G':
            self.board[self.agent_loc] = 'A&G'
        elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'X':
            self.board[self.agent_loc] = 'A&X'
        elif pas_loc == self.agent_loc:
            bump = True
            reward = -base_reward

        # return state, reward, done, info
        return self._get_current_state(scream, bump), reward, gameover, {}

    def _get_current_state(self, scream, bump):
        # agent_location and current position things!
        # [stench, breeze, glitter, bump, scream]
        stench = False
        breeze = False
        glitter = False

        agent_fours = [
            (self.agent_loc[0] - 1, self.agent_loc[1]) if self.agent_loc[0] - 1 >= 0 else None,
            (self.agent_loc[0] + 1, self.agent_loc[1]) if self.agent_loc[0] + 1 < len(self.board) else None,
            (self.agent_loc[0], self.agent_loc[1] - 1) if self.agent_loc[1] - 1 >= 0 else None,
            (self.agent_loc[0], self.agent_loc[1] + 1) if self.agent_loc[1] + 1 < len(self.board[0]) else None,
            (self.agent_loc[0], self.agent_loc[1])
        ]

        for loc in agent_fours:
            if loc != None:
                if 'P' in self.board[loc]:
                    breeze = True
                elif 'W' in self.board[loc]:
                    stench = True
                elif 'G' in self.board[loc]:
                    glitter = True
        return [stench, breeze, glitter, bump, scream]

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
                    # print agent in a different way -> use heading
                    p = self.board[row, col]
                    if self.agent_head == 0:
                        p = p.replace('A', '^')
                    elif self.agent_head == 1:
                        p = p.replace('A', '>')
                    elif self.agent_head == 2:
                        p = p.replace('A', 'v')
                    elif self.agent_head == 3:
                        p = p.replace('A', '<')
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
