# Wrapper class for handling queue / expanded nodes

class NodeHandler :
	def __init__( self ) :
		self.expanded = []
		self.queue = []
		self.currPathLeft = []
		self.currPathRight = []

	def __nonzero__( self ) :
		return bool( self.queue )

	def Add( self, eqLeft, eqRight ) :
		if (eqLeft, eqRight) in self.expanded :
			return
		if (eqRight, eqLeft) in self.expanded :
			return
		self.queue.insert( 0, (eqLeft, eqRight) )

	def Pop( self ) :
		if self.queue :
			temp = self.queue.pop( )
			if temp in self.expanded :
				return self.Pop( )
			self.expanded.append( temp )  # Assumes exploration on pop
			return temp
		else :
			return None
