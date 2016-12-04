# coding: utf-8

import sys

class Board:
  board = []

  def __init__(self, size):
    self.create_board(size)

  # Places the piece on the board
  def place_piece(self, piece, loc):
    board = self.board

    board[loc[0]][loc[1]] = piece.color
    for d in piece.path:
      loc = self.next_loc(loc, d)
      board[loc[0]][loc[1]] = piece.color

  def clear_row(self, row):
    board = self.board

    loc = row[0]
    try:
      while (True):
        board[loc[0]][loc[1]] = 0
        loc = self.next_loc(loc, row[1])
    except:
      pass

  # Location helper
  def next_loc(self, loc, direction):
    b = (len(self.board) - 1)/2

    if direction == 'l':
      return [loc[0], loc[1]-1]
    elif direction == 'r':
      return [loc[0], loc[1]+1]
    elif direction == 'ul':
      return [loc[0]-1, loc[1] - (0 if loc[0] > b else 1)]
    elif direction == 'ur':
      return [loc[0]-1, loc[1] + (0 if loc[0] <= b else 1)]
    elif direction == 'dl':
      return [loc[0]+1, loc[1] - (0 if loc[0] < b else 1)]
    elif direction == 'dr': 
      return [loc[0]+1, loc[1] + (0 if loc[0] >= b else 1)]

  # Tells you if you can place a piece in a certain location
  def can_place_piece(self, piece, loc):
    board = self.board
    try:
      if board[loc[0]][loc[1]] != 0:
        return False
      for d in piece.path:
        loc = self.next_loc(loc, d)
        if loc[0] < 0 or loc[1] < 0 or board[loc[0]][loc[1]] != 0:
          return False
    except Exception:
      return False
    return True

  def val(self, loc):
    return self.board[loc[0]][loc[1]]

  # Creates a new board
  def create_board(self, board_size):
    board = []
    m = (board_size + 1)/2
    for i in range(0, m):
      row = []
      for i in xrange(0, m+i):
        row.append(0)
      board.append(row)
    for i in range(1, m):
      board.append(board[m-1-i][:])
    self.board = board

  # Prints out itself
  def print_self(self):
    board = self.board
    board_size = len(board)

    for row in board:
      sys.stdout.write(" " * (board_size + 1 - len(row)))
      for i in row:
        if i == 0: # empty
          sys.stdout.write("⬡ ")
        elif i == 1: # black
          sys.stdout.write("⬢ ")
        elif i == 2: # green
          sys.stdout.write('\033[92m' + "⬢ " + '\033[0m')
        elif i == 3: # magenta
          sys.stdout.write('\033[95m' + "⬢ " + '\033[0m')
        elif i == 4: # red
          sys.stdout.write('\033[91m' + "⬢ " + '\033[0m')
        elif i == 5: # yellow
          sys.stdout.write('\033[93m' + "⬢ " + '\033[0m')
        elif i == 6: # blue
          sys.stdout.write('\033[94m' + "⬢ " + '\033[0m')
      print ""