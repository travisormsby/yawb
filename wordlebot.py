# model pattern as a 5-tuple. Incorrect letter is -1, correct letter is 0, correct letter and position is 1

# For each possible guess, check against each possible answer

guessesFile = "testguesses.txt"
answersFile = "testanswers.txt"

with open(guessesFile, "r") as g:
    guesses = [word.rstrip() for word in g.readlines()]
with open(answersFile, "r") as a:
    answers = [word.rstrip() for word in a.readlines()]
for guess in guesses:
    for answer in answers:
        pattern = []
        for index, letter in enumerate(guess):
            if letter == answer[index]:
                pattern.append(1)
            elif letter in answer:
                pattern.append(0)
            else:
                pattern.append(-1)
        print(guess, answer, pattern)
        # break
    # break


# Create a dictionary where the keys are all possible patterns, values are a 2-tuple of 1) a tuple of all possible solutions and 2) a tuple of all possible guesses with that pattern for a given guess

# Pick the guess with the highest entropy

# Rerun again, with the reduced list of guesses and answers
