def read_and_write():
    try:
        with open('ds.csv', 'r', encoding='utf-8') as csv_file:
            with open('ds.tsv', 'w', encoding='utf-8') as tsv_file:
                in_quotes = False
                for line in csv_file:
                    new_line = []
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                            new_line.append(char)
                        elif char == ',' and not in_quotes:
                            new_line.append('\t')
                        else:
                            new_line.append(char)
                    tsv_file.write(''.join(new_line))
        print("Конвертация ds.csv -> ds.tsv завершена успешно")
    except FileNotFoundError:
        print("Ошибка: файл ds.csv не найден")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    read_and_write()