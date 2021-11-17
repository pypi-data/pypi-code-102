#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:38:16 2016

@author: becker
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
if __name__ == '__main__':
    import newtondata
else:
    from . import newtondata

#----------------------------------------------------------------------
def backtracking(f, x0, dx, resfirst, sdata, verbose=False):
    maxiter, omega, c = sdata.bt_maxiter, sdata.bt_omega, sdata.bt_c
    step = 1
    x = x0 + step*dx
    res = f(x)
    resnorm = np.linalg.norm(res)
    it = 0
    if verbose:
        print("{} {:>3} {:^10} {:^10}  {:^9}".format("bt", "it", "resnorm", "resfirst", "step"))
        print(f"bt {it:3} {resnorm:10.3e} {resfirst:10.3e} {step:9.2e}")
    while resnorm > (1-c*step)*resfirst and it<maxiter:
        it += 1
        step *= omega
        x = x0 + step * dx
        res = f(x)
        resnorm = np.linalg.norm(res)
        if verbose:
            print(f"bt {it:3} {resnorm:10.3e} {resfirst:10.3e} {step:9.2e}")
    return x, res, resnorm, step

#----------------------------------------------------------------------
class Baseopt:
    def __init__(self, f, sdata, n, verbose=False):
        self.f, self.sdata, self.verbose = f, sdata, verbose
        if not hasattr(sdata, 'nbase'): raise ValueError(f"please give 'nbase' in sdata")
        self.nbase, self.nused = sdata.nbase, 0
        self.sdata = sdata
        self.du = np.zeros(shape=(self.nbase,n))
        self.u0, self.u, self.r = np.zeros(n), np.zeros(n), np.zeros(n)
        self.ind = []
        self.iter = 0
    def res(self, x):
        self.u[:] = self.u0[:]
        for i in range(self.nused):
            # print(f"{i=} {np.linalg.norm(self.du[self.ind[i]])=}")
            self.u += x[i]*self.du[self.ind[i]]
        self.r = self.f(self.u)
        # print(f"{x=} {np.linalg.norm(self.u0)=}  {np.linalg.norm(self.u)=} {np.linalg.norm(self.r)=}")
        # x0 = x*x*(1-x)*(1-x)
        return np.linalg.norm(self.r)
        return self.r.dot(self.r)
    def step(self, u0, du, resfirst):
        # print(f"+++++++ {np.linalg.norm(u0)=} {np.linalg.norm(du)=} {resfirst=}")
        from scipy import optimize
        self.u0[:] = u0[:]
        self.resfirst = resfirst
        self.last = self.iter%self.nbase
        if self.nused == self.nbase:
            sp = np.abs([du.dot(self.du[self.ind[i]])/np.linalg.norm(self.du[self.ind[i]]) for i in range(self.nbase)])
            i = np.argmax(sp)
            self.last = i
            # print(f"{i=} {sp=}" )
            self.ind.pop(i)
        else:
            self.nused += 1
        self.ind.append(self.last)
        # print(f"{self.iter} {self.ind=} {np.linalg.norm(self.u0)}")
        self.du[self.last] = du
        x0 = np.zeros(self.nused)
        self.res(x0)
        # x0[-1] = 1
        self.iter += 1
        x0[-1] = 0.9
        # print(f"????????????? {self.iter=}")
        # if self.iter==1:
        #     resnorm = self.res(x0)
        #     return self.u, self.r, resnorm, 1
        method = 'COBYLA'
        # method = 'TNC'
        # method = 'BFGS'
        # method = 'CG'
        cons = ({'type': 'ineq', 'fun': lambda x:  self.res(x) - self.resfirst})
        options={'disp':True, 'maxiter':self.sdata.maxter_stepsize, 'gtol':1e-6}
        out = optimize.minimize(fun=self.res, constraints=cons, x0=x0, method=method, options=options)
        print(f"*************{out=}")
        if np.linalg.norm(self.r) > self.resfirst:
            print(f"*** nonmonotone {np.linalg.norm(self.r)=} {self.resfirst=} ** run again")
            options={'disp':False, 'maxiter':self.sdata.maxter_stepsize, 'gtol':1e-4}
            print(f"{out=}")
            x0.fill(0)
            x0[-1] = 0.5
            out2 = optimize.minimize(fun=self.res, x0=x0, method=method, options=options)
            print(f"{out2=}")
            # assert 0
        return self.u, self.r, np.linalg.norm(self.r), out.x

