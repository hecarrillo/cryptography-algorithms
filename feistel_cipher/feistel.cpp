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

// to run: g++ feistel.cpp -std=c++14 -Wall -Wextra -pedantic && ./a.out

int main()
{   
    string file_name;
    cout << "Enter the file name: ";
    cin >> file_name;
    cout << "\nEnter the number of iterations: ";
    int iterations;
    cin >> iterations;

    // Read the file
    FILE *file = fopen(file_name.c_str(), "r");
    if (file == NULL)
    {
        cout << "Error opening file" << endl;
        return 0;
    }

    // Read the file and encrypt it using the feistel cipher in 64 bit blocks
    int message = 0;
    string final_message = "";
    int c;
    int i = 0;
    while ((c = fgetc(file)) != EOF)
    {
        message = message << 8;
        message += c;
        i++;
        if (i == 8)
        {
            Feistel feistel(iterations, 32);
            feistel.setMessage(message);
            feistel.encrypt();
            feistel.printMessage();
            final_message += to_string(feistel.getMessage()) + " ";
            i = 0;
            message = 0;
        }
    }
    if (i != 0)
    {
        Feistel feistel(iterations, 32);
        feistel.setMessage(message);
        feistel.encrypt();
        final_message += to_string(feistel.getMessage()) + " ";
    }
    // Write the encrypted message to a file
    FILE *encrypted_file = fopen("encrypted.bin", "w");
    if (encrypted_file == NULL)
    {
        cout << "Error opening file" << endl;
        return 0;
    }
    for (int i = 0; i < final_message.length(); i++)
    {
        if (final_message[i] == ' ')
        {
            fputc(' ', encrypted_file);
        }
        else
        {
            int num = stoi(final_message.substr(i, 8));
            fwrite(&num, sizeof(int), 1, encrypted_file);
            i += 7;
        }
    }
    fclose(encrypted_file);
    fclose(file);
    return 0;
}