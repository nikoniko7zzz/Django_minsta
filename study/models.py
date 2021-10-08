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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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


class Record(models.Model):
    '''勉強した時間の保存'''
    category = models.CharField(
        verbose_name='教科', blank=True, null=True, max_length=10)
    time = models.CharField(verbose_name="分", blank=True,
                            null=True,  max_length=10)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    # created_at = models.DateField('いつ', blank=True, null=True)
    # on_delete = models.PROTECT カテゴリモデルと紐づいているから削除できない
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # '教科 - 時間' のように返す
        return '{} - {}'.format(self.category, self.time)


class Test(models.Model):
    '''テスと結果の保存'''
    japanese = models.IntegerField(
        verbose_name='国語', blank=True, null=True)
    math = models.IntegerField(
        verbose_name='数学', blank=True, null=True)
    english = models.IntegerField(
        verbose_name='英語', blank=True, null=True)
    science = models.IntegerField(
        verbose_name='理科', blank=True, null=True)
    social_studies = models.IntegerField(
        verbose_name='社会', blank=True, null=True)
    date = models.DateField('いつまでに', blank=True,
                            null=True)  # このDateFieldが対象です。

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # '日付 - ユーザー' のように返す
        return '{} - {}'.format(self.date, self.author)