#--------------------------------------------------------------------
def newton(x0, f, computedx=None, sdata=None, verbose=False, jac=None, maxiter=None, resred=0.1):
    """
    Aims to solve f(x) = 0, starting at x0
    computedx: gets dx from f'(x) dx =  -f(x)
    if not given, jac is called and linalg.solve is used
    """
    if sdata is None:
        if maxiter is None: raise ValueError(f"if sdata is None please give 'maxiter'") 
        sdata = newtondata.StoppingData(maxiter=maxiter)
    atol, rtol, atoldx, rtoldx = sdata.atol, sdata.rtol, sdata.atoldx, sdata.rtoldx
    maxiter, divx = sdata.maxiter, sdata.divx
    x = np.asarray(x0)
    assert x.ndim == 1
    # n = x.shape[0]
    # print(f"{x0=}")
    if not computedx:  assert jac
    xnorm = np.linalg.norm(x)
    res = f(x)
    resnorm = np.linalg.norm(res)
    # print(f"--------- {np.linalg.norm(x)=} {resnorm=}")
    tol = max(atol, rtol*resnorm)
    toldx = max(atoldx, rtoldx*xnorm)
    name = 'newton'
    if hasattr(sdata,'addname'): name += '_' + sdata.addname
    if verbose:
        print("{} {:>3} {:^10} {:^10} {:^10} {:^5} {:^5} {:^3} {:^9}".format(name, "it", "|x|", "|dx|", '|r|','rhodx','rhor','lin', 'step'))
        print("{} {:3} {:10.3e} {:^10} {:10.3e} {:^9} {:^5} {:^5} {:^3}".format(name, 0, xnorm, 3*'-', resnorm, 3*'-', 3*'-', 3*'-', 3*'-'))
    # while( (resnorm>tol or dxnorm>toldx) and it < maxiter):
    dx, step, resold = None, None, np.zeros_like(res)
    iterdata = newtondata.IterationData(resnorm)
    if sdata.steptype == 'rb':
        bt = Baseopt(f, sdata, x.shape[0], verbose)
    while(resnorm>tol  and iterdata.iter < maxiter):
        if not computedx:
            J = jac(x)
            dx, liniter = linalg.solve(J, -res), 1
        else:
            dx, liniter = computedx(-res, x, iterdata)
        assert dx.shape == x0.shape
        if np.linalg.norm(dx) < sdata.atoldx:
            raise ValueError(f"*** correction too small: {liniter=} {np.linalg.norm(dx)=}")
        resold[:] = res[:]
        # print(f"--------- {np.linalg.norm(x)=} {resnorm=}")
        if sdata.steptype == 'rb':
            x, res, resnorm, step = bt.step(x, dx, resnorm)
        else:
            x, res, resnorm, step = backtracking(f, x, dx, resnorm, sdata, verbose=False)
        res2 = f(x)
        assert np.allclose(res, res2)
        iterdata.newstep(dx, liniter, resnorm, step)
        xnorm = linalg.norm(x)
        if verbose:
            print(f"{name} {iterdata.iter:3} {xnorm:10.3e} {iterdata.dxnorm[-1]:10.3e} {resnorm:10.3e} {iterdata.rhodx:5.2f} {iterdata.rhor:5.2f} {liniter:3d} {step}")
        if xnorm >= divx:
            return (x, maxiter, np.mean(iterdata.liniter))
    return (x,iterdata.iter, np.mean(iterdata.liniter))


# ------------------------------------------------------ #

if __name__ == '__main__':
    f = lambda x: 10.0 * np.sin(2.0 * x) + 4.0 - x * x
    df = lambda x: 20.0 * np.cos(2.0 * x) - 2.0 * x
    f = lambda x: x**2 -11
    df = lambda x: 2.0 * x
    def computedx(r, x, info):
        return r/df(x),1
    x0 = [3.]
    info = newton(x0, f, jac=df, verbose=True, maxiter=10)
    info2 = newton(x0, f, computedx=computedx, verbose=True, maxiter=10)
    print(('info=', info))
    assert info==info2
    x = np.linspace(-1., 4.0)
    plt.plot(x, f(x), [x[0], x[-1]], [0,0], '--r')
    plt.show()
