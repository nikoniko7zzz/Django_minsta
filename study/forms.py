from django import forms
from django.contrib.admin import widgets
from .models import Comment, Post, Record, Test
from django.contrib.admin.widgets import AdminDateWidget  # カレンダー形式で入力
# from django.forms import MultiWidget #カレンダーに使う

# ◆◆◆◆◆◆◆◆◆↓↓↓今回実装なし↓↓↓◆◆◆◆◆◆◆◆◆
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
                'class': 'form-select mb-3',
                'style': 'background-color:#212529; color:#999;'}
            self.fields['title'].widget.attrs = {
                'class': 'form-control mb-3',
                'style': 'background-color:#212529; color:#999;'}
            self.fields['text'].widget.attrs = {
                'class': 'form-control mb-3',
                'style': 'background-color:#212529; color:#999;'}


# class CommentCreateForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model = Comment
#         fields = ('name', 'text')
# ◆◆◆◆◆◆◆◆◆↑↑↑今回実装なし↑↑↑◆◆◆◆◆◆◆◆◆


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
    """勉強時間追加フォーム"""
    category = forms.ChoiceField(
        label='教科',
        required=False,  # 入力項目を必須項目ではなく、任意の入力項目にする=false
        widget=forms.RadioSelect,
        # widget=forms.RadioSelect(attrs={'class': 'radiobutton'}),
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

class DatePickWidget(forms.DateInput): #カレンダー用
    input_type="date"

class TestForm(forms.ModelForm):
    """テスト結果追加フォーム"""
    class Meta:
        model = Test
        # 偏差値の総合はviewで計算をするのでform不要
        fields = ('date',
                'rank_japanese', 'rank_math','rank_english', 'rank_science', 'rank_social_studies', 'rank_overall',
                'tscore_japanese', 'tscore_math','tscore_english', 'tscore_science', 'tscore_social_studies')
        widgets = {
            # 'date': DatePickWidget,
            'date': DatePickWidget(attrs={'style': 'background-color:#aaaaaa;'}),

            'rank_japanese' : forms.NumberInput(attrs={'class':'ef'}),
            'rank_math' : forms.NumberInput(attrs={'class':'ef'}),
            'rank_english' : forms.NumberInput(attrs={'class':'ef'}),
            'rank_science' : forms.NumberInput(attrs={'class':'ef'}),
            'rank_social_studies' : forms.NumberInput(attrs={'class':'ef'}),
            'rank_overall' : forms.NumberInput(attrs={'class':'ef'}),

            'tscore_japanese' : forms.NumberInput(attrs={'class':'ef'}),
            'tscore_math' : forms.NumberInput(attrs={'class':'ef'}),
            'tscore_english' : forms.NumberInput(attrs={'class':'ef'}),
            'tscore_science' : forms.NumberInput(attrs={'class':'ef'}),
            'tscore_social_studies' : forms.NumberInput(attrs={'class':'ef'}),
            # 'date': AdminDateWidget(),  # インポートしたadminウィジェット用
            # 'date': DatePickerInput(format='%Y-%m-%d') #bootstrapカレンダー
        }
        # japanese = forms.NumberInput(attrs={'style':'placeholder:"国語";'}),

