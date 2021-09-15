from django.db.models import Post

japanese_cnt = Post.objects.filter(target__category='国語').count()
math_cnt = Post.objects.filter(target__category='数学').count()
english_cnt = Post.objects.filter(target__category='英語').count()
science_cnt = Post.objects.filter(target__category='理科').count()
society_cnt = Post.objects.filter(target__category='社会').count()
