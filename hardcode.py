board = [
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

def next_loc(loc, direction):
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

# Horizontal
all_rows = []
for i, row in enumerate(board):
  a = []
  for j, pos in enumerate(row):
    a.append([i, j])
  all_rows.append(a)

# Down-right
start_locs = [
  [0,0],[0,1],[0,2],[0,3],[0,4],
  [1,0],[2,0],[3,0],[4,0]
]
for loc in start_locs:
  a = []
  try:
    while (loc[0] >= 0 and loc[1] >= 0):
      a.append(loc)
      loc = next_loc(loc, 'dr')
      board[loc[0]][loc[1]]
  except Exception as e:
    pass
  all_rows.append(a)

# Down-left
start_locs = [
  [0,0],[0,1],[0,2],[0,3],[0,4],
  [1,5],[2,6],[3,7],[4,8]
]
for loc in start_locs:
  a = []
  try:
    while (loc[0] >= 0 and loc[1] >= 0):
      a.append(loc)
      loc = next_loc(loc, 'dl')
      board[loc[0]][loc[1]]
  except Exception as e:
    pass
  all_rows.append(a)

print all_rows