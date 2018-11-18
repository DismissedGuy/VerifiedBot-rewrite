import os
import datetime

class logging_dir():
    @property
    def amount(self):
        return len([f for f in os.listdir('logs/msgcount/') if f.endswith('.json')])

    @property
    def size(self):
        return sum(os.path.getsize(f'logs/msgcount/{f}') for f in os.listdir('logs/msgcount/') if f.endswith('.json'))

def get_log_info():
    return logging_dir()

def get_logname():
    """Returns a relative path of the current log file name."""
    now = datetime.datetime.utcnow()
    filename = now.strftime('%d.%m.%Y')
    return f'logs/msgcount/{filename}.json'
