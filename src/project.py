from random import randint

def project(particle, TargetDefinitions):
	rVal = rand(0, RAND_MAX)
	pTotal = 0
	transition = False
	space = " "
	for j in range(nLinks):
		if self.weightMatrix[particle.nodeIndex*nLinks+j] == 0:
			continue
		pTotal += self.weightMatrix[particle.nodeIndex*nLinks+j]
		if pTotal >= np.ceil(rVal*self.totalWeights[particle.nodeIndex]):
			particle.nodeIndex = self.childMatrix[particle.nodeIndex*nLinks+j]
			if len(particle.history) >0 and particle.history[particle.history.length()-1:1] == " ":
				particle.curWord = ""
			if language_code == 1 and mLinks[j:1].compare("\x8F") == 1:
				particle.history = particle.history.append("\xCE")
				particle.curWord = particle.curWord.append("\xCE")

			elif language_code == 1 and mLinks[j:1].compare("\x7A") == 1 and mLinks[j:1].compare("\x8F") == -1 and mLinks[j:1] != " ":
				particle.history = particle.history.append("\xCF")
				particle.curWord = particle.curWord.append("\xCF")

			elif language_code == 2 andmLinks[j:1].compare("\x80") == 1:
				particle.history=particle.history.append("\xC3")
				particle.curWord=particle.curWord.append("\xC3")
			
			particle.history = particle.history.append(mLinks[j:1])
			particle.curWord = particle.curWord.append(mLinks[j:1])

			particle.fullWord = 0
			particle.location = j
			particle.nFlashes=0
			particle.flashCount = sampleNegBin(particle.nFlashes)
			nParticles += 1
			transition = true
			break
	if not transition:
		particle.weight = np.log(0)
		particle.location = -1
		particle.fullWord = 0