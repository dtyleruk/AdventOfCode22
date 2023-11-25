f = open("../../Inputs/day25/part1.dat", "r")
input = f.read().splitlines()


SNAFU_char_converter = {
    '2' : 2,
    '1' : 1,
    '0' : 0,
    '-' : -1,
    '=' : -2
}


def int_to_SNAFU_converter(integer):

    first_digit = calc_starting_point(integer)
    # For each digit, take value away until number is in bound +-2 * 5^(n-1)
    snafu = []
    while first_digit >= 1:
        next_snafu_char = calc_next_digit(integer, first_digit)
        snafu.append(next_snafu_char)
        integer -= first_digit * SNAFU_char_converter[next_snafu_char]
        first_digit /= 5
    return ''.join(snafu)


def calc_next_digit(integer, digit):

    target_range = (-2 * digit/5, 2 * digit/5)

    if target_range[0] <= integer <= target_range[1]:
        return "0"

    if integer < 0:
        if integer + digit >= target_range[0]:
            return "-"
        elif integer + 2*digit >= target_range[0]:
            return "="
        else:
            exit("Broken")

    if integer > 0:
        if integer - digit <= target_range[1]:
            return "1"
        elif integer - 2*digit <= target_range[1]:
            return "2"
        else:
            exit("Broken")

# Determine first digit of integer
def calc_starting_point(integer):
    # x > 2*5^n

    # Haha at how inefficient this is
    n = 0
    x = integer
    while x > 0:
        x -= 2*5**n
        n+=1

    return 5**(n-1)

def SNAFU_to_int_converter(SNAFU):

    digit_mult = 1
    sum = 0
    for char in reversed(SNAFU):
        sum += SNAFU_char_converter[char] * digit_mult
        digit_mult *= 5
    return sum


ints = []
int_sum = 0
for line in input:
    this_int = SNAFU_to_int_converter(line)
    ints.append(this_int)
    int_sum += this_int

print("Integer sum of values is:", int_sum)
print("SNAFU sum of values is:", int_to_SNAFU_converter(int_sum))

# Well it can't do this number from the example, but I got lucky with part 1
print(int_to_SNAFU_converter(314159265))