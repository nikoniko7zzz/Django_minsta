# from re import X
# from django.db.models import Q
# from django.http import request
# from django.http.response import HttpResponse  # Qオブジェクトは、モデルのデータの中からor検索をする
from django.shortcuts import get_object_or_404, redirect, render
# from django.views import generic
# from plotly import graph_objs
# from .forms import RecordCreateForm, TestForm, PostCreateForm
# from .models import Post, Category, Comment, Record, Test
from .models import Record, Test
from register.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages  # ラジオ
# from django.views.generic.edit import FormView
# from django.views.generic import TemplateView
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



# ■■■■■■■■■■■■■■■■■■■■■■■■
# ■          グラフ作成用データ加工            ■
# ■■■■■■■■■■■■■■■■■■■■■■■■
# Stacked Subplots with Shared X-Axes
@login_required
def GraphView(request):


# ■■■■■■データが入っていないときは、入力ページに飛ばす■■■■■■
    record_data = Record.objects.filter(author=request.user).all()
    test_data = Test.objects.filter(author=request.user).all() #テストデータ
    if record_data.count() == 0 and test_data.count() == 0:
        return redirect('study:two_input')



# ■■■■■■ 勉強時間入力データの加工 ■■■■■■
    record_data = Record.objects.filter(author=request.user).all()

    record_df = read_frame(record_data, fieldnames=[
                           'author', 'created_at', 'category', 'time'])
    record_df = record_df.replace(
        {'国語': '1', '数学': '2', '英語': '3', '理科': '4', '社会': '5'})
    record_df['date'] = pd.to_datetime(record_df['created_at'].dt.strftime("%Y-%m-%d"))
    record_df['time'] = record_df['time'].astype(int)  # 時間の加工
    record_df = record_df.drop(['created_at', 'author'], axis=1)  # 列の削除
    # category  time       date
    # 0        1    30 2021-11-01
    # 1        4    60 2021-11-01
    # 2        1    30 2021-11-01


# ■■■■■■ テスト結果入力データの加工 ■■■■■■
    test_df = Test.objects.filter(author=request.user).all()
    test_df = read_frame(test_df)
    test_df = test_df.rename(
        columns={'japanese': '国語', 'math': '数学', 'english': '英語', 'science': '理科', 'social_studies': '社会'})
    test_df['date'] = pd.to_datetime(test_df['date']).dt.tz_localize(None) #timezone:UTCを無くす
    test_df = test_df.drop(['created_at', 'author'], axis=1)
    test_df = test_df.sort_values('date', ascending=False) # 日付で並び替え 古いのが下
    #    id  国語  数学  英語  理科  社会       date
    # 3   9  75  65  55  45  35 2021-10-24
    # 1   7  72  62  52  42  32 2021-10-17
    # 0   6  70  60  50  40  30 2021-10-10

