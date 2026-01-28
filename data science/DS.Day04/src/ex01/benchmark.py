#!/usr/bin/env python3
import timeit

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

if __name__ == '__main__':
    loop_result = loop_approach()
    comprehension_result = list_comprehension_approach()
    map_result = map_approach()
    
    correct_emails = ['john@gmail.com', 'james@gmail.com', 'philipp@gmail.com'] * 5
    if loop_result != correct_emails or comprehension_result != correct_emails:
        print("Error: Results are incorrect")
        exit(1)
    if not any(email is None for email in map_result):
        print("Error: Map result should contain None values")
        exit(1)
    
    test_number = 90000000
    loop_time = timeit.timeit(loop_approach, number=test_number)
    comprehension_time = timeit.timeit(list_comprehension_approach, number=test_number)
    map_time = timeit.timeit(map_approach, number=test_number)
    
    times = [loop_time, comprehension_time, map_time]
    min_time = min(times)
    
    if min_time == map_time:
        print("it is better to use a map")
    elif min_time == comprehension_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")
    
    sorted_times = sorted(times)
    print(f"{sorted_times[0]} vs {sorted_times[1]} vs {sorted_times[2]}")

    #print(f"Loop: {loop_result}")
    #print(f"List: {comprehension_result}")
    #print(f"Map: {map_result}")