from datetime import date, datetime
import json

SAVE_FILE_NAME = 'saves.json'
DEFAULT_GAMEMODE = 'normal'
MAX_RANKING_POSITIONS = 10

HIGH_SCORES_TEMPLATE = {
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


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code
        Solution to serialising high score 'occurred' values.
        From:
        https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def openSaveFile():
    try:
        with open(SAVE_FILE_NAME) as savefile:
            data = json.load(savefile)
            return data
    except FileNotFoundError:
        with open(SAVE_FILE_NAME, 'w') as savefile:
            json.dump(HIGH_SCORES_TEMPLATE, savefile)
            return HIGH_SCORES_TEMPLATE


def getTopScores(gamemode):
    highscores = openSaveFile()
    if gamemode in highscores:
        return highscores[gamemode]
    return highscores[DEFAULT_GAMEMODE]


def save(score, gamemode, position, name):
    highscores = openSaveFile()

    if gamemode not in highscores:
        return
    
    if position['moves'] >= 0:
        # Moves high score
        highScore = {
            'name': name,
            'score': score['moves'],
            'occurred': datetime.now()
        }
        highscores[gamemode]['moves'].insert(position['moves'], highScore)
    
    if position['time'] >= 0:
        # Moves high score
        highScore = {
            'name': name,
            'score': score['time'],
            'occurred': datetime.now()
        }
        highscores[gamemode]['time'].insert(position['time'], highScore)
    
    # truncate to max ranking count
    if len(highscores[gamemode]['moves']) >= MAX_RANKING_POSITIONS:
        highscores[gamemode]['moves'] = highscores[gamemode]['moves'][:MAX_RANKING_POSITIONS]
    
    if len(highscores[gamemode]['time']) >= MAX_RANKING_POSITIONS:
        highscores[gamemode]['time'] = highscores[gamemode]['time'][:MAX_RANKING_POSITIONS]

    with open(SAVE_FILE_NAME, 'w') as savefile:
        json.dump(highscores, savefile, default=json_serial)

    
def checkRanking(score, gamemode):
    highscores = openSaveFile()

    # the value -1 means that the score did not make a ranking
    position = {'moves': -1, 'time': -1}

    if gamemode not in highscores:
        return position
        
    # Check if score ranks within moves results
    movesListLength = len(highscores[gamemode]['moves'])
    if movesListLength <= 0:
        position['moves'] = 0
    else:
        for index in range(0,MAX_RANKING_POSITIONS):
            if index < movesListLength:
                # Check if new score is better than an existing ranked score
                if highscores[gamemode]['moves'][index]['score'] >= score['moves']:
                    # Give a ranking only if the score is within the largest amount of 
                    # ranking positions (default is top 10)
                    position['moves'] = index if index < MAX_RANKING_POSITIONS else -1
                    break
            else:
                position['moves'] = index
                break
        
    # Check if score ranks within time results
    timeListLength = len(highscores[gamemode]['time'])
    if timeListLength <= 0:
        position['time'] = 0
    else:
        for index in range(0,MAX_RANKING_POSITIONS):
            if index < timeListLength:
                # Check if new score is better than an existing ranked score
                if highscores[gamemode]['time'][index]['score'] >= score['time']:
                    # Give a ranking only if the score is within the largest amount of 
                    # ranking positions (default is top 10)
                    position['time'] = index if index < MAX_RANKING_POSITIONS else -1
                    break
            else:
                position['time'] = index
                break
        
    return position

