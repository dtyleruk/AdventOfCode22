# Read input section
f = open("../Inputs/day2/part1.dat", "r")
# In each row, the first element is what the opponent plays, the second is what we play
rounds = f.read().splitlines()


# Part one's code, where ABC and XYZ mean opponent's and our Rock Paper Scissors
def determine_round_outcome_score(this_round):

    if (this_round[0] == 'A' and this_round[2] == 'Y') or (this_round[0] == 'B' and this_round[2] == 'Z') or (this_round[0] == 'C' and this_round[2] == 'X'):
        return 6

    if (this_round[0] == 'A' and this_round[2] == 'X') or (this_round[0] == 'B' and this_round[2] == 'Y') or (this_round[0] == 'C' and this_round[2] == 'Z'):
        return 3

    return 0


def score_round(this_round):
    round_outcome_score = determine_round_outcome_score(this_round)

    if this_round[2] == 'X':
        return round_outcome_score + 1

    if this_round[2] == 'Y':
        return round_outcome_score + 2

    if this_round[2] == 'Z':
        return round_outcome_score + 3


total_score = 0

for this_round in rounds:
    total_score += score_round(this_round)

print("Total score following guide in part 1 is: ", total_score)


def determine_score_from_what_we_play(this_round):

    if this_round == 'A Y' or this_round == 'B X' or this_round == 'C Z':
        return 1

    if this_round == 'A Z' or this_round == 'B Y' or this_round == 'C X':
        return 2

    if this_round == 'A X' or this_round == 'B Z' or this_round == 'C Y':
        return 3


def score_round_part_2(this_round):
    our_played_score = determine_score_from_what_we_play(this_round)

    if this_round[2] == 'X':
        return our_played_score + 0

    if this_round[2] == 'Y':
        return our_played_score + 3

    if this_round[2] == 'Z':
        return our_played_score + 6


total_score_part_2 = 0

for this_round in rounds:
    total_score_part_2 += score_round_part_2(this_round)

print("Total score following guide in part 2 is: ", total_score_part_2)
