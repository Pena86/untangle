import json

DEFAULTGAMEMODE = 'normal'

class Score:
    scores = {
        'easy': {
            'moves':[],
            'time':[]
        },
        'normal': {
            'moves':[],
            'time':[]
        },
        'hard': {
            'moves':[],
            'time':[]
        }
    }


    def __init__(self):
        pass


    def getTopScores(self, gamemode):
        if gamemode in self.scores:
            return self.scores[gamemode]
        return self.scores[DEFAULTGAMEMODE]

    
    def saveScore(self, score, gamemode):
        position = {}

        if gamemode not in self.scores:
            return {'moves': -1, 'time': -1}
        
        movesListLength = len(self.scores[gamemode]['moves'])
        if movesListLength <= 0:
            self.scores[gamemode]['moves'].insert(0,score['moves'])
            position['moves'] = 0
        else:
            for index in range(0,movesListLength):
                if self.scores[gamemode]['moves'][index] >= score['moves']:
                    self.scores[gamemode]['moves'].insert(index,score['moves'])