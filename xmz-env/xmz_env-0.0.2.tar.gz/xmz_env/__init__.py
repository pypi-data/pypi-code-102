from gym.envs.registration import register

register(
    id='xmz_env-v1',
    entry_point='xmz_env.envs:Tic_Tac_Toe',
)