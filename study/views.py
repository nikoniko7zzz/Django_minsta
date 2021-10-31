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
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():  # フォームに入力された値にエラーがないかをバリデートする
            post = form.save(commit=False)
            post.author = request.user  # ログインユーザーをformに入れている
            post.save()
            print('テスト結果を記録しました。')
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

# /////////////////////////////////////////////////////////////
# /  グラフ表示画面      //////////////////////////////////////
# /////////////////////////////////////////////////////////////


# @login_required
# def GraphView(request):

#     # recordデータの加工///
#     record_data = Record.objects.filter(author=request.user).all()
#     record_df = read_frame(record_data, fieldnames=[
#                            'author', 'created_at', 'category', 'time'])
#     record_df1 = record_df.replace(
#         {'国語': 5, '数学': 4, '英語': 3, '理科': 2, '社会': 1})
#     record_df1['date'] = record_df1['created_at'].dt.strftime(
#         "%Y-%m-%d")  # 日付の加工//
#     record_df1['time_int'] = record_df1['time'].astype(int)  # 時間の加工
#     record_df2 = record_df1.drop(['created_at', 'author'], axis=1)  # 列の削除
#     # record_df2.dtypes データの型の確認

#     # 日付一覧作成
#     base = datetime.date.today()  # 今日の日付
#     datenum = 60  # 表示したい日数
#     # dayday=request.user.created_at
#     dates = base - np.arange(datenum) * datetime.timedelta(days=1)
#     # dates = base - np.arange(dayday) * datetime.timedelta(days=1)
#     dates_df = pd.DataFrame({'date': dates})
#     dates_df['category'] = int(1)  # 日付データにいったんカテゴリ列(国語)を作成
#     dates_df.loc[datenum] = [base, 2]  # 最後の行にデータ追加 カテゴリを用意
#     dates_df.loc[datenum + 1] = [base, 3]
#     dates_df.loc[datenum + 2] = [base, 4]
#     dates_df.loc[datenum + 3] = [base, 5]
#     dates_df['time_int'] = int(0)  # 日付データにいったん時間をを作成
#     # dates_df.dtypes データの型の確認

#     # 結合表作成
#     comb_df = pd.merge(dates_df, record_df2, on=[
#                        'date', 'category', 'time_int'], how='outer')  # 結合
#     comb_df['date_str'] = comb_df['date'].astype(str)
#     comb_df1 = comb_df.drop(['date'], axis=1)  # 列の削除
#     comb_df2 = comb_df1.pivot_table(
#         index='category', columns='date_str', values='time_int', aggfunc='sum')  # クロス集計表の作成
#     # cate_list=[1,2,3,4,5]
#     # add_colum = [i for i in cate_list if i not in comb_df2.columns] #集計データにない列を探す
#     # comb_df2[[add_colum]]=int(0) # 集計データにない列を追加する

#     # comb_df3 = comb_df2.sort_values('date_str', ascending=False).fillna(0)
#     comb_df3 = comb_df2.fillna(0)

#     subject = ['国', '数', '英', '理', '社']

#     # z = np.random.poisson(size=(len(subject), len(dates)))
#     heatmap_z = comb_df3
#     x = dates[::-1]  # 逆順にする 今日を左にする
#     # y = subject[::-1]

#     # plot =[]

#     fig = go.Figure(data=go.Heatmap(
#         # d = go.Heatmap(
#         z=heatmap_z,  # 色が変化するデータ
#         x=x,  # X軸
#         y=subject[::-1],   # Y軸
#         # # x=(1, 7),  # 縦軸ラベルに表示する値、10刻み
#         # # opacity=0.5,  # マップの透明度を0.5に
#         colorbar=dict(
#             thickness=10,
#             thicknessmode='pixels',
#             len=1.1,  # カラーバーの長さを0.8に（デフォルトは1）
#             lenmode='fraction',
#             outlinewidth=0,
#             # outlinecolor='gray',  # カラーバーの枠線の色
#             # outlinewidth=1,  # カラーバーの枠線の太さ
#             # bordercolor='gray',  # カラーバーとラベルを含むカラーバー自体の枠線の色
#             # borderwidth=1,  # カラーバーとラベルを含むカラーバー自体の枠線の太さ
#             title=dict(
#                 text='分',
#                 side='top')  # カラーバーのタイトルをつける位置（デフォルトはtop）
#         ),
#         colorscale=[
#             [0, 'rgb(17, 17, 17)'],  # NaNに該当する値を区別する
#             [0.01, 'rgb(255,255,255)'],  # NaNに該当する値を灰色にして区別する
#             [1, 'rgb(255,20,147)']
#         ]
#     ))

