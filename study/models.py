from config.settings import STATIC_ROOT
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


# class Record(models.Model):
#     '''勉強した時間の保存'''
#     class Meta:
#         db_table = 'Record_table'

#     CATEGORY = (
#         ('1', '国語'),
#         ('2', '数学'),
#         ('3', '英語'),
#         ('4', '理科'),
#         ('5', '社会'),
#     )
#     START_STOP = (
#         ('0', 'START'),
#         ('1', 'STOP'),
#     )
#     category = models.IntegerField(verbose_name='教科', choices=CATEGORY, default=None)
#     start_stop = models.IntegerField(verbose_name='START/STOP', choices=START_STOP, default=None)
#     time = models.TimeField(verbose_name="打刻時間")
#     date = models.DateField(verbose_name='打刻日')
#     # on_delete = models.PROTECT カテゴリモデルと紐づいているから削除できない
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.time


class Record(models.Model):
    '''勉強した時間の保存'''
    CATEGORY = (
        ('国語', '国語'),
        ('数学', '数学'),
        ('英語', '英語'),
        ('理科', '理科'),
        ('社会', '社会'),
    )
    TIME = (
        ('30', '30分'),
        ('40', '40分'),
        ('50', '50分'),
        ('60', '60分'),
        ('70', '70分'),
        ('80', '80分'),
        ('90', '90分'),
        ('100', '100分'),
    )
    category = models.CharField(verbose_name='教科', choices=CATEGORY, blank=True, null=True, max_length=10)
    time = models.CharField(verbose_name="分", choices=TIME, blank=True, null=True,  max_length=10)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    # on_delete = models.PROTECT カテゴリモデルと紐づいているから削除できない
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # '教科 - 時間' のように返す
        return '{} - {}'.format(self.category, self.time)



