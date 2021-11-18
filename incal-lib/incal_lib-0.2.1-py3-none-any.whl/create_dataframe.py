import pandas as pd
import numpy as np


def create_calr_example_df(n_rows, start_date):
    '''

    '''
    np.random.seed(20)
    array = np.random.rand(n_rows)
    cumulative = np.cumsum(array)
    d = {
        'feature1_subject_1': array,
        'feature1_subject_2': array,
        'feature2_subject_1': cumulative,
        'feature2_subject_2': cumulative*2
    }
    idx = pd.date_range(start_date, periods=n_rows,
                        freq="MIN", name='Date_Time_1')
    return pd.DataFrame(data=d, index=idx)
