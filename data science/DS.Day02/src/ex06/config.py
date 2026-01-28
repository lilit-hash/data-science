import os
import logging

DATA_FILE = "data.csv"
REPORT_FILE = "report.txt"
ANALYTICS_LOG = "analytics.log"
TELEGRAM_BOT_TOKEN = "8290143048:AAHZ9YBE0QZgsmVnZtfm2QeWG9SKl3LPxKQ"  
TELEGRAM_CHAT_ID = "976825900"     

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(ANALYTICS_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)