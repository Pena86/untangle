# Untangle
Untangle game with pygame

![alt text](https://img.shields.io/badge/python-2.7-red.svg?v=1 "Python 2.7")
![alt text](https://img.shields.io/badge/python-3.5-blue.svg?v=1 "Python 3.5")
![alt text](https://img.shields.io/badge/PyGame-1.9.3-blue.svg?v=1 "PyGame 1.9.3")

Currently all texts goes to console, so run it from commandline.

------

python untangle.py -h
```
usage: untangle.py [-h] [nodes] [animation] [difficulty]

optional arguments:
  -h, --help  show this help message and exit

  nodes       Ammount of nodes (>3)
  animation   Show puzzle build (bool | n | y)
  difficulty  Puzzle difficulty (easy | normal | hard)
```

python untangle.py 30
```
Keys:
  LMB drag to move a node
  RMB drag to move all nodes
  RMB to mark / unmark a node
  Wheel to zoom
  ESC to exit
  Space to move all nodes closer to each other
Have fun with a game of Untangle
```


![alt text](https://github.com/Pena86/untangle/blob/master/screenshots/Untangle_generate_50.png "Untangle generate")
![alt text](https://github.com/Pena86/untangle/blob/master/screenshots/Untangle_beginning_50.png "Untangle beginning")
![alt text](https://github.com/Pena86/untangle/blob/master/screenshots/Untangle_complete.png "Untangle complete")
