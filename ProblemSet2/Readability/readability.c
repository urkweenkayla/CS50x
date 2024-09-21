#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int getLetters(string text);
int getWords(string text);
int getSentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    int letters = getLetters(text);
    int words = getWords(text);
    int sentences = getSentences(text);
    float l = (float) letters / (float) words * 100;
    float s = (float) sentences / (float) words * 100;

    float grade = 0.0588 * l - 0.296 * s - 15.8;
    if (grade < 0)
    {
        printf("Before Grade 1\n");
        exit(0);
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
        exit(0);
    }
    printf("Grade %i\n", (int) round(grade));
}

int getLetters(string text)
{
    int letters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

int getWords(string text)
{
    int words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}

int getSentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }
    return sentences;
}