#     # plot.append(d)

#     # layout = go.Layout(
#     # autosize = True,   # HTMLで表示したときページに合わせてリサイズするかどうか
#     # width=700, #図の幅を指定
#     # height=450,
#     # margin=dict(l=50, r=50, t=100, b=50, autoexpand=False),
#     # height=450,
#     # width=700,

#     #     # layout = go.Layout(
#     fig.update_layout(
#         # title='Study time',
#         width=380,
#         height=210,
#         template='plotly_dark',
#         plot_bgcolor = '#212529',
#         margin=dict(     # グラフ領域の余白設定
#             l=15, r=30, t=30, b=10,
#             pad = 0,         # グラフから軸のラベルまでのpadding
#             autoexpand=True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
#         )
#     )

#     fig.update_traces(
#         # xaxis=dict(showgrid=False),
#         # yaxis=dict(
#         #     showgrid=False,
#         #     scaleanchor=x, #Y軸のスケールをX軸と同じに
#         #     scaleratio =1,
#         #     autorange = 'reversed'),
#         ygap=2,  # y軸の隙間
#         xgap=2  # x軸の隙間
#     )

#     fig.update_xaxes(
#         title=None, # X軸タイトルを指定
#         # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
#         rangeslider={"visible":True}, # X軸に range slider を表示（下図参照）
#     )


#     plot_fig_heatmap = fig.to_html(fig, include_plotlyjs=False)
#     # heatmapとlineグラフとまとめて返すため、コメントアウト
#     # return render(request, "study/graph.html", {
#     #     "graph_heatmap": plot_fig_heatmap
#     # })

# # /  ライングラフ  ////////////////////////////////////////////

#     # Testデータの加工///
#     test_data = Test.objects.filter(author=request.user).all() #テストデータ
#     test_df = read_frame(test_data) #dfにする
#     test_df1 = test_df.rename(
#         columns={'japanese': '国', 'math': '数', 'english': '英', 'science': '理', 'social_studies': '社'})
#     test_df2 = test_df1.sort_values('date', ascending=False)

#     # test_df2.dtypes データの型の確認

#     fig_line = px.line(
#         test_df2, #データ
#         x='date',
#         y=['国', '数', '英', '理', '社'],
#         color_discrete_sequence=['#ffff7a', '#ff77af', '#7affbc', '#7a7aff', '#ffbc7a'])

#     fig_line.update_xaxes(
#         title=None, # X軸タイトルを指定
#         # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
#         rangeslider={"visible":True}, # X軸に range slider を表示（下図参照）
#         )

#     fig_line.update_yaxes(
#         title=None, # Y軸タイトルを指定
#         autorange = 'reversed', # y軸を逆にする ランキング上位が上表示にした
#         # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
#         # scaleanchor="x",
#         # scaleratio=1, # Y軸のスケールをX軸と同じに（plt.axis("equal")
#         )

#     fig_line.update_layout(
#         showlegend=True, # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
#         # xaxis_type="linear",
#         # yaxis_type="log", # X軸はリニアスケール、Y軸はログスケールに
#         width=380,
#         height=320, # 図の高さを幅を指定
#         template='plotly_dark',
#         plot_bgcolor = '#212529',
#         legend=dict(
#             xanchor='left',
#             yanchor='bottom',
#             x=0.02, #左下を(0,0)、右上を(1,1)
#             y=1,
#             orientation='h',
#             title=None,
#         ),
#         margin = dict(     # グラフ領域の余白設定
#             l=15, r=30, t=40, b=40,
#             pad=0,         # グラフから軸のラベルまでのpadding
#             autoexpand = True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
#         )
#     )

#     plot_fig_line = fig_line.to_html(include_plotlyjs='cdn',
#                                  full_html=False).encode().decode('unicode-escape')




#     # /  heatmapとライングラフを返す  ////////////////////////////////////////////
#     return render(request, "study/graph.html", {
#         "graph_heatmap": plot_fig_heatmap,
#         "graph_line": plot_fig_line
#     })













# @login_required
# def GraphView(request):


#     # データが入っていないときは、入力ページに飛ばす
#     record_data = Record.objects.filter(author=request.user).all()

#     record_df = read_frame(record_data, fieldnames=[
#                            'author', 'created_at', 'category', 'time'])
#     record_df = record_df.replace(
#         {'国語': '1', '数学': '2', '英語': '3', '理科': '4', '社会': '5'})
#     record_df['date'] = record_df['created_at'].dt.strftime(
#         "%Y-%m-%d")  # 日付の加工//
#     record_df["date"] = pd.to_datetime(record_df["date"])
#     record_df['time'] = record_df['time'].astype(int)  # 時間の加工
#     record_df = record_df.drop(['created_at', 'author'], axis=1)  # 列の削除
#     # category        date  time
#     # 0         1  2021-10-02        30
#     # 1         2  2021-10-02        40
#     # 2         3  2021-10-02       100
#     # 3         1  2021-10-01       100


