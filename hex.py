from timing import timing
from board import Board, Move
from pieces import new_piece
import math, time
from multiprocessing.dummy import Pool as ThreadPool 

class Player:
  def __init__(self):
    self.pieces = [new_piece(), new_piece(), new_piece()]
    self.moves = []
    self.done = False
    self.finished_board = None
    self.current_board = Board([])

  def append_move(self, board, move):
    b = board.duplicate()
    b.make_move(move)
    return b

  def weight(self, b, move, pieces, depth, max_depth):
    board = self.append_move(b, move)
    next_moves = board.get_moves(pieces)
    w = board.score_last + board.space() + 2 * len(next_moves)
    if depth + 1 < max_depth:
      for move in next_moves:
        p = pieces[:]
        p.remove(move.piece)

        w += self.weight(board, move, p, depth + 1, max_depth)
    return w

  def get_best_move(self, depth):
    board = self.current_board.duplicate()
    valid_moves = board.get_moves(self.pieces)

    best_weight = 0
    best_move = None
    for move in valid_moves:
      w = self.weight(board, move, self.pieces, 0, depth)
      if w > best_weight:
        best_weight = w
        best_move = move

    return best_move

  def play(self):
    move = self.get_best_move(1)

    if (move == None):
      self.done = True
    else:
      self.moves.append(move)
      self.current_board.make_move(move)
      self.pieces.remove(move.piece)
      self.pieces.append(new_piece())

  def status(self):
    print self.finished_board.score
    self.finished_board.print_self()

  def score(self):
    return self.finished_board.score

  @timing
  def finish(self):
    while (not self.done):
      self.play()

    self.finished_board = Board(self.moves)

best_player = None

def average_time():
  diff = 0
  for i in xrange(1, 20):
    t = time.time()
    player = Player()
    player.finish()
    diff += (time.time() - t)

  print diff / 20 # Number of seconds

def evaluate(a):
  print evaluate
  global best_player
  for i in xrange(1, 100):
    print i
    player = Player()
    player.finish()

    if best_player is None or player.score() > best_player.score():
      best_player = player
      best_player.status()

average_time()

# pool = ThreadPool(4)
# results = pool.map(evaluate, [1, 2, 3, 4])