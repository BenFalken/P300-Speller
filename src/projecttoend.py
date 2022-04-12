def projectToEnd(particle, TargetDefinitions):
	print("projecting")
	count = 0;
	while particle.history[len(particle.history) - 1:1] != " " and particle.location >=0:
		print(str(particle.history) + ", ")
		nParticles -= 1
		project(particle,TargetDefinitions)
		count += 1
		if count > 100:
			print("infinite loop on word completion")
			break

	particle.location = -1
	particle.fullWord = 1
	nParticles += 1