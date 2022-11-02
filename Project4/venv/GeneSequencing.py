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

    def __init__(self):
        pass

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length

        seq1 = seq1[:align_length]
        seq2 = seq2[:align_length]

        sequence_table = {}

        # populate table

        final_i = 0
        final_j = 0
        start_place = 1
        # Calculate minimum cost to change one string to other
        if banded:
            self.backptrs = {}

            if abs(len(seq1) - len(seq2)) > MAXINDELS:
                return {'align_cost': float('inf'), 'seqi_first100': "no alignment", 'seqj_first100': "no alignmnet"}

            for i in range(0, MAXINDELS + 1):
                sequence_table[(i, 0)] = i * INDEL
                if (i - 1, 0) in self.backptrs:
                    self.backptrs[(i, 0)] = (i - 1, 0)
                else:
                    self.backptrs[(i, 0)] = None
            for j in range(0, MAXINDELS + 1):
                sequence_table[(0, j)] = j * INDEL
                if (0, j - 1) in self.backptrs:
                    self.backptrs[(0, j)] = (0, j - 1)
                else:
                    self.backptrs[(0, j)] = None

            for i in range(1, len(seq1) + 1):
                for j in range(start_place, len(seq2) + 1):
                    if abs(i - j) <= MAXINDELS:
                        diagonal_cell = sequence_table[(i - 1, j - 1)] + SUB
                        if sequence_table.get(((i - 1), j)) is None:
                            up_cell = float('inf')
                        else:
                            up_cell = sequence_table[(i - 1, j)] + INDEL
                        if sequence_table.get((i, (j - 1))) is None:
                            left_cell = float('inf')
                        else:
                            left_cell = sequence_table[(i, j - 1)] + INDEL

                        if seq1[i - 1] == seq2[j - 1]:
                            sequence_table[(i, j)] = sequence_table[(i - 1, j - 1)] + MATCH
                            self.backptrs[(i, j)] = (i - 1, j - 1)
                        elif left_cell <= diagonal_cell and left_cell <= up_cell:
                            sequence_table[(i, j)] = left_cell
                            self.backptrs[(i, j)] = (i, j - 1)
                        elif up_cell <= diagonal_cell and up_cell <= left_cell:
                            sequence_table[(i, j)] = up_cell
                            self.backptrs[(i, j)] = (i - 1, j)
                        else:
                            sequence_table[(i, j)] = diagonal_cell
                            self.backptrs[(i, j)] = (i - 1, j - 1)
                        final_i = i
                        final_j = j
                    if up_cell == float('inf'):
                        break
                if i >= MAXINDELS + 1:
                    start_place += 1
        else:
            self.backptrs = {}

            for i in range(0, len(seq1) + 1):
                sequence_table[(i, 0)] = i * INDEL
                if (i - 1, 0) in self.backptrs:
                    self.backptrs[(i, 0)] = (i - 1, 0)
                else:
                    self.backptrs[(i, 0)] = None
            for j in range(0, len(seq2) + 1):
                sequence_table[(0, j)] = j * INDEL
                if (0, j - 1) in self.backptrs:
                    self.backptrs[(0, j)] = (0, j - 1)
                else:
                    self.backptrs[(0, j)] = None

            for i in range(1, len(seq1) + 1):
                for j in range(1, len(seq2) + 1):
                    diagonal_cell = sequence_table[(i - 1, j - 1)] + SUB
                    if sequence_table.get(((i - 1), j)) is None:
                        up_cell = float('inf')
                    else:
                        up_cell = sequence_table[(i - 1, j)] + INDEL
                    if sequence_table.get((i, (j - 1))) is None:
                        left_cell = float('inf')
                    else:
                        left_cell = sequence_table[(i, j - 1)] + INDEL

                    # document backtrace
                    if seq1[i - 1] == seq2[j - 1]:
                        sequence_table[(i, j)] = sequence_table[(i - 1, j - 1)] + MATCH
                        self.backptrs[(i, j)] = (i - 1, j - 1)
                    elif left_cell <= diagonal_cell and left_cell <= up_cell:
                        sequence_table[(i, j)] = left_cell
                        self.backptrs[(i, j)] = (i, j - 1)
                    elif up_cell <= diagonal_cell and up_cell <= left_cell:
                        sequence_table[(i, j)] = up_cell
                        self.backptrs[(i, j)] = (i - 1, j)
                    else:
                        sequence_table[(i, j)] = diagonal_cell
                        self.backptrs[(i, j)] = (i - 1, j - 1)
                final_i = i
                final_j = j

        new_seq1 = ""
        new_seq2 = ""

        curr_pos = (len(seq1), len(seq2))
        prev_pos = self.backptrs[curr_pos]

        while prev_pos is not None:
            if prev_pos == (curr_pos[0], curr_pos[1] - 1):
                new_seq1 = "-" + new_seq1
                new_seq2 = seq2[curr_pos[1] - 1] + new_seq2
            elif prev_pos == (curr_pos[0] - 1, curr_pos[1]):
                new_seq1 = seq1[curr_pos[0] - 1] + new_seq1
                new_seq2 = "-" + new_seq2
            elif prev_pos == (curr_pos[0] - 1, curr_pos[1] - 1):
                new_seq1 = seq1[curr_pos[0] - 1] + new_seq1
                new_seq2 = seq2[curr_pos[1] - 1] + new_seq2


            curr_pos = prev_pos
            prev_pos = self.backptrs[curr_pos]


        ###################################################################################################
        # your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
        score = sequence_table[(final_i, final_j)]
        alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
            len(seq1), align_length, ',BANDED' if banded else '')
        alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
            len(seq2), align_length, ',BANDED' if banded else '')
        return {'align_cost': score, 'seqi_first100': new_seq1[:100], 'seqj_first100': new_seq2[:100]}
        #return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
        ###################################################################################################



