import sys
def find_name(email):
    with open('employees.tsv', 'r') as file:
        lines = file.read().splitlines()
    
    for line in lines[1:]: 
        if not line.strip():
            continue
        current_email = line.split('\t')[2]
        if current_email == email:
            name = line.split('\t')[0]
            return f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."
    return None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Incorrect number of arguments")
    email = sys.argv[1]
    letter = find_name(email)
    if letter:
        print(letter)
    else:
        print("Email not found in the database.")