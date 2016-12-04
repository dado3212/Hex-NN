from timing import timing
from board import Board
from game import Game

# @timing
def test():
  best_score = 0
  best_game = None
  for i in xrange(0, 10):
    g = Game()
    g.play()

    if g.score > best_score:
      best_score = g.score
      best_game = g

  best_game.print_outcome()
  print best_score

test()