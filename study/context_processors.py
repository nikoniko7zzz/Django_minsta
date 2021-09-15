from .models import Category


def common(request: object) -> object:
    # テンプレートに毎回渡すデータ
    context = {
        'category_list': Category.objects.all(),
    }
    return context
