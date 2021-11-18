def bayes_theorem(p_a: float, p_b_a: float, p_b_n_a: float):
    '''
        Function to calculate the probability of an event A occurring knowing that event B has already occurred
        Calculate P(A|B) given P(A), P(B|A), P(B|not A).

        :param p_a: P(A)
        :param p_b_a: P(B|A)
        :param p_b_n_a: P(B|not A)
        :return:  probability of an event

    '''
    not_a = 1 - p_a
    return p_b_a * p_a / (p_b_a * p_a + p_b_n_a * not_a)

#pypi-AgEIcHlwaS5vcmcCJDUyMjFiMDc4LTI4NzktNDk5NC1hNWM1LTU3MmM5OTJjYzM3OAACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgoc3UabQQW-GQuJA_46-9cbU3nkyM-m14zYwnevil1v0