# losses.py
# Authors: Jacob Schreiber <jmschreiber91@gmail.com>

"""
This module contains the losses used by BPNet for training.
"""

import torch

def MNLLLoss(logps, true_counts):
	"""A loss function based on the multinomial negative log-likelihood.

	This loss function takes in a tensor of normalized log probabilities such
	that the sum of each row is equal to 1 (e.g. from a log softmax) and
	an equal sized tensor of true counts and returns the probability of
	observing the true counts given the predicted probabilities under a
	multinomial distribution. Can accept tensors with 2 or more dimensions
	and averages over all except for the last axis, which is the number
	of categories.

	Adapted from Alex Tseng.

	Parameters
	----------
	logps: torch.tensor, shape=(n, ..., L)
		A tensor with `n` examples and `L` possible categories. 

	true_counts: torch.tensor, shape=(n, ..., L)
		A tensor with `n` examples and `L` possible categories.

	Returns
	-------
	loss: float
		The multinomial log likelihood loss of the true counts given the
		predicted probabilities, averaged over all examples and all other
		dimensions.
	"""

	log_fact_sum = torch.lgamma(torch.sum(true_counts, dim=-1) + 1)
	log_prod_fact = torch.sum(torch.lgamma(true_counts + 1), dim=-1)
	log_prod_exp = torch.sum(true_counts * logps, dim=-1) 
	return -torch.mean(log_fact_sum - log_prod_fact + log_prod_exp)

def log1pMSELoss(predicted_counts, true_counts):
	"""A MSE loss on the log(x+1) of the inputs.

	This loss will accept tensors of predicted counts and a vector of true
	counts and return the MSE on the log of the values. The squared error
	is calculated for each position in the tensor and then averaged, regardless
	of the shape.

	Note: Both tensors are in count space, not in log count space.

	Parameters
	----------
	predicted_counts: torch.tensor, shape=(n, ...)
		A tensor of predicted counts where the first axis is the number of
		examples.

	true_counts: torch.tensor, shape=(n, ...)
		A tensor of the true counts where the first axis is the number of
		examples.

	Returns
	-------
	loss: float
		The MSE loss on the log of the two inputs, averaged over all examples
		and all other dimensions.
	"""

	#log_pred = numpy.log(predicted_counts+1)
	log_pred = predicted_counts
	log_true = torch.log(true_counts+1)
	return torch.nn.MSELoss()(log_pred, log_true)