NUM_STEPS = 3  
REPORT_TEMPLATE = """

Сделала {observations} наблюдений при подбрасывании монеты: {heads} из них — решка, {tails} — орел.
Вероятности составляют {heads_percent:.2f}% и {tails_percent:.2f}% соответственно.
Прогноз: в следующих {num_steps} наблюдениях выпадет {pred_heads} раз(а) решка и {pred_tails} раз(а) орел.
"""