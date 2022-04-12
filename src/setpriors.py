from const import *
import numpy as np
from random import randint

c1 = "_";
c2 = "_";
ic1 = 35;
ic2 = 35;

def setpriors():
	if self.MultipleMenus():
		self.TargetDefinitions = self.TargetDefinitions[mCurMenu]

  	if mAlgorithm == 2: #naive bayes
		for i in range(len(self.mTargets)):
			index = (ic1*len(self.mTargets) + ic2)*len(self.mTargets) + i
			self.priors[i] = np.log(self.triCounts[index])

  	if mAlgorithm == 3: # hidden markov model
	  	fProbs2, vProbs2 = [], []
	  	vHistories2 = []

	  	fProbs2sum = 0

		for i in range(fProbs2.size):
		  	b = int(i / len(self.mTargets))
		  	c = i % len(self.mTargets)

		  	if self.biCounts[b*len(self.mTargets)+c] > 0:
		    	for a in range(len(self.mTargets)):
			  		bind = a*len(self.mTargets)+b
			  		tind = a*self.fProbs.size+i
			  		cProb = 0
				  	if self.biCounts[bind] > 0:
						cProb = self.triCounts[tind]/self.biCounts[bind]
				  	fProbs2[i] += np.exp(self.fProbs[bind])*cProb
				  	if self.vProbs[bind] + np.log(cProb) > vProbs2[i]:
						vProbs2[i] = self.vProbs[bind] + np.log(cProb)
						vHistories2[i] = self.vHistories[bind]

		  	nextChar = self.TargetDefinitions[c][0]
		  	vHistories2[i].append(nextChar)
		  	fProbs2sum += fProbs2[i]
		  	self.priors[i%len(self.mTargets)] += fProbs2[i]

	  	for i in range(len(fProbs2)):
		  	fProbs2[i] = np.log(fProbs2[i]/fProbs2sum)

	  	for i in range(self.priors.size()):
		  	self.priors[i] = np.log(self.priors[i]/fProbs2sum)

	  	self.fProbs = fProbs2
	  	self.vProbs = vProbs2
	  	self.vHistories = vHistories2

  	if mAlgorithm >= 4:
	  	nParticles = 0
	  	wordScores = {}
	  	wordParticles = {}
	  
	  	totalWords = 0
	  	for i in range(len(self.particles)):
	  		if mWordCompletion == 0:
	  			r = 0
	  		else:
	  			r = randint(RAND_MAX)
			if r > mCompletionPrior: #should be <, but preserved for current config files
				projectToEnd(self.particles[i], self.TargetDefinitions)
			else:
				project(self.particles[i], self.TargetDefinitions)
			
			if self.particles[i].fullWord:
				wordScores[self.particles[i].curWord] += 1
				wordParticles[self.particles[i].curWord].append(self.particles[i])
				totalWords += 1
			
			self.particles[i].weight = 0
			if self.particles[i].location >= 0:
				self.priors[targetMap[self.particles[i].location]] += 1

			topWords = [{"":0} for _ in range(mNSuggestions)]

	  	for key in wordScores:
		  	for j in range(mNSuggestions - 1, -1, -1):
			  	if wordScores[key] > topWords[j].values()[0]:
				  	if j < mNSuggestions - 1:
					  	topWords[j + 1] = topWords[j]
				  	topWords[j] = item
			 
	  	for stimulus in self.mTextStimuli:
		  	displaySize = 1
		  	if self.TargetDefinitions.NumColumns() > DisplaySize:
			  	displaySize = self.TargetDefinitions( stimulus.Tag()-1, DisplaySize )
		  	targetHeight = self.MenuParam( "TargetHeight", mCurMenu ) / 100.0
		  	targetWidth = self.MenuParam( "TargetWidth", mCurMenu ) / 100.0
		  	targetTextHeight = self.MenuParam( "TargetTextHeight", mCurMenu ) / 100.0 / targetHeight
		  	windowWidth = self.Parameter("WindowWidth")
		  	windowHeight = self.Parameter("WindowHeight")
		  	textRatio = self.Parameter("TextRatio")
		  	#std::string text = (*stimulus)->Text()
		  	text = self.TargetDefinition[stimulus.Tag()-1][0]
		  	ti = -1

		  	try:
		  	ti == text.split()[0]:
		  	if ti is not None:
		  		suggestion = ti<=mNSuggestions and ti > 0
		  	else:
		  		suggestion = False
		 	except:
		  		suggestion = False

		  	if suggestion:
			  	stimulus.SetText(topWords[ti-1].keys()[0][:len(topWords[ti-1].keys()[0])-1])
			  	stimulus.SetTextHeight(displaySize*targetTextHeight*np.min(float(1.0), textRatio*float(targetWidth)*windowWidth/windowHeight/float((len(topWords[ti-1].keys()[0])-1)*targetTextHeight*targetHeight)))
			  	l = wordParticles[topWords[ti-1].keys()[0]]
			  	for p in range(len(l)):
				  	l_item =stimulus.Tag()-1
				  	l[p].location = invMap[l_item]
				 	 self.priors[l_item] += 1
				  	#bciout << (*p)->weight << ", " << (*p)->history << ", " << (*p)->location <<endl

	  	tProb = 0
	  	for i in range(len(self.priors)):
		  	self.priors[i] /= nParticles
		  	tProb += self.priors[i]
		  	#bciout << links.substr(i,1) << ": " << self.priors[i] << endl
		  	if mAlgorithm==5: # not too important rn
		  		self.priors[i] = 0
		  	else:
		  		self.priors[i]= np.log(self.priors[i])




