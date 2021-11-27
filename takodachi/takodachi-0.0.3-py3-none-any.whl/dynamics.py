"""Routine for dyanmics"""

import numpy as np
from numpy import exp

def get_traj_from_steps(xtar_indices, xc, dt, gam, with_xtar=False):

    step_indices, = np.nonzero(np.diff(xtar_indices))
    N_step = step_indices.size
    N_interval = N_step + 1
    
    num_accum_arr = np.empty(N_interval,dtype=int)
    num_accum_arr[:-1] = step_indices + 1
    num_accum_arr[-1] = xtar_indices.size
    
    num_arr = np.empty((N_interval,), dtype=int)
    num_arr[0] = num_accum_arr[0]
    num_arr[1:] = np.diff(num_accum_arr)
    
    j_start_arr = np.array([Nacc-N for Nacc, N in zip(num_accum_arr, num_arr)])

    xtar = xc[xtar_indices]

    x_eq_of_interval_arr = xc[xtar_indices[j_start_arr]] 

    
    #### Evaluate trajectory : `x`
    
    x = np.empty(xtar.size)

    x[0] = xtar[0]
    xdot0 = 0.

    x[0:num_arr[0]] = x_eq_of_interval_arr[0]

    for j_interval in range(1,j_start_arr.size):
        j_start = j_start_arr[j_interval]
        N_interval = num_arr[j_interval]
        t_interval_arr = dt * np.arange(1,N_interval+1)
        x_eq = x_eq_of_interval_arr[j_interval]
        x0 = x[j_start-1] - x_eq  # displacment
        x[j_start:j_start+N_interval] = \
                x_eq + exp(-gam*t_interval_arr) \
                        * ( x0 + (xdot0 + gam*x0)*t_interval_arr )
        xdot0 = exp(-gam*t_interval_arr[-1]) \
                    * (xdot0 - gam*(xdot0+gam*x0)*t_interval_arr[-1])  
        
    res = x
    if with_xtar: res = (res,xtar)
    return res

