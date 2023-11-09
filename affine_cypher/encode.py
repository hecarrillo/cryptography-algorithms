# Affine Cipher Implementation in Python

# Function to calculate the greatest common divisor
def compute_gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

# Load the plaintext from 'input.txt' file
with open("input.txt", "r") as f:
    plaintext = f.read().strip()

print(f'\nOriginal Text: {plaintext}')

# Get the 'a' and 'b' values from the user
# Ensure 'a' is coprime with 26 and both values are between 0 and 25
while True:
    try:
        a = int(input("\nEnter the value for a (multiplicative constant): "))
        b = int(input("Enter the value for b (additive constant): "))
        if (0 <= a <= 25 and compute_gcd(a, 26) == 1) and (0 <= b <= 25):
            break
        else:
            print(f'\nError: Both "a" and "b" should be between 0 and 25. Also, "a" must be coprime with 26.')
    except ValueError:
        print(f'\nError: Please enter valid numbers between 0 and 25.')

# Cipher the message using 'a' and 'b'
ciphered_text = []

for char in plaintext:
    # Only encrypt letters; leave spaces and other characters untouched
    if char.isalpha():
        base = ord('A') if char.isupper() else ord('a')
        char_value = ord(char) - base
        ciphered_char = chr((a * char_value + b) % 26 + base)
        ciphered_text.append(ciphered_char)
    else:
        ciphered_text.append(char)

# Display the ciphered text
ciphered_result = "".join(ciphered_text)
print(f'\nCiphered Text: {ciphered_result}\n')

# Save the ciphered text to 'encrypted.txt' file
with open('encrypted.txt', 'w') as f:
    f.write(ciphered_result)
