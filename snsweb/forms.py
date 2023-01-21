from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from api.models import Posts,Details

gender_choices=[('Female','Female'),('Male','Male'),('Others','Others')]

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
      
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()        

class PostForm(forms.ModelForm):

    class Meta:
        model=Posts
        fields=["title","image"]
        widget={
            "title":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-select"})
        }

class DetailsForm(forms.ModelForm):
   
    class Meta:
        model=Details
        fields=["profile_img","work","hobby","gender"]
        widget={
            "profile_img":forms.FileInput(attrs={"class":"form-select"}),
            "work":forms.Textarea(attrs={"class":"form-control"}),
            "hobby":forms.Textarea(attrs={"class":"form-control"}),
            "gender":forms.ChoiceField(choices=gender_choices)
        }

