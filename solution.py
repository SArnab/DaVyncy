import sys

fragments = {};
fragmentCount = 1
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
		overlapScores[`fragment1.index` + '_' + `fragment2.index`] = [smallFragment,largeFragment,0,smallFragment.length]
		return smallFragment.length;
	
	maxOverlap = 0

	# Anchor The Larger String. Move Smaller String Along To Find Largest Overlap.
	largeAnchor_l = leftAnchor(largeFragment,smallFragment)
	largeAnchor_r = rightAnchor(largeFragment,smallFragment)
	if largeAnchor_l[1] >= largeAnchor_r[1]:
		largeAnchor_max = largeAnchor_l
	else:
		largeAnchor_max = largeAnchor_r
	# Anchor The Smaller String. Move Larger String Along To Find Largest Overlap.
	smallAnchor_l = leftAnchor(smallFragment,largeFragment)
	smallAnchor_r = rightAnchor(smallFragment,largeFragment)
	if smallAnchor_l[1] >= smallAnchor_r[1]:
		smallAnchor_max = smallAnchor_l
	else:
		smallAnchor_max = smallAnchor_r

	if(largeAnchor_max[1] == 0 & smallAnchor_max[1] == 0):
		return False # No Overlap
	elif largeAnchor_max[1] >= smallAnchor_max[1]:
		overlapScores[`fragment1.index` + '_' + `fragment2.index`] = [smallFragment,largeFragment,largeAnchor_max[0],largeAnchor_max[1]]
		return largeAnchor_max[1]
	else:
		overlapScores[`fragment1.index` + '_' + `fragment2.index`] = [largeFragment,smallFragment,smallAnchor_max[0],smallAnchor_max[1]]
		return smallAnchor_max[1]

def leftAnchor(anchorString,traversalString,verbose = False):
	maxOverlap = 0
	returnList = [0,0]
	for i in range(0,traversalString.length):
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
	for i in reversed(range(0,traversalString.length)):
		if maxOverlap >= i:
			break;
		if traversalString.value[i] == anchorString.value[anchorString.length-1]:
			traverseAnchored = False
			if verbose:
				print "Starting match found at index %d of traversal fragment. Character is %s" % (i,anchorString.value[anchorString.length-1])
			if i == traversalString.length-1:
				traverseAnchored = True
				if verbose:
					print "The starting match is an anchor point for the traversal fragment."
			overlapLength = 1;
			for (x,y) in zip(reversed(range(0,i)),reversed(range(0,anchorString.length-1))):
				if anchorString.value[y] == traversalString.value[x]:
					if verbose:
						print "Anchor Fragment at position %d = Traversal Fragment at position %d. Character is %s" % (y,x,anchorString.value[y])
					overlapLength += 1
				else:
					if traverseAnchored == False & x != 0:
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

def combineStrings(runningMaxKey):
	(spliceString,anchorString,index,overlapLength) = overlapScores[runningMaxKey]
	print "Splice: %s %d %d" % (spliceString.value,index,overlapLength)
	print anchorString.value

def main():
	fh = open("input.txt","r")
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