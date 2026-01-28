#!/usr/bin/env python3
import sys
import resource

def read_file_ordinary(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines() #читаем все строки в память и возвращаем их список
    return lines

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    filename = sys.argv[1]
    start_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime + resource.getrusage(resource.RUSAGE_SELF).ru_stime
    lines = read_file_ordinary(filename)
    for line in lines:
        pass
    end_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime + resource.getrusage(resource.RUSAGE_SELF).ru_stime
    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024
    total_time = end_time - start_time
    print(f"Peak Memory Usage = {peak_memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")