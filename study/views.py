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
from django_pandas.io import read_frame


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

@login_required
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

@login_required
def GraphView(request):

        # recordデータの加工///
    record_data = Record.objects.all()
    record_df = read_frame(record_data, fieldnames=['author', 'created_at', 'category', 'time'])
    record_df1 = record_df.replace({'国語':5, '数学':4, '英語':3, '理科':2, '社会':1})
    record_df1['date'] = record_df1['created_at'].dt.strftime("%Y-%m-%d") # 日付の加工//
    record_df1['time_int'] = record_df1['time'].str[:-1].astype(int) # 時間の加工
    record_df2 = record_df1.drop(['created_at', 'time','author'], axis=1) # 列の削除

    # 日付一覧作成
    base = datetime.date.today() #今日の日付
    datenum = 14
    dates = base - np.arange(datenum) * datetime.timedelta(days=1)
    dates_df = pd.DataFrame({'date':dates})
    dates_df['category'] = int(1) #日付データにいったんカテゴリ列(国語)を作成
    dates_df.loc[datenum] = [base,2]
    dates_df.loc[datenum+1] = [base,3]
    dates_df.loc[datenum+2] = [base,4]
    dates_df.loc[datenum+3] = [base,5]

    dates_df['time_int'] = 0 #日付データにいったんカテゴリ列(国語)を作成

    # 結合表作成
    comb_df = pd.merge(dates_df, record_df2, on=['date','category','time_int'], how='outer') #結合
    comb_df['date_str'] = comb_df['date'].astype(str)
    comb_df1 = comb_df.drop(['date'], axis=1) # 列の削除
    comb_df2 = comb_df1.pivot_table(index='category', columns='date_str', values='time_int', aggfunc='sum') # クロス集計表の作成
    # cate_list=[1,2,3,4,5]
    # add_colum = [i for i in cate_list if i not in comb_df2.columns] #集計データにない列を探す
    # comb_df2[[add_colum]]=int(0) # 集計データにない列を追加する

    # comb_df3 = comb_df2.sort_values('date_str', ascending=False).fillna(0)
    comb_df3 = comb_df2.fillna(0)





    subject = ['国語','数学','英語','理科','社会']

    # z = np.random.poisson(size=(len(subject), len(dates)))
    z = comb_df3
    x = dates[::-1] #逆順にする 今日を左にする
    # y = subject[::-1]
    fig = go.Figure(
        data=go.Heatmap(
            z=z,  #色が変化するデータ
            x=x, #X軸
            y=subject[::-1],   #Y軸
            # x=(1, 7),  # 縦軸ラベルに表示する値、10刻み
            # opacity=0.5,  # マップの透明度を0.5に
            colorbar=dict(
                # len=0.8,  # カラーバーの長さを0.8に（デフォルトは1）
                outlinecolor='gray',  # カラーバーの枠線の色
                outlinewidth=1,  # カラーバーの枠線の太さ
                # bordercolor='gray',  # カラーバーとラベルを含むカラーバー自体の枠線の色
                # borderwidth=1,  # カラーバーとラベルを含むカラーバー自体の枠線の太さ
                title=dict(
                    text='分',
                    side='top',  # カラーバーのタイトルをつける位置（デフォルトはtop）
                ),
            ),
            # colorscale='BuPu'
            colorscale=[
                [0, 'rgb(255,255,255)'],  # NaNに該当する値を灰色にして区別する
                [1, 'rgb(255,20,147)']
            # # zmin=0,  # カラーバーの最小値
            # # zmax=5,  # カラーバーの最大値
            ],
        ),
    )

    layout = go.Layout(
        title='Study day',
        # width=400, #図の幅を指定
        # height=50,
        # xaxis=dict(
        #     title='subject'
        # ),
        yaxis=dict(
            # title='y'
            scaleanchor = 'x', # マス目をxと同じスケールにする
            # scaleratio=1,
            autorange = 'reversed',
        ),
        # xaxis = axis_template,
        # yaxis = axis_template,
        # showlegend = False,
        # width = 700, height = 100,
        # autosize = False
    )


    # )
    # fig.update_layout(
    #     title='Study day',
    #     # width=400, #図の幅を指定
    #     # height=400,

    # )

    fig.update_traces(
        ygap=2, #y軸の隙間
        xgap=2, #x軸の隙間
        # yaxis=10,
        # y0=1,
        # dy=2,
        selector=dict(type='heatmap'))

    plot_fig = fig.to_html(fig, include_plotlyjs=False)
    return render(request, "study/graph.html", {
       "graph": plot_fig
    })


