from django import forms
from .models import Comment, Post, Record, Test
from django.contrib.admin.widgets import AdminDateWidget  # カレンダー形式で入力


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
            self.fields['category'].widget.attrs = {
                'class': 'form-select mb-3'}
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

# class RecordCreateForm(forms.ModelForm):///////////////////
#     """時間投稿フォーム"""

#     class Meta:
#         # 表示するモデルクラスのフィールドを定義 入力不要は必要ない
#         model = Record
#         fields = ('category', 'time')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             # widget.attrs htmlで表示されるclass設定をしている
#             self.fields['category'].widget=forms.RadioSelect
#             self.fields['time'].widget.attrs = {'class': 'form-select mb-3'}

CATEGORY_CHOICES = [
    ('国語', '国語'),
    ('数学', '数学'),
    ('英語', '英語'),
    ('理科', '理科'),
    ('社会', '社会'),
]
TIME_CHOICES = [
    ('30', '30分'),
    ('40', '40分'),
    ('50', '50分'),
    ('60', '60分'),
    ('70', '70分'),
    ('80', '80分'),
    ('90', '90分'),
    ('100', '100分'),
]


class RecordCreateForm(forms.ModelForm):

    category = forms.ChoiceField(
        label='教科',
        required=False,  # 入力項目を必須項目ではなく、任意の入力項目にする=false
        widget=forms.RadioSelect,
        choices=CATEGORY_CHOICES,
        # initial=0
    )
    time = forms.ChoiceField(
        label='時間',
        required=False,  # 入力項目を必須項目ではなく、任意の入力項目にする=false
        widget=forms.RadioSelect,
        choices=TIME_CHOICES,
    )

    class Meta:
        model = Record
        fields = ('category', 'time')


class TestForm(forms.ModelForm):
    """テスト結果追加フォーム"""
    class Meta:
        model = Test
        fields = '__all__'
        widgets = {
            'date': AdminDateWidget(),  # インポートしたウィジェットを使う指示
        }
