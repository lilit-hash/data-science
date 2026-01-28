#!/usr/bin/env python3
import sys
from random import randint
class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    def file_reader(self, has_header=True):
        try:
            with open(self.file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            raise ValueError("Невозможно открыть файл")
        if not lines:
            raise ValueError("Файл пуст")
        data = []
        start_idx = 0
        if has_header:
            if len(lines) < 2:
                raise ValueError("Нет данных после заголовка")
            if lines[0] != 'head,tail':
                raise ValueError("Неверный формат заголовка")
            start_idx = 1

        for i in range(start_idx, len(lines)):
            parts = lines[i].split(',')
            if len(parts) != 2:
                raise ValueError(f"Ошибка в строке {i+1}: нужно 2 значения")
            try:
                a, b = int(parts[0]), int(parts[1])
            except ValueError:
                raise ValueError(f"Ошибка в строке {i+1}: значения должны быть 0 или 1")
            if {a, b} != {0, 1}:
                raise ValueError(f"Ошибка в строке {i+1}: недопустимые значения")
            data.append([a, b])
        return data
class Calculations:
    def __init__(self, data):
        self.data = data
    def counts(self):
        heads = sum(x[0] for x in self.data)
        return heads, len(self.data) - heads
    def fractions(self):
        heads, tails = self.counts()
        total = heads + tails
        return heads/total*100, tails/total*100
class Analytics(Calculations):
    def predict_random(self, n=3):
        predictions = []
        for _ in range(n):
            first = randint(0, 1)
            predictions.append([first, 1 - first])  
        return predictions

    def predict_last(self):
        return self.data[-1] if self.data else None
def main():
    if len(sys.argv) != 2:
        print("./first_child.py <файл.csv>", file=sys.stderr)
        sys.exit(1)
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        analytics = Analytics(data)
        print(data)
        print("\nКоличество:")
        print(*analytics.counts())
        print("\nПроценты:")
        print(*analytics.fractions())
        print("\nСлучайные предсказания:")
        print(analytics.predict_random())
        print("\nПоследнее наблюдение:")
        print(analytics.predict_last())
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
if __name__ == '__main__':
    main()