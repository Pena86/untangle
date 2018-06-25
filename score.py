import json

DEFAULT_GAMEMODE = 'normal'
MAX_RANKING_POSITIONS = 10

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
        return self.scores[DEFAULT_GAMEMODE]


    def save(self, score, gamemode, position):
        pass

    
    def checkRanking(self, score, gamemode):
        # the value -1 means that the score did not make a ranking
        position = {'moves': -1, 'time': -1}

        if gamemode not in self.scores:
            return position
        
        # Check if score ranks within moves results
        movesListLength = len(self.scores[gamemode]['moves'])
        if movesListLength <= 0:
            position['moves'] = 0
        else:
            for index in range(0,movesListLength - 1):
                # Check if new score is better than an existing ranked score
                if self.scores[gamemode]['moves'][index] >= score['moves']:
                    # Give a ranking only if the score is within the largest amount of 
                    # ranking positions (default is top 10)
                    position['moves'] = index if index <= MAX_RANKING_POSITIONS else -1
        

        # Check if score ranks within moves results
        timesListLength = len(self.scores[gamemode]['time'])
        if timesListLength <= 0:
            position['time'] = 0
        else:
            for index in range(0,timesListLength - 1):
                # Check if new score is better than an existing ranked score
                if self.scores[gamemode]['time'][index] >= score['time']:
                    # Give a ranking only if the score is within the largest amount of 
                    # ranking positions (default is top 10)
                    position['time'] = index if index <= MAX_RANKING_POSITIONS else -1
        
        return position
