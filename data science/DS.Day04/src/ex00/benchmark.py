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

if __name__ == '__main__':
    loop_result = loop_approach()
    comprehension_result = list_comprehension_approach()
    
    if loop_result != comprehension_result:
        print("Error: Functions return different results")
        exit(1)
    
    loop_time = timeit.timeit(loop_approach, number=90000000)
    comprehension_time = timeit.timeit(list_comprehension_approach, number=90000000)
    times = [loop_time, comprehension_time]
    sorted_times = sorted(times)
    
    if comprehension_time <= loop_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")
    
    print(f"{sorted_times[0]} vs {sorted_times[1]}")

    #print(f"Loop: {loop_result}")
    #print(f"List: {comprehension_result}")