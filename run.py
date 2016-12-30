# Driver script for testing ProofGenerator

# lib
import sympy
from sympy.parsing.sympy_parser import parse_expr
import argparse
from collections import Counter

# src
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
	givenLeft = parse_expr( sGivenLeft, evaluate=False )
	givenRight = parse_expr( sGivenRight, evaluate=False )

	sProveLeft, sProveRight = args['prove'].split( '=' )
	proveLeft = parse_expr( sProveLeft, evaluate=False )
	proveRight = parse_expr( sProveRight, evaluate=False )

	symbolsOrig = givenLeft.free_symbols | givenRight.free_symbols | proveLeft.free_symbols | proveRight.free_symbols

	print symbolsOrig

	symbols = []
	symbols.extend( symbolsOrig )
	for m in modifiers :
		for s in symbolsOrig :
			symbols.append( m( s ) )

	print symbols

	# Testing cost function
	print Cost( givenLeft, givenRight, proveLeft, proveRight )

	return

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
def Cost( aLeft, aRight, bLeft, bRight ) :
	aLeftTokens = Tokenize( aLeft )
	aRightTokens = Tokenize( aRight )
	bLeftTokens = Tokenize( bLeft )
	bRightTokens = Tokenize( bRight )

	aLeftCounter = Counter( aLeftTokens )
	aRightCounter = Counter( aRightTokens )
	bLeftCounter = Counter( bLeftTokens )
	bRightCounter = Counter( bRightTokens )

	# compare left vs left, right vs right
	cost1 = (sum( (aLeftCounter - bLeftCounter).values( ) ) + sum( (bLeftCounter - aLeftCounter).values( ) )
			 + sum( (aRightCounter - bRightCounter).values( ) ) + sum( (bRightCounter - aRightCounter).values( ) ))

	# compare left vs right
	cost2 = (sum( (aLeftCounter - bRightCounter).values( ) ) + sum( (bRightCounter - aLeftCounter).values( ) )
			 + sum( (aRightCounter - bLeftCounter).values( ) ) + sum( (bLeftCounter - aRightCounter).values( ) ))

	# return min as cost
	return min( [cost1, cost2] )

def Tokenize( expr ) :
	tokens = []
	# Add solo term
	if len( expr.args ) == 0 :
		tokens.append( str( expr ) )
	# Add func if only modifier
	if len( expr.args ) == 1 :
		tokens.append( str( expr.func ) )
	# Recursively traverse expressions
	for a in expr.args :
		if a.args :
			tokens.extend( Tokenize( a ) )
		else :
			tokens.append( str( a ) )
	return tokens

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
