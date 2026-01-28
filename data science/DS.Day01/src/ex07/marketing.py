import sys
clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
           'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
           'elon@paypal.com', 'jessica@gmail.com']
participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

def call_center():
    clients_set, recipients_set = set(clients), set(recipients)
    return list(clients_set - recipients_set)

def potential_clients():
    clients_set, participants_set  = set(clients),set(participants)
    return list(participants_set - clients_set)

def loyalty_program():
    clients_set, participants_set  = set(clients), set(participants)
    return list(clients_set - participants_set)

def main():
    if len(sys.argv) != 2:
        raise Exception("Incorrect number of arguments")
    
    task = sys.argv[1]
    if task == "call_center":
        res = call_center()
    elif task == "potential_clients":
        res = potential_clients()
    elif task == "loyalty_program":
        res = loyalty_program()
    else:
        raise Exception("Invalid task name")
    for email in res:
        print(email)

if __name__ == '__main__':
    main()