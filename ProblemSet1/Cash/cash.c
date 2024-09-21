#include <cs50.h>
#include <stdio.h>

int giveCoins(int currN, int currCoin);

int main(void)
{
    int n;
    int currentCoin;
    int quarters = 0;
    int dimes = 0;
    int nickles = 0;
    int quarter = 25;
    int dime = 10;
    int nickle = 5;
    int change = 0;

    do
    {
        n = get_int("Change owed: ");
    }
    while (n < 1 && n < 100);

    for (int i = 0; i < n; i++)
    {
        if (n >= 25)
        {
            currentCoin = 25;
            quarters += giveCoins(n, currentCoin);
            n -= quarters * currentCoin;
        }
        else if (n >= 10)
        {
            currentCoin = 10;
            dimes += giveCoins(n, currentCoin);
            n -= dimes * currentCoin;
        }
        else if (n >= 5)
        {
            currentCoin = 5;
            nickles += giveCoins(n, currentCoin);
            n -= nickles * currentCoin;
        }
        change = quarters + dimes + nickles + n;
    }
    printf("change: %i\n", change);
}

int giveCoins(int currN, int currCoin)
{
    int currChange = 0;
    do
    {
        currN -= currCoin;
        currChange++;
    }
    while (currN >= currCoin);
    return currChange;
}
