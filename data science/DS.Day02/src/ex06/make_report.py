#!/usr/bin/env python3
import logging
from config import DATA_FILE, REPORT_FILE
from analytics import Research, Analytics

def create_report():
    try:
        data = Research.file_reader(DATA_FILE)
        logging.info(f"Прочитано {len(data)} наблюдений")
        analytics = Analytics(data)
        
        heads, tails = analytics.counts()
        head_percent, tail_percent = analytics.fractions()
        
        predictions = analytics.predict_random(3)
        last_prediction = analytics.predict_last()
        
        report_content = f"""Отчет
Всего наблюдений: {len(data)}
Орлы: {heads} ({head_percent:.1f}%)
Решки: {tails} ({tail_percent:.1f}%)

Предсказания:

Следующие 3 броска: {', '.join(['Орел' if p[0] == 1 else 'Решка' for p in predictions])}
На основе последнего: {'Орел' if last_prediction[0] == 1 else 'Решка'}"""

        with open(REPORT_FILE, 'w', encoding='utf-8') as report:
            report.write(report_content)
        
        logging.info(f"Отчет сохранен в {REPORT_FILE}")
        
        Research.send_telegram_message(success=True)
        return True
        
    except Exception as e:
        logging.error(f"Ошибка создания отчета: {e}")
        Research.send_telegram_message(success=False)
        return False

if __name__ == '__main__':
    create_report()
