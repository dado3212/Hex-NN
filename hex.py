from timing import timing
from board import Board, Move
from pieces import new_piece
import math, time

def copy_board(board):
  return board.duplicate()

class Player:
  def __init__(self):
    self.pieces = [new_piece(), new_piece(), new_piece()]
    self.moves = []
    self.done = False

  def append_move(self, board, move):
    b = copy_board(board)
    b.make_move(move)
    return b

  def weight(self, b, move, pieces, depth, max_depth):
    if (depth == max_depth):
      return 0

    board = self.append_move(b, move)
    w = board.score
    for move in board.get_moves(pieces):
      p = pieces[:]
      p.remove(move.piece)

      w += self.weight(board, move, p, depth + 1, max_depth)
    return w

  def get_best_move(self, depth):
    board = Board(self.moves)
    valid_moves = board.get_moves(self.pieces)
    if (len(valid_moves) < 50):
      depth += 1

    best_weight = 0
    best_move = None
    for move in valid_moves:
      w = self.weight(board, move, self.pieces, 0, depth)
      if w > best_weight:
        best_weight = w
        best_move = move

    return best_move

  def play(self):
    move = self.get_best_move(2)

    if (move == None):
      self.done = True
    else:
      self.moves.append(move)
      self.pieces.remove(move.piece)
      self.pieces.append(new_piece())

  def status(self):
    board = Board(self.moves)
    print board.score
    board.print_self()

player = Player()
while (not player.done):
  player.play()
  player.status()

player.status()