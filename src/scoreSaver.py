# Name: Nayalash Mohammad
# Date: January 20 2020
# File Name: scoreSaver.py
# Description: File containing all the methods to save the score in a txt file

# Module to Read File
import os

# Method to Check to Overwrite File
def isHighScore(score):
    highscore = getScore()
    if(score > highscore):
        return True
    return False

# Method To Read Score From .txt File
def getScore():
    file = open("score.txt", "r")
    if(os.path.getsize("score.txt") < 1):
        return 0
    highscore = int(file.read())
    return highscore

# Method to Set High Score
def setHighScore(highscore):
    file = open("score.txt","w")
    file.write(str(highscore))
    file.close()
