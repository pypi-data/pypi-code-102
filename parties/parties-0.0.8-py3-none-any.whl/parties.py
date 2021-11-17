import numpy as np
import pandas as pd
import os
import subprocess
from subprocess import PIPE
import h5py
import sys
from collections import OrderedDict
from itertools import product
from icecream import ic
import fileinput

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

ic.enable()

class simulation:
    def __init__(self,
                 proc_num = 2,
                 PARTIESINP = 'parties.inp',
                 BOUNDARYH = 'srx/Include/Boundary.h',
                 log_name = 'tmp.log',
                 run_command = 'mpirun',
                 ):
        #Default variables
        self.proc_num = proc_num
        self.PARTIESINP = PARTIESINP
        self.log_name = log_name
        self.run_command = run_command
        self.tmp_log_file = None
        self.parties = None #process variable - to start/stop simulation
        self.run_status = False
        self.vars = None
        self.stop_flag = False
        
    def rm_log(self):
        os.system('rm '+ self.log_name)

    def run(self):
        self.tmp_log_file = open(self.log_name,'a')
        if self.proc_num > 1:
            self.parties = subprocess.Popen([self.run_command,'-np', str(self.proc_num), './parties'],stdout=self.tmp_log_file)
        if self.proc_num == 1:
            self.parties = subprocess.Popen(['./parties'],stdout=self.tmp_log_file)
        self.status = True

    def stop(self):
        self.parties.kill()
        self.status = False
        self.stop_flag = False

    def cartesian_product(self,vars):
        od = OrderedDict(sorted(vars.items()))
        cart = list(product(*od.values()))
        return pd.DataFrame(cart,columns=od.keys())

    def change_line(self, file_name, line_keyword, value):
        for line in fileinput.input([file_name], inplace=True):
            if line.strip().startswith(line_keyword):
                new_line = line_keyword + str(value) + '\n'
                line = new_line
            sys.stdout.write(line)

    def change_parties_inp(self,cols,row):
        for comp in range(len(cols)):
            line_keyword = cols[comp]
            value = row[cols[comp]]
            self.change_line(self.PARTIESINP,line_keyword,value)

    def make(self):
        os.system('make clean')
        os.system('make')
        print('make')



class post_process:
    def __init__(self, **kwargs):
        self.text_out_files = None
        self.figures_folders = None
        self.postfix = ""
    
    def get(self, name, idx, flags, **kwargs):
        filename= name +'_'+str(idx)+'.h5'
        try:
            f = h5py.File(filename,'r')
        except:
            print('Unable to open the file')

        try:
            for i,flag in enumerate(flags):
                if i is 0: 
                    res = f.get(flag)
                else: res = res.get(flag)
            return res
        except:
            print('Unable to find the variable')
            return -1.0
        
    def set_postfix(self,cols,row):
        self.postfix=""
        for comp in range(len(cols)):
            line_keyword = cols[comp]
            value = row[cols[comp]]
            if type(value) is np.float64: value = round(value,3)
            tmp = line_keyword.replace(" ","")
            tmp = tmp.replace("=","")
            self.postfix += tmp + "_" + str(value)
            if comp < (len(cols)-1): self.postfix += "_"

    #revisit this function to account for staggered grid
    def plot_XY_vel_mag_contour(self,
                                out_name,
                                file_idx,
                                plane_position='mid',
                                **kwargs):

        prev_kwargs = kwargs

        #Position of the slicing plane
        if plane_position is 'mid': p_pos=int(self.get('Data',file_idx,['grid','NZ'])[0]/2)
        else: p_pos=plane_position

        u = self.get('Data',file_idx,['u'])[p_pos]
        v = self.get('Data',file_idx,['v'])[p_pos]
        w = self.get('Data',file_idx,['w'])[p_pos]

        #Create a x,y data matrix for plot
        NX = self.get('Data',file_idx,['grid','NX'])[0]
        nx=complex(0,NX)
        NY = self.get('Data',file_idx,['grid','NY'])[0]
        ny = complex(0,NY)
        x_min = self.get('Data',file_idx,['grid','xu'])[0]
        x_max = self.get('Data',file_idx,['grid','xu'])[NX-1]
        y_min = self.get('Data',file_idx,['grid','yv'])[0]
        y_max = self.get('Data',file_idx,['grid','yv'])[NY-1]

        Y, X = np.mgrid[y_min:y_max:ny, x_min:x_max:nx]
        speed = np.sqrt(u**2 + v**2 + w**2)

        #Figure parameters
        fig = plt.figure(figsize=(NX/20+(0.05*NX/20), NY/20))
        gs = gridspec.GridSpec(nrows=1, ncols=1)
        plt.pcolormesh(X,Y, speed,shading="nearest", alpha = 1.0,**prev_kwargs)
        
        #Colorbar parameters
        ax = plt.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(cax=cax)
        
        #Savefigure
        plt.savefig(out_name + str(file_idx) + '.png')



class multiple_simulations:
    def __init__(self,
                 n_avail_proc = 20,
                 n_pps = 10
                 ):
        self.sim_list=[]
        self.n_avail_proc = n_avail_proc
        self.n_pps = n_pps #number of processors per simulation
    def run_serial(self):
        #create pandas table of simulations
        #while loop to run in sequence
        return 0
    def run_parallel(self):
        #create pandas table of simulations
        # sim_index | sim_name | sim_runs | status | list of parameters
        #While loop which check the status of simulations
        return 0
