from cs50 import get_int

# Prompt user for height. Check whether input is positive integer and reprompt user if not
while True:
    n = get_int("Height: ")
    if 1 <= n <= 8:
        break
    else:
        print("Please enter a number between 1 and 8")

# Three loops, one outer to handle the rows and two inner to handle each place within the rows
for i in range(n):
    for j in range(n - 1, -1, -1):
        if j > i:
            print(" ", end="")
        else:
            print("#", end="")
    print("  ", end="")
    for k in range(n):
        if k > i:
            print("", end="")
        else:
            print("#", end="")
    print()
