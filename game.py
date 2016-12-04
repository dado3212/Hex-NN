from board import Board
from pieces import new_piece
import math, copy

class Game:
  def __init__(self):
    self.score = 0
    self.board = Board(9)
    self.pieces = [new_piece(), new_piece(), new_piece()]

  def add_piece(self):
    self.pieces.append(new_piece())

  def game_over(self):
    possible = False
    for piece in self.pieces:
      for row in range(len(self.board.board)):
        for pos in range(len(self.board.board[row])):
          if self.board.can_place_piece(piece, [row, pos]):
            possible = True
            break
        else:
          continue
        break
      else:
        continue
      break

    return (not possible)

  # Checks to see if there are any full rows
  # Rows are defined by a starting position, a direction, and a length (for calculation ease)
  def completed_rows(self, board, piece, loc):
    piece_locations = [loc]
    for d in piece.path:
      loc = board.next_loc(loc, d)
      piece_locations.append(loc)

    completed = []

    for location in piece_locations:
      # Check each 'row' the piece is in to see if any of them are full
      # Horizontal
      loc = location[:]
      found_horizontal = True
      for pos in range(0, len(board.board[loc[0]])):
        if board.val([loc[0], pos]) == 0:
          found_horizontal = False
          break
      if found_horizontal:
        row = [[location[0], 0], 'r', len(board.board[location[0]])]
        if row not in completed:
          completed.append(row)

      # Down-right
      loc = location[:]
      found_dr = True
      top = []
      c = 0
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if board.val(loc) == 0:
            found_dr = False
            break
          top = loc[:]
          loc = board.next_loc(loc, 'ul')
          c+=1
      except Exception as e:
        pass

      loc = location[:]
      c-=1 # don't double count point
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if board.val(loc) == 0:
            found_dr = False
            break
          loc = board.next_loc(loc, 'dr')
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
          if board.val(loc) == 0:
            found_dl = False
            break
          top = loc[:]
          loc = board.next_loc(loc, 'ur')
          c+=1
      except Exception as e:
        pass

      loc = location[:]
      c-=1 # don't double count point
      try:
        while (loc[0] >= 0 and loc[1] >= 0):
          if board.val(loc) == 0:
            found_dl = False
            break
          loc = board.next_loc(loc, 'dl')
          c+=1
      except Exception as e:
        pass
      if found_dl:
        row = [top, 'dl', c]
        if row not in completed:
          completed.append(row)

    return completed

  # Make a move
  def make_move(self, piece, loc):
    # Places the piece
    self.board.place_piece(piece, loc)

    # Check to see if any rows were completed (by the piece)
    rows = self.completed_rows(self.board, piece, loc)

    # Handles scoring
    score = 40 # for placing a piece
    if len(rows) > 0:
      base = 10 * (len(rows) + 1)
      for i, row in enumerate(rows):
        # Number of pieces * (base score * 1.2^row index)
        score += int(row[2] * (math.floor((base * max(1.2**i, 1)))))

    # Clears those rows
    for row in rows:
      self.board.clear_row(row)

    self.score += score

  def print_board(self):
    self.board.print_self()