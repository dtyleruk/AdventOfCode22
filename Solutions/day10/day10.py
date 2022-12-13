from Solutions.day10.CPU import CPU

# Read input section
f = open("../../Inputs/day10/part1.dat", "r")
input = f.read().splitlines()

cpu = CPU(input, 20, 40)
cpu.run_instructions()
print("Total interesting signal:", cpu.poll_sum)


cpu2 = CPU(input, 40, 40)

cpu2.run_instructions()
cpu2.render_output()
