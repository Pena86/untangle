#!/usr/bin/env python3

from __future__ import print_function
import pygame
import random
import score

import math
import sys


class det:
# ---------------------------------------------------------------------
# A python implementation of:
# https://www.cdn.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
#
# A -C++- python program to check if two given line segments intersect
# ---------------------------------------------------------------------

    #struct Point -> pygame Rect

    # import pygame

    # Given three colinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    @staticmethod
    def onSegment(p, q, r):
        if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
            return True

        return False

    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are colinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise
    @staticmethod
    def orientation(p, q, r):
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/
        # for details of below formula.
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        if (val == 0): return 0  # colinear

        return 1 if (val > 0) else 2 # clock or counterclock wise

    # The main function that returns true if line segment 'p1q1'
    # and 'p2q2' intersect
    @staticmethod
    def doIntersect(p1, q1, p2, q2):
        # Find the four orientations needed for general and
        # special cases
        o1 = det.orientation(p1, q1, p2);
        o2 = det.orientation(p1, q1, q2);
        o3 = det.orientation(p2, q2, p1);
        o4 = det.orientation(p2, q2, q1);

        # General case
        if (o1 != o2 and o3 != o4):
            return True

        # Special Cases
        # p1, q1 and p2 are colinear and p2 lies on segment p1q1
        if (o1 == 0 and det.onSegment(p1, p2, q1)): return True

        # p1, q1 and q2 are colinear and q2 lies on segment p1q1
        if (o2 == 0 and det.onSegment(p1, q2, q1)): return True

        # p2, q2 and p1 are colinear and p1 lies on segment p2q2
        if (o3 == 0 and det.onSegment(p2, p1, q2)): return True

         # p2, q2 and q1 are colinear and q1 lies on segment p2q2
        if (o4 == 0 and det.onSegment(p2, q1, q2)): return True

        return False # Doesn't fall in any of the above cases

# ---------------------------------------------------------------------



# https://en.wikipedia.org/wiki/X11_color_names (not all apply)
# pygame.color.Color('Black')

SCREEN_SIZES = {
    'easy':{'width':600, 'height':400},
    'normal':{'width':800, 'height':600},
    'hard':{'width':1280, 'height':1024}
}

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

NODES = {
    'easy':10,
    'normal':20,
    'hard':50
}
DEFAULTNODES = 20
DEFAULTANIMAT = True
DEFAULTDIFFICULTY = 'normal'

# Game state constants:
START = 1
GENERATE = 2
RUN = 3
PAUSE = 4
END = 5

