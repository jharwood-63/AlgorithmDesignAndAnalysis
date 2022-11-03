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


def alignBanded(seq1, seq2, seq1Length, seq2Length):
	score = 0
	alignmentTable = [[math.inf] * 7 for _ in range(seq2Length)]
	path = [[""] * 7 for _ in range(seq2Length)]

	for j in range(3, 7):
		alignmentTable[0][j] = abs(j - 3) * 5

	currIndex = 0
	for i in range(3, 0, -1):
		alignmentTable[i][currIndex] = i * 5
		currIndex += 1

	bottomRightStart = seq1Length - 3
	startIndex = 3
	endIndex = 5
	offsetStart = 1
	offset = 1
	for i in range(1, seq2Length):
		currIndex = startIndex
		while currIndex < 7:
			if i >= bottomRightStart and currIndex > endIndex:
				currIndex += 7
				continue
			else:
				if i <= 4:
					seq1Index = currIndex - startIndex
				else:
					seq1Index = offset
					offset += 1

				equality = seq2[i - 1] == seq1[seq1Index]
				if equality:
					diagonal = MATCH + alignmentTable[i-1][currIndex]
				else:
					diagonal = SUB + alignmentTable[i-1][currIndex]

				if currIndex > 0:
					left = INDEL + alignmentTable[i][currIndex - 1]
				else:
					left = math.inf

				if (currIndex + 1) < 7:
					top = INDEL + alignmentTable[i-1][currIndex + 1]
				else:
					top = math.inf

				if left <= diagonal and left <= top:
					alignmentTable[i][currIndex] = left
					path[i][currIndex] = "l"
				elif top <= diagonal and top < left:
					alignmentTable[i][currIndex] = top
					path[i][currIndex] = "t"
				elif diagonal < left and diagonal < top:
					alignmentTable[i][currIndex] = diagonal
					if equality:
						path[i][currIndex] = "e"
					else:
						path[i][currIndex] = "s"
				currIndex += 1

		if i >= bottomRightStart:
			endIndex -= 1

		if i > 4:
			offsetStart += 1
			offset = offsetStart

		if startIndex != 0:
			startIndex -= 1

	vertIndex = seq2Length - 1
	if seq2Length == seq1Length:
		horizIndex = 3
	else:
		horizIndex = 2
	seq2Index = seq2Length - 2
	seq1Index = seq1Length - 2
	alignment1 = ""
	alignment2 = ""
	for i in range(len(seq2)):
		if path[vertIndex][horizIndex] == "l":  # insert
			alignment2 = alignment2 + "-"
			alignment1 = alignment1 + seq1[seq1Index]
			score += 5
			horizIndex -= 1
			seq1Index -= 1
		elif path[vertIndex][horizIndex] == "t":  # delete
			alignment2 = alignment2 + seq2[seq2Index]
			alignment1 = alignment1 + "-"
			score += 5
			vertIndex -= 1
			horizIndex += 1
			seq2Index -= 1
		elif path[vertIndex][horizIndex] == "s":  # swap
			alignment2 = alignment2 + seq2[seq2Index]
			alignment1 = alignment1 + seq1[seq1Index]
			score += 1
			vertIndex -= 1
			seq1Index -= 1
			seq2Index -= 1
		elif path[vertIndex][horizIndex] == "e":  # leave it
			alignment2 = alignment2 + seq2[seq2Index]
			alignment1 = alignment1 + seq1[seq1Index]
			score -= 3
			vertIndex -= 1
			seq1Index -= 1
			seq2Index -= 1

	alignment1 = alignment1[::-1]
	alignment2 = alignment2[::-1]

	alignment1 = alignment1[0:100]
	alignment2 = alignment2[0:100]

	return score, alignment1, alignment2


def alignNotBanded(seq1, seq2, seq1Length, seq2Length):
	score = 0
	alignmentTable = [[0] * seq1Length for _ in range(seq2Length)]
	path = [[""] * seq1Length for _ in range(seq2Length)]

	for i in range(seq2Length):
		alignmentTable[i][0] = i * INDEL

	for j in range(seq1Length):
		alignmentTable[0][j] = j * INDEL

	for i in range(1, seq2Length):
		for j in range(1, seq1Length):
			equality = seq2[i - 1] == seq1[j - 1]
			if equality:
				diagonal = MATCH + alignmentTable[i - 1][j - 1]
			else:
				diagonal = SUB + alignmentTable[i - 1][j - 1]

			left = INDEL + alignmentTable[i][j - 1]
			top = INDEL + alignmentTable[i - 1][j]

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

	# insertion -> - in alignment 2, character in alignment 1
	# deletion -> - in alignment 1, character in alignment 2
	# swap -> keep both characters
	# equal -> keep both characters

	# The score is tracked when you go back to create the path
	vertIndex = seq2Length - 1
	horizIndex = seq1Length - 1
	seq2Index = seq2Length - 2
	seq1Index = seq1Length - 2
	alignment1 = ""
	alignment2 = ""
	for i in range(len(seq2)):
		if path[vertIndex][horizIndex] == "l":  # insert
			alignment2 = alignment2 + "-"
			alignment1 = alignment1 + seq1[seq1Index]
			score += 5
			horizIndex -= 1
			seq1Index -= 1
		elif path[vertIndex][horizIndex] == "t":  # delete
			alignment2 = alignment2 + seq2[seq2Index]
			alignment1 = alignment1 + "-"
			score += 5
			vertIndex -= 1
			seq2Index -= 1
		elif path[vertIndex][horizIndex] == "s":  # swap
			alignment2 = alignment2 + seq2[seq2Index]
			alignment1 = alignment1 + seq1[seq1Index]
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

	alignment1 = alignment1[0:100]
	alignment2 = alignment2[0:100]

	return score, alignment1, alignment2


class GeneSequencing:

	def __init__(self):
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

		if not banded:
			score, alignment1, alignment2 = alignNotBanded(seq1, seq2, seq1Length, seq2Length)
		else:
			difference = abs(seq1Length - seq2Length)
			if difference <= 1:
				score, alignment1, alignment2 = alignBanded(seq1, seq2, seq1Length, seq2Length)
			else:
				score = math.inf
				alignment1 = "No Alignment Possible"
				alignment2 = "No Alignment Possible"


		###################################################################################################

		return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
