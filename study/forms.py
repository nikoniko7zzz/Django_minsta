from django import forms
from .models import Comment, Post, Record


class PostCreateForm(forms.ModelForm):
    """問題投稿フォーム"""

    class Meta:
        # 表示するモデルクラスのフィールドを定義 入力不要は必要ない
        model = Post
        fields = ('category', 'title', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # widget.attrs htmlで表示されるclass設定をしている
            self.fields['category'].widget.attrs = {'class': 'form-select mb-3'}
            self.fields['title'].widget.attrs = {'class': 'form-control mb-3'}
            self.fields['text'].widget.attrs = {'class': 'form-control mb-3'}



class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('name', 'text')


# class RecordCreateForm(forms.ModelForm):
#     """勉強時間"""

#     class Meta:
#         # 表示するモデルクラスのフィールドを定義 入力不要は必要ない
#         model = Record
#         fields = ('category', 'start_stop')

class RecordCreateForm(forms.ModelForm):
    """時間投稿フォーム"""

    class Meta:
        # 表示するモデルクラスのフィールドを定義 入力不要は必要ない
        model = Record
        fields = ('category', 'time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # widget.attrs htmlで表示されるclass設定をしている
            self.fields['category'].widget.attrs = {'class': 'form-select mb-3'}
            self.fields['time'].widget.attrs = {'class': 'form-select mb-3'}



