import sys

def caesar_cipher(text, shift, mode):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            new = ord(char) + shift if mode == 'encode' else ord(char) - shift
            result.append(chr((new - ord('a')) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            new = ord(char) + shift if mode == 'encode' else ord(char) - shift
            result.append(chr((new - ord('A')) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def main():
    if len(sys.argv) != 4:
        raise Exception("Incorrect number of arguments")
    
    mode, text, shift = sys.argv[1], sys.argv[2], sys.argv[3]
    
    try:
        shift = int(shift)
    except ValueError:
        raise Exception("Shift must be an integer")
    
    if mode not in {'encode', 'decode'}:
        raise Exception("First argument must be 'encode' or 'decode'")
    
    if any(not c.isascii() or (c.isalpha() and not c.isupper() and not c.islower()) for c in text):
        raise Exception("The script does not support your language yet")
    
    print(caesar_cipher(text, shift, mode))

if __name__ == "__main__":
    main()