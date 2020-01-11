import os

def isHighScore(score):
    highscore = getScore()
    if(score > highscore):
        return True
    return False

def getScore():
    file = open("score.txt", "r")
    if(os.path.getsize("score.txt") < 1):
        return 0
    highscore = int(file.read())
    return highscore

def setHighScore(highscore):
    file = open("score.txt","w")
    file.write(str(highscore))
    file.close()
