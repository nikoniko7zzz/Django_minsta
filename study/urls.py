from django.urls import path
from .import views
from .import graph_views


app_name = 'study'

urlpatterns = [
     # path('', views.IndexView.as_view(), name='index'),
     path('', views.RecordInputView, name='index'),# 作成画面(時間レコード)
     path('category/<int:pk>/', views.CategoryView.as_view(), name='category'), # 教科選択した後の表示リスト
     #     path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
     #     path('comment/<int:post_pk>', views.CommentView.as_view(), name='comment'),
     path('new/', views.PostNewView, name='new'),  # 問題作成
     path('post_list/', views.PostListView.as_view(), name='post_list'),  # 問題作成

     # path('record_creat/', views.RecordCreatView,
     #      name='record_creat'),  # 作成画面(時間レコード)

     path('record_list/', views.RecordListView.as_view(),
          name='record_list'),  # リスト画面(時間レコード)
     path('r^/record_delete/<int:pk>/', views.RecordDeleteView.as_view(),
          name='record_delete'),  # 削除画面(時間レコード)
     path('graph/', graph_views.GraphView, name='graph'),
     path('two_input/', views.TwoInputView,
          name='two_input'),  # 作成画面(テスト結果入力画面)
     # path('graph_everyone/', views.GraphEveryoneView,
     #      name='graph_everyone'),  # 作成画面(テスト結果入力画面)

]


# # heroku上でエラー500の時に内容を表示する
# handler500 = views.my_customized_server_error
