import datetime

def format_dates(date_data):
    if date_data is None:
        return None
    elif isinstance(date_data, list):
        return [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in date_data if dt is not None]
    else:
        return datetime.datetime.strptime(str(date_data), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    
def ensure_list(value):
    if value is None:
        return []
    if not isinstance(value, list):
        return [value]
    return value
