# Shift Cipher Implementation in Python

with open("input.txt", "r") as f:
    plaintext = f.read().strip()

print(f'\nOriginal Text: {plaintext}')

# Get the shift value from the user, ensuring it's between 0 and 25
while True:
    try:
        shift_value = int(input(f'\nEnter the shift amount (key): '))
        if 0 <= shift_value <= 25:
            break
        else:
            print(f'\nError: Key should be between 0 and 25 inclusive.\n')
    except ValueError:
        print(f'\nError: Please enter a valid number.\n')

# Cipher the message using the shift value
ciphered_text = []

for char in plaintext:
    # Only encrypt letters; leave spaces and other characters untouched
    if char.isalpha():
        is_upper = char.isupper()
        base = ord('A') if is_upper else ord('a')
        
        ciphered_char = chr((ord(char) - base + shift_value) % 26 + base)
        ciphered_text.append(ciphered_char)
    else:
        ciphered_text.append(char)

# Display the ciphered text
ciphered_result = "".join(ciphered_text)
print(f'\nCiphered Text: {ciphered_result}\n')

# Save the ciphered text to 'encrypted.txt' file
with open('encrypted.txt', 'w') as f:
    f.write(ciphered_result)
