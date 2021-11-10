from gym.envs.registration import register

register(
    id='wumpus-v0',
    entry_point='wumpus_env.envs:WumpusWorld',
)
