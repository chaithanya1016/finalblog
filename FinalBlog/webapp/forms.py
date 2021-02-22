from django import forms
from .models import Comment, Article
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'email': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'body': forms.Textarea(attrs={'class': 'form-control col-md-8'}),
        }


#Add Article Form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','slug','overview','article_image','author','category','body','tags','read','publish','status','previous_post','next_post']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control col-md-6'}),
            'slug' : forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'overview': forms.Textarea(attrs={'class': 'form-control col-md-6'}),
            #'body': forms.Textarea(attrs={'class':'ckeditor col-md-6'}),
            'body': forms.CharField(widget=CKEditorWidget()),
            'tags': forms.TextInput(attrs={'class':'form-control col-md-4'}),
            'read': forms.TextInput(attrs={'class':'form-control col-md-4'}),
            'publish': forms.TextInput(attrs={'class':'form-control col-md-4'}),
        }
    
    