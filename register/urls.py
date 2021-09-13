from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    # ログイン
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    # メール登録
    path('user_create/',
         views.UserCreate.as_view(), name='user_create'),
    path('user_create/done',
         views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/',
         views.UserCreateComplete.as_view(), name='user_create_complete'),
    # ユーザー情報閲覧・更新ページ
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    # パスワード変更ページと再設定ページ
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(),
         name='password_change_done'),
    # パスワード忘れ
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),


]
