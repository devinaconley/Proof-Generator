# Driver script for testing ProofGenerator

import sympy
from sympy.parsing.sympy_parser import parse_expr
import argparse

from src.NodeHandler import NodeHandler

# Quick POC for simple graph style search
def main( ) :
	# Operators and modifiers of interest
	operators = [sympy.Mul, sympy.Add]  # , sympy.Pow]
	modifiers = [sympy.sin, sympy.cos]  # , sympy.exp]

	# Pull command line args
	args = ParseArguments( )

	# Parse into left and right expressions
	sGivenLeft, sGivenRight = args['given'].split( '=' )
	givenLeft = parse_expr( sGivenLeft )
	givenRight = parse_expr( sGivenRight )

	sProveLeft, sProveRight = args['prove'].split( '=' )
	proveLeft = parse_expr( sProveLeft )
	proveRight = parse_expr( sProveRight )

	symbolsOrig = givenLeft.free_symbols | givenRight.free_symbols | proveLeft.free_symbols | proveRight.free_symbols

	print symbolsOrig


	symbols = []
	symbols.extend( symbolsOrig )
	for m in modifiers :
		for s in symbolsOrig :
			symbols.append( m( s ) )

	print symbols


	# Testing cost function



	#  Do search

	maxDepth = 1000

	handler = NodeHandler( )
	handler.Add( givenLeft, givenRight )

	k = 0
	while k < maxDepth and handler :
		tempL, tempR = handler.Pop( )
		k += 1
		print tempL, ' = ', tempR
		if (tempL == proveLeft and tempR == proveRight) or (tempL == proveRight and tempR == proveLeft) :
			break
		# Add simplified and expanded to queue (partial variations of these?)
		handler.Add( sympy.simplify( tempL ), sympy.simplify( tempR ) )
		handler.Add( sympy.expand( tempL ), sympy.expand( tempR ) )

		# iterate through operators
		for op in operators :
			for sym in symbols :
				handler.Add( op( tempL, sym ), op( tempR, sym ) )

	print('Expanded nodes: ' + str( k ))

# Need some distance metric to implement a priority queue
def Cost( ) :
	return 0

# Command Line Arguments
def ParseArguments( ) :
	# Define arguments
	parser = argparse.ArgumentParser( )
	parser.add_argument( '-g', '--given', help='Given or starting statement',
						 default='sin(x)/cos(x) + cos(x)/sin(x) = y/( cos(x) + sin(x) )' )
	parser.add_argument( '-p', '--prove', help='Statement to prove',
						 default='1 = y' )

	# Parse arguments and return
	args = vars( parser.parse_args( ) )

	return args

if __name__ == '__main__' :
	main( )
