from django.db.models import Q  # Qオブジェクトは、モデルのデータの中からor検索をする
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .forms import CommentCreateForm, PostCreateForm
from .models import Post, Category, Comment
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

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


    # def NewView(request):
    # # params = {'message': 'newです'}
    # params = {'message':'', 'form':None}
    # if request.method == 'POST':
    #     form = PostCreateForm(request.POST)
    #     if form.is_valid(): #フォームに入力された値にエラーがないかをバリデートする
    #         post = form.save(commit=False)
    #         post.author = request.user #ログインユーザーをformに入れている
    #         post.save()
    #         print('問題を作成しました。')
    #         # return redirect('new')
    #     else:
    #         params['message'] = '再入力してください'
    #         params['form'] = form
    # else:
    #     params['form'] = PostCreateForm()
    # return render(request, 'study/post_input.html', params)



