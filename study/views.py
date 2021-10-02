from re import X
from django.db.models import Q  # Qオブジェクトは、モデルのデータの中からor検索をする
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .forms import CommentCreateForm, PostCreateForm, RecordCreateForm
from .models import Post, Category, Comment, Record
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# グラフ用///////////////////////////////
import plotly.graph_objects as go
# import plotly.express as px
import pandas as pd
import datetime
import numpy as np
import plotly.io as pio
import plotly.figure_factory as ff





# render 単純なテンプレートとしてHttpResponseをreturnするときのショートカット
# reverse url.pyで決めた名前を解析する関数
# reverse_lazy reverseをクラスベースビューのクラス変数として書くときに利用

class IndexView(generic.ListView):
    # リスト表示用
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')  # -で降順
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset




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


class DetailView(generic.DetailView):
    model = Post


class CommentView(generic.CreateView):
    model = Comment
    #fields = ('name', 'text')
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['post_pk']
        comment = form.save(commit=False)  # コメントはDBに保存されていません
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()  # ここでDBに保存
        return redirect('study:detail', pk=post_pk)


# class PostIndexView(generic.ListView):
#     model = Post


def PostNewView(request):
    # params = {'message': 'newです'}
    params = {'message':'', 'form':None}
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid(): #フォームに入力された値にエラーがないかをバリデートする
            post = form.save(commit=False)
            post.author = request.user #ログインユーザーをformに入れている
            post.save()
            print('問題を作成しました。')
            # return redirect('new')
        else:
            params['message'] = '再入力してください'
            params['form'] = form
    else:
        params['form'] = PostCreateForm()
    return render(request, 'study/post_input.html', params)
    # return render(request, 'study/post_input.html', params)


# 一覧画面
class RecordListView(generic.ListView):
    # テーブル連携
    model = Record
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "record_list"
    #テンプレートファイル連携
    template_name = "study/record_list.html"

#削除画面
class RecordDeleteView(generic.DeleteView):
    model = Record
    template_name = "record_delete.html"
    print('レコードを削除しました')
    #削除後のリダイレクト先
    success_url = reverse_lazy("study:record_list")


def RecordCreatView(request):
    # params = {'message': 'newです'}
    params = {'message':'', 'form':None}
    if request.method == 'POST':
        form = RecordCreateForm(request.POST)
        if form.is_valid(): #フォームに入力された値にエラーがないかをバリデートする
            post = form.save(commit=False)
            post.author = request.user #ログインユーザーをformに入れている
            post.save()
            print('時間を作成しました。')
            # print(post)
            return redirect('study:record_list')
        else:
            params['message'] = '再入力してください'
            params['form'] = form
    else:
        params['form'] = RecordCreateForm()
    return render(request, 'study/record_input.html', params)

# def RecordAddView(request):
#     t1 = Todo()
#     t1.todo_id = len(Todo.objects.order_by('-todo_id'))+1
#     t1.update_date = timezone.now()
#     t = RecordCreateForm(request.POST, instance=t1)
#     t.save()
#     return HttpResponseRedirect(reverse('index'))

# def add(request):
#     t1 = Todo()
#     t1.todo_id = len(Todo.objects.order_by('-todo_id'))+1
#     t1.update_date = timezone.now()
#     t = TodoForm(request.POST, instance=t1)
#     t.save()
#     return HttpResponseRedirect(reverse('index'))


def GraphView(request):

    # np.random.seed(1) #作成した乱数の固定

    subject = ['国語','数学','英語','理科','社会']

    base = datetime.date.today()
    dates = base - np.arange(30) * datetime.timedelta(days=1) #何日間表示するかの指定 npで日付配列取得
    z = np.random.poisson(size=(len(subject), len(dates)))

    fig = go.Figure(
        data=go.Heatmap(
            z=z,  #色が変化するデータ
            y=subject, #X軸
            x=dates,   #Y軸
            # y=(10, 20),  # 縦軸ラベルに表示する値、10刻み
            # opacity=0.5,  # マップの透明度を0.5に
            colorscale='Purp'
            # colorscale=[
            #     [0, 'blue'],  # NaNに該当する値を灰色にして区別する
            #     [1, 'rgb(255,4,97)']
            # # zmin=0,  # カラーバーの最小値
            # # zmax=5,  # カラーバーの最大値
            # ],
        ),
    )

    fig.update_yaxes(
        title="教科", # X軸タイトルを指定
    )

    fig.update_xaxes(
        title="日付",
        scaleanchor='x', # マス目をxと同じスケールにする
        scaleratio=1,


    )
    fig.update_layout(
        title='Study day',
        # width=400, #図の幅を指定
        # height=400,

    )

    fig.update_traces(
        ygap=1, #y軸の隙間
        xgap=1, #x軸の隙間
        selector=dict(type='heatmap'))

    plot_fig = fig.to_html(fig, include_plotlyjs=False)
    return render(request, "study/graph.html", {
       "graph": plot_fig
    })

