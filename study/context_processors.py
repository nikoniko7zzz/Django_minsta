import itertools
from .models import Category
from django.conf import settings


def common(request: object) -> object:
    # テンプレートに毎回渡すデータ
    context = {
        'category_list': Category.objects.all(),
    }
    return context
