from re import X
from django.db.models import Q
from django.http import request
from django.http.response import HttpResponse  # Qオブジェクトは、モデルのデータの中からor検索をする
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from plotly import graph_objs
from .forms import RecordCreateForm, TestForm, PostCreateForm
from .models import Post, Category, Comment, Record, Test
from register.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages  # ラジオ
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
# from django.contrib.auth.models import User

# グラフ用///////////////////////////////
import plotly.graph_objects as go
# import plotly.express as px
import pandas as pd
import datetime
# from datetime import datetime, date, time
import pytz
import numpy as np
import plotly.io as pio
import plotly.offline as po
import plotly.figure_factory as ff
from django_pandas.io import read_frame
import plotly.express as px  # 折線グラフで追加
from plotly.subplots import make_subplots #グラフの融合

# heroku用 エラー500の時に内容を表示させる//////////////////////////////////
# from django.views.decorators.csrf import requires_csrf_token
# from django.http import HttpResponseServerError

# @requires_csrf_token
# def my_customized_server_error(request, template_name='500.html'):
#     import sys
#     from django.views import debug
#     error_html = debug.technical_500_response(request, *sys.exc_info()).content
#     return HttpResponseServerError(error_html)
# heroku用 エラー500の時に内容を表示させる//////////////////////////////////




# render 単純なテンプレートとしてHttpResponseをreturnするときのショートカット
# reverse url.pyで決めた名前を解析する関数
# reverse_lazy reverseをクラスベースビューのクラス変数として書くときに利用


def RecordInputView(request):
    # params = {'message': 'newです'}
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = RecordCreateForm(request.POST)
        if form.is_valid():  # フォームに入力された値にエラーがないかをバリデートする
            post = form.save(commit=False)
            post.author = request.user  # ログインユーザーをformに入れている
            post.save()
            print('時間を作成しました。')
            # print(post)
            return redirect('study:graph')
        else:
            params['message'] = '再入力してください'
            params['form'] = form
    else:
        params['form'] = RecordCreateForm()
    return render(request, 'study/record_input.html', params)



# ◆◆◆◆◆◆◆◆◆↓↓↓今回実装なし↓↓↓◆◆◆◆◆◆◆◆◆
# カテゴリ検索
class CategoryView(generic.ListView):
    # カテゴリ別のリスト
    model = Post
    paginate_by = 10

    def get_queryset(self):
        """
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Post.objects.order_by('-created_at').filter(category=category)
        """
        category_pk = self.kwargs['pk']
        queryset = Post.objects.order_by(
            '-created_at').filter(category__pk=category_pk)
        return queryset


# class DetailView(generic.DetailView):
#     model = Post


# class CommentView(generic.CreateView):
#     model = Comment
#     #fields = ('name', 'text')
#     form_class = CommentCreateForm

#     def form_valid(self, form):
#         post_pk = self.kwargs['post_pk']
#         comment = form.save(commit=False)  # コメントはDBに保存されていません
#         comment.post = get_object_or_404(Post, pk=post_pk)
#         comment.save()  # ここでDBに保存
#         return redirect('study:detail', pk=post_pk)




@login_required
def PostNewView(request):
    # params = {'message': 'newです'}
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():  # フォームに入力された値にエラーがないかをバリデートする
            post = form.save(commit=False)
            post.author = request.user  # ログインユーザーをformに入れている
            post.save()
            print('問題を作成しました。')
            return redirect('study:post_list')
        else:
            params['message'] = '再入力してください'
            params['form'] = form
    else:
        params['form'] = PostCreateForm()
    return render(request, 'study/post_input.html', params)

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = "study/post_list.html"

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset


# ◆◆◆◆◆◆◆◆◆↑↑↑今回実装なし↑↑↑◆◆◆◆◆◆◆◆◆


# 一覧画面
# class RecordListView(TemplateView):
class RecordListView(generic.ListView):
    # テーブル連携
    model = Record
    # レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "record_list"
    # テンプレートファイル連携
    template_name = "study/record_list.html"

# 削除画面


class RecordDeleteView(generic.DeleteView):
    model = Record
    template_name = "record_delete.html"
    # 削除後のリダイレクト先
    success_url = reverse_lazy("study:record_list")



# /////////////////////////////////////////////////////////////
# /  テスト結果登録画面  //////////////////////////////////////
# /////////////////////////////////////////////////////////////
@login_required
def TwoInputView(request):
    # params = {'message': 'newです'}
    params = {'message': '', 'test_form': None}
    print('twoinputスタート')
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():  # フォームに入力された値にエラーがないかをバリデートする
            post = form.save(commit=False)
            print('テスト結果を受け取りました。')
            # print('post= ', post)
            post.tscore_overall = (
                post.tscore_japanese + post.tscore_math + post.tscore_english + post.tscore_science
                 + post.tscore_social_studies) / 5
            post.author = request.user  # ログインユーザーをformに入れている
            print('ログインユーザーを受け取りました。')

            print('post.tscore_overall= ',post.tscore_overall)
            post.save()
            print('テスト結果を記録しました。')
            # print('post= ',post)
            # print(request.user.username)
            # print(request.user.date_joined)
            # print(post)
            return redirect('study:graph')
        else:
            params['message'] = '再入力してください'
            params['test_form'] = form
    else:
        params['test_form'] = TestForm()
    return render(request, 'study/two_input.html', params)

