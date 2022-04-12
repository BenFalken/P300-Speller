import numpy as np
import pickle as pkl
from P3SpellerTask import P3SpellerTask

#set counts is where the model is constructed
def SetCounts():
	print("setCounts")

	if self.MultipleMenus():
		self.TargetDefinitions = self.TargetDefinitions[mCurMenu]
	#self.TargetDefinitions is the list of elements that are displayed on the screen in the grid. This is stored in the parameters.
	
	mLinks  =  ""
	#the set of characters that we allow (this also includes accented characters that might not be in the grid
	
	links  =  ""
	#these are only the characters that appear in the grid (no accents). These are also converted to lower case
	
	targetMap = []
	#maps from mLinks to targets (e.g., links from accented letters to unaccented letters)
	
	invMap = []
	#maps from targets to mLinks

	#the reason for these links is so that accented letters can be used in the language model. We want to include them because we later link the
	#unaccented letters to both unaccented and accented versions

	language_code  =  0
	ti  =  -1

	for i in range(self.TargetDefinitions.shape[0]):
		temp  =  self.TargetDefinitions[i][0]
		replace  =  ""

		search  =  "\xCE"
		found_at_index  =  temp.find(search) 
		if found_at_index !=  -1:
			
			temp = temp.replace(search, replace)
			language_code  =  1
			#greek

		search  =  "\xCF"
		found_at_index  =  temp.find(search) 
		if found_at_index !=  -1:
			temp = temp.replace(search, replace)
			language_code  =  1
			#greek

		search  =  "\xC3"
		found_at_index  =  temp.find(search) 
		if found_at_index !=  -1:
			temp = temp.replace(search, replace)
			language_code  =  2
			#spanish

		if len(temp) > 1:
			#if the element is longer than one character, we don't include it (this will likely change if using unicode)
			#the reason for this is because there can be commands in the grid like "delete" or "quit", which don't type anything
			#the assumption is that anything that is longer than one letter is one of these commands, so it isn't actually something we can type
			mLinks += "*"
			#add an asterisk as a placeholder
			links += "*"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		try:
			ti = temp.split(" ")[-1]
			if ti is not None:
				suggestion = ti <=  mNSuggestions and ti > 0
			else:
				suggestion = False
		except:
			suggestion = False

		elif suggestion:
			#these are the conditions for word suggestions
			#we don't want to include these either because these values cannot be typed.
			#for example, if the cell in the grid that says "1" will be replaced by a suggested word, we won't actually be able to type "1",
			#so it shouldn't be included as a possible selection
			mLinks += "*"
			links.append += "*"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 2 and (temp == "\x91" or temp == "\xB1"):
		#tolower doesn't work for Ñ so this has to be done manually
		#elif temp == Ñ") == 0:#tolower doesn't work for Ñ so this has to be done manually
			#note that this was originally temp == Ñ") but I switched it when starting to convert to UTF8 (\xC3\x91 is UTF8 code for Ñ)
			#bciout << "Ñ" << " here " << "\xD1" << endl
			mLinks += "\x91"
			#links.append += "ñ")#add lower case version to links
			links.append += "\xB1" #add lower case version to links
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x91" or temp == "\xB1"):
			#mLinks += "\x91")
			mLinks += "\xB1"
			links.append += "\xB1"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x86") # Add Accented Upper Case to mLinks
			mLinks += "\xAC" # Add Accented Letter To Links
			links.append += "\xAC" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x92" temp == "\xB2"):
			#mLinks += "\x92")
			mLinks += "\xB2"
			links.append += "\xB2"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x93" or temp == "\xB3"):
			#mLinks += "\x93")
			mLinks += "\xB3"
			links.append += "\xB3"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x94" temp == "\xB4"):
			#mLinks += "\x94")
			mLinks += "\xB4"
			links.append += "\xB4"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x95" or temp == "\xB5"): 
			#mLinks += "\x95")
			mLinks += "\xB5"
			links.append += "\xB5"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x88") # Add Accented Upper Case to mLinks
			mLinks += "\xAD" # Add Accented Letter To Links
			links.append += "\xAD" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x96" or temp == "\xB6"):
			#mLinks += "\x96")
			mLinks += "\xB6"
			links.append += "\xB6"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x97" or temp == "\xB7"):
			#mLinks += "\x97")
			mLinks += "\xB7"
			links.append += "\xB7"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x89") # Add Accented Upper Case to mLinks
			mLinks += "\xAE" # Add Accented Letter To Links
			links.append += "\xAE" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x98" or temp == "\xB8"):
			#mLinks += "\x98")
			mLinks += "\xB8"
			links.append += "\xB8"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x99" or temp == "\xB9"):
			#mLinks += "\x99")
			mLinks += "\xB9"
			links.append += "\xB9"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x8A") # Add Accented Upper Case to mLinks
			mLinks += "\xAF" # Add Accented Letter To Links
			links.append += "\xAF" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x9A" or temp == "\xBA"):
			#mLinks += "\x9A")
			mLinks += "\xBA"
			links.append += "\xBA"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x9B" or temp == "\xBB"):
			#mLinks += "\x9B")
			mLinks += "\xBB"
			links.append += "\xBB"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x9C" or temp == "\xBC"):
			#mLinks += "\x9C")
			mLinks += "\xBC"
			links.append += "\xBC"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x9D" or temp == "\xBD"):
			#mLinks += "\x9D")
			mLinks += "\xBD"
			links.append += "\xBD"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x9E" or temp == "\xBE"):
			#mLinks += "\x9E")
			mLinks += "\xBE"
			links.append += "\xBE"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\x9F" or temp == "\xBF"):
			#mLinks += "\x9F")
			mLinks += "\xBF"
			links.append += "\xBF"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x8C") # Add Accented Upper Case to mLinks
			mLinks += "\x8C" # Add Accented Letter To Links
			links.append += "\x8C" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA0" or temp == "\x80"):
			#mLinks += "\xA0")
			mLinks += "\x80"
			links.append += "\x80"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA1" or temp == "\x81"):
			#mLinks += "\xA1")
			mLinks += "\x81"
			links.append += "\x81"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA2" or temp == "\x82" or temp == "\xA3" or temp == "\x83"):
			#mLinks += "\xA2")
			mLinks += "\x82"
			links.append += "\x82"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\xA3")
			mLinks += "\x83"
			links.append += "\x83"
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA4" or temp == "\x84"):
			#mLinks += "\xA4")
			mLinks += "\x84"
			links.append += "\x84"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA5" or temp == "\x85"):
			#mLinks += "\xA5")
			mLinks += "\x85"
			links.append += "\x85"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x8E") # Add Accented Upper Case to mLinks
			mLinks += "\x8D" # Add Accented Letter To Links
			links.append += "\x8D" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA6" or temp == "\x86"):
			#mLinks += "\xA6")
			mLinks += "\x86"
			links.append += "\x86"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA7" or temp == "\x87"):
			#mLinks += "\xA7")
			mLinks += "\x87"
			links.append += "\x87"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA8" or temp == "\x88"):
			#mLinks += "\xA8")
			mLinks += "\x88"
			links.append += "\x88"
			targetMap.append(i)
			invMap.append(len(links) - 1)

		elif language_code == 1 and (temp == "\xA9" or temp == "\x89"):
			#mLinks += "\xA9")
			mLinks += "\x89"
			links.append += "\x89"
			targetMap.append(i)
			invMap.append(len(links) - 1)
			#mLinks += "\x8F") # Add Accented Upper Case to mLinks
			mLinks += "\x8E" # Add Accented Letter To Links
			links.append += "\x8E" # Add Accented Letter To Links
			targetMap.append(i)
			#invMap.append(len(links) - 1)

		else:
			mLinks += temp#for regular letters, add the letter to links and mlings
			links.append += temp
			targetMap.append(i)
			invMap.append(len(links) - 1)

			if links.lower() == "a":
			#if the letter is a vowel, include the accented versions as well
				#mLinks += "Á")
				#links.append += "á")#need to make these lowercase because tolower doesn't work for these
				mLinks += "\x81"
				links.append += "\xA1" #need to make these lowercase because tolower doesn't work for these
				targetMap.append(i)

			elif links.lower() == "e":
				#mLinks += "É")
				#links.append += "é")
				mLinks += "\x89"
				links.append += "\xA9"
				targetMap.append(i)

			elif links.lower() == "i":
				#mLinks += "Í")
				#links.append += "í")
				mLinks += "\x8D"
				links.append += "\xAD"
				targetMap.append(i)

			elif links.lower() == "o":
				#mLinks += "Ó")
				#links.append += "ó")
				mLinks += "\x93"
				links.append += "\xB3"
				targetMap.append(i)

			elif links.lower() == "u":
				#mLinks += "Ú")
				#links.append += "ú")
				mLinks += "\x9A"
				links.append += "\xBA"
				targetMap.append(i)

			elif temp == "":
				mLinks += ""
				links.append += ""
				targetMap.append(i)

	links = links.lower()
	new_links = links
	#probabilistic automaton model
	nLinks = len(mLinks) #find the total number of links

	if self.ModelFlag():
		#if the model is already loaded, we don't need to build the model. This occurs if the input file is .bin
		print("model loaded")
		childMatrix = self.ChildMatrix() #get the matrices from stimulustask
		weightMatrix = self.WeightMatrix()
		totalWeights = self.TotalWeights()

		rootIndex = -1 #starting point the matrix
		counter = 1

		while rootIndex == -1:
			rootIndex = childMatrix[counter*nLinks-1]#set the root index to the appropriate element in the matrix
			counter += 1

	else:
		#if the model is not already loaded, we have to create it from the data read in from the text file in stimulustask
		childMatrix = -1*np.ones((len(self.LanguageModel()) + 1)*nLinks) #initialize the child matrix
		#this matrix has all of the links from nodes in the model to their children. Each value in the model is the index of the child node

		self.SetChildMatrix(childMatrix)
		weightMatrix = np.zeros((len(self.LanguageModel())+1)*nLinks) #initial the weight matrix
		#this matrix has the relative weights for each of the links in thechild matrix. This is based on the frequencies from the text file

		self.SetWeightMatrix(weightMatrix)

		totalWeights = np.zeros((len(self.LanguageModel())+1)) #initialize the total weight matrix
		#this matrix hasthe total weight for all links leaving a state. Each value in this will be the sum of the corresponding column in the weight matrix
		self.SetTotalWeights(totalWeights)

		indexMap = {} #maps keys to their index in the model
		index = 0

		rootIndex = len(self.LanguageModel()) #get the starting pofor the model
		#langNodes.clear()
		#LangNode *root  =  &langNodes[""]
		#bciout << mLinks << " " << rootIndex << endl
		links = links.replace(" ", "_")
		print("generating model" ) #debug message showing that the model is being constructed
		##########for std::map<std::string,int>::iterator i = LanguageModel().begin()i! = LanguageModel().end()i++:#loop through all of the elements in LanguageModel (the map built in StimulusTask)
		for item_key in self.LanguageModel():
			indexMap[item_key]  =  index
			#i->first is the key for the element in the map. This assigns the key to an index in the model starting at 0
			index += 1#increment the index
			key  =  item_key #get the key
			#std::replace(key.begin(),key.end(),'_',' ')
			parentKey  =  key[:-1]
			#the parent for the node is the string that is one letter shorter (e.g., the parent of "the" is "th")
			letter  =  key[-1]
			#the last letter in the key
			if self.LanguageModel()[item_key]  ==  0 or links.find(letter)  ==  -1:
			#if the letter doesn't appear in links or doesn't have any weight, skip it
				continue
			index2  =  links.find(letter)
			#std::replace(parentKey.begin(),parentKey.end(),' ','_')
			if len(parentKey) > 0:
				parentIndex = ndexMap[parentKey]
			else:
				parentIndex = rootIndex
			
			if letter == "_":
				childMatrix[parentIndex*nLinks+index2] = rootIndex
			else:
				childMatrix[parentIndex*nLinks+index2] = self.LanguageModel()[item_key] 

			#add a link from the parent to current node
			weightMatrix[parentIndex*nLinks+index2] = self.LanguageModel()[item_key]  #assign the link the corresponding weight
			totalWeights[parentIndex] +=  self.LanguageModel()[item_key] #update the total weight of the parent
			if index < 20:
				print(str(index2) + " " + str(parentIndex) + " " + str(nLinks))
		print("model generated")
	
	#bciout << sizeof(childMatrix) << " " << sizeof(weightMatrix) << " " << sizeof(totalWeights) << " " << len(LanguageModel()) << " " << nLinks << endl
	#code for writing out the language model structures to bin files

	myFile1 = open('test_child.bin', 'ab')
	char_childMatrix = childMatrix.astype(str)
	pkl.dump(childMatrix, myFile1)
	myFile1.close()

	myFile2 = open('test_weight.bin', 'ab')
	char_weightMatrix = weightMatrix.astype(str)
	pkl.dump(weightMatrix, myFile2)
	myFile2.close()

	myFile3 = open('test_total.bin', 'ab')
	char_totalWeights = totalWeights.astype(str)
	pkl.dump(totalWeights, myFile3)
	myFile3.close()

	#n-gram model
	#these are older models. We don't really use them anymore, so it isn't important that they still work. It is always better to be backwards compatible, however.
	biCounts = [0 for _ in range(self.fProbs.size)]
	triCounts = [0 for _ in range(self.fProbs.size*len(self.mTargets))]

	for i in range(self.fProbs.size):

		b = int(i/len(self.mTargets))
		c = i%len(self.mTargets)

		for a in range(len(self.mTargets)):
			d = a

			if self.TargetDefinitions[b][1] == " ":
				d = b

			key  =  ""
			key2  =  ""

			key += self.TargetDefinitions[d][0] + self.TargetDefinitions[b][0] + self.TargetDefinitions[c][0]
			key2 += self.TargetDefinitions[d][0] + self.TargetDefinitions[b][0]

			key = key.replace(" ", "_")
			key2 = key2.replace(" ", "_")

			key = lower(key)
			key2 = lower(key2)

			key2 += "X"

			bind  =  a*len(self.mTargets)+b
			tind  =  a*self.fProbs.size+i

			biCounts[bind] = self.LanguageModel()[key2]
			triCounts[tind] = self.LanguageModel()[key]