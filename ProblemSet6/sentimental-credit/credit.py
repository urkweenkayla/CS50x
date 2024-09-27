# from cs50 import get_int
from cs50 import get_string
import sys

# Check for valid length, valid card type determine card type
while True:
    card_number = get_string("Number: ")
    card_number_len = len(card_number)
    first_digits = card_number[0] + card_number[1]
    valid_first_digits = ["34", "37", "40", "41", "42", "43", "44",
                          "45", "46", "47", "48", "49", "51", "52", "53", "54", "55"]
    valid_len = [13, 15, 16]
    if first_digits not in valid_first_digits:
        print("INVALID")
        sys.exit(1)
    elif card_number_len in valid_len:
        break
    else:
        print("INVALID")
        sys.exit(2)

# Implement Luhn's algorithm
# Total, an array for numbers to multiply by two, and array for remaining numbers
total = 0
times_two = []
remainders = []

# Add the first number of the card to the remainders if card number is odd
if card_number_len % 2 != 0:
    remainders.append(int(card_number[0]))

# Iterate through card numbers and separate into two arrays
for i in range(card_number_len - 2, -1, -2):
    times_two.append(int(card_number[i])*2)
    remainders.append(int(card_number[i + 1]))

# Sum of numbers (as digits) multiplied by two
for number in times_two:
    if number <= 9:
        total += number
    # If number is two digits, add two digits together then add to total
    elif number >= 10:
        n = str(number)
        numbers = int(n[0]) + int(n[1])
        total += numbers

# Add numbers in remainders array to total
for number in remainders:
    total += number

# If total ends in 0, determine valid card type, and return same
if total % 10 == 0:
    if card_number[0] == "3":
        print("AMEX")
    elif card_number[0] == "4":
        print("VISA")
    elif card_number[0] == "5":
        print("MASTERCARD")
# If total doesn't end in 0, return invalid
else:
    print("INVALID")
    sys.exit(0)
