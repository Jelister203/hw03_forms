import datetime


def year(*args):
    year = datetime.datetime.now().strftime("%Y")
    return {
        'year': year,
    }