class Game:
    name = 'entangled'

    def __init__(self, clock = None, nodes = None, anim = DEFAULTANIMAT, difficulty = DEFAULTDIFFICULTY):
        if nodes is None:
            if difficulty not in NODES:
                difficulty = DEFAULTDIFFICULTY
            nodes = NODES[difficulty]
            self.gamedifficulty = difficulty
        
        self.rectsAmmount = nodes


        self.blockSize = 14
        self.gridSize = 1 # self.blockSize /2 +1 #rougher grid makes it a cluncky to use

        self.showBuildAnimation = anim # show placing of the nodes at beginning

        self.colorPalette = {
            'intersecting' : pygame.color.Color('Brown'),
            'nonintersecting' : pygame.color.Color('Lime Green'),
            'selected' : pygame.color.Color('White'),
            'selectedConnecting' : pygame.color.Color('Blue'),
            'marked' : pygame.color.Color('Blue'),
            'markedConnecting' : pygame.color.Color('White'),
            'background' : pygame.color.Color('Dim Gray'),
            'line' : pygame.color.Color('Black'),
        }

        self.selected = None
        self.mark = None
        self.tileMoved = True
        self.moves = 0
        self.untangledCount = 0
        self.gameState = START

        self.clock = clock
        self.gameRunning = True
        self.gameStartTime = pygame.time.get_ticks()
        self.gameduration = '0:00'

        self.selfSolveCountdown = 0 # count of rounds to move all nodes closer together
        self.selfSolveOrder = []
        self.selfSolveIndex = 0

        self.placeNodes = 3 # node placement state at beginning
        self.placeCountdown = 25 # timer before suffle nodes

        # Create nodes (rects)
        self.rects = []
        for x in range(self.rectsAmmount):
            self.rects.append( [pygame.Rect(self.myRound(20), self.myRound(20),
                        self.blockSize, self.blockSize),
                        [], [], self.colorPalette['intersecting']
            ])

        for x in range(len(self.rects)):
            self.selfSolveOrder.append(x)
        random.shuffle(self.selfSolveOrder)

        print("\nKeys:\n" \
                "  LMB drag to move a node\n" \
                "  RMB to mark / unmark a node\n" \
                "  ESC to exit\n" \
                "  Space to move all nodes closer to each other\n" \
                "Have fun with a game of Untangle\n")

    def getRunningState(self):
        return self.gameRunning

    def updateGameDuration(self):
        self.gameduration = "{:d}:{:02d}".format(
                int(((pygame.time.get_ticks() - self.gameStartTime) / 1000) / 60), 
                int(((pygame.time.get_ticks() - self.gameStartTime) / 1000) % 60))

    def printGameStats(self):
        if self.gameState == RUN:
            self.updateGameDuration()
            print ("Untangled {0}/{1} in {2} with {3} moves".format(self.untangledCount, len(self.rects), self.gameduration, self.moves), end = '\r')
    

    def checkRanking(self):
        gamescore = {'moves': self.moves, 'time': self.gameduration}
        rank = score.checkRanking(gamescore, self.gamedifficulty)
        if rank['moves'] >= 0 or rank['time'] >= 0:
            # Ranked so get name
            name = input("Congratulations! You have a new high score! Please enter your name: ")
            score.save(gamescore, self.gamedifficulty, rank, name)
        self.printRankings(score.getTopScores(self.gamedifficulty))


    def printRankings(self, rankings):
        print ("\nHigh Scores for {0} mode".format(self.gamedifficulty, end = '\n'))
        print ("-- Moves --\n")
        print ("Rank -- Moves - Name -- Time")
        moves_length = len(rankings['moves'])
        for index in range(0, len(rankings['moves'])):
            print ("{0} -- {1} - {2} -- {3}".format(index + 1, rankings['moves'][index]['score'], 
            rankings['moves'][index]['name'], rankings['moves'][index]['occurred'], end = '\n'))
        
        print ("-- Time --\n")
        print ("Rank -- Time - Name -- Time")
        for index in range(0, len(rankings['time'])):
            print ("{0} -- {1} - {2} -- {3}".format(index + 1, rankings['time'][index]['score'], 
            rankings['time'][index]['name'], rankings['time'][index]['occurred'], end = '\n'))


    def updateUntangledCount(self):
        if self.gameState == RUN:
            self.moves += 1
            count = 0
            for r in self.rects:
                if r[3] == self.colorPalette['nonintersecting']:
                    count += 1
            self.untangledCount = count

    def createCirclePoints(self, points, radius, center = (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))):
        '''
        An algorithm to create positions to points in circle raduis
        Python implementation of:
        https://stackoverflow.com/questions/5300938/calculating-the-position-of-points-in-a-circle
        '''
        positions = []

        slice = 2 * math.pi / points
        for i in range(0, int(points)):
            angle = slice * i
            x = self.myRound(int(center[0] + radius * math.cos(angle)))
            y = self.myRound(int(center[1] + radius * math.sin(angle)))
            positions.append((x,y))
        return positions

    def myRound(self, x):
        '''
        https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
        To place nodes to a certain grid
        '''
        return int(self.gridSize * round(float(x)/self.gridSize))

    def testSegmentIntercet(self, i, c):
        collides = False
        for j in range(0, len(self.rects)): # other nodes...
            for d in self.rects[j][1] + self.rects[j][2]: #... ande their connections
                #print (i, c, j, d)
                if j == i or j == c or d == i or d == c: # but not the node or its connections itself
                    pass
                elif det.doIntersect(self.rects[i][0], self.rects[c][0], self.rects[j][0], self.rects[d][0]):
                    return True
                    #print ("collides")
                    break
            if collides:
                break
        return False

    def placeOnCircle(self, rects):
        # Create node positions to circle and apply
        circlePositions = self.createCirclePoints(len(rects), 
                    min(len(rects)*5, int(SCREEN_WIDTH/2) - self.blockSize , 
                    int(SCREEN_HEIGHT/2) - self.blockSize))
        random.shuffle(circlePositions)
        for i, p in enumerate(circlePositions):
            rects[i][0].center = p

    def performSelfSolveAction(self):
        nodeToMove = self.selfSolveOrder[self.selfSolveIndex]
        x = self.rects[nodeToMove][0].x
        y = self.rects[nodeToMove][0].y
        for r in self.rects[nodeToMove][1] + self.rects[nodeToMove][2]:
            x += self.rects[r][0].x
            y += self.rects[r][0].y
        total = 1 + len(self.rects[nodeToMove][1] + self.rects[nodeToMove][2])
        self.rects[nodeToMove][0].topleft = (int(x/total), int(y/total))

        self.selfSolveIndex += 1
        if self.selfSolveIndex == len (self.selfSolveOrder):
            self.selfSolveIndex = 0
            self.selfSolveCountdown -= 1
            random.shuffle(self.selfSolveOrder)
        self.tileMoved = nodeToMove


    def updateAllNodesUntangleSatatus(self):
        self.tileMoved = False
        for i in range(0, len(self.rects)): # a node ...
            self.rects[i][3] = self.colorPalette['nonintersecting']
            for c in self.rects[i][1] + self.rects[i][2]: # ...has connections to
                if self.testSegmentIntercet(i, c):
                    self.rects[i][3] = self.colorPalette['intersecting']
                    # print ("ALL collides", i, c)
                    break

