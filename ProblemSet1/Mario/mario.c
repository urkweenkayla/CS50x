#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;

    do
    {
        n = get_int("size: ");
    }
    while (n < 1)

    for (int i = 0; i < n; i++)
    {
        for (int j = n - 1; j >= 0; j--)
        {
            if (j > i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("  ");
        for (int k = 0; k < n; k++)
        {
            if (k <= i)
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
