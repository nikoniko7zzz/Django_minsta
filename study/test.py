# グラフデータの作り方まとめ/////////////////////

# データの加工
# python manage.py shell
from study.models import Record
from django_pandas.io import read_frame
import datetime
import numpy as np
import pandas as pd
# recordデータの加工///
record_data = Record.objects.all()
recode_df = read_frame(record_data, fieldnames=['author', 'created_at', 'category', 'time'])
recode_df['date'] = recode_df['created_at'].dt.strftime("%Y-%m-%d") # 日付の加工//
recode_df['time_int'] = recode_df['time'].str[:-1].astype(int) # 時間の加工
record_df1 = recode_df.drop(['created_at', 'time','author'], axis=1) # 列の削除

# 日付一覧作成
base = datetime.date.today() #今日の日付
dates = base - np.arange(10) * datetime.timedelta(days=1)
dates_df = pd.DataFrame({'date':dates})
dates_df['category'] = '国語' #日付データにいったんカテゴリ(国語)を作成

# 結合表作成
comb_df = pd.merge(dates_df, record_df1, on=['date','category'], how='outer') #結合
comb_df['date_str'] = comb_df['date'].astype(str)
comb_df1 = comb_df.drop(['date'], axis=1) # 列の削除
comb_df2 = comb_df1.pivot_table(index='date_str', columns='category', values='time_int', aggfunc='sum') # クロス集計表の作成
result_df = comb_df2.fillna(0)
# result_df = comb_df2.drop(['0'], axis=1) # 列の削除



cate_list=['国語','数学','英語','理科','社会']
add_colum = [i for i in cate_list if i not in comb_df2.columns] #集計データにない列を探す
comb_df2[[add_colum]]=int(0) # 集計データにない列を追加する





  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">





df_sum = df.pivot_table(index='date', columns='category', values='int_time', aggfunc='sum') # クロス集計表の作成
df
# df_sum = df.pivot_table(index='created_at', columns='category', values='int_time', aggfunc='sum') # クロス集計表の作成

# 日付一覧作成
base = datetime.date.today() #今日の日付
dates = base - np.arange(10) * datetime.timedelta(days=1)
df_dates = pd.DataFrame({'date':dates})
# df_dates = pd.DataFrame({'date':dates})


pd.concat([df1, df2])

# # recordデータと日付一覧データの結合、NaN値をゼロに置換/////
new_df = pd.merge(df_dates, df_sum, on='date', how='outer')
df_result = new_df.pivot_table(index='date', columns='category', values='int_time', aggfunc='sum') # クロス集計表の作成
df_result = df2.pivot_table(index='date', columns='category', values='int_time', aggfunc='sum') # クロス集計表の作成
df_result.duplicated(subset='index', keep='last')
df_result.drop_duplicates(subset='date', keep='last', inplace=True)
df_result.drop_duplicates(subset='date', keep='last')

# new_df["date"].astype(str)
# new_df.fillna(0)

cate_list=['国語','数学','英語','理科','社会']
add_colum = [i for i in cate_list if i not in df_sum.columns] #集計データにない列を探す
df_sum[[add_colum]]=int(0) # 集計データにない列を追加する


# dnew_dff2 = new_df.groupby(["date"], sort=False, as_index=False).agg({"count":"sum"})
# df.groupby('date').sum()
# df.groupby(['date', 'category']).sum()
# df_dates['created_at'].astype(datetime64)
# df2 = neo_df.groupby(["dates","国語","数学","英語","理科","社会"], sort=False, as_index=False).agg({"int_time":"sum"})
df2 = nozero_df.groupby(["date","category"], sort=False, as_index=False).agg({"int_time":"sum"})


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


