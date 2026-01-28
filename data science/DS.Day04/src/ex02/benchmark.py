#!/usr/bin/env python3
import timeit
import sys

def loop_approach():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
              'anna@live.com', 'philipp@gmail.com'] * 5
    gmail_emails = []
    for email in emails:
        if email.endswith('@gmail.com'):
            gmail_emails.append(email)
    return gmail_emails

def list_comprehension_approach():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
              'anna@live.com', 'philipp@gmail.com'] * 5
    gmail_emails = [email for email in emails if email.endswith('@gmail.com')]
    return gmail_emails

def map_approach():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
              'anna@live.com', 'philipp@gmail.com'] * 5
    
    def get_gmail(email):
        return email if email.endswith('@gmail.com') else None
    gmail_emails = list(map(get_gmail, emails))
    return gmail_emails

def filter_approach():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
              'anna@live.com', 'philipp@gmail.com'] * 5
    
    def is_gmail(email):
        return email.endswith('@gmail.com')
    gmail_emails = list(filter(is_gmail, emails))
    return gmail_emails

def get_function_by_name(name):
    functions = {
        'loop': loop_approach,
        'list_comprehension': list_comprehension_approach,
        'map': map_approach,
        'filter': filter_approach
    }
    return functions.get(name)

def verify_results():
    functions = [loop_approach, list_comprehension_approach, filter_approach]
    results = []
    for func in functions:
        result = func()
        if func == map_approach:  #убираем none для map
            result = [email for email in result if email is not None]
        results.append(result)

    first_result = results[0] #наш эталон для сравнения
    for result in results[1:]:   #проверяем остальные и сравниваем результаты
        if result != first_result:
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)
    function_name = sys.argv[1]
    try:
        num_calls = int(sys.argv[2])
    except ValueError:
        sys.exit(1)
      
    func = get_function_by_name(function_name)
    if func is None:
        print(f"Function '{function_name}' not found")
        sys.exit(1)
    #function_result = func()      
    if not verify_results():
        sys.exit(1)
    time_taken = timeit.timeit(func, number=num_calls) #замеряем время
    print(time_taken)
    #print(f"function '{function_name}' result: {function_result}")