#     # ログインユーザー作成日を取得
#     result = User.objects.get(id=request.user.id)
#     user_date = result.date_joined
#     # print(result.date_joined)
#     # print(type(result.date_joined))
#     # user_date = datetime.datetime.date(result.date_joined)
#     # print(user_date)
#     # print(type(user_date))
#     # user_date = datetime.datetime.strptime(user_date, '%Y-%m-%d')

#     print('user_date= ', user_date)
#     print(type(user_date))


#     test_df = Test.objects.filter(author=request.user).all()
#     test_df = read_frame(test_df)
#     # print('test_df= ',test_df)
#     test_df = test_df.rename(
#         columns={'japanese': '1', 'math': '2', 'english': '3', 'science': '4', 'social_studies': '5'})
#     # test_df["date"] = pd.to_datetime(test_df["date"], format='%Y-%m-%d')
#     # test_df["date"] = pd.to_datetime(test_df["date"])
#     # test_df["date"] = test_df["date"].strftime('%Y-%m-%d')

#     # x = np.datetime64('2010-06-01T00:00:00.000000000')
#     # x = pd.to_datetime(x)
#     # x.strftime('%Y-%m-%d')

#     # print(test_df["date"])
#     # print(test_df["date"].dtypes)
#     test_df = test_df.sort_values('date', ascending=False)
#     # id   1   2   3   4   5        date                   author
#     # 14  20  80  80  80  80  80  2021-11-07  matsuokuniko7@gmail.com
#     # 13  19  88  90  99  90  88  2021-10-31  matsuokuniko7@gmail.com
#     # df[-5:]
#     # df['stock'].values[0])
#     # loc[[0, 2], 'id']
#     # data['val1'][-2]
#     # df['stock'].values[0])
#     d = test_df['date'].values[-1]

#     tstr = '2012-12-29 13:49:37'
# tdatetime = dt.strptime(tstr, '%Y-%m-%d %H:%M:%S')
#     print('d=',d)
#     d = date(2020, 4, 20)
#     dt = datetime.combine(d, time())
#     print(pytz.timezone('Asia/Tokyo').localize(dt))
#     dt = datetime.combine(d, time())
#     print(pytz.timezone('Asia/Tokyo').localize(dt))
#     # test_df_old_date1 = datetime.datetime.strptime(test_df_old_date, "%d/%m/%Y %H:%M:%S")
#     # test_df_old_date = datetime.datetime(test_df_old_date)
#     datetime.combine(d, time())
#     print('test_df_old_date= ', test_df_old_date)
#     print(type(test_df_old_date))


#     base = datetime.datetime.today()  # 今日の日付
#     # グラフ作成の一番古い日を選ぶ
#     if user_date - test_df_old_date >= 0:
#         last_day = base - user_date
#     else:
#         last_day = base - test_df_old_date

#     dates = base - np.arange(last_day) * datetime.timedelta(days=1) #グラフ作成の一番古い日〜今日までの日付

#     dates_df = pd.DataFrame({'date': dates, 'category':'1', 'time_int':int(0)}) #日付データ作成
#     dates_df_5cate = pd.DataFrame([
#                             [base, '1', int(0)],
#                             [base, '2', int(0)],
#                             [base, '3', int(0)],
#                             [base, '4', int(0)],
#                             [base, '5', int(0)]],
#                             columns=['date', 'category', 'time_int'])

#     base_df = pd.concat([dates_df, dates_df_5cate])
#     #             date category  time_int
#     # 0  2021-10-25        1         0
#     # 1  2021-10-24        1         0
#     # 2  2021-10-23        1         0
#     # 3  2021-10-22        1         0
#     # 0  2021-10-25        2         0
#     # 1  2021-10-25        3         0
#     # 2  2021-10-25        4         0
#     # 3  2021-10-25        5         0


#     # 結合表作成
#     # record_df3 = pd.concat([record_df2, base_df]).sort_values('date')

#     record_df3 = pd.merge(record_df2, base_df, how='outer')  # 結合
#     record_df3['date_str'] = record_df3['date'].astype(str)
#     # record_df4 = record_df3.sort_values('date_str')

