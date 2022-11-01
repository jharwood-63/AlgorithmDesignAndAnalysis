#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time
import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass
	
# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment

	def align(self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length

###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
		if len(seq1) > align_length:
			seq1Length = align_length + 1
		else:
			seq1Length = len(seq1) + 1

		if len(seq2) > align_length:
			seq2Length = align_length + 1
		else:
			seq2Length = len(seq2) + 1

		score = 0
		alignmentTable = [[0] * seq1Length for _ in range(seq2Length)]
		path = [[""] * seq1Length for _ in range(seq2Length)]

		for i in range(seq2Length):
			alignmentTable[i][0] = i * 5

		for j in range(seq1Length):
			alignmentTable[0][j] = j * 5

		for i in range(1, seq2Length):
			for j in range(1, seq1Length):
				equality = seq2[i-1] == seq1[j-1]
				if equality:
					diagonal = alignmentTable[i-1][j-1] - 3
				else:
					diagonal = 1 + alignmentTable[i-1][j-1]

				left = 5 + alignmentTable[i][j-1]
				top = 5 + alignmentTable[i-1][j]

				if left <= diagonal and left <= top:
					alignmentTable[i][j] = left
					path[i][j] = "l"
				elif top <= diagonal and top < left:
					alignmentTable[i][j] = top
					path[i][j] = "t"
				elif diagonal < left and diagonal < top:
					alignmentTable[i][j] = diagonal
					if equality:
						path[i][j] = "e"
					else:
						path[i][j] = "s"

		# The score is tracked when you go back to create the path
		vertIndex = seq2Length - 1
		horizIndex = seq1Length - 1
		seq2Index = seq2Length - 2
		seq1Index = seq1Length - 2
		alignment1 = ""
		alignment2 = ""
		for i in range(len(seq2)):
			if path[vertIndex][horizIndex] == "l":  # insert
				alignment2 = alignment2 + seq1[seq1Index]
				alignment1 = alignment1 + "_"
				score += 5
				horizIndex -= 1
				seq1Index -= 1
			elif path[vertIndex][horizIndex] == "t":  # delete
				alignment2 = alignment2 + "_"
				alignment1 = alignment1 + seq2[seq2Index]
				score += 5
				vertIndex -= 1
				seq2Index -= 1
			elif path[vertIndex][horizIndex] == "s":  # swap
				alignment2 = alignment2 + seq1[seq1Index]
				alignment1 = alignment1 + seq2[seq2Index]
				score += 1
				horizIndex -= 1
				vertIndex -= 1
				seq1Index -= 1
				seq2Index -= 1
			elif path[vertIndex][horizIndex] == "e":  # leave it
				alignment2 = alignment2 + seq2[seq2Index]
				alignment1 = alignment1 + seq1[seq1Index]
				score -= 3
				horizIndex -= 1
				vertIndex -= 1
				seq1Index -= 1
				seq2Index -= 1

		alignment1 = alignment1[::-1]
		alignment2 = alignment2[::-1]
###################################################################################################					
		
		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}


