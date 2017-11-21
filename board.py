# coding: utf-8

from timing import timing
import sys, math, numpy as np

class Move:
  def __init__(self, piece, loc):
    self.piece = piece
    self.loc = loc

class Board:
  def __init__(self, moves):
    self.board = [
          [0,0,0,0,0],
         [0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
         [0,0,0,0,0,0],
          [0,0,0,0,0]
    ]
    self.score = 0
    self.score_last = 0
    self.spaces = 61

    # Iterate through all of the previous moves
    for move in moves:
      self.make_move(move)

  def key(self):
    return "".join(["".join([str(pos) for pos in row]) for row in self.board])

  # Figure out how many spaces are left open
  def space(self):
    return self.spaces

  def duplicate(self):
    b = Board([])
    b.board = [x[:] for x in self.board]
    b.score = self.score
    b.spaces = self.spaces
    return b

  # Get all valid moves
  def get_moves(self, pieces):
    valid = []
    for piece in pieces:
      for row in range(9):
        for pos in range(len(self.board[row])):
          if self.can_place_piece(piece, [row, pos]):
            valid.append(Move(piece, [row, pos]))
    return valid

  # Make a move
  def make_move(self, move):
    piece = move.piece
    loc = move.loc

    # Place the piece
    self.place_piece(piece, loc)

    # Check to see if any rows were completed (by the piece)
    rows = self.completed_rows(piece, loc)

    # Handles scoring
    score = 40 # for placing a piece
    if len(rows) > 0:
      base = 10 * (len(rows) + 1)
      for i, row in enumerate(rows):
        # Number of pieces * (base score * 1.2^row index)
        score += int(row[2] * (math.floor((base * max(1.2**i, 1)))))

    # Clears those rows
    for row in rows:
      self.clear_row(row)

    self.score_last = score
    self.score += score

  # Checks to see if there are any full rows
  # Rows are defined by a starting position, a direction, and a length (for calculation ease)
  def completed_rows(self, piece, loc):
    piece_locations = [loc]
    for d in piece.path:
      loc = self.next_loc(loc, d)
      piece_locations.append(loc)

    completed = []

    for location in piece_locations:
      # Check each 'row' the piece is in to see if any of them are full
      # Horizontal
      loc = location[:]
      found_horizontal = True
      for pos in range(0, len(self.board[loc[0]])):
        if self.val([loc[0], pos]) == 0:
          found_horizontal = False
          break
      if found_horizontal:
        row = [[location[0], 0], 'r', len(self.board[location[0]])]
        if row not in completed:
          completed.append(row)

      # Down-right
      loc = location[:]
      found_dr = True
      top = []
      c = 0
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if self.val(loc) == 0:
            found_dr = False
            break
          top = loc[:]
          loc = self.next_loc(loc, 'ul')
          c+=1
      except Exception as e:
        pass

      loc = location[:]
      c-=1 # don't double count point
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if self.val(loc) == 0:
            found_dr = False
            break
          loc = self.next_loc(loc, 'dr')
          c+=1
      except Exception as e:
        pass
      if found_dr:
        row = [top, 'dr', c]
        if row not in completed:
          completed.append(row)

      # Down-left
      loc = location[:]
      found_dl = True
      top = []
      c = 0
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if self.val(loc) == 0:
            found_dl = False
            break
          top = loc[:]
          loc = self.next_loc(loc, 'ur')
          c+=1
      except Exception as e:
        pass

      loc = location[:]
      c-=1 # don't double count point
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if self.val(loc) == 0:
            found_dl = False
            break
          loc = self.next_loc(loc, 'dl')
          c+=1
      except Exception as e:
        pass
      if found_dl:
        row = [top, 'dl', c]
        if row not in completed:
          completed.append(row)

    return completed

  # Places the piece on the board
  def place_piece(self, piece, loc):
    board = self.board

    self.spaces -= 1

    board[loc[0]][loc[1]] = piece.color
    for d in piece.path:
      self.spaces -= 1
      loc = self.next_loc(loc, d)
      board[loc[0]][loc[1]] = piece.color

  def clear_row(self, row):
    board = self.board

    loc = row[0]
    try:
      while (True):
        board[loc[0]][loc[1]] = 0
        loc = self.next_loc(loc, row[1])
        self.spaces += 1
    except:
      pass

  # Location helper
  def next_loc(self, loc, direction):
    b = 4

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

  '''
    Get the value at a specific location
  '''
  def val(self, loc):
    return self.board[loc[0]][loc[1]]

  '''
    Prints out the full board
  '''
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