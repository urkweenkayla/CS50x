#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_alpha(string key);
bool unique_chars(string key);
char encrypt_char(string key, char ch);

int main(int argc, string argv[])
{
    if (argc == 1 || argc > 2)
    {
        printf("Usage: ./substitution key\nKey must contain 26 alphabetic characters without "
               "spaces.\n");
        exit(1);
    }
    else if (strlen(argv[1]) > 26 || strlen(argv[1]) < 26 )
    {
         printf("Usage: ./substitution key\nKey must contain exactly 26 alphabetic characters without spaces.\n");
        exit(1);
    }
    else if (!only_alpha(argv[1]))
    {
        printf("Usage: ./substitution key\nKey must contain 26 alphabetic (no numbers) characters "
               "without spaces.\n");
        exit(1);
    }
    else if (!unique_chars(argv[1]))
    {
        printf("Usage: ./substitution key\nKey must contain each letter of the alphabet once with "
               "no repeating characters for a total of 26 characters.\n");
        exit(1);
    }
    else
    {
        string plaintext = get_string("plaintext: ");
        printf("plaintext - %s\nlength: %lu\n", plaintext, strlen(plaintext));
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            plaintext[i] = encrypt_char(argv[1], plaintext[i]);

            if (n == i + 1)
            {
                printf("ciphertext: %s\n", plaintext);
            }
        }
        exit(0);
    }
}

bool only_alpha(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
    }
    return true;
}

bool unique_chars(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (key[i] == key[j])
            {
                return false;
            }
        }
    }
    return true;
}

char encrypt_char(string key, char ch)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (isspace(ch))
        {
            return ' ';
        }
        if (isupper(ch))
        {
            return toupper(key[ch - 'A']);
        }
        else if (islower(ch))
        {
            return tolower(key[ch - 'a']);
        }
        else
        {
            return ch;
        }
    }
    exit(0);
}
