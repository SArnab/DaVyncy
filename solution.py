import sys

fragments = {};
overlapScores = {};

class Fragment:

	value = '';
	length = 0;

	def __init__(self,value,index):
		self.index = index;
		self.value = value
		self.length = len(value)

# Finds The Maximum Overlap Between Two Fragments
def findOverlap(fragment1,fragment2):
	# Which Is the larger fragment?
	if fragment1.length >= fragment2.length:
		largeFragment = fragment1
		smallFragment = fragment2
	else:
		largeFragment = fragment2
		smallFragment = fragment1

	# First, check if one is a complete substring
	substr_index = largeFragment.value.find(smallFragment.value)
	if substr_index != -1:
		overlapScores[`fragment1.index` + '_' + `fragment2.index`] = [smallFragment,largeFragment,0,smallFragment.length,0]
		return smallFragment.length;
	
	maxOverlap = 0

	# Anchor The Larger String. Move Smaller String Along To Find Largest Overlap.
	largeAnchor_l = leftAnchor(largeFragment,smallFragment)
	largeAnchor_r = rightAnchor(largeFragment,smallFragment)
	if largeAnchor_l[1] == 0 and largeAnchor_r[1] == 0:
		return False
	elif largeAnchor_r[1] >= largeAnchor_l[1]:
	 	overlapScores[`fragment1.index` + '_' + `fragment2.index`] = [smallFragment,largeFragment,largeAnchor_r[0],largeAnchor_r[1],1]
	 	return largeAnchor_r[1]
	else:
	 	overlapScores[`fragment1.index` + '_' + `fragment2.index`] = [smallFragment,largeFragment,largeAnchor_l[0],largeAnchor_l[1],2]
	 	return largeAnchor_l[1]

def leftAnchor(anchorString,traversalString,verbose = False):
	maxOverlap = 0
	returnList = [0,0]
	for i in reversed(range(0,traversalString.length)):
		# No point in checking remaining overlap if the remaining length is smaller
		if maxOverlap >= (traversalString.length - i):
			break;
		if traversalString.value[i] == anchorString.value[0]:
			if verbose:
				print "Starting match found at index %d of traversal fragment. Character is %s" % (i,anchorString.value[0])
			overlapLength = 1;
			# Awesome. Check If The Next Few Letters Match.
			for (x,y) in zip(range(i+1,traversalString.length),range(1,anchorString.length)):
				if anchorString.value[y] == traversalString.value[x]:
					if verbose:
						print "Anchor Fragment at position %d = Traversal Fragment at position %d. Character is %s" % (y,x,anchorString.value[y])
					overlapLength += 1
				else:
					overlapLength = 0
					if verbose:
						print "Match ended before the end of the traversal string."
					break;
			if verbose:
				print "Total Overlap Length For This Match: %d" % (overlapLength)
			if(overlapLength > maxOverlap):
				maxOverlap = overlapLength
				returnList = [i,maxOverlap]

	return returnList

def rightAnchor(anchorString,traversalString,verbose = False):
	maxOverlap = 0
	returnList = [0,0]
	for i in range(0,traversalString.length):
		if traversalString.value[i] == anchorString.value[anchorString.length-1]:
			traverseAnchored = False
			if verbose:
				print "Starting match found at index %d of traversal fragment. Character is %s" % (i,traversalString.value[i])
			overlapLength = 1;
			for (x,y) in zip(range(0,i),range(anchorString.length-i-1,anchorString.length)):
				# If We Are Not Anchored..No Point Just Move On.
				if x == 0 and anchorString.value[y] != traversalString.value[x]:
					traversalAnchored = False
					overlapLength = 0
					if verbose:
						print "Traversal string is not anchored at index 0. Overlap worthless."
					break;

				if anchorString.value[y] == traversalString.value[x]:
					if x == 0:
						traversalAnchored = True
					if verbose:
						print "Anchor Fragment at position %d = Traversal Fragment at position %d. Character is %s" % (y,x,anchorString.value[y])
					overlapLength += 1
				else:
					if traverseAnchored == False:
						overlapLength = 0
					if verbose:
						print "Match ended before the end of the traversal string."
					break;
			if verbose:
				print "Total Overlap Length For This Match: %d" % (overlapLength)
			if(overlapLength > maxOverlap):
				maxOverlap = overlapLength
				returnList = [(i+1)-maxOverlap,maxOverlap]

	return returnList