# ---------------------------------------------------------------------
#
# node placement functions
#
# ---------------------------------------------------------------------

    def createRandomConnections(self):
        # Just for dev purposes, no animation
        # Create random connections between nodes, does not check if its solvable aka untangleable
        # works with low node counts like max 10
        once = True
        while self.placeNodes and (not self.showBuildAnimation or once):
            self.placeNodes = 0
            for i, r in enumerate(self.rects):
                r[0].topleft = (random.randint(0, SCREEN_WIDTH - self.blockSize),
                                random.randint(0, SCREEN_HEIGHT - self.blockSize))
                connections = 2
                while connections:
                    connection = random.randint(0, len(self.rects)-1)
                    if connection != i and not i in self.rects[connection][1]:
                        r[1].append(connection)
                        self.rects[connection][2].append(i)
                        connections -= 1
            # self.placeOnCircle(self.rects)
            self.updateAllNodesUntangleSatatus()
            self.gameState = RUN

    def buildNodesConnection(self, rects):
        # Just for dev purposes
        # Place nodes and create valid connections between
        # works actually quite ok, but with larger node counts, produces quite repeating pattern
        groupMembers = 7
        if not hasattr(self, 'placeCount'):
            self.placeCount = 0
        once = True
        while self.placeNodes == 3 and (not self.showBuildAnimation or once):
            once = False
            self.gameState = GENERATE
            #for i in range(0, int(len(rects)/groupMembers)):
            #    for j in range(0, groupMembers):
            i = int(self.placeCount/groupMembers)
            j = int(self.placeCount%groupMembers)
            #print (i, j)
            currNode = i*groupMembers+j
            if j == 0 and i > 0:
                rects[currNode][1].append(currNode-groupMembers)
                rects[currNode-groupMembers][2].append(currNode)
            if j > 0:
                rects[currNode][1].append(currNode-1)
                rects[currNode-1][2].append(currNode)
            if j > 1:
                rects[currNode][1].append(currNode-2)
                rects[currNode-2][2].append(currNode)
            if j == groupMembers-1 and i > 0:
                rects[currNode][1].append(currNode-groupMembers)
                rects[currNode-groupMembers][2].append(currNode)

            rects[currNode][0].center = (40 + i*80 + self.placeCount%2*20 + random.randint(-10,10),
                    40 + j*40 + random.randint(-10,10))
            self.placeCount += 1
            if self.placeCount >= len(rects):
                self.placeNodes = 2
                if j != 0:
                    tries = groupMembers*3
                    connections = 2
                    while connections and tries:
                        connection = random.randint(max(0, currNode - int(groupMembers*1.5)), currNode-2)
                        if connection != currNode and not connection in rects[currNode][1] and \
                                not self.testSegmentIntercet(currNode, connection):
                            rects[currNode][1].append(connection)
                            rects[connection][2].append(currNode)
                            connections -= 1
                        tries -= 1
                        # print (currNode, connection, tries, connections)
                '''
                print (rects[currNode])
                for n in rects[currNode][1] + rects[currNode][2]:
                    print (n, rects[n])
                '''
        while self.placeNodes == 2 and (not self.showBuildAnimation or once):
            once = False
            for currNode in range(0, len(rects)):
                tries = groupMembers*2
                connections = 2
                while connections and tries:
                    connection = random.randint(0, len(rects)-1)
                    if connection != currNode and not connection in rects[currNode][1] and \
                            not self.testSegmentIntercet(currNode, connection):
                        rects[currNode][1].append(connection)
                        rects[connection][2].append(currNode)
                        connections -= 1
                    tries -= 1
            self.placeNodes = 1

        while self.placeNodes == 1 and (not self.showBuildAnimation or once):
            once = False
            self.placeCountdown -= 1
            if self.placeCountdown <= 0:
                self.placeOnCircle(self.rects)
                self.placeNodes = 0
                self.tileMoved = True
                self.selected = None
                self.mark = None
                self.updateAllNodesUntangleSatatus()
                self.gameState = RUN

    def buildPuzzleConnection(self, rects):
        # Place nodes and create valid connections between
        # Should create an algorithm that makes nice puzzles
        # Some work should sill be done...
        once = True
        while self.placeNodes == 3 and (not self.showBuildAnimation or once):
            once = False
            self.gameState = GENERATE

            layerDiameter = 50
            layerDiameterIncrease = 50
            if len(rects) < 6:
                layers = 2
                ammount = 1
            elif len(rects) < 12:
                layers = 2
                ammount = 3
            elif len(rects) < 20:
                layers = 2
                ammount = 5
            else:
                layers = 3 + len(rects) / 50
                ammount = len(rects)/layers
                layerDiameterIncrease = min((SCREEN_HEIGHT /2 - 2*self.blockSize) / (len(rects) / ammount), 50)

            if not hasattr(self, 'placeCount'):
                self.placeCount = 0
            if not hasattr(self, 'curLayer'):
                self.curLayer = 0
            if not hasattr(self, 'firsNodeOfLayer'):
                self.firsNodeOfLayer = 0

            if not hasattr(self, 'positionList') or not self.positionList: # create positions for nodes, do only once
                self.positionList = self.createCirclePoints(
                        ammount if self.curLayer < layers -1 else len(rects) - self.placeCount,
                        layerDiameter + layerDiameterIncrease * self.curLayer)
                # print (self.positionList)
                self.firsNodePrevLayer = self.firsNodeOfLayer
                self.firsNodeOfLayer = self.placeCount

            rects[self.placeCount][0].center = self.positionList.pop() # place node

            # create connection to previous
            if not self.firsNodeOfLayer == self.placeCount:
                rects[self.placeCount][1].append(self.placeCount-1)
                rects[self.placeCount-1][2].append(self.placeCount)
            if len(self.positionList) == 0:
                rects[self.placeCount][1].append(self.firsNodeOfLayer)
                rects[self.firsNodeOfLayer][2].append(self.placeCount)
                self.curLayer += 1

            # create some ranfom connections
            if self.curLayer == 0:
                tries = 2
            else:
                tries = max(self.curLayer *5, 15)
            connections = 2
            while connections and tries:
                connection = random.randint(self.firsNodePrevLayer, self.placeCount)
                if connection != self.placeCount and not connection in rects[self.placeCount][1] and \
                        not self.testSegmentIntercet(self.placeCount, connection):
                    rects[self.placeCount][1].append(connection)
                    rects[connection][2].append(self.placeCount)
                    connections -= 1
                tries -= 1
            #print (self.placeCount, len(self.positionList), self.curLayer, rects[self.placeCount][1] + rects[self.placeCount][2])

            self.placeCount += 1
            if self.placeCount >= len(rects): # when all done, clean up and move on
                self.placeNodes = 1
                #print (dir(self))
                del(self.curLayer)
                del(self.firsNodeOfLayer)
                del(self.firsNodePrevLayer)
                del(self.positionList)
                del(self.placeCount)
                #print (dir(self))

        # delay before suffling the nodes
        while self.placeNodes == 1 and (not self.showBuildAnimation or once):
            once = False
            self.placeCountdown -= 1
            if self.placeCountdown <= 0:
                self.placeOnCircle(self.rects)
                self.placeNodes = 0
                self.tileMoved = True
                self.selected = None
                self.mark = None
                self.updateAllNodesUntangleSatatus()
                self.gameState = RUN

