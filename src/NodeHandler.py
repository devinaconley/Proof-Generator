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

	def Add( self, eqLeft, eqRight, dist ) :
		if (eqLeft, eqRight, dist) in self.expanded :
			return
		if (eqRight, eqLeft, dist) in self.expanded :
			return
		if (eqLeft, eqRight, dist) in self.queue :
			return
		if (eqRight, eqLeft, dist) in self.queue :
			return
		self.queue.add( (eqLeft, eqRight, dist) )

	def Pop( self ) :
		if self.queue :
			temp = self.queue.pop(0)
			if temp in self.expanded :
				return self.Pop( )
			self.expanded.add( temp )  # Assumes exploration on pop
			return temp
		else :
			return None
