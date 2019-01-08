from django import forms
from blog.models import User,Profile,Contact,Post
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

from blog.models import Comment
class CommentForm(forms.ModelForm):
    body = forms.CharField( widget=forms.Textarea(attrs={'rows': 4, 'cols': 30}))
    class Meta:
        model=Comment
        fields=('name','email','body')

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']


class ContactForm(forms.ModelForm):
    body = forms.CharField( widget=forms.Textarea(attrs={'rows': 8, 'cols': 35}))
    class Meta:
        model=Contact
        fields='__all__'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']

class UserAddForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name']

class PostAddForm(forms.ModelForm):
    body = forms.CharField( widget=forms.Textarea(attrs={'rows': 6, 'cols': 35}))
    class Meta:
        model=Post
        fields=('title','slug','body','status','tags',)

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','slug','body','status','tags',)
