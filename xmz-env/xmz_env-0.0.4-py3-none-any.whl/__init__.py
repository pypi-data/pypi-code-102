from gym.envs.registration import register

register(
    id='Tic_Tac_Toe-v4',
    entry_point='xmz_env.envs:Tic_Tac_Toe',
)