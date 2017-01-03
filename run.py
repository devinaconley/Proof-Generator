# Driver script for testing ProofGenerator

# lib
import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.power import Pow
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
	tempDist = Distance( givenLeft, givenRight, proveLeft, proveRight )

	# return

	#  Do search
	maxDepth = 1000

	handler = NodeHandler( )
	handler.Add( givenLeft, givenRight, tempDist )

	k = 0
	while k < maxDepth and handler :
		currL, currR, currDist = handler.Pop( )
		k += 1
		print currL, ' = ', currR, '... Estim. Dist: ', currDist
		if (currL == proveLeft and currR == proveRight) or (currL == proveRight and currR == proveLeft) :
			break
		# Add simplified and expanded to queue (partial variations of these?)
		tempL, tempR = sympy.simplify( currL ), sympy.simplify( currR )
		tempDist = Distance( tempL, tempR, proveLeft, proveRight )
		handler.Add( tempL, tempR, tempDist )

		tempL, tempR = sympy.expand( currL ), sympy.expand( currR )
		tempDist = Distance( tempL, tempR, proveLeft, proveRight )
		handler.Add( tempL, tempR, tempDist )

		# iterate through operators
		for op in operators :
			for sym in symbols :
				tempL, tempR = op( currL, sym ), op( currR, sym )
				tempDist = Distance( tempL, tempR, proveLeft, proveRight )
				handler.Add( tempL, tempR, tempDist )

	print('Expanded nodes: ' + str( k ))

# Need some distance metric to implement a priority queue
def Distance( aLeft, aRight, bLeft, bRight ) :
	aLeftTokens = Tokenize( aLeft )
	aRightTokens = Tokenize( aRight )
	bLeftTokens = Tokenize( bLeft )
	bRightTokens = Tokenize( bRight )

	aLeftCounter = Counter( aLeftTokens )
	aRightCounter = Counter( aRightTokens )
	bLeftCounter = Counter( bLeftTokens )
	bRightCounter = Counter( bRightTokens )

	aMaxCoeff = max(
		[float( x ) for x in aLeftCounter.elements( ) and aRightCounter.elements( ) if x.isdigit( )] or [1] )
	bMaxCoeff = max(
		[float( x ) for x in bLeftCounter.elements( ) and bRightCounter.elements( ) if x.isdigit( )] or [1] )

	# compare left vs left, right vs right
	dist1 = (sum( (aLeftCounter - bLeftCounter).values( ) ) + sum( (bLeftCounter - aLeftCounter).values( ) )
			 + sum( (aRightCounter - bRightCounter).values( ) ) + sum( (bRightCounter - aRightCounter).values( ) ))

	# compare left vs right
	dist2 = (sum( (aLeftCounter - bRightCounter).values( ) ) + sum( (bRightCounter - aLeftCounter).values( ) )
			 + sum( (aRightCounter - bLeftCounter).values( ) ) + sum( (bLeftCounter - aRightCounter).values( ) ))

	# return min distance
	return min( [dist1, dist2] ) + abs( aMaxCoeff - bMaxCoeff )

def Tokenize( expr ) :
	tokens = []
	args = []  # want this to be mutable for pow expansion
	args.extend( expr.args )

	# Add solo term
	if len( args ) == 0 :
		tokens.append( str( expr ) )
	# Add func if only modifier
	elif len( args ) == 1 :
		tokens.append( str( expr.func ) )
	# Append terms to decompose power
	elif expr.func == Pow and args[1] > 0 :
		# print 'Power!', expr, expr.func, args[0], args[1]
		args.extend( [args[0] for i in range( args[1] )] )

	# Recursively traverse expressions
	for a in args :
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
						 default='sin(x)/cos(x) + cos(x)/sin(x) = y/( cos(x) * sin(x) )' )
	parser.add_argument( '-p', '--prove', help='Statement to prove',
						 default='1 = y' )

	# Parse arguments and return
	args = vars( parser.parse_args( ) )

	return args

if __name__ == '__main__' :
	main( )
