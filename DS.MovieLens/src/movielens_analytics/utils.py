import sys
from typing import Any, Dict, Iterable, List, Tuple


class ReportUtils:
    """
    Класс с кастомными реализациями встроенных функций
    """

    @staticmethod
    def print(text: str) -> None:
        """
        Кастомная реализация функции print с использованием sys.stdout.write
        Это реализация вместо использования встроенной функции print()

        Args:
            text (str): Текст для вывода в стандартный поток вывода

        Returns:
            None: Функция не возвращает значение, только выводит текст
        """
        sys.stdout.write(text + "\n")

    @staticmethod
    def get_length(collection: Iterable) -> int:
        """
        Кастомная реализация функции len() для любого итерируемого объекта
        Подсчитывает элементы вручную без использования встроенной функции len()

        Args:
            collection (Iterable): Любой итерируемый объект (список, кортеж, генератор и т.д.)

        Returns:
            int: Количество элементов в коллекции
        """
        count = 0
        for _ in collection:
            count += 1
        return count

    @staticmethod
    def to_list(collection: Iterable) -> List[Any]:
        """
        Кастомная реализация преобразования в список
        Преобразует любой итерируемый объект в список без использования встроенной функции list().

        Args:
            collection (Iterable): Итерируемый объект для преобразования

        Returns:
            List[Any]: Новый список со всеми элементами из итерируемого объекта
        """
        result = []
        for item in collection:
            result.append(item)
        return result

    @staticmethod
    def sorted_dict(dictionary: Dict[Any, Any], reverse: bool = False) -> List[Tuple[Any, Any]]:
        """
        Кастомная сортировка словаря по значениям с использованием алгоритма пузырьковой сортировки
        Реализует сортировку без использования встроенной функции sorted()

        Args:
            dictionary (Dict[Any, Any]): Словарь для сортировки по значениям
            reverse (bool): Если True, сортировка в порядке убывания (по умолчанию False)

        Returns:
            List[Tuple[Any, Any]]: Список пар (ключ, значение), отсортированных по значению
        """
        items = ReportUtils.to_list(dictionary.items())
        n = ReportUtils.get_length(items)

        # сортировка пузырьком
        for i in range(n):
            for j in range(0, n - i - 1):
                if reverse:
                    if items[j][1] < items[j + 1][1]:
                        items[j], items[j + 1] = items[j + 1], items[j]
                else:
                    if items[j][1] > items[j + 1][1]:
                        items[j], items[j + 1] = items[j + 1], items[j]
        return items

    @staticmethod
    def slice_collection(collection: Iterable, start: int = 0, end: int = None) -> List[Any]:
        """
        Кастомная реализация среза для любого итерируемого объекта
        Работает как collection[start:end], но без использования встроенных срезов.

        Args:
            collection (Iterable): Итерируемый объект для среза
            start (int): Начальный индекс (включительно, по умолчанию 0)
            end (int): Конечный индекс (исключительно, None - без верхнего предела)

        Returns:
            List[Any]: Срезанная часть коллекции в виде нового списка
        """
        result = []
        for i, item in enumerate(collection):
            if i < start:
                continue
            if end is not None and i >= end:
                break
            result.append(item)
        return result

    @staticmethod
    def join_strings(strings: Iterable[str], separator: str = "") -> str:
        """
        Кастомная реализация объединения строк
        Работает как str.join() но без использования встроенного метода.

        Args:
            strings (Iterable[str]): Итерируемый объект со строками для объединения
            separator (str): Строка для вставки между объединяемыми строками (по умолчанию "")

        Returns:
            str: Объединенная строка с разделителями
        """
        result = ""
        for i, s in enumerate(strings):
            if i > 0:
                result += separator
            result += s
        return result