# ---------------------------------------------------------------------

    def gameEvent(self, event):
        if event.type == pygame.QUIT:
            self.gameRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.gameRunning = False

            if event.key == pygame.K_SPACE:
                if self.selfSolveCountdown:
                    self.selfSolveCountdown = 0
                else:
                    self.selfSolveCountdown = 1

# ---------------------------------------------------------------------
#
# Mouse drag template is from:
#
# pygame (simple) template - by furas
#
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
#
# http://pastebin.com/9VdUEPXi
#
# __author__  = 'Bartlomiej "furas" Burek'
# __webpage__ = 'http://blog.furas.pl'
#
# ---------------------------------------------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # select
                for i, r in enumerate(self.rects):
                    # Pythagoras a^2 + b^2 = c^2
                    dx = r[0].centerx - event.pos[0] # a
                    dy = r[0].centery - event.pos[1] # b
                    distance_square = dx**2 + dy**2 # c^2

                    if distance_square <= int(self.blockSize/2)**2: # c^2 <= radius^2
                        self.selected = i
                        self.selected_offset_x = r[0].x - event.pos[0] # makes the cursor drag at current position
                        self.selected_offset_y = r[0].y - event.pos[1] # not at the top left corner
                        #print ("selected:", i, r[1], r[2])

            if event.button == 3: # mark
                found = False
                for i, r in enumerate(self.rects):
                    # Pythagoras a^2 + b^2 = c^2
                    dx = r[0].centerx - event.pos[0] # a
                    dy = r[0].centery - event.pos[1] # b
                    distance_square = dx**2 + dy**2 # c^2

                    if distance_square <= int(self.blockSize/2)**2: # c^2 <= radius^2
                        if self.mark == i:
                            self.mark = None
                        else:
                            self.mark = i
                        found = True
                        break
                if not found:
                    self.mark = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.selected is not None:
                self.rects[self.selected][0].x = self.myRound(self.rects[self.selected][0].x)
                self.rects[self.selected][0].y = self.myRound(self.rects[self.selected][0].y)
                self.tileMoved = self.selected
                self.selected = None

        elif event.type == pygame.MOUSEMOTION:
            if self.selected is not None: # selected can be `0` so `is not None` is required
                # move object
                self.rects[self.selected][0].x = self.myRound(event.pos[0] + self.selected_offset_x)
                self.rects[self.selected][0].y = self.myRound(event.pos[1] + self.selected_offset_y)

    def gameLoop(self):
        ##### select node placement function:
        #self.createRandomConnections() # pure random
        #self.buildNodesConnection(self.rects) # some pattern
        self.buildPuzzleConnection(self.rects) # should do better
        ##### end of select node placement function

        if self.selfSolveCountdown: # move nodes closer to others they connect to
            self.performSelfSolveAction()

        if self.tileMoved is not False: # test only moved node (can be 0) ...
            i = self.tileMoved # this node
            self.tileMoved = False
            self.rects[i][3] = self.colorPalette['nonintersecting']
            for c in self.rects[i][1] + self.rects[i][2]: # ...has connections to
                # print (i, c)
                for j in range(0, len(self.rects)): # other nodes...
                    for d in self.rects[j][1] + self.rects[j][2]: #... ande their connections
                        # print (i, c, j, d)
                        if j == i or j == c or d == i or d == c: # but not the node or its connections itself
                            # print ("one of own")
                            pass

                        elif det.doIntersect(self.rects[i][0], self.rects[c][0], self.rects[j][0], self.rects[d][0]): # test if collides
                            self.rects[i][3] = self.colorPalette['intersecting']
                            self.rects[c][3] = self.colorPalette['intersecting']
                            self.rects[j][3] = self.colorPalette['intersecting']
                            self.rects[d][3] = self.colorPalette['intersecting']
                            # print ("ONLY collides", i, c)

            # test if previously intersected nodes still intersect
            for i in range(0, len(self.rects)): # a node ...
                collides = False
                if self.rects[i][3] == self.colorPalette['intersecting']:
                    for c in self.rects[i][1] + self.rects[i][2]: # ...has connections to
                        if self.testSegmentIntercet(i, c):
                            collides = True
                            # print ("PREV collides", i, c)
                            break
                if collides:
                    self.rects[i][3] = self.colorPalette['intersecting']
                else:
                    self.rects[i][3] = self.colorPalette['nonintersecting']
            self.updateUntangledCount()

        # Test for game complete
        if self.untangledCount >= len(self.rects) and self.gameState == RUN:
            self.printGameStats()
            self.gameState = END
            self.checkRanking()
            print("\nGame complete! Restart for new game of Untangle")
        else:
            self.printGameStats()

    def draw(self, screen):
        screen.fill(self.colorPalette['background'])

        # draw lines
        for r in self.rects:
            for l in r[1]:
                pygame.draw.line(screen, self.colorPalette['line'], r[0].center, self.rects[l][0].center, 2)

        # draw rects aka. nodes
        for i, r in enumerate(self.rects):
            pygame.draw.circle(screen, r[3], r[0].center, int(self.blockSize/2))
            #textToScreen(screen, i, r[0].x, r[0].y, 20, self.colorPalette['line'])

        # draw selected in its color
        if self.selected is not None:
            pygame.draw.circle(screen, self.colorPalette['selected'], self.rects[self.selected][0].center, int(self.blockSize/2))
            for r in self.rects[self.selected][1] + self.rects[self.selected][2]:
                pygame.draw.circle(screen, self.colorPalette['selectedConnecting'], self.rects[r][0].center, int(self.blockSize/2))

        # draw marked with a ring
        if self.mark is not None:
            pygame.draw.circle(screen, self.colorPalette['marked'], self.rects[self.mark][0].center, int(self.blockSize/2), 2)
            for r in self.rects[self.mark][1] + self.rects[self.mark][2]:
                pygame.draw.circle(screen, self.colorPalette['markedConnecting'], self.rects[r][0].center, int(self.blockSize/2), 2)

