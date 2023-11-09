#include <iostream>
#include <string>
#include <cmath>
#include <vector>

using namespace std;

class Feistel
{
public:
    Feistel(int iterations, int block_size)
    {
        this->iterations = iterations;
        this->block_size = block_size;
    }

    int block_size, iterations;
    int L, R;

    void setMessage(int message)
    {
        L = message >> block_size;             // This works the following way: 10101111 >> 4 = 1010, 1010 & 1111 = 1010
        R = message & ((1 << block_size) - 1); // This works the following way: 10101111 & 1111 = 1111
    }

    int getMessage()
    {
        return (L << block_size) + R;
    }

    int F(int i)
    {
        // For now, we will just rotate the bits, where the order of the bits is reversed
        int result = 0;
        for (int j = 0; j < block_size; j++)
        {
            result = result << 1;   // Shift the result to the left by 1
            result += (i >> j) & 1; // Add the jth bit of i to the result,
        }
        return result;
    }

    void printBlock(int block)
    {
        string block_str = "";
        for (int i = 0; i < block_size; i++)
        {
            block_str = to_string((block >> i) & 1) + block_str;
        }
        cout << block_str;
    }

    void printMessage()
    {
        printBlock(this->L);
        printBlock(this->R);
    }

    void round()
    {
        int temp = R;
        int fn = F(R);
        R = L ^ fn;
        L = temp;
    }

    void encrypt()
    {
        for (int i = 0; i < iterations; i++)
        {
            round();
        }
    }
};

int main()
{
    int message = 0b10101110;
    Feistel feistel(4, 4);
    feistel.setMessage(message);
    feistel.encrypt();
    feistel.printMessage();
    return 0;
}