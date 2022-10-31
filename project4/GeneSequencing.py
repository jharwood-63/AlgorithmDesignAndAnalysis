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

	def align( self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length

###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
		score = 0
		alignmentTable = [[0] * (len(seq2) + 1) for i in range(len(seq1) + 1)]
		path = []

		for i in range(len(seq2) + 1):
			alignmentTable[i][0] = i

		for j in range(len(seq1) + 1):
			alignmentTable[0][j] = j

		for i in range(1, (len(seq2) + 1)):
			for j in range(1, (len(seq1) + 1)):
				equality = seq2[i-1] == seq1[j-1]
				if equality:
					diagonal = 1 + alignmentTable[i-1][j-1]
				else:
					diagonal = alignmentTable[i-1][j-1] - 3

				left = 5 + alignmentTable[i][j-1]
				top = 5 + alignmentTable[i-1][j]

				if left <= diagonal and left <= top:
					print("left")
				elif top <= diagonal and top < left:
					print("top")
				elif diagonal < left and diagonal < top:
					print("diagonal")



		alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
			len(seq1), align_length, ',BANDED' if banded else '')
		alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
			len(seq2), align_length, ',BANDED' if banded else '')
###################################################################################################					
		
		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}


