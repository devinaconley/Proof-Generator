# Driver script for testing ProofGenerator

# lib
import argparse

# src
from src.ProofGenerator import ProofGenerator

# Quick POC for simple graph style search
def main( ) :

	# Pull command line args
	args = ParseArguments( )

	# Run proof generator
	pg = ProofGenerator( args['given'], args['prove'] )
	pg.Run()


# Command Line Arguments
def ParseArguments( ) :
	# Define arguments
	parser = argparse.ArgumentParser( )
	parser.add_argument( '-g', '--given', help='Given or starting statement',
						 default='sin(x)/cos(x) + cos(x)/sin(x) = y/( cos(x) * sin(x) )' )
	parser.add_argument( '-p', '--prove', help='Statement to prove',
						 default='y = 1' )

	# Parse arguments and return
	args = vars( parser.parse_args( ) )

	return args

if __name__ == '__main__' :
	main( )
