import datetime


def year(*args):
    """Возвращает год, который отображается в подвале каждой страницы сайта"""
    year = datetime.datetime.now().strftime("%Y")
    return {
        'year': year,
    }
