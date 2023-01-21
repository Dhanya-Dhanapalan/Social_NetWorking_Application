from django.urls import path
from snsweb.views import SignInView,SignUpView,IndexView,add_comments,post_like_view,signout_view,MyPostView,post_delete_view,ProfileView,MyProfileView

urlpatterns=[
    path("register",SignUpView.as_view(),name="signup"),
    path("login",SignInView.as_view(),name="signin"),
    path("index",IndexView.as_view(),name="index"),
    path("posts/<int:id>/comments/add",add_comments,name="add-comment"),
    path("posts/<int:id>/likes/add",post_like_view,name="add-like"),
    path("logout",signout_view,name="sign-out"),
    path("myposts",MyPostView.as_view(),name="my-post"),
    path("posts/<int:id>/posts/remove",post_delete_view,name="post-delete"),
    path("detailedit",ProfileView.as_view(),name="fill-detail"),
    path("profile",MyProfileView.as_view(),name="profile-view")
   
]