import logging
import requests
from random import randint
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class Calculations:
    def __init__(self, data):
        self.data = data
      
    def counts(self):
        logging.info("Подсчет количества орлов и решек")
        heads = sum(pair[0] for pair in self.data)
        tails = len(self.data) - heads
        return heads, tails
    
    def fractions(self):
        logging.info("Расчет процентов")
        heads, tails = self.counts()
        total = heads + tails
        if total == 0:
            return 0.0, 0.0
        return heads/total*100, tails/total*100

class Analytics(Calculations):
    def __init__(self, data):
        super().__init__(data)
    def predict_random(self, n):
        logging.info(f"Генерация {n} случайных предсказаний")
        predictions = []
        for _ in range(n):
            first = randint(0, 1)
            predictions.append([first, 1 - first])
        return predictions
    def predict_last(self):
        logging.info("Получение последнего наблюдения")
        if not self.data:
            return None
        return self.data[-1]

class Research:
    @staticmethod
    def file_reader(file_path, has_header=True):
        logging.info(f"Чтение файла {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
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
        logging.info(f"Прочитано {len(data)} записей")
        return data

    @staticmethod
    def send_telegram_message(success=True):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.warning("Токен Telegram не настроен")
            return
        try:
            message = "Отчет успешно создан" if success else "Отчёт не создан из-за ошибки"
            logging.info(f"Отправка в Telegram: {message}")
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            }
            response = requests.post(url, data=payload, timeout=5)
            response.raise_for_status()
            logging.info("Уведомление отправлено в Telegram")
        except Exception as e:
            logging.error(f"Не удалось отправить в Telegram: {e}")