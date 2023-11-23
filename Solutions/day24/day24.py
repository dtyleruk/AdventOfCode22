from Solutions.day24.Blizzard import Blizzard

f = open("../../Inputs/day24/part1.dat", "r")
input = f.read().splitlines()

blizzard = Blizzard(input)

blizzard.step_down_until_done()
blizzard.step_up_until_done()
blizzard.step_down_until_done()

belb = 1