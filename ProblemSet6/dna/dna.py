import csv
import sys
# can use argv and exit methods


def main():

    # TODO: Check for command-line usage
    # Take one arg for CSV file w/STR counts, take second arg for txt file w/dna to id
    # If incorrect number of cli print error
    argv = sys.argv
    if len(argv) != 3:
        print(f"Error. Invalid input. Please enter a database file and a sequence file.")
        sys.exit(1)

    # TODO: Read database file into a variable
    database = []
    with open(argv[1]) as database_file:
        reader = csv.DictReader(database_file)
        for data in reader:
            database.append(data)

    # TODO: Read DNA sequence file into a variable

    with open(argv[2]) as sequence_file:
        sequence = sequence_file.read()
    sequence_file.close()

    # TODO: Find longest match of each STR in DNA sequence
    # Create dict with STRs and longest corresponding match for each
    strs = list(database[0].keys())
    sequence_matches = {}
    for i in range(len(strs)):
        sequence_matches[strs[i]] = longest_match(sequence, strs[i])

    # TODO: Check database for matching profiles
    # Loop through each dict in the database and for each check whether there is a match at
    # each STR, if number of matches matches number of STRs return current name as a match,
    # otherwise return "no match"

    for i in range(len(database)):
        current = database[i]
        match_count = 0
        for str_count in strs:
            if current[str_count] == current['name']:
                continue
            if int(current[str_count]) != sequence_matches[str_count]:
                continue
            if int(current[str_count]) == sequence_matches[str_count]:
                match_count += 1
            if match_count == len(strs) - 1:
                print(current['name'])
                return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
