from multiprocessing import context
from .models import Category


def get_all_category(request):
    categories=Category.objects.all()
    context={
        'categories':categories,
    }
    return context