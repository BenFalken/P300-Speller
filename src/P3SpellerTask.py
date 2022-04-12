class P3SpellerTask:
	def __init__():
		self.TargetDefinitions = np.array(
			["A A 1 % % % "  "B B 1 % % % "  "C C 1 % % % "  "D D 1 % % % "  "E E 1 % % % "  "F F 1 % % % "
			"G G 1 % % % "  "H H 1 % % % "  "I I 1 % % % "  "J J 1 % % % "  "K K 1 % % % "  "L L 1 % % % "
			"M M 1 % % % "  "N N 1 % % % "  "O O 1 % % % "  "P P 1 % % % "  "Q Q 1 % % % "  "R R 1 % % % "
			"S S 1 % % % "  "T T 1 % % % "  "U U 1 % % % "  "V V 1 % % % "  "W W 1 % % % "  "X X 1 % % % "
			"Y Y 1 % % % "  "Z Z 1 % % % "  "1 1 1 % % % "  "2 2 1 % % % "  "3 3 1 % % % "  "4 4 1 % % % "
			"5 5 1 % % % "  "6 6 1 % % % "  "7 7 1 % % % "  "8 8 1 % % % "  "9 9 1 % % % "  "_ %20 1 % % % "])
		
		self.mTargets = {} #this is a set!!
		self.particles = [] #empty for now??

		self.vProbs = np.zeros((len(self.mTargets)*len(self.mTargets)))
		self.fProbs = np.zeros((len(self.mTargets)*len(self.mTargets)))
		self.priors = np.zeros((len(self.mTargets)))
		self.vHistories = np.array(["" for _ in range(self.len(self.mTargets)*len(self.mTargets))])

		self.NumMatrixColumns = 1
		self.NumMatrixRows= 1
		self.WordCompletion= 0
		self.CompletionPrior= 0
		self.NSuggestions= 0
		self.TextRatio= 1

		self.mNumberOfSequences = 0

		#mInterpretMode_( InterpretModes::None )

		self.mDisplayResults = False
		self.mTestMode = False
		self.mCurMenu = 0
		self.mNumMatrixRows = 0
		self.mNumMatrixCols = 0
		self.mSequenceCount = 0

		#mSequencePos( mSequence.begin() )

		self.mAvoidStimulusRepetition = False
		self.mSleepMode = 0
		self.mPaused = False
		self.mpStatusBar = None
		self.mpTextWindow = None

		#mSummaryFile( SummaryFileExtension().c_str() ),

		self.mRunCount = 0
		self.mNumSelections = 0
		self.mSleepDuration = 0
		self.weightMatrix = 0
		self.childMatrix = 0
		self.totalWeights = 0

		self.biCounts = np.zeros((self.fProbs.size))
		self.triCounts = np.zeros((self.fProbs.size*len(self.mTargets)))