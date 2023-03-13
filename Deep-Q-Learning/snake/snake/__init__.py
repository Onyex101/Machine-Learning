from gym.envs.registration import register

register(
    id='yeks_snake-v0',
    entry_point='snake.envs:SnakeEnv'
)