if __name__ == "__main__" :
    # --- command line arguments parse
    # Yes, i could use the argparse -package, but choose to build the parser myself

    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print ('usage: untangle.py [-h] [nodes] [animation] [difficulty]\n\n' \
                'optional arguments:\n' \
                '  -h, --help  show this help message and exit\n\n' \
                '  nodes       Ammount of nodes (>3)\n' \
                '  animation   Show puzzle build (bool | n | y)\n' \
                '  difficulty  Puzzle difficulty (easy | normal | hard)')
        exit()

    nodes = None
    for a in sys.argv[1:]: # search first int for nodecount
        try:
            if int(a) > 3:
                nodes = int(a)
                break
        except:
            pass

    anim = DEFAULTANIMAT
    if any(word in sys.argv[1:] for word in ['n', 'N', 'no', 'No', 'False', 'false']):
        # search for placement animation hide code
        anim = False

    difficulty = DEFAULTDIFFICULTY
    for word in sys.argv[1:]:
        if str(word).lower() in ['easy','normal','hard']:
            difficulty = str(word).lower()
            break
    SCREEN_WIDTH = SCREEN_SIZES[difficulty]['width']
    SCREEN_HEIGHT = SCREEN_SIZES[difficulty]['height']
    # --- command line arguments parse

    pygame.init()
    pygame.display.set_caption('Untangle')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    game = Game(clock, nodes, anim, difficulty)
    running = True
    try:
        while( running and game.getRunningState() ):
            for event in pygame.event.get():
                game.gameEvent(event)

            game.gameLoop()
            game.draw(screen)
            pygame.display.update()
            clock.tick(25)

    except KeyboardInterrupt:
        running = False
    print("\nGoodbye\n")
    pygame.quit()
