from django import forms
from .models import Post, PostImage


class PostNewForm(forms.Form):
    title = forms.CharField(max_length=500, required=True)
    subtitle = forms.CharField(max_length=500, required=False)
    content = forms.CharField(widget=forms.Textarea, required=False)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'sub_title', 'content']


class PostWithImages(PostForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ['images', ]
