class particle:
	def __init__(self):
		self.history = ""
		self.curWord = ""
		self.fullWord = False		# This used to be 0, 1 valued but that shall be fixed
		self.location = 0
		self.flashCount = 0
		self.nFlashes = 0
		self.weight = 0
		self.nodeIndex = rootIndex