# ■■■■■■ グラフの表示日数計算＆データ作成用 ■■■■■■
    # 1. テスト結果入力の古い日付を取得
    old_test_day = test_df.iloc[-1]['date']
    print('テスト結果入力の古い日付を取得=', old_test_day)

    # 2. 今日の日付を取得
    base = datetime.datetime.today()

    # 3. ログインユーザー作成日を取得
    result = User.objects.get(id=request.user.id)
    user_creat_day = result.date_joined
    user_day = pd.to_datetime(user_creat_day).tz_localize(None)

    # 4. グラフ作成の一番古い日(last_day)を選び、表示日数を決める
    which_day = user_day - old_test_day
    if which_day.days < 0:
        last_day = (base - user_day).days
    else:
        last_day = (base - old_test_day).days
    print('user_day=', user_day)
    print('old_test_day=', old_test_day)
    print('last_day=', last_day)

    # 5. 今日からlast_dayまでのデータを作る
    dates = base - np.arange(last_day+1) * datetime.timedelta(days=1)
    # dates_df = pd.DataFrame({'date': dates})
    # dates_df['category'] = int(1)  # 日付データにいったんカテゴリ列(国語)を作成
    # dates_df.loc[last_day] = [base, 2]  # 最後の行にデータ追加 カテゴリを用意
    # dates_df.loc[last_day + 1] = [base, 3]
    # dates_df.loc[last_day + 2] = [base, 4]
    # dates_df.loc[last_day + 3] = [base, 5]
    # dates_df['time_int'] = int(0)  # 日付データにいったん時間をを作成

    # 日付データに国語、ゼロ時間を入れる
    dates_df = pd.DataFrame({'date': dates, 'category':'1', 'time':int(0)})
    # 今日の日付で5教科をゼロ時間でデータを入れる（初期の5教科入力前の表示枠もれを防ぐ）
    dates_df_5cate = pd.DataFrame([
                            [base, '1', int(0)],
                            [base, '2', int(0)],
                            [base, '3', int(0)],
                            [base, '4', int(0)],
                            [base, '5', int(0)]],
                            columns=['date', 'category', 'time'])

    base_df = pd.concat([dates_df, dates_df_5cate])
    print('base_df=',base_df)
    #             date category  time_int
    # 0  2021-10-25        1         0
    # 1  2021-10-24        1         0
    # 2  2021-10-23        1         0
    # 3  2021-10-22        1         0
    # 0  2021-10-25        2         0
    # 1  2021-10-25        3         0
    # 2  2021-10-25        4         0
    # 3  2021-10-25        5         0

# ■■■■■■ クロス集計表の作成 ■■■■■■
    # dfを縦に結合
    record_df = pd.concat([record_df, base_df]).sort_values('date')
    record_df['date'] = pd.to_datetime(record_df['date']).dt.strftime("%Y-%m-%d")
    # (record_df['created_at'].dt.strftime("%Y-%m-%d"))
    # print('dfを縦に結合後のrecord_df= ',record_df)
#     record_df3 = pd.merge(record_df2, base_df, how='outer')  # 結合
#     record_df3['date_str'] = record_df3['date'].astype(str)
#     # record_df4 = record_df3.sort_values('date_str')

    record_df = record_df.pivot_table(
        index='category', columns='date', values='time', aggfunc='sum')  # クロス集計表の作成
    record_df = record_df.reindex(index=['5', '4', '3', '2', '1'])
    record_df = record_df.fillna(0)
    print('クロス集計後のrecord_df= ',record_df)

    subject = ['国', '数', '英', '理', '社']
    print('record_df.columns.values= ',record_df.columns.values)

# ■■■■■■■■■■■■■■■■■■■■■■■■
# ■          グラフ表示用 plotly作成           ■
# ■■■■■■■■■■■■■■■■■■■■■■■■

    # グラフ作成    /////////////////////////////////////////////
    fig_two = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
    )

    fig_two.add_trace(

        go.Heatmap(
            x=record_df.columns.values,
            y=subject[::-1],
            z=record_df,

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
                # [0, '#212529'],  # NaNに該当する値を区別する
                [0, '#202020'],  # NaNに該当する値を区別する
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
            ygap=2,  # y軸の隙間
            xgap=2 # x軸の隙間
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
            name='国語',
            x=test_df2['date'], y=test_df2['国'], mode="lines+markers",
            marker=dict(color='#ffff00'),
            showlegend=True,
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            name='数学',
            x=test_df2['date'], y=test_df2['数'], mode="lines+markers",
            marker=dict(color='#7f00f0'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            name='英語',
            x=test_df2['date'], y=test_df2['英'], mode="lines+markers",
            marker=dict(color='#ff0000'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            name='理科',
            x=test_df2['date'], y=test_df2['理'], mode="lines+markers",
            marker=dict(color='#0000ff'),
        ),
        row=2, col=1
    )
    fig_two.add_trace(go.Scatter(
            name='社会',
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
