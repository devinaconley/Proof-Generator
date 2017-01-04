from sortedcontainers import SortedListWithKey

# Wrapper class for handling queue / expanded nodes

class NodeHandler :
	def __init__( self ) :
		self.expanded = SortedListWithKey( key=lambda node: node[2] )
		self.queue = SortedListWithKey( key=lambda node : node[2] )
		self.currPathLeft = []
		self.currPathRight = []

	def __nonzero__( self ) :
		return bool( self.queue )

	def Add( self, eqLeft, eqRight, dist, path ) :
		if self.Unseen( eqLeft, eqRight, dist ) :
			self.queue.add( (eqLeft, eqRight, dist, path) )

	def Pop( self ) :
		if self.queue :
			temp = self.queue.pop(0)
			if temp in self.expanded :
				return self.Pop( )
			self.expanded.add( temp )  # Assumes exploration on pop
			return temp
		else :
			return None

	def Unseen(self, eqLeft, eqRight, dist ) :
		if any( [ x for x in self.expanded
				  if eqRight == x[0] and eqLeft == x[1]
				  or eqRight == x[1] and eqLeft == x[0] ] ) :
			return False

		if any( [ x for x in self.queue
				  if eqRight == x[0] and eqLeft == x[1]
				  or eqRight == x[1] and eqLeft == x[0] ] ) :
			return False

		return True