from rich import console
from rich.prompt import Prompt

import random

class Wordle:
    def __init__(self,wordFile="words_alpha.txt"):
        self.wordList = []
        self.loadFile(wordFile)
        self._randomWord = self.pickRandomWord()
        self.guessResults = None
        self.guessStatus = None

    @property
    def randomWord(self):
        return self._randomWord

    @randomWord.setter
    def randomWord(self, word):
        self._randomWord = word

    def loadFile(self, wordFile):
        with open(wordFile, "r") as wordFile:
            for line in wordFile:
                word = line.strip()
                if len(word) == 5:
                    self.wordList.append(word)
    
    def pickRandomWord(self):
        randomWord = random.choice(self.wordList)
        self.randomWord = randomWord
        return randomWord

    def checkWordGuess(self, guess):
        letterCounter = 0
        letterStatusCount = 0
      
        #Dictionaries can be used to store the status of the guess
        guessDict = {}
        usedLetterCount = {}

        for letter in guess:
            #See how many times each letter appears in the guess
            letterCountInGuess = guess.count(letter)

            #See how many times each letter appears in the randomly chosen word
            letterCountInRandomWord = self.randomWord.count(letter)

            #Stick each letter in a dict to show when it has been used
            if letter not in usedLetterCount:
                usedLetterCount[letter] = 1
            else:
                usedLetterCount[letter] += 1

            #If the letter does not appear in the randomly chosen word, mark it as such
            if letter not in self.randomWord:
                guessDict[letterCounter] = {"letter":letter, "reason":"letterNotInChosenWord", "string":f"[red]{letter}[/red]"}
            else:

                #Now we need to check how many times a letter is in the guess vs the chosen word
                #and act accordingly
                if usedLetterCount[letter] <= letterCountInGuess:
                    if letter == self.randomWord[letterCounter]:
                        guessDict[letterCounter] = {"letter":letter, "reason":"letterCorrectPosition", "string":f"[green]{letter}[/green]"}
                        letterStatusCount += 1
                    else:
                        guessDict[letterCounter] = {"letter":letter, "reason":"letterWrongPosition", "string":f"[yellow]{letter}[/yellow]"}
                elif letterCountInGuess >= letterCountInRandomWord and usedLetterCount[letter] >= letterCountInRandomWord:
                    guessDict[letterCounter] = {"letter":letter, "reason":"letterNotInChosenWord", "string":f"[red]{letter}[/red]"}
            letterCounter += 1
        self.guessResults = guessDict
        self.guessStatus = False
        if letterStatusCount == len(self.randomWord):
            self.guessStatus = True
        return guessDict, self.guessStatus
    
if __name__ == "__main__":
    console = console.Console()
    a = Wordle()

    console.print("*****************************")
    console.print("Welcome to Wordle - have fun!")
    console.print("*****************************")

    carryOn = True
    while carryOn:
        console.print("1) Generate random word")
        console.print("2) Guess the word")
        console.print("3) Quit")
        response = Prompt.ask("")
        if response == "1":
            a.pickRandomWord()
        elif response == "2":
            guessCount = 5
            while guessCount > 0:
                guess = Prompt.ask("Enter your guess")
                if guess.lower() not in a.wordList:
                    console.print("Your guess is not a dictionary word. Try again")
                else:
                    guessResult, guessStatus = a.checkWordGuess(guess.lower())
                    guessString = ""
                    for letterGuess in guessResult:
                        guessString += guessResult[letterGuess]["string"]
                    console.print(guessString)
                    if guessStatus == False:
                        guessCount -= 1
                        if guessCount == 0:
                            console.print("Bad luck - fingers crossed for next time!")
                            console.print(f"The selected word was: [green]{a.randomWord}[/green]")
                    else:
                        console.print("Congratulations - you did it!")
                        guessCount = 0
        elif response == "3" or response.lower() == "q":
            carryOn = False