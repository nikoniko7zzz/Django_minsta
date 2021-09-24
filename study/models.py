from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.contrib.auth.models import User


class Category(models.Model):
    # カテゴリ 管理画面でのみ編集できる
    name = models.CharField('カテゴリ名', max_length=255)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    # 管理サイトでの一覧表示用

    def __str__(self):
        return self.name


class Post(models.Model):
    # 問題の投稿
    title = models.TextField('問題', max_length=255)
    text = models.TextField('答え')

    created_at = models.DateTimeField('作成日', default=timezone.now)
    # on_delete = models.PROTECT カテゴリモデルと紐づいているから削除できない
    category = models.ForeignKey(
        Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # author = models.ForeignKey(User,on_delete=models.CASCADE)
    # author = models.ForeignKey(get_user_model(),on_delete=CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # ブログのコメント
    name = models.CharField('お名前', max_length=30, default='名無し')
    text = models.TextField('コメント')
    post = models.ForeignKey(Post, verbose_name='紐づく記事',
                             on_delete=models.PROTECT)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:10]
