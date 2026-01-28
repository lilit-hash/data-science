#!/usr/bin/env python3
import sys
import os

class Research:
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Ошибка: файл '{file_path}' не найден")
        self.file_path = file_path
    def file_reader(self, has_header=True):
        with open(self.file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise ValueError("файл пуст")
        data = []
        start_idx = 0
        if has_header:
            if len(lines) < 2:
                raise ValueError("файл с заголовком должен содержать хотя бы одну строку данных")
            header = lines[0].split(',')
            if len(header) != 2 or header != ['head', 'tail']:
                raise ValueError("неверный формат заголовка. Должно быть 'head,tail'")
            start_idx = 1
        
        for i in range(start_idx, len(lines)):
            values = lines[i].split(',')
            if len(values) != 2:
                raise ValueError(f"Ошибка в строке {i+1}: ожидается 2 значения, получено {len(values)}")
            try:
                a, b = int(values[0]), int(values[1])
            except ValueError:
                raise ValueError(f"Ошибка в строке {i+1}: значения должны быть числами 0 или 1")
            if {a, b} != {0, 1}:
                raise ValueError(f"Ошибка в строке {i+1}: значения должны быть 0 и 1")
            if a == b:
                raise ValueError(f"Ошибка в строке {i+1}: значения должны различаться")
            data.append([a, b])
        if not data:
            raise ValueError("в файле нет корректных данных")
        return data

class Calculations:
    @staticmethod
    def counts(data):
        heads = sum(pair[0] for pair in data)
        tails = len(data) - heads
        return heads, tails
    @staticmethod
    def fractions(data):
        heads = sum(pair[0] for pair in data)
        tails = len(data) - heads
        total = heads + tails
        if total == 0:
            return 0.0, 0.0
        return heads/total*100, tails/total*100

def main():
    if len(sys.argv) != 2:
        print("./first_nest.py <файл.csv>", file=sys.stderr)
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        
        try:
            data = research.file_reader(has_header=True)
        except ValueError as e:
            try:
                data = research.file_reader(has_header=False)
            except ValueError as e:
                sys.exit(f"Ошибка: {e}")
        print(data)
        heads, tails = Calculations.counts(data)
        print(heads, tails)
        head_percent, tail_percent = Calculations.fractions(data)
        print(f"{head_percent:.1f} {tail_percent:.1f}")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()