def printFragments():
	for (index,fragmentObj) in fragments.iteritems():
		print fragmentObj.value

def combineStrings(runningMaxKey,verbose = False):
	(spliceString,anchorString,index,overlapLength,spliceType) = overlapScores[runningMaxKey]

	if verbose:
		print "Splice Type: %d" % (spliceType)
		print "Splice String: %s Start Index: %d Length: %d" % (spliceString.value,index,overlapLength)

	if spliceType == 0:
		newString = anchorString.value
	elif spliceType == 1:
		newString = anchorString.value + spliceString.value[index+overlapLength::]
	elif spliceType == 2:
		newString = spliceString.value[0:index] + anchorString.value
	
	if verbose:
		print "Fragment %d is being removed" % (spliceString.index)

	for i in fragments:
		if i == spliceString.index:
			continue;

		if i < spliceString.index:
			key = `i`+'_'+`spliceString.index`
		else:
			key = `spliceString.index` + '_' + `i`
		if verbose:
			print "Attempting to remove overlap score %s" % (key)
		if key in overlapScores:
			if verbose:
				print "Overlap score %s removed" % (key)
			del overlapScores[key]
		else:
			if verbose:
				print "Key does not exist. Moving on."
	del fragments[spliceString.index], spliceString

	fragments[anchorString.index].value = newString
	fragments[anchorString.index].length = len(newString)
	# Recalculate All Overlaps
	runningMaxKey = ''
	runningMaxOverlap = 0
	for (i,fragment2) in fragments.iteritems():
		if(i == anchorString.index):
			continue
		if verbose:
			print "Recalculating overlap between newly formed fragment %d and existing fragment %d" % (anchorString.index,i)

		if(fragment2.index < anchorString.index):
			runningMaxKey = `fragment2.index` + '_' + `anchorString.index`
			overlap = findOverlap(fragment2,anchorString)
		else:
			runningMaxKey = `anchorString.index` + '_' + `fragment2.index`
			overlap = findOverlap(anchorString,fragment2)
		if(overlap > runningMaxOverlap):
			runningMaxOverlap = overlap
	# Are We Finished?		
	if len(overlapScores) == 0:
		if verbose:
			print "No remaining fragments overlap. The final output is below."
		printFragments()
		sys.exit()

	runningMaxKey = max(overlapScores,key = lambda x: overlapScores[x][3])
	if verbose:
		print "The maximum key is %s" % (runningMaxKey)
	combineStrings(runningMaxKey)

def main():
	fh = open(sys.argv[1],"r")
	fragmentCount = -1
	for line in fh.readlines(): 
		for fragment in line.split(";"):
			fragmentCount += 1
			fragments[fragmentCount] = Fragment(fragment,fragmentCount)
	fh.close()

	runningMaxKey = ''
	runningMaxOverlap = 0

	for (fragmentKey,fragment1) in fragments.iteritems():
		# Check Overlap With All Fragments Ahead Of This
		for i in range(fragmentKey+1,fragmentCount+1):
			fragment2 = fragments[i]
			overlap = findOverlap(fragment1,fragment2)
			if overlap > runningMaxOverlap:
				runningMaxOverlap = overlap
				runningMaxKey = `fragment1.index` + '_' + `fragment2.index`
	# Combine The Strings With Maximum Overlap
	if(runningMaxKey != ''):
		combineStrings(runningMaxKey)

main()