from timing import timing
from board import Board
from game import Game
import math, pickle, pygame

from neat import nn, population, config, statistics

class Player:
  def __init__(self, genome):
    self.genome = genome
    self.nn = nn.create_feed_forward_phenotype(genome)
    self.game = Game()
    self.done = False

    # Generate quick way to find the location
    self.locs = []
    for row in range(len(self.game.board.board)):
      for pos in range(len(self.game.board.board[row])):
        self.locs.append([row, pos])

  def make_move(self):
    # Input 1: the board in an array of 0's and 1's
    board = [1 if x > 0 else 0 for x in sum(self.game.board.board, [])]

    #Input 2: the pieces available in an array of 3 numbers representing the pieces
    pieces = [x.index for x in self.game.pieces]

    outputs = self.nn.serial_activate(board + pieces)

    output_locs = sorted(enumerate(outputs[:-1]), key=lambda x: x[1], reverse=True)
    piece = self.game.pieces.pop(int((outputs[-1] - 1e-16) * 3))

    self.game.add_piece()

    # Place the best possible move
    for loc in output_locs:
      if (self.game.board.can_place_piece(piece, self.locs[loc[0]])):
        self.game.make_move(piece,  self.locs[loc[0]])
        return True
    return False

generations = 0
best_fitness = 0
fitness_history = []
best_genome = None

# Pygame
screen = None
font = None

# Run one set of evolutions
def evolve(genomes):
  global best_fitness, best_genome, generations
  gen_best = 0
  generations += 1

  global screen, font
  done = False

  print " ******** Generation " + str(generations) + " ********"

  players = []
  for genome in genomes:
    players.append(Player(genome))

  # Keep playing until every game is finished
  still_playing = len(players)
  while (still_playing and not done):
    # Pygame close functionality

    for player in players:
      if player.done:
        continue
      else:
        success = player.make_move()
        if (not success or player.game.game_over()):
          player.done = True
          still_playing -= 1
          player.genome.fitness = player.game.score

          # Save the generational best
          if (player.game.score > gen_best):
            gen_best = player.game.score

          # Save the current best genome
          if (player.game.score > best_fitness):
            best_fitness = player.game.score
            best_genome = player.genome
            fitness_history.append(best_fitness)
            # player.game.print_board()
            with open('curr_best_genome_v3', 'wb') as f:
              pickle.dump(best_genome, f)


  print "Best player: " + str(gen_best)

# Initialize display window

config = config.Config('hex_config')
config.report = False
pop = population.Population(config)
pop.run(evolve, 2500)
pop.save_checkpoint("checkpoint.csv")

statistics.save_stats(pop.statistics)
statistics.save_species_count(pop.statistics)
statistics.save_species_fitness(pop.statistics)

print fitness_history