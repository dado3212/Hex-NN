from timing import timing
from board import Board, Move
from pieces import new_piece, all_pieces
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
    global score_weighting, space_weighting, move_weighting
    board = self.append_move(b, move)
    next_moves = board.get_moves(pieces)
    possible_moves = board.get_moves(all_pieces())
    w = board.score_last * score_weighting + (board.spaces / 61.0) * space_weighting + len(next_moves) * move_weighting + len(possible_moves) * possible_move_weighting
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

  # @timing
  def finish(self):
    while (not self.done):
      self.play()

    self.finished_board = Board(self.moves)

best_player = None

def average_run(num_iterations):
  diff = 0
  score = 0

  for i in xrange(1, num_iterations):
    t = time.time()
    player = Player()
    player.finish()
    diff += (time.time() - t)
    score += player.finished_board.score
    # player.finished_board.print_self()

  return [float(score)/diff, score/num_iterations]

def evaluate(a):
  print evaluate
  global best_player
  for i in xrange(1, a):
    print i
    player = Player()
    player.finish()

    if best_player is None or player.score() > best_player.score():
      best_player = player
      best_player.status()

# Got up to 3-180
score_weighting = 2
space_weighting = 180
move_weighting = 1
possible_move_weighting = 1
evaluate(100)
# try:
#   best = []
#   best_score = 0
#   for score_weighting in range(1, 5):
#     for space_weighting in range(0, 220, 20):
#       for move_weighting in range(1, 5):
#         a = average_run(10)
#         print str(score_weighting) + " - " + str(space_weighting) + " - " + str(a[1])
#         if a[1] > best_score:
#           best = [score_weighting, space_weighting, move_weighting]
#           best_score = a[1]
#           print best_score
# except KeyboardInterrupt:
#   print ""
#   print score_weighting
#   print space_weighting
#   print move_weighting
#   print best
#   print best_score

print "=====" # 0< 4, 100
print best_score
print best

# average_time(30)
# parameters(5)

# pool = ThreadPool(4)
# results = pool.map(evaluate, [1, 2, 3, 4])