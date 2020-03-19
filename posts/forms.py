from django import forms
from .models import Post, PostImage, PostComment


class MakePost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('content',)
        widgets = {
                'content': forms.Textarea(attrs={
                "rows": 5,
                "cols": 68,
            })
        }


class AddImage(forms.ModelForm):

     class Meta:
        model = PostImage
        fields = ('image',)


class AddComment(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={
                                        "rows": 1,
                                        "cols": 60
                                        })
                }

class SendPostReport(forms.Form):
    report = forms.CharField(widget=forms.Textarea(attrs={
                                                        "rows": 6,
                                                        "cols": 60,
                                                        }))
