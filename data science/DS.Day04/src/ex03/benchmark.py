#!/usr/bin/env python3
import timeit
import sys
from functools import reduce

def loop_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

def reduce_sum(n):
    numbers = list(range(1, n + 1))
    total = reduce(lambda x, y: x + y * y, numbers, 0)
    return total

def get_function_by_name(name):
    functions = {
        'loop': loop_sum,
        'reduce': reduce_sum
    }
    return functions.get(name) #возвращаем функцию по имени

def verify_results(n):
    loop_result = loop_sum(n)
    reduce_result = reduce_sum(n)
    return loop_result == reduce_result

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(1)
    function_name = sys.argv[1]
    try:
        num_calls = int(sys.argv[2])
        n_value = int(sys.argv[3])
    except ValueError:
        sys.exit(1)
    func = get_function_by_name(function_name)
    if func is None:
        print(f"Function '{function_name}' not found")
        sys.exit(1)
    #function_result = func(n_value)
    if not verify_results(n_value):
        sys.exit(1)
    time_taken = timeit.timeit(lambda: func(n_value), number=num_calls)
    print(time_taken)
    #print(f"function '{function_name}' result for n={n_value}: {function_result}")