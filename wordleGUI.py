from guizero import PushButton, TextBox, App, CheckBox
from wordle import Wordle

if __name__ == "__main__":

    #Variables
    app = App(layout="grid")
    app.text_size = 20
    a = Wordle()

    guessBoxes = []
    guessChecks = []
    guessCount = 0
    correctGuess = False

    # If the game is finished, without correct guesses, display a message
    def finishGame():
        global guessCount
        if guessCount == 6 and correctGuess == False:
            guessCount += 1
            app.info("info", f"Bad luck. The word was {a.randomWord}")

    # When the New game button is pressed, reset the game
    def newGame():

        a.pickRandomWord()
        resetGame()

    # Reset the game by wiping text boxes and resetting variables
    def resetGame():
        # Reset the game
        global guessCount
        global correctGuess

        guessCount = 0
        correctGuess = False
        checkCount = 0

        for row in guessBoxes:
            for guessBox in row:
                guessBox.value = ""
                guessBox.bg = "white"    
        
        for checkBox in guessChecks:
            if checkCount == 0:
                checkBox.value = True
            else:
                checkBox.value = False
            checkCount += 1

    # Check if the guess is correct or not
    def checkGuess():
        global guessCount

        if guessCount < 6:

            guess = ""
            for guessBox in guessBoxes[guessCount]:
                guess += guessBox.value

            if guess == "" or len(guess) != 5:
                app.info("info", "Please enter a guess - 1 letter per textbox")
                return
            
            if guess not in a.wordList:
                app.info("info", "Please enter a dictionary word")
                return
            
            guessResult, guessStatus = a.checkWordGuess(guess)
            if guessStatus:
                for guessBox in guessBoxes[guessCount]:
                    guessBox.bg="green"

                completed = app.yesno("Congratulations!", f"You guessed it in {guessCount+1}. Play again?")
                if completed:
                    resetGame()
            else:
                colCount = 0
                for guessLetter in guessResult:
                    letterDict = guessResult[guessLetter]
                    if letterDict["reason"] == "letterCorrectPosition":
                        guessBoxes[guessCount][colCount].bg = "green"
                    elif letterDict["reason"] == "letterNotInChosenWord":
                        guessBoxes[guessCount][colCount].bg = "red"
                    elif letterDict["reason"] == "letterWrongPosition":
                        guessBoxes[guessCount][colCount].bg = "orange"

                    colCount += 1
                guessCount += 1
            guessChecks[guessCount- 1].value = False

            if guessCount < 6:
                guessChecks[guessCount].value = True

    # Create items for the GUI and link to functions
    generateWordButton = PushButton(app, text="New Game", width="fill", command=newGame, grid=[0,0, 6, 2])
    checkGuess = PushButton(app, text="Check Guess", width="fill", command=checkGuess, grid=[6,0,6,1])

    app.repeat(10, finishGame)

    # Now add some text boxes for the guesses
    for rowCount in range(2,14,2):
        row = []
        for colCount in range(0,12,2):
            if colCount == 0:
                 pass
                 guessChecks.append(CheckBox(app, grid=[0, rowCount, 2, 2]))
            else:
                row.append(TextBox(app, width=4,grid=[colCount, rowCount, 2, 2]))
        guessBoxes.append(row)
        rowCount += 1

        guessChecks[0].value = True
    app.display()