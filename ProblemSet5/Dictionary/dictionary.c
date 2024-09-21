// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1132;

// Hash table (array of node pointers, every element points to a node)
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // get index/hash value of word
    int index = hash(word);
    // node to go to start of list and traverse list
    node *ptr = table[index];

    for (node *i = ptr; i != NULL; i = i->next)
    {
        // check to see if words match, regardless of case
        if (strcasecmp(i->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int index = 0;
    index = toupper(word[0]) - 'A';
    index *= LENGTH;
    index += strlen(word);
    return index % N;
}

// to store size
int word_count = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *source = fopen(dictionary, "r");

    if (source == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }

    // to store word
    char word[LENGTH + 1];

    // loop over each string in file
    while (fscanf(source, "%s", word) != EOF)
    {
        // count number of words for size
        word_count++;

        // allocate memory for new node
        node *n = malloc(sizeof(node));
        // return false if n is null
        if (n == NULL)
        {
            // unload();
            printf("Memory error.\n");
            return false;
        }

        // copy word into n->word
        strcpy(n->word, word);
        n->next = NULL;
        // get hash value of word
        unsigned int hash_value = hash(n->word);

        // add to table if hash value does not have a node
        if (table[hash_value] == NULL)
        {
            table[hash_value] = n;
        }
        else
        {
            // add to table if hash value has a node
            n->next = table[hash_value];
            table[hash_value] = n;
        }
        //  printf("hash_value in load: %i\n", hash_value);
    }
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // return word count from load function
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // make two loops to free all the memory. one loop goes over the indexes and a loop inside goes
    // through each list. pointer to traverse array and list, another to hold memory to be freed
    node *tmp = NULL;
    node *ptr = NULL;

    for (int i = 0; i < N; i++)
    {
        ptr = table[i];
        while (ptr != NULL)
        {
            tmp = ptr;
            ptr = ptr->next;
            free(tmp);
        }
    }
    return true;
}
