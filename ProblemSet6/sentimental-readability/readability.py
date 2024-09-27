from cs50 import get_string

# main fn to get string, call data fn, and grade fn


def main():
    text = get_string("Text: ")
    data = get_data(text)
    grade = get_grade(data)
    if grade < 0:
        return print("Before Grade 1")
    elif grade > 16:
        return print("Grade 16+")
    else:
        return print(f"Grade: {grade}")

# Get letters, words and sentences, return data


def get_data(text):
    # store data in dict
    # start words at one to account for lack of white space at end of text
    data = {
        "letters": 0,
        "words": 1,
        "sentences": 0,
    }
    # array to check for punctuation
    punctuation = ['.', '?', '!']

    # iterate over text and update data accordindly
    for i in range(len(text)):
        if text[i].isalnum():
            data["letters"] += 1
        if text[i].isspace():
            data["words"] += 1
        if text[i] in punctuation:
            data["sentences"] += 1
    # return data
    return data

# Assess grade


def get_grade(data):
    # deconstruct data
    letters = data["letters"]
    words = data["words"]
    sentences = data["sentences"]

    # implement Coleman-Liau index to get grade
    l = letters / words * 100
    s = sentences / words * 100
    grade = 0.0588 * l - 0.296 * s - 15.8
    grade = round(grade)

    # return grade
    return grade


# main fn call
main()
