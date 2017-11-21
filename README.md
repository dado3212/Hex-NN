# Hex-NN
A Pythonic search implementation of Hex FRVR

Timing improvements: (should be using points/sec as the general metric) (30 games unless specified)

- Made all of the moves (20 games):
* 4s
* No better breakdown

- Duplication of board:
* 9,155 points
* 4,980 points/sec

- Keeping track of available space:
* 15,266 points
* 6,013 points/sec

- Removing absolutely useless key
* 14,879 points
* 6,706 points/sec

- Hardcoding board length
* 15,652 points
* 6,957 points/sec

- Some bit hacks