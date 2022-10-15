from django.utils.timezone import now


def year(request):
    year = now().year
    return {
        'year': year,
    }
