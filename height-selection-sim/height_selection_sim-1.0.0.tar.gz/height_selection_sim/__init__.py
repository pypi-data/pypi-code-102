#!/usr/bin/env python

"""
height_selection_sim: Simple Python program to simulate the effects of negative selection on a synthetic population of humans
"""

###########
# imports #
###########
import logging
import numpy
import random
import sys

####################
# Version and name #
####################
__proj_name__ = 'height_selection_sim'
__version__ = '1.0.0'

#############
# constants #
#############
death_prob = [ 0.005, 0.001, 0.02, 0.03, 0.05, 0.07, 0.10, 0.20, 0.50, 0.80, 1.0 ]
reproduce_prob = [ 0.0, 0.0015, 0.45, 0.75, 0.55, 0.45, 0.20, 0.0095, 0.00475, 0.0, 0.0 ]
ref_male_average_height = 175.0
ref_male_standard_dev_height = 7.0
ref_female_average_height = 162.2
ref_female_standard_dev_height = 6.0
high_standard_dev_trigger = 14.0
low_standard_dev_trigger = 1.0
zscore_trigger = 15.0

###########
# Classes #
###########
class Person:
	def __init__( self, logger, male_height_avg, male_height_sd, female_height_avg, female_height_sd, father = None, mother = None, lower_bound = 54.6, upper_bound = 272.0 ):

		# Boundaries default:
		# Upper - Robert Wadlow
		# Lower - Chandra Bahadur Dangi
		logger.debug( "Making person..." )

		############
		# validity #
		############
		if male_height_avg is None or male_height_avg <= 0.0:
			logger.error( "Male height average must be greater than 0.0 and not None" )
			sys.exit( 1 )

		if male_height_sd is None or male_height_sd <= 0.0:
			logger.error( "Male height standard deviation must be greater than 0.0 and not None" )
			sys.exit( 1 )

		if female_height_avg is None or female_height_avg <= 0.0:
			logger.error( "Female height average must be greater than 0.0 and not None" )
			sys.exit( 1 )

		if female_height_sd is None or female_height_sd <= 0.0:
			logger.error( "Female height standard deviation must be greater than 0.0 and not None" )
			sys.exit( 1 )

		#######################
		# assign sex randomly #
		#######################
		self.sex = random.choice( [ 'male', 'female' ] )

		#################################################
		# generate age and height based on if this is a #
		# reproduction or initialization                #
		#################################################
		# initialization - height based on population sex averages
		if father is None and mother is None:
			self.age = random.choice( [ 0, 1, 2, 3, 4, 5 ] )

			if self.sex == 'male':
				self.height = numpy.random.normal( loc = male_height_avg, scale = male_height_sd )
			else:
				self.height = numpy.random.normal( loc = female_height_avg, scale = female_height_sd )
		# reproduction - height biased up and down by parents height Z scores
		elif father is not None and mother is not None:
			self.age = 0

			# MEAN CENTERED BY AVG Z SCORE
			z_father = ( father.height - male_height_avg ) / male_height_sd
			z_mother = ( mother.height - female_height_avg ) / female_height_sd
			z_avg = ( z_father + z_mother ) / float( 2.0 )

			logger.debug( "Average Z-score is %.2f" % ( z_avg ) )

			if abs( z_avg ) > zscore_trigger:
				logger.debug( "Detected z-score > %.2f (%.2f). Resetting." % ( zscore_trigger, z_avg ) )
				z_avg = float( random.randint( 100, 258 ) ) / float( 100 ) * random.choice( [ -1.0, 1.0 ] )

			if self.sex == 'male':
				local_male_average_height = male_height_avg + ( z_avg * male_height_sd )
				self.height = numpy.random.normal( loc = local_male_average_height, scale = male_height_sd )
			else:
				local_female_average_height = female_height_avg + ( z_avg * female_height_sd )
				self.height = numpy.random.normal( loc = local_female_average_height, scale = female_height_sd )

		self.height = round( self.height, 2 )

		if self.height > lower_bound and self.height < upper_bound:
			self.dead = False
		else:
			self.dead = True

		logger.debug( "Sex: %s" % ( self.sex ) )
		logger.debug( "Age: %s" % ( self.age ) )
		logger.debug( "Height: %s" % ( self.height ) )

	def will_reproduce( self ):
		return random.choices( [ True, False ], k = 1, cum_weights = [ reproduce_prob[ self.age ], 1.0 ] )[ 0 ]

	def next_tick( self, logger, lower_cutoff, upper_cutoff, selection_weight ):
		if not self.dead:
			chance_to_die = death_prob[ self.age ]

			if self.height > upper_cutoff or self.height < lower_cutoff:
				chance_to_die = chance_to_die * selection_weight

			logger.debug( "Chance of death: %s" % ( chance_to_die ) )

			if chance_to_die >= 1.0:
				self.dead = True
			else:
				self.dead = random.choices( [ True, False ], k = 1, cum_weights = [ chance_to_die, 1.0 ] )[ 0 ]

		if self.dead:
			logger.debug( "Died" )
		else:
			logger.debug( "Lived" )
			self.age = self.age + 1

	def info_string( self ):
		return( "%s,%s,%s" % ( self.sex, self.age, self.height ) )

#############
# Functions #
#############
def remove_dead( a_list_of_people ):
	for idx in range( len( a_list_of_people ) - 1, -1, -1 ):
		if a_list_of_people[ idx ].dead:
			del a_list_of_people[ idx ]

	return a_list_of_people

def index_population( a_list_of_people ):
	female_idx = []
	male_idx = []

	for idx in range( len( a_list_of_people ) ):
		if a_list_of_people[ idx ].sex == "female":
			female_idx.append( idx )
		else:
			male_idx.append( idx )

	return female_idx, male_idx

def get_mean_sd( population_of_people, sex_index ):
	n = len( sex_index )

	avg = 0.0
	variance = 0.0

	for idx in range( n ):
		avg += population_of_people[ sex_index[ idx ] ].height

	avg = round( avg / float( n ), 2 )

	for idx in range( n ):
		variance += ( population_of_people[ sex_index[ idx ] ].height - avg ) ** 2
	variance = variance / float( n )

	sd = round( variance ** 0.5, 2 )

	return avg, sd

########
# main #
########
if __name__ == "__main__":
	pass
