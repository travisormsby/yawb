import math

# model pattern as a 5-tuple. Incorrect letter is -1, correct letter is 0, correct letter and position is 1

# For each possible guess, check against each possible answer

guessesFile = "guesses.txt"
answersFile = "answers.txt"
testAnswersFile = "testanswers.txt"

with open(guessesFile, "r") as g:
    guesses = [word.rstrip() for word in g.readlines()]
with open(answersFile, "r") as a:
    answers = [word.rstrip() for word in a.readlines()]


def createPattern(guess, answer):
    patternDict = {}
    softMatchGuess = {}
    softMatchAnswer = [l for l in answer]
    # find all exact matches, remove them from the softmatch possibilities
    for index, letter in enumerate(guess):
        if letter == answer[index]:
            patternDict[index] = "M"
            softMatchAnswer.remove(letter)
        # If it is not an exact match, add it to a dictionary of softmatch possibilities. Use letter position as key to preserve position
        else:
            softMatchGuess[index] = letter
    # Loop through the letters in the guess that aren't exact matches, see if they softmatch any letters in answer that aren't exact matches. Remove them from the softmatch possibilities if they softmatch
    for index, letter in softMatchGuess.items():
        if letter in softMatchAnswer:
            patternDict[index] = "S"
            softMatchAnswer.remove(letter)
        # Note if not a softmatch
        else:
            patternDict[index] = "X"
    pattern = "".join([patternDict[k] for k in sorted(patternDict.keys())])
    return pattern


def best_guesser(guesses, answers, answerPattern=None):
    best_expected_information = 0
    for guess in guesses:
        guessDict = {}

        for answer in answers:
            pattern = createPattern(guess, answer)
            if pattern in guessDict:
                guessDict[pattern].append(answer)
            else:
                guessDict[pattern] = [answer]

        # expected information is sum of probability of a pattern times information received from that pattern.
        # information is log2(1/(p(x)))
        guessDictP = {}
        totalWords = len(answers)
        for pattern in guessDict:
            numWordsMatchingPattern = len(guessDict[pattern])
            p_of_pattern = numWordsMatchingPattern / totalWords
            information_of_pattern = math.log(1 / p_of_pattern, 2)
            guessDictP[pattern] = p_of_pattern * information_of_pattern
        expected_information = sum(guessDictP.values())
        # Pick the guess with the highest entropy
        if expected_information > best_expected_information:
            best_expected_information = expected_information
            best_guess = guess
            best_guessDict = guessDict
    if answerPattern:
        return best_guessDict[answerPattern]
    else:
        return best_guess


# Rerun again, with the reduced list of guesses and answers
def guesser(
    guessList, guess="soare", answers=None, interactive=False, answer=None, counter=0
):
    counter += 1
    if interactive:
        guess = input(f"I sugggest you play {guess}. What word did you play? ")
        pattern = input("What pattern did you get? ")
    else:
        pattern = createPattern(guess, answer)
    if pattern == "MMMMM":
        if interactive:
            print(f"Congratulations! You got it in {counter} guesses!")
        return counter
    else:
        answers = best_guesser([guess], answers, pattern)
        if len(answers) == 1:
            counter = guesser(
                guessList, answers[0], answers, interactive, answer, counter
            )
        else:
            guess = best_guesser(guessList, answers)
            counter = guesser(guessList, guess, answers, interactive, answer, counter)
    return counter


def wordlebot_test(guesses, answers):
    guess_distribution = {}
    for answer in answers:
        guessCount = guesser(guesses, answers=answers, answer=answer)
        if guessCount in guess_distribution:
            guess_distribution[guessCount] += 1
        else:
            guess_distribution[guessCount] = 1

    print(guess_distribution)


# uncomment this line to test the bot against the answer list
# wordlebot_test(guesses, answers)

# uncomment this line to run the script interactively to solve today's Wordle
guesser(guesses, answers=answers, interactive=True)
