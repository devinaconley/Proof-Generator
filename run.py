# Driver script for testing ProofGenerator

import sympy
from src.NodeHandler import NodeHandler

# Quick POC for simple graph style search

x, y = sympy.symbols( 'x y' )

operators = [sympy.Mul, sympy.Add]#, sympy.Pow]
symbolsOrig = [x, y]
modifiers = [sympy.sin, sympy.cos]#, sympy.exp]

maxDepth = 1000

symbols = []
symbols.extend( symbolsOrig )
for m in modifiers :
	for s in symbolsOrig :
		symbols.append( m( s ) )

# Given left == right
givenLeft = sympy.sin( x ) / sympy.cos( x ) + sympy.cos( x ) / sympy.sin( x )
givenRight = y / (sympy.cos( x ) * sympy.sin( x ))

# Prove y == 1
proveLeft = 1
proveRight = y

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

print len( handler.queue )

# Need some distance metric to implement a priority queue