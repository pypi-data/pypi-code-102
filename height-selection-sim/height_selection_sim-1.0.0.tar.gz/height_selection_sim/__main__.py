#!/usr/bin/env python

###########
# imports #
###########
import argparse
import logging
import numpy
import random
import sys

from height_selection_sim import __proj_name__, __version__, death_prob, reproduce_prob, ref_male_average_height, ref_male_standard_dev_height, ref_female_average_height, ref_female_standard_dev_height, high_standard_dev_trigger, low_standard_dev_trigger, Person, remove_dead, index_population, get_mean_sd

############
# function #
############
def run():
	#############
	# arg parse #
	#############
	parser = argparse.ArgumentParser( prog = __proj_name__, epilog = "%s v%s" % ( __proj_name__, __version__ ) )

	parser.add_argument( "--outfile", help = "Name of output file", default = "selection_simulation_generations.csv" )
	parser.add_argument( "--initial_population", help = "Initialize how many individuals?", type = int, default = 50 )
	parser.add_argument( "--iterations", help = "How many population iterations?", type = int, default = 100 )
	parser.add_argument( "--upper_cutoff", help = "Apply selection above what height?", type = float, default = 272 )
	parser.add_argument( "--lower_cutoff", help = "Apply selection below what height?", type = float, default = 54.6 )
	parser.add_argument( "--selection_weight", help = "Increased death risk?", type = float, default = 10.0 )
	parser.add_argument( "--selection_after", help = "Apply selection starting at what generation?", type = int, default = 1 )
	parser.add_argument( "--loglevel", choices=[ 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ], default='WARNING' )

	args = parser.parse_args()

	#################
	# setup logging #
	#################
	logging.basicConfig( format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
	logger = logging.getLogger( __proj_name__ )
	logger.setLevel( args.loglevel )

	#####################
	# validity checking #
	#####################
	if args.initial_population < 1:
		logger.error( "Initial population must be greater than 1" )
		sys.exit( 1 )

	if args.upper_cutoff < 1.0:
		logger.error( "Upper cutoff to apply selection must be greater than 1" )
		sys.exit( 1 )

	if args.lower_cutoff < 1.0:
		logger.error( "Lower cutoff to apply selection must be greater than 1" )
		sys.exit( 1 )

	if args.lower_cutoff >= args.upper_cutoff:
		logger.error( "Lower cutoff must be less than upper cutoff" )
		sys.exit( 1 )

	###################
	# Options to info #
	###################
	options_set =  "\n%s v%s\n\n" % ( __proj_name__, __version__ )
	options_set += "Options\n=======\n"
	options_set += "Initial population: %s\n" % ( args.initial_population )
	options_set += "Iterations: %s\n" % ( args.iterations )
	options_set += "Upper cutoff: %s\n" % ( args.upper_cutoff )
	options_set += "Lower cutoff: %s\n" % ( args.lower_cutoff )
	options_set += "Selection weight: %s\n" % ( args.selection_weight )
	options_set += "Outfile: %s\n" % ( args.outfile )
	options_set += "Logging level: %s\n" % ( str( args.loglevel ) )

	logger.info( options_set )

	##############
	# initialize #
	##############
	population = [ Person( logger = logger, male_height_avg = ref_male_average_height, male_height_sd = ref_male_standard_dev_height, female_height_avg = ref_female_average_height, female_height_sd = ref_female_standard_dev_height ) for x in range( args.initial_population ) ]
	logger.info( "Population initialized" )

	###############################
	# Setup male / female indexes #
	###############################
	female_idx, male_idx = index_population( population )

	#############################
	# initialize average height #
	#############################
	male_average_height = ref_male_average_height
	male_standard_dev_height = ref_male_standard_dev_height
	female_average_height = ref_female_average_height
	female_standard_dev_height = ref_female_standard_dev_height

	###########
	# iterate #
	###########
	with open( args.outfile, 'w' ) as OUT:
		for iteration_idx in range( args.iterations ):
			logger.info( "Starting iteration %s of %s (%.1f%%)" % ( iteration_idx + 1, args.iterations, ( float( iteration_idx + 1 ) / float( args.iterations ) ) * 100.0 ) )

			logger.info( "Population size: %s" % ( len( population ) ) )

			if len( population ) == 0:
				logger.warning( "Extinction" )
				break

			#########
			# birth #
			#########
			logger.info( "Births..." )
			for f_idx in range( len( female_idx ) ):
				if population[ female_idx[ f_idx ] ].will_reproduce():
					m_idx = None
					male_found = False
					while male_found == False:
						m_idx = random.randint( 0, len( male_idx ) - 1 )
						male_found = population[ male_idx[ m_idx ] ].will_reproduce()

					population.append( Person( logger = logger, father = population[ m_idx ], mother = population[ f_idx ], male_height_avg = male_average_height, male_height_sd = male_standard_dev_height, female_height_avg = female_average_height, female_height_sd = female_standard_dev_height ) )

			#########
			# death #
			#########
			# def next_tick( self, logger, lower_cutoff, upper_cutoff, selection_weight ):
			logger.info( "Deaths..." )

			if iteration_idx >= args.selection_after:
				local_selection = args.selection_weight
			else:
				local_selection = 1.0

			for idx in range( len( population ) ):
				population[ idx ].next_tick( logger = logger, lower_cutoff = args.lower_cutoff, upper_cutoff = args.upper_cutoff, selection_weight = local_selection )
				OUT.write( "%s,%s\n" % ( iteration_idx + 1, population[ idx ].info_string() ) )

			population = remove_dead( population )

			###############################
			# Setup male / female indexes #
			###############################
			female_idx, male_idx = index_population( population )

			if len( male_idx ) == 0:
				logger.warning( "Males dead - extinction" )
				break
			elif len( female_idx ) == 0:
				logger.warning( "Females dead - extinction" )
				break

			#####################
			# renew mean and sd #
			#####################
			female_average_height, female_standard_dev_height = get_mean_sd( population, female_idx )
			male_average_height, male_standard_dev_height = get_mean_sd( population, male_idx )

			if female_standard_dev_height > high_standard_dev_trigger or female_standard_dev_height < low_standard_dev_trigger:
				logger.debug( "Height std. dev. drift detected in females (%.2f). Resetting." % ( female_standard_dev_height ) )
				female_standard_dev_height = 0.0
				while female_standard_dev_height < 1.0:
					female_standard_dev_height = round( numpy.random.normal( loc = ref_female_standard_dev_height, scale = 1.5 ), 2 )
			if male_standard_dev_height > high_standard_dev_trigger or male_standard_dev_height < low_standard_dev_trigger:
				logger.debug( "Height std. dev. drift detected in males (%.2f). Resetting." % ( male_standard_dev_height ) )
				male_standard_dev_height = 0.0
				while male_standard_dev_height < 1.0:
					male_standard_dev_height = round( numpy.random.normal( loc = ref_male_standard_dev_height, scale = 1.5 ), 2 )

	logger.info( "Finished" )

########
# main #
########
if __name__ == "__main__":
	run()
