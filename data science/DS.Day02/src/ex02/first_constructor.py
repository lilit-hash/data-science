#!/usr/bin/env python3
import sys
import os

class Research:
    def __init__(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        self.file_path = file_path
    
    def file_reader(self):
        with open(self.file_path, 'r') as f:
            content = f.read().strip()
        lines = content.split('\n')
        if len(lines) < 2:
            raise ValueError("Файл должен содержать заголовок и хотя бы одну строку данных")
        
        header = lines[0].split(',')
        if len(header) != 2 or header[0] != 'head' or header[1] != 'tail':
            raise ValueError("Заголовок должен быть 'head,tail'")
        
        for i, line in enumerate(lines[1:], 1):
            if not line:
                continue
            values = line.split(',')
            if len(values) != 2:
                raise ValueError(f"Строка {i}: ожидалось 2 значения, а получено {len(values)}")
            if values[0] not in ('0', '1') or values[1] not in ('0', '1'):
                raise ValueError(f"Строка {i}: значения должны быть 0 или 1")
            if values[0] == values[1]:
                raise ValueError(f"Строка {i}: значения должны различаться")
        return content

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Используем {sys.argv[0]} <файл.csv>", file=sys.stderr)
        sys.exit(1)
    try:
        print(Research(sys.argv[1]).file_reader())
    except Exception as e:
        print(f"Ошибка: {str(e)}", file=sys.stderr)
        sys.exit(1)