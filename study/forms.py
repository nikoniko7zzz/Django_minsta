from django import forms
from .models import Comment, Post
# from .models import Post



class PostCreateForm(forms.ModelForm):
    """問題投稿フォーム"""

    class Meta:
        # 表示するモデルクラスのフィールドを定義 入力不要は必要ない
        model = Post
        fields = ('category', 'title', 'text')

        # 表示ラベルを定義
        labels = {'category':'教科',
                  'title': '問題',
                  'text': '答え',
                  }

class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('name', 'text')
