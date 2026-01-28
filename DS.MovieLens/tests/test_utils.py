import sys
from io import StringIO
import pytest
from movielens_analytics.utils import ReportUtils


class TestReportUtils:
    """Тесты для класса ReportUtils"""

    def test_print(self):
        """Вывод текста"""
        captured_output = StringIO()
        sys.stdout = captured_output
        ReportUtils.print("тест")
        sys.stdout = sys.__stdout__
        assert captured_output.getvalue() == "тест\n"

    def test_get_length(self):
        """Получение длины коллекции"""
        assert ReportUtils.get_length([1, 2, 3]) == 3
        assert isinstance(ReportUtils.get_length("abc"), int)

    def test_to_list(self):
        """Преобразование в список"""
        result = ReportUtils.to_list((1, 2, 3))
        assert result == [1, 2, 3]
        assert isinstance(result, list)

    def test_sorted_dict(self):
        """Сортировка словаря"""
        test_dict = {"a": 3, "b": 1, "c": 2}
        result = ReportUtils.sorted_dict(test_dict, reverse=False)
        assert result == [("b", 1), ("c", 2), ("a", 3)]
        assert all(isinstance(item, tuple) for item in result)

    def test_slice_collection(self):
        """Срез коллекции"""
        result = ReportUtils.slice_collection([1, 2, 3, 4, 5], start=1, end=4)
        assert result == [2, 3, 4]
        assert isinstance(result, list)

    def test_join_strings(self):
        """Объединение строк"""
        result = ReportUtils.join_strings(["a", "b", "c"], separator=",")
        assert result == "a,b,c"
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
