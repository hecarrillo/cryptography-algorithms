# Vigenère Cipher Implementation in Python

# Read the plaintext from a text file named 'input.txt'
with open("input.txt", "r") as f:
    plaintext = f.read()

print(f'\nOriginal Text: {plaintext}')

# Get the length of the plaintext
text_length = len(plaintext) - 1

# Ensure the plaintext length is within [5,100]
if(text_length < 5 or text_length > 100):
    print(f'\nText length should be between 5 and 100 characters.\n')
    exit()

print(f'\nLength of Text: {text_length}')

# Create a list to store the key values
key_values = []

while True:
    try:
        num_keys = int(input(f'\nEnter the number of keys for encryption: '))
    except ValueError:
        print(f'\nError: Only numeric values are allowed.\n')
        continue

    if (num_keys >= 1 and num_keys <= text_length):
        break
    else:
        print(f'\nError: Number of keys should be between 1 and {text_length}.\n')

for i in range(num_keys):
    while True:
        try:
            key = int(input(f'\nEnter shift value (key) {i}: '))
        except ValueError:
            print(f'\nError: Only numeric values are allowed.\n')
            continue

        if (key >= 0 and key <= 25):
            key_values.append(key)
            break
        else:
            print(f'\nError: Key value should be between 0 and 25.\n')

# List to store the encrypted text
encrypted_text = []

key_counter = 0
base_ascii = ord("A")

# Iterate over each character in the plaintext
for char in plaintext:
    if(key_counter == num_keys):
        key_counter = 0
    if(char == '\n'):
        break
    if (char == " "):
        encrypted_text.append(" ")
        continue

    ascii_val = 0

    if (ord(char) >= ord("A") and ord(char) <= ord("Z")):
        ascii_val = ord(char) - ord("A")
        encrypted_text.append(chr(((ascii_val + key_values[key_counter]) % 26) + base_ascii))
    else: 
        encrypted_text.append(char)
    

    key_counter += 1

print("\nEncrypted Text: " + "".join(encrypted_text) + "\n")

# Write the encrypted text to a file
with open('encryptedOutput.txt', 'w') as f:
    f.write("".join(encrypted_text) + "\n")