#     record_df4 = record_df3.pivot_table(
#         index='date_str', columns='category', values='time_int', aggfunc='sum')  # クロス集計表の作成
#     record_df5 = record_df4.fillna(0)
#     # category        1      2      3      4      5
#     # date_str
#     # 2021-09-01    0.0    0.0    0.0   90.0    0.0
#     # 2021-09-10   40.0    0.0    0.0    0.0    0.0
#     # 2021-09-13    0.0    0.0    0.0    0.0   60.0

#     subject = ['国', '数', '英', '理', '社']

#     # z = np.random.poisson(size=(len(subject), len(dates)))
#     heatmap_z = record_df5
#     x = dates[::-1]  # 逆順にする 今日を左にする



    # # Stacked Subplots with Shared X-Axes ///////////
@login_required
def GraphView(request):
    # データが入っていないときは、入力ページに飛ばす
    record_data = Record.objects.filter(author=request.user).all()
    test_data = Test.objects.filter(author=request.user).all() #テストデータ
    if record_data.count() == 0 and test_data.count() == 0:
        return redirect('study:two_input')


    # recordデータの加工///
    record_df = read_frame(record_data, fieldnames=[
                           'author', 'created_at', 'category', 'time'])
    record_df1 = record_df.replace(
        {'国語': 5, '数学': 4, '英語': 3, '理科': 2, '社会': 1})
    record_df1['date'] = record_df1['created_at'].dt.strftime(
        "%Y-%m-%d")  # 日付の加工//
    record_df1['time_int'] = record_df1['time'].astype(int)  # 時間の加工
    record_df2 = record_df1.drop(['created_at', 'author'], axis=1)  # 列の削除
    # record_df2.dtypes データの型の確認

    # 日付一覧作成
    base = datetime.date.today()  # 今日の日付
    datenum = 60  # 表示したい日数
    dates = base - np.arange(datenum) * datetime.timedelta(days=1)
    dates_df = pd.DataFrame({'date': dates})
    dates_df['category'] = int(1)  # 日付データにいったんカテゴリ列(国語)を作成
    dates_df.loc[datenum] = [base, 2]  # 最後の行にデータ追加 カテゴリを用意
    dates_df.loc[datenum + 1] = [base, 3]
    dates_df.loc[datenum + 2] = [base, 4]
    dates_df.loc[datenum + 3] = [base, 5]
    dates_df['time_int'] = int(0)  # 日付データにいったん時間をを作成
    # dates_df.dtypes データの型の確認

    # 結合表作成
    comb_df = pd.merge(dates_df, record_df2, on=[
                       'date', 'category', 'time_int'], how='outer')  # 結合
    comb_df['date_str'] = comb_df['date'].astype(str)
    comb_df1 = comb_df.drop(['date'], axis=1)  # 列の削除
    comb_df2 = comb_df1.pivot_table(
        index='category', columns='date_str', values='time_int', aggfunc='sum')  # クロス集計表の作成
    # cate_list=[1,2,3,4,5]
    # add_colum = [i for i in cate_list if i not in comb_df2.columns] #集計データにない列を探す
    # comb_df2[[add_colum]]=int(0) # 集計データにない列を追加する

    # comb_df3 = comb_df2.sort_values('date_str', ascending=False).fillna(0)
    comb_df3 = comb_df2.fillna(0)

    subject = ['国', '数', '英', '理', '社']

    # z = np.random.poisson(size=(len(subject), len(dates)))
    heatmap_z = comb_df3
    x = dates[::-1]  # 逆順にする 今日を左にする
    # y = subject[::-1]

    # plot =[]


    # グラフ作成    /////////////////////////////////////////////
    fig_two = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
    )

    fig_two.add_trace(

        go.Heatmap(
            x=x,
            y=subject[::-1],
            z=heatmap_z,
            # # # x=(1, 7),  # 縦軸ラベルに表示する値、10刻み
            # # # opacity=0.5,  # マップの透明度を0.5に
            showlegend=True, # 凡例を強制的に表示
            colorbar_tickangle=-90, #目盛り数字の角度
            colorbar_y=0.75, #たて位置
            colorbar=dict(
                thickness=10,
                thicknessmode='pixels',
                len=0.5,  # カラーバーの長さを0.8に（デフォルトは1）
                lenmode='fraction',
                outlinewidth=0,
                # outlinecolor='gray',  # カラーバーの枠線の色
                # outlinewidth=1,  # カラーバーの枠線の太さ
                # bordercolor='gray',  # カラーバーとラベルを含むカラーバー自体の枠線の色
                # borderwidth=1,  # カラーバーとラベルを含むカラーバー自体の枠線の太さ
                title=dict(
                    text='分',
                    side='top')  # カラーバーのタイトルをつける位置（デフォルトはtop）
            ),
            colorscale=[
                [0, 'rgb(17, 17, 17)'],  # NaNに該当する値を区別する
                [0.01, 'rgb(255,255,255)'],  # NaNに該当する値を灰色にして区別する
                [1, 'rgb(255,20,147)']
            ],
            # update_layout(
            #     # title='Study time',
            #     width=380,
            #     height=210,
            #     template='plotly_dark',
            #     plot_bgcolor = '#212529',
            #     margin=dict(     # グラフ領域の余白設定
            #         l=15, r=30, t=30, b=10,
            #         pad = 0,         # グラフから軸のラベルまでのpadding
            #         autoexpand=True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
            #     )
            # ),
            # fig.update_traces(
            ygap=1,  # y軸の隙間
            xgap=1 # x軸の隙間
            # ),
            # update_xaxes(
            #     title=None, # X軸タイトルを指定
            #     # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
            #     rangeslider={"visible":True}),# X軸に range slider を表示（下図参照）
        ),

        row=1,col=1
    )


