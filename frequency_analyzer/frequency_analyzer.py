# Script for analyzing the frequency of letter occurrences

# Initialize a list to count the occurrences of each letter
letter_counts = [0] * 26

# Prompt the user for the file name (full path needed if not in the same directory)
file_path = input("\nEnter the file name for analysis: ")

# Read the content of the specified file
with open(file_path, "r") as file:
    content = file.read()

# Count the occurrences of each letter in the content
total_letters = 0

for char in content:
    if 'a' <= char <= 'z':
        letter_counts[ord(char) - ord('a')] += 1
        total_letters += 1
    elif 'A' <= char <= 'Z':
        letter_counts[ord(char) - ord('A')] += 1
        total_letters += 1

# Write the results to an output file
with open("letterFrequencyOutput.txt", "w") as output_file:
    output_file.write(f'Total number of letters [A-Z | a-z]: {total_letters}\n')
    
    for i in range(26):
        output_file.write(f'\n{chr(i + ord("A"))} -> {letter_counts[i]/total_letters:.4f}')

print("\nAnalysis results saved in 'letterFrequencyOutput.txt'\n")
