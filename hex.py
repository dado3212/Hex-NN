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

    loc = self.locs[int((outputs[0] - 1e-16) * (len(self.locs)))]
    piece = self.game.pieces.pop(int((outputs[1] - 1e-16) * 3))

    self.game.add_piece()

    # Check if it's a valid move
    if (self.game.board.can_place_piece(piece, loc)):
      self.game.make_move(piece, loc)
      return True
    else:
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
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True 
        break

    # Game display code
    screen.fill(pygame.Color(255, 255, 255, 255))
    pygame.draw.rect(screen, (20, 50, 100), [10, 70, 500, 210])
    screen.blit(font.render("ALIVE: " + str(still_playing), 2, (255,255,255)), (20, 80))
    #screen.blit(font.render("TIME: " + str(round(time.time() - lifespanStart, 2)) + " s", 2, (255,255,255)), (20, 120))
    screen.blit(font.render("GENERATION: " + str(generations), 2, (255,255,255)), (20, 160))
    screen.blit(font.render("CURRENT BEST SCORE: " + str(best_fitness) + " pts", 2, (255,255,255)), (20, 200))
    #screen.blit(font.render("CURRENT BEST FITNESS: " + str(currentBestFitness), 2, (255,255,255)), (20, 240))

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
            player.game.print_board()
            with open('curr_best_genome_4', 'wb') as f:
              pickle.dump(best_genome, f)

    pygame.display.update()
    pygame.display.flip()

  print "Best player: " + str(gen_best)

# Initialize display window
pygame.init()
font = pygame.font.SysFont("Arial", 12)
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Hex Player')
pygame.display.update()

config = config.Config('hex_config')
config.report = False
pop = population.Population(config)
pop.run(evolve, 10000)
pop.save_checkpoint("checkpoint.csv")

statistics.save_stats(pop.statistics)
statistics.save_species_count(pop.statistics)
statistics.save_species_fitness(pop.statistics)

print fitness_history