from django import forms
from .models import Article, Comment, Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('liker_set', 'author', 'club')

    def __init__(self, member, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        if not member.is_admin:
            self.fields['category'].queryset = Category.objects.exclude(name="공지사항")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'article', 'liker_set', )