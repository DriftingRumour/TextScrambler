import sys
import numpy as np
import os
import random
import argparse
import textwrap

# Dictionary to map characters to a list of possible symbols
char_to_symbol = {
    'a': ['#', '@', '~'], 'A': ['#', '/-\\', '%'],
    'b': ['8', '|3'], 'B': ['8', '|3', '%'],
    'c': ['(', '<', '~'], 'C': ['(', '<', '%'],
    'd': ['|)', '[)'], 'D': ['|)', '[)', '%'],
    'e': ['@', '-', '~'], 'E': ['3', '|#', '%'],
    'f': ['/-', '|-'], 'F': ['/#', '|#', '%'],
    'g': ['9', '&'], 'G': ['@', '&', '%'],
    'h': ['#', '},'], 'H': ['#', '}{', '%'],
    'i': ['!', '~'], 'I': ['!`', '1', '%'],
    'j': [';', ',|'], 'J': [';', '_|', '%'],
    'k': ['|<', '|{'], 'K': ['|<', '|{', '%'],
    'l': ['1', '|'], 'L': ['1', '|_', '%'],
    'm': ['|v|', '.-,', '.~,'], 'M': ['|v|', '/\\/\\', '%'],
    'n': [',-,', ',~,'], 'N': ['|\\|', '/\\/', '%'],
    'o': ['0', '@'], 'O': ['0', '@', '%'],
    'p': ['|*', '|o'], 'P': ['|*', '|o', '%'],
    'q': ['0_', '0,'], 'Q': ['@,', '@.', '%'],
    'r': ['|``', '|`', ',-', ',~'], 'R': ['|2', '|?', '%'],
    's': ['$', '5', '~'], 'S': ['$', '5', '%'],
    't': ['+', '+.', '~'], 'T': ['+', '7'],
    'u': ['|_|', '(_)'], 'U': ['|_|', '(_)'],
    'v': ['\\/', '|/', '\\|'], 'V': ['\\/', '|/', '\\|', '%'],
    'w': ['\\/\\/', 'VV', '~'], 'W': ['\\/\\/', 'VV', '%'],
    'x': ['%', '><', '~'], 'X': ['><', '%'],
    'y': ['`/', '¥'], 'Y': ['`/', '¥', '%'],
    'z': ['2', '7_', '~'], 'Z': ['2', '7_', '%']
    # Add more mappings as needed
}
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def wrap_text(text, width=60):
    wrapped_lines = []
    for line in text.split('\n'):
        wrapped_lines.extend(textwrap.wrap(line, width=width, break_long_words=False, replace_whitespace=False))
    return '\n'.join(wrapped_lines)

def transform_text(text, float_value):
    transformed_text = []
    for char in text:
        if char.lower() in char_to_symbol and np.random.rand() < float_value:
            transformed_text.append(np.random.choice(char_to_symbol[char.lower()]))
        else:
            transformed_text.append(char)
    return ''.join(transformed_text)

def burn_holes(text, num_holes, radii):
    lines = text.split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    text_array = [list(line.ljust(width)) for line in lines]

    for i in range(num_holes):
        center_x = random.randint(0, width - 1)
        center_y = random.randint(0, height - 1)
        radius = radii[i] if isinstance(radii, list) else radii
        for y in range(height):
            for x in range(width):
                # Adjust the ellipse equation to make the hole wider than it is tall
                if ((x - center_x) ** 2) / (radius ** 2) + ((y - center_y) ** 2) / ((radius / 2) ** 2) <= 1:
                    text_array[y][x] = chr(9608)
    return '\n'.join(''.join(line) for line in text_array)

def edge_charring(text, edge_charring_value):
    lines = text.split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    text_array = [list(line.ljust(width)) for line in lines]

    min_burn = round(np.sqrt(edge_charring_value))
    max_burn = edge_charring_value + min_burn

    for y in range(height):
        for x in range(width):
            if x < random.randint(min_burn, max_burn) or x >= width - random.randint(min_burn, max_burn) or \
               y < random.randint(min_burn, max_burn) or y >= height - random.randint(min_burn, max_burn):
                text_array[y][x] = chr(9608)
    return '\n'.join(''.join(line) for line in text_array)

def save_transformed_text(original_file_path, transformed_text, smudge_value, num_holes):
    base, ext = os.path.splitext(original_file_path)
    new_file_path = f"{base}_{smudge_value}Smudged_{num_holes}Holes{ext}"
    with open(new_file_path, 'w') as file:
        file.write(transformed_text)
    print(f"Transformed text saved to {new_file_path}")

def main():
    parser = argparse.ArgumentParser(
        description="""Example usage:       python TextFucker.py input.txt --smudge 0.4 --holes 3 --radius [2,3,4] --wrap 50"""
    )
    parser.add_argument("file_path", type=str, help="Path to the input text file.")
    parser.add_argument("--smudge", type=float, default=0.3, help="Float value between 0 and 1 to determine the probability of character smudging. Default is 0.3")
    parser.add_argument("--holes", type=int, default=2, help="Number of holes to burn in the text. Default is 2.")
    parser.add_argument("--radius", type=str, default = "4", help="Radius or list of radii for the holes. If a list, its length must equal the number of holes and use list brackets => [1,2,3].")
    parser.add_argument("--wrap", type=int, default=70, help="Width at which to wrap the text. Default is 60.")
    parser.add_argument("--EdgeCharring", type=int, default=0, help="Value to determine the extent of edge charring.")
    args = parser.parse_args()

    try:
        # Ensure the radius is treated as a string and convert it to a list or single value
        if args.radius.startswith('[') and args.radius.endswith(']'):
            radii = eval(args.radius)  # Convert to list
        else:
            radii = float(args.radius)  # Convert to single float value

        if isinstance(radii, list) and len(radii) != args.holes:
            raise ValueError("The length of the radii list must equal the number of holes.")
    except ValueError as e:
        print(f"Error: {e}")
        print("The float value must be a valid number between 0 and 1, num_holes must be an integer, and radius_or_radii must be a single value or a list of values.")
        sys.exit(1)
    
    text = read_file(args.file_path)
    wrapped_text = wrap_text(text, args.wrap)
    smudged_text = transform_text(wrapped_text, args.smudge)
    burnt_text = burn_holes(smudged_text, args.holes, radii)
    charred_text = edge_charring(burnt_text, args.EdgeCharring)
    save_transformed_text(args.file_path, charred_text, args.smudge, args.holes)

if __name__ == "__main__":
    main()