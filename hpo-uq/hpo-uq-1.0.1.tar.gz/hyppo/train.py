# System
import os
import sys
import pickle
import logging
import importlib
import time

# External
import yaml
import numpy
from scipy.stats import median_abs_deviation

# Local
from .datasets import get_loader
from .dnnmodels import training, run_uq
from .hyperparams import get_hyperprms
from .utils.extract import gather_trials, check_evaluation_outer_loss
from .obj_fct import *


def train_evaluation(x_sc, samples, trainer, model, dist, output='out', data={}, uq={}, **kwargs):
    """
    Execute training according to requested trainer mode. This function looks at the
    trainer mode requested in the configuration file and initiate the training
    accordingly.
    
    Parameters
    ----------
    x_sc : :class:`dict`
      Random hyperparameter set. Each key corresponds to the hyperparameter names
      and the corresponding value to the randomly selected sample value.
    trainer : :class:`str`
      Trainer mode to be used.
    data : :class:`dict`
      Data setting extracted from the YAML configuration file.
    model : :class:`dict`
      Model setting extracted from the YAML configuration file.
    output : :class:`str`
      Directory name to save output training results.
      
    Returns
    -------
    res : :class:`float`
      Output of objective function.
    """
    # Start timer for recording function evaluation time
    start_time = time.time()
    # Display hyperparameter set only once, before the first trial
    hyperprms = get_hyperprms(x_sc, **model)
    # Prepare list of trial indexes to be evaluated in rank
    trials = numpy.arange(model['trial'])
    if dist['split']=='trial':
        trials = trials[dist['rank']::dist['size']]
    # Loop through all selected trials
    all_results = []
    for i in trials:
        out_path = '%s-%02i' % (output,i+1)
        if trainer=='internal':
            loaders = get_loader(data, **hyperprms, **model, **dist)
            results = training(itrial=i,data=loaders,hyperprms=hyperprms,output=out_path,**model,**dist)
        else:
            results = external_training(i, x_sc, trainer, out_path, model)
        all_results.append(results)
    # Prepare single results dictionary
    results = all_results[0]
    results['loss'] = [all_results[n]['loss'] for n in range(len(all_results))]
    results['models'] = [all_results[n]['models'] for n in range(len(all_results))]
    # Check if all losses over all trials are found
    res = None
    if dist['rank']==0:
        if dist['ntasks']>1:
            while len(gather_trials(results,samples,out_path,**model,**dist)['loss']) != model['trial']:
                continue
            results = gather_trials(results,samples,out_path,**model,**dist)
        # Remove trials that gave nan values
        idxs = numpy.argwhere(numpy.isnan(results['loss']))
        results['loss'] = numpy.delete(results['loss'],idxs)
        results['models'] = numpy.delete(results['models'],idxs)
        # Execute UQ or not
        if 'uq_on' in uq.keys() and uq['uq_on']==True:
            res = run_uq(**results,**model,**dist)
        else:
            logging.info('-'*40)
            logging.info('OUTER OBJECTIVE FUNCTION {:>8} TRIALS'.format(len(results['loss'])))
            logging.info('-'*40)
            logging.info('\tOuter Loss : {:>11.5f}'.format(numpy.median(results['loss'])))
            logging.info('\tMAD        : {:>11.5f}'.format(median_abs_deviation(results['loss'],scale='normal')))
            logging.info('\tMean Loss  : {:>11.5f}'.format(numpy.mean(results['loss'])))
            logging.info('\tSTD        : {:>11.5f}'.format(numpy.std(results['loss'])))
            res = numpy.nanmedian(results['loss'])
    else:
        logging.info('-'*40)
        logging.info('Waiting for other processes to finish...')
        while check_evaluation_outer_loss(samples,out_path,**dist)==False:
            continue
    logging.info('-'*40)
    logging.info("Execution Time : %.3f s" % (time.time() - start_time))
    return res

def external_training(itrial, x_sc, trainer, output_dir, model):
    start_time = time.time()
    logging.info('-'*40)
    logging.info('{} {:>3} / {:<3} {:>24}'.format('TRIAL',itrial+1,model['trial'],'TESTING'))
    logging.info('-'*40)
    if 'output_dir' in model.keys():
        model['output_dir'] = output_dir
    if 'yaml_input' in model.keys():
        params = yaml_creation(x_sc,output_dir,**model['yaml_input'])
    else:
        params = {**model,**x_sc}
    modlist = trainer.split('.')
    module = importlib.import_module('.' + modlist[-2], '.'.join(modlist[:-2]))
    loss = eval('module.'+modlist[-1])(**params)
    print(loss)
    logging.info('\t\tLoss : {:>11.5f}'.format(loss))
    logging.info('\t\tTime : {:>11.5f} s'.format(time.time()-start_time))
    return {'loss':loss,'models':None}

def yaml_creation(x_sc,output_dir,src,config=None,**kwargs):
    # Extract input configuration file
    with open(src) as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    # Update parameters
    if config==None:
        params = {**params,**x_sc}
    else:
        params[config] = {**params[config],**x_sc}
    # Save new input configuration file
    os.makedirs(output_dir,exist_ok=True)
    yaml_config = os.path.join(output_dir,'config.yaml')
    with open(yaml_config, 'w') as f:
        yaml.dump(params, f, default_flow_style=False)
    params = {'yaml_config':yaml_config,'config':config,**kwargs}
    return params