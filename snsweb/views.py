from django.shortcuts import render,redirect
from django.views.generic import View
from snsweb.forms import UserRegistrationForm,LoginForm,PostForm,DetailsForm
from django.views.generic import CreateView,FormView,TemplateView,ListView
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from api.models import Posts,Comments,Details


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid Session,Login First")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decs=[signin_required,never_cache]    

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")
    model=User

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"please fill correctly..")
        return super().form_valid(form)

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                messages.error(request,"Invalid Credentials")
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    success_url=reverse_lazy("index")
    model=Posts
    context_object_name="posts"


    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Post added")
        return super().form_valid(form)

    def get_queryset(self):
        return Posts.objects.all().order_by("-created_date")

decs
def  add_comments(request,*args,**kw):
    id=kw.get("id")
    pst=Posts.objects.get(id=id)
    comment=request.POST.get("comment")
    Comments.objects.create(post=pst,comment=comment,user=request.user)
    messages.success(request,"Comment added")
    return redirect("index")

decs
def post_like_view(request,*args,**kw):
    id=kw.get("id")
    pst=Posts.objects.get(id=id)
    pst.like.add(request.user)
    return redirect("index")

def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")

@method_decorator(decs,name="dispatch")
class MyPostView(ListView):
    template_name="mypost.html"
    context_object_name="posts"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")

def post_delete_view(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()
    messages.success(request,"Post Deleted")
    return redirect("my-post")

@method_decorator(decs,name="dispatch")
class ProfileView(CreateView):
    template_name="filldetail.html"
    form_class=DetailsForm
    success_url=reverse_lazy("index")
    model=Details

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
        
class MyProfileView(ListView):
    template_name="myprofile.html"
    context_object_name="profiles"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Details.objects.filter(user=self.request.user)





    





