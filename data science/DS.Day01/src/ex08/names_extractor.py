import sys
def process_emails(input_file):
    with open(input_file, 'r') as file:
        emails = file.read().splitlines()
    
    employees = []
    for email in emails:
        if not email.strip():
            continue
        name_part = email.split('@')[0]
        name, surname = name_part.split('.')
        name = name.capitalize()
        surname = surname.capitalize()
        employees.append(f"{name}\t{surname}\t{email}")
    
    with open('employees.tsv', 'w') as file:
        file.write("Name\tSurname\tE-mail\n")
        file.write('\n'.join(employees))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Incorrect number of arguments")
    input_file = sys.argv[1]
    process_emails(input_file)