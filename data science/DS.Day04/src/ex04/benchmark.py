#!/usr/bin/env python3
import timeit
import random
from collections import Counter

def generate_data():
    return [random.randint(0, 100) for _ in range(1000000)] #миллион случайных чисел

def my_function_count(data):
    count_dict = {}
    for num in data:
        if num in count_dict:
            count_dict[num] += 1 #увеличиваем счетчик, если число уже есть в словаре
        else:
            count_dict[num] = 1
    return count_dict

def my_function_top10(data):
    count_dict = my_function_count(data)
    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True) #сортируем по убыванию количества
    return sorted_items[:10] #возвращаем первые 10

def counter_function_count(data):
    return Counter(data)

def counter_function_top10(data):
    counter = Counter(data)
    return counter.most_common(10)

if __name__ == '__main__':
    data = generate_data()
    my_count = my_function_count(data)
    counter_count = counter_function_count(data)
    my_top = my_function_top10(data)
    counter_top = counter_function_top10(data)
#проверяем, что результаты одинаковы
    if dict(my_count) != dict(counter_count):
        print("Error: Count results are different")
    elif my_top != counter_top:
        print("Error: Top-10 results are different")
    else:
        my_count_time = timeit.timeit(lambda: my_function_count(data), number=1)
        counter_count_time = timeit.timeit(lambda: counter_function_count(data), number=1)
        my_top_time = timeit.timeit(lambda: my_function_top10(data), number=1)
        counter_top_time = timeit.timeit(lambda: counter_function_top10(data), number=1)

    print(f"my function: {my_count_time:.7f}")
    print(f"Counter: {counter_count_time:.7f}")
    print(f"my top: {my_top_time:.7f}")
    print(f"Counter's top: {counter_top_time:.7f}")


    #print("My func:", dict(my_count))
    #print("Counter:", dict(counter_count))
    #print("My top:", my_top)
    #print("Counter's top:", counter_top)