# /  ライングラフ  ////////////////////////////////////////////

    # Testデータの加工///
    test_data = Test.objects.filter(author=request.user).all() #テストデータ
    test_df = read_frame(test_data) #dfにする
    test_df = read_frame(test_data, fieldnames=[
                        #    'author', 'created_at', 'category', 'time'])
                           'japanese', 'math', 'english', 'science', 'social_studies', 'date', 'author', 'created_at'])

    test_df1 = test_df.rename(
        columns={'japanese': '国', 'math': '数', 'english': '英', 'science': '理', 'social_studies': '社'})
    test_df2 = test_df1.sort_values('date', ascending=False)



    fig_two.add_trace(go.Scatter(
            x=test_df2['date'], y=test_df2['国'], mode="lines+markers",
            marker=dict(color='#ffff00'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            x=test_df2['date'], y=test_df2['数'], mode="lines+markers",
            marker=dict(color='#7f00f0'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            x=test_df2['date'], y=test_df2['英'], mode="lines+markers",
            marker=dict(color='#ff0000'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            x=test_df2['date'], y=test_df2['理'], mode="lines+markers",
            marker=dict(color='#0000ff'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            x=test_df2['date'], y=test_df2['社'], mode="lines+markers",
            marker=dict(color='#00ff00'),
        ),
        row=2, col=1
    )

        # test_df2, #データ
        # x='date',
        # y=['国', '数', '英', '理', '社'],
        # color_discrete_sequence=['#ffff7a', '#ff77af', '#7affbc', '#7a7aff', '#ffbc7a'],
        # update_xaxes(
        #     title=None, # X軸タイトルを指定
        #     # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
        #     rangeslider={"visible":True}, # X軸に range slider を表示（下図参照）
        # ),
        # update_yaxes(
        #     title=None, # Y軸タイトルを指定
        #     autorange = 'reversed', # y軸を逆にする ランキング上位が上表示にした
        # ),
        # update_layout(
        #     showlegend=True, # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
        #     # xaxis_type="linear",
        #     # yaxis_type="log", # X軸はリニアスケール、Y軸はログスケールに
        #     # width=380,
        #     # height=320, # 図の高さを幅を指定
        #     template='plotly_dark',
        #     plot_bgcolor = '#212529',
        #     legend=dict(
        #         xanchor='left',
        #         yanchor='bottom',
        #         x=0.02, #左下を(0,0)、右上を(1,1)
        #         y=1,
        #         orientation='h',
        #         title=None,
        #     ),
        #     margin = dict(     # グラフ領域の余白設定
        #         l=15, r=30, t=40, b=40,
        #         pad=0,         # グラフから軸のラベルまでのpadding
        #         autoexpand = True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
        #     ),
        # ),

    fig_two.update_layout(
        # title='Study time',
        width=380,
        # height=210,
        showlegend=False, # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
        template='plotly_dark',
        plot_bgcolor = '#212529',
        margin=dict(     # グラフ領域の余白設定
            l=15, r=30, t=30, b=10,
            pad = 0,         # グラフから軸のラベルまでのpadding
            autoexpand=True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
        ),
        # xaxis=dict(
        #     rangeslider=dict(
        #         visible=True
        #     ),
        #     type="date"
        # )
    )

    fig_two_graph = fig_two.to_html(include_plotlyjs='cdn',
                                 full_html=False).encode().decode('unicode-escape')

    # /  heatmapとライングラフを返す  ////////////////////////////////////////////
    return render(request, "study/graph.html", {
        "graph_heatmap": fig_two_graph,
    })
