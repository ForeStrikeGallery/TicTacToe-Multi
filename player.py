import time

class Player:
		
	def __init__(self, symbol):
		self.points = 0
		self.stretches = list()
		self.symbol = symbol

	def getSymbol(self):
		return self.symbol

	def getPoints(self):
		return self.points
	
	def getStretches(self):
		return self.stretches
		
	def reset(self):
		self.points = 0
		self.stretches = list()

	def addBox(self, x, y):	
		updatedStretches = list()
		sizeTwoStretches = list()
		sizeOneStretches = list()

		for stretch in self.stretches:
			s = self.fitIfPossible((x, y), stretch)
			#print("fit if possible: ", s)

			if s:
				if len(s) == 2:
					sizeTwoStretches.append((stretch, s))	
					sizeOneStretches.append(stretch)
					continue
				updatedStretches.append(s)
			else:
				updatedStretches.append(stretch)	

		#print("size two ", sizeTwoStretches)
		#print("updated stretch", updatedStretches)

		filteredSizeTwo = list()
		
		for k in sizeTwoStretches:
			val = k[0][0]

			flag = True 
			for s in stretch:
				if val in s:
					flag = False
					break

			if flag:
				filteredSizeTwo.append(k[1])

		#print("filtered size two ", filteredSizeTwo)
		updatedStretches.append([(x, y)])
		updatedStretches.extend(filteredSizeTwo)
		updatedStretches.extend(sizeOneStretches)
		self.stretches = updatedStretches
		
		self.mergeConnectedStretches()
		print("Before ", self.stretches)
		self.stretches = self.dedupe(self.stretches)
		print("After ", self.stretches)
		self.updatePoints()

		print(self.stretches)

	def mergeConnectedStretches(self):
		mergedStretches = list()
		itemsToRemove = list()

		#print("Stretches: ", self.stretches)
		for i in range(len(self.stretches) - 1):
			for j in range(i, len(self.stretches)):
				if i == j:
					continue

				res = self.stretches[i].copy()
				res.extend(self.stretches[j])

				if self.validStretch(res):

					flag = True
					for s in self.stretches:
						if set(res).issubset(set(s)):
							flag = False 
							break

					if not flag:
						continue 	

					#print(" valid stretch ", res)
			
					mergedStretches.append(res)
					
					if len(self.stretches[i]) > 1:
						itemsToRemove.append(self.stretches[i])
			
					if len(self.stretches[j]) > 1:
						itemsToRemove.append(self.stretches[j])
				
					continue 

		for item in itemsToRemove:
			self.stretches.remove(item)

		mergedStretches = self.dedupe(mergedStretches)
		self.stretches.extend(mergedStretches)

		if len(mergedStretches) > 0:
			self.mergeConnectedStretches()

	def dedupe(self, stretches):
		res = list()

		stretches = sorted(stretches, key = len, reverse = True)
		for s in stretches:
			f = True 
			for r in res:
				if set(s).issubset(set(r)) and len(s) != 1:
					f = False 
					continue 	

			if not f:
				continue

			res.append(s)

		return res

	def updatePoints(self):

		self.points = 0 
		for stretch in self.stretches:
			if len(stretch) < 3:
				continue

			self.points += (len(stretch) - 2) * 2 - 1

	def printInfo(self):
		print("Points: ", self.points)


	def fitIfPossible(self, pos, stretch):

		result = stretch.copy()
		result.append(pos)

		if self.validStretch(result):
			return result 

		result = stretch.copy()
		result.insert(0, pos)

		if self.validStretch(result):
			return result

		return None 

	def validStretch(self, stretch):
		if (len(stretch)) == 1:
			return True 

		diff_x = stretch[0][0] - stretch[1][0]
		diff_y = stretch[0][1] - stretch[1][1]

		if abs(diff_x) > 1 or abs(diff_y) > 1:
			return False

		for i in range(1, len(stretch) - 1):
			if stretch[i][0] - stretch[i+1][0] != diff_x:
				return False

			if stretch[i][1] - stretch[i+1][1] != diff_y:
				return False

		return True 
		
