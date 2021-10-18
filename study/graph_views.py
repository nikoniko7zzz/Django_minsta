from re import X
from django.db.models import Q
from django.http.response import HttpResponse  # Qオブジェクトは、モデルのデータの中からor検索をする
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .forms import CommentCreateForm, PostCreateForm, RecordCreateForm, TestForm
from .models import Post, Category, Comment, Record, Test
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages  # ラジオ
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User

# グラフ用///////////////////////////////
import plotly.graph_objects as go
# import plotly.express as px
import pandas as pd
import datetime
import numpy as np
import plotly.io as pio
import plotly.offline as po
import plotly.figure_factory as ff
from django_pandas.io import read_frame
import plotly.express as px  # 折線グラフで追加
from plotly.subplots import make_subplots #グラフの融合



# /////////////////////////////////////////////////////////////
# /  グラフ表示画面      //////////////////////////////////////
# /////////////////////////////////////////////////////////////


@login_required
def GraphView(request):

    # recordデータの加工///
    record_data = Record.objects.filter(author=request.user).all()
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
    fig_two = make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02)

    fig_two.add_trace(go.Figure(data=go.Heatmap(
        z=heatmap_z,  # 色が変化するデータ
        x=x,  # X軸
        y=subject[::-1],   # Y軸
        # # x=(1, 7),  # 縦軸ラベルに表示する値、10刻み
        # # opacity=0.5,  # マップの透明度を0.5に
        colorbar=dict(
            thickness=10,
            thicknessmode='pixels',
            len=1.1,  # カラーバーの長さを0.8に（デフォルトは1）
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
        update_layout(
            # title='Study time',
            width=380,
            height=210,
            template='plotly_dark',
            plot_bgcolor = '#212529',
            margin=dict(     # グラフ領域の余白設定
                l=15, r=30, t=30, b=10,
                pad = 0,         # グラフから軸のラベルまでのpadding
                autoexpand=True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
            )
        ),
        fig.update_traces(
            ygap=2,  # y軸の隙間
            xgap=2  # x軸の隙間
        ),
        update_xaxes(
            title=None, # X軸タイトルを指定
            # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
            rangeslider={"visible":True}, # X軸に range slider を表示（下図参照）
        ),
        row=1,
        col=1,
    )))


# /  ライングラフ  ////////////////////////////////////////////

    # Testデータの加工///
    test_data = Test.objects.filter(author=request.user).all() #テストデータ
    test_df = read_frame(test_data) #dfにする
    test_df1 = test_df.rename(
        columns={'japanese': '国', 'math': '数', 'english': '英', 'science': '理', 'social_studies': '社'})
    test_df2 = test_df1.sort_values('date', ascending=False)

    # test_df2.dtypes データの型の確認

    fig_two.add_trace(px.line(
        test_df2, #データ
        x='date',
        y=['国', '数', '英', '理', '社'],
        color_discrete_sequence=['#ffff7a', '#ff77af', '#7affbc', '#7a7aff', '#ffbc7a']
        update_xaxes(
            title=None, # X軸タイトルを指定
            # range=(base+datetime.timedelta(days=-60),base), # X軸の最大最小値を指定
            rangeslider={"visible":True}, # X軸に range slider を表示（下図参照）
        ),
        update_yaxes(
            title=None, # Y軸タイトルを指定
            autorange = 'reversed', # y軸を逆にする ランキング上位が上表示にした
        ),
        update_layout(
            showlegend=True, # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
            # xaxis_type="linear",
            # yaxis_type="log", # X軸はリニアスケール、Y軸はログスケールに
            width=380,
            height=320, # 図の高さを幅を指定
            template='plotly_dark',
            plot_bgcolor = '#212529',
            legend=dict(
                xanchor='left',
                yanchor='bottom',
                x=0.02, #左下を(0,0)、右上を(1,1)
                y=1,
                orientation='h',
                title=None,
            ),
            margin = dict(     # グラフ領域の余白設定
                l=15, r=30, t=40, b=40,
                pad=0,         # グラフから軸のラベルまでのpadding
                autoexpand = True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
            )
        ),
        row=1,
        col=1,
    ))




    fig_two_graph = fig_two.to_html(include_plotlyjs='cdn',
                                 full_html=False).encode().decode('unicode-escape')




    # /  heatmapとライングラフを返す  ////////////////////////////////////////////
    return render(request, "study/graph.html", {
        "graph_heatmap": fig_two_graph,
    })















# # Stacked Subplots with Shared X-Axes ///////////
# @login_required
# def GraphView(request):
#     # heatmapのデータ作り
#     # lineのデータ作り
#     # グラフの作成
#     # グラフにheatmapとlineのデータを追加と指示
#     # グラフのレイアウト加工

#     # recordデータの加工 -> heatmap Yとz    /////////////////////////////////////////////
#     record_data = Record.objects.all()
#     record_df = read_frame(record_data, fieldnames=[
#                            'author', 'created_at', 'category', 'time'])
#     record_df1 = record_df.replace(
#         {'国語': 5, '数学': 4, '英語': 3, '理科': 2, '社会': 1})
#     record_df1['date'] = record_df1['created_at'].dt.strftime("%Y-%m-%d")  # 日付の加工//
#     record_df1['time_int'] = record_df1['time'].astype(int)  # 時間の加工
#     record_df2 = record_df1.drop(['created_at', 'author'], axis=1)  # 列の削除
#     # record_df2.dtypes データの型の確認

#     # 日付一覧作成 -> heatmap x    ///////
#     base = datetime.date.today()  # 今日の日付
#     datenum = 60  # 表示したい日数
#     dates = base - np.arange(datenum) * datetime.timedelta(days=1)
#     dates_df = pd.DataFrame({'date': dates})
#     dates_df['category'] = int(1)  # 日付データにいったんカテゴリ列(国語)を作成
#     dates_df.loc[datenum] = [base, 2]  # 最後の行にデータ追加 カテゴリを用意
#     dates_df.loc[datenum + 1] = [base, 3]
#     dates_df.loc[datenum + 2] = [base, 4]
#     dates_df.loc[datenum + 3] = [base, 5]
#     dates_df['time_int'] = int(0)  # 日付データにいったん時間をを作成
#     # dates_df.dtypes データの型の確認

#     # 結合表作成 -> heatmapデータ
#     comb_df = pd.merge(dates_df, record_df2, on=[
#                        'date', 'category', 'time_int'], how='outer')  # 結合
#     comb_df['date_str'] = comb_df['date'].astype(str)
#     comb_df1 = comb_df.drop(['date'], axis=1)  # 列の削除
#     comb_df2 = comb_df1.pivot_table(
#         index='category', columns='date_str', values='time_int', aggfunc='sum')  # クロス集計表の作成
#     comb_df3 = comb_df2.fillna(0)

#     # heatmapデータ
#     x = dates[::-1]  # x軸 逆順にする 今日を左にする
#     subject = ['国', '数', '英', '理', '社'] # y軸
#     heatmap_z = comb_df3 # z value

#     # Testデータの加工 -> line_graph    /////////////////////////////////////////////

#     test_data = Test.objects.all() #テストデータ
#     test_df = read_frame(test_data) #dfにする
#     test_df1 = test_df.rename(
#         columns={'japanese': '国', 'math': '数', 'english': '英', 'science': '理', 'social_studies': '社'})
#     test_df2 = test_df1.sort_values('date', ascending=False)



#     # グラフ作成    /////////////////////////////////////////////
#     fig = make_subplots(rows=2, cols=1,
#                     shared_xaxes=True,
#                     vertical_spacing=0.02)


#     # fig.add_trace(go.Figure(data=go.Heatmap(
#     #     z=heatmap_z,  # 色が変化するデータ
#     #     x=x,  # X軸
#     #     y=subject[::-1],   # Y軸
#     #     # # x=(1, 7),  # 縦軸ラベルに表示する値、10刻み
#     #     colorbar=dict(
#     #         thickness=10,
#     #         thicknessmode='pixels',
#     #         len=1.1,  # カラーバーの長さを0.8に（デフォルトは1）
#     #         lenmode='fraction',
#     #         outlinewidth=0,
#     #         title=dict(
#     #             text='分',
#     #             side='top')),  # カラーバーのタイトルをつける位置（デフォルトはtop）
#     #     colorscale=[
#     #         [0, 'rgb(17, 17, 17)'],  # NaNに該当する値を区別する
#     #         [0.01, 'rgb(255,255,255)'],  # NaNに該当する値を灰色にして区別する
#     #         [1, 'rgb(255,20,147)']],
#     #     row=1,
#     #     col=1,)))



#     fig.add_trace(px.line(
#             test_df2, #データ
#             x=record_df1['date'],
#             y=['国', '数', '英', '理', '社'],
#             color_discrete_sequence=['#ffff7a', '#ff77af', '#7affbc', '#7a7aff', '#ffbc7a']),
#         row=1,
#         col=1)
#     fig.add_trace(px.line(
#             test_df2, #データ
#             x=record_df1['date'],
#             y=['国', '数', '英', '理', '社'],
#             color_discrete_sequence=['#ffff7a', '#ff77af', '#7affbc', '#7a7aff', '#ffbc7a']),
#         row=2,
#         col=1)



#     fig.update_layout(
#         width=380,
#         height=530, # 図の高さを幅を指定
#         template='plotly_dark',
#         plot_bgcolor = '#212529',
#         showlegend=True, # 凡例を強制的に表示
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

#     fig_graph = fig.to_html(include_plotlyjs='cdn',
#                                  full_html=False).encode().decode('unicode-escape')

#     # /  heatmapとライングラフを返す  ////////////////////////////////////////////
#     return render(request, "study/graph.html", {
#         "graph": fig_graph,
#     })
