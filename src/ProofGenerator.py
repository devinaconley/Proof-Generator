# Main Proof Generator class

# lib
import sympy
from sympy.parsing.sympy_parser import parse_expr
from collections import Counter

# src
from src.NodeHandler import NodeHandler

class ProofGenerator :
	def __init__( self, given, prove ) :
		# Operators and modifiers of interest
		self.operators = [sympy.Mul, sympy.Add]  # , sympy.Pow]
		self.modifiers = [sympy.sin, sympy.cos, sympy.exp]

		print 'Proof Generator initialized...'
		print 'Given: ', given
		print 'Prove: ', prove

		# Parse into left and right expressions
		sGivenLeft, sGivenRight = given.split( '=' )
		self.givenLeft = parse_expr( sGivenLeft, evaluate=False )
		self.givenRight = parse_expr( sGivenRight, evaluate=False )

		sProveLeft, sProveRight = prove.split( '=' )
		self.proveLeft = parse_expr( sProveLeft, evaluate=False )
		self.proveRight = parse_expr( sProveRight, evaluate=False )

		# Setup full set of possible symbols
		symbolsOrig = (self.givenLeft.free_symbols | self.givenRight.free_symbols
					   | self.proveLeft.free_symbols | self.proveRight.free_symbols)

		print symbolsOrig

		self.symbols = []
		self.symbols.extend( symbolsOrig )
		for m in self.modifiers :
			for s in symbolsOrig :
				self.symbols.append( m( s ) )

		print self.symbols

		# Setup node handler
		self.handler = NodeHandler( )
		tempDist = self.Distance( self.givenLeft, self.givenRight, self.proveLeft, self.proveRight )
		self.handler.Add( self.givenLeft, self.givenRight, tempDist )

	# Do search
	def Run( self, maxDepth=1000 ) :
		k = 0
		while k < maxDepth and self.handler :
			currL, currR, currDist = self.handler.Pop( )
			k += 1
			print currL, ' = ', currR, '... Estim. Dist: ', currDist
			if ((currL == self.proveLeft and currR == self.proveRight)
				or (currL == self.proveRight and currR == self.proveLeft)) :
				break
			# Add simplified and expanded to queue (partial variations of these?)
			tempL, tempR = sympy.simplify( currL ), sympy.simplify( currR )
			tempDist = self.Distance( tempL, tempR, self.proveLeft, self.proveRight )
			self.handler.Add( tempL, tempR, tempDist )

			tempL, tempR = sympy.expand( currL ), sympy.expand( currR )
			tempDist = self.Distance( tempL, tempR, self.proveLeft, self.proveRight )
			self.handler.Add( tempL, tempR, tempDist )

			# iterate through operators
			for op in self.operators :
				for sym in self.symbols :
					tempL, tempR = op( currL, sym ), op( currR, sym )
					tempDist = self.Distance( tempL, tempR, self.proveLeft, self.proveRight )
					self.handler.Add( tempL, tempR, tempDist )

		print('Expanded nodes: ' + str( k ))

	# Need some distance metric to implement a priority queue
	def Distance( self, aLeft, aRight, bLeft, bRight ) :
		aLeftTokens = self.Tokenize( aLeft )
		aRightTokens = self.Tokenize( aRight )
		bLeftTokens = self.Tokenize( bLeft )
		bRightTokens = self.Tokenize( bRight )

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

	def Tokenize( self, expr ) :
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
		elif expr.func == sympy.Pow and args[1] > 0 :
			# print 'Power!', expr, expr.func, args[0], args[1]
			args.extend( [args[0] for i in range( args[1] )] )

		# Recursively traverse expressions
		for a in args :
			if a.args :
				tokens.extend( self.Tokenize( a ) )
			else :
				tokens.append( str( a ) )
		return tokens
