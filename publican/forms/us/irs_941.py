from datetime import datetime, timedelta

def quarters(start, end):
    y = start.year
    q = (start.month + 2) // 3
    while datetime(y, q * 3 - 2, 1) < end:
        yield '{}-Q{}'.format(y, q)
        y, q = (y + 1, 1) if (q == 4) else (y, q + 1)

def periods(company):
    return list(quarters(company.incorporation_date, company.now))
