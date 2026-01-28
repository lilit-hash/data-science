#!/usr/bin/env python3
from analytics import Research, Analytics
import config

def analyze_data(file_path):
    try:
        research = Research(file_path)
        data = research.file_reader()
        analytics = Analytics(data, config.NUM_STEPS)  

        observations = len(data)
        heads, tails = analytics.counts()
        heads_percent, tails_percent = analytics.fractions()
        
        predictions = analytics.predict_random()
        pred_heads = sum(p[0] for p in predictions)
        pred_tails = config.NUM_STEPS - pred_heads

        report = config.REPORT_TEMPLATE.format(
            observations=observations,
            heads=heads,
            tails=tails,
            heads_percent=heads_percent,
            tails_percent=tails_percent,
            num_steps=config.NUM_STEPS,
            pred_heads=pred_heads,
            pred_tails=pred_tails
        )

        report_file = analytics.save_file(report, 'report')
        print(f"Отчет успешно сохранен в {report_file}")
        return report

    except Exception as e:
        print(f"Ошибка: {e}")
        raise

if __name__ == '__main__':
    analyze_data('data.csv')