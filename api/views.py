from django.shortcuts import render

from api.serializers import UserSerializer,PostSerializer,CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action

class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class PostsView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kw):
        qs=request.user.posts_set.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kw):
        id=kw.get("pk")
        pst=Posts.objects.get(id=id)
        usr=request.user
        serializer=CommentSerializer(data=request.data,context={"post":pst,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/posts/1/list_comments
    @action(methods=["get"],detail=True)
    def list_comments(self,request,*args,**kw):
        id=kw.get("pk")
        pst=Posts.objects.get(id=id)
        qs=pst.comments_set.all()
        serializer=CommentSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["get"],detail=True)
    def likes(self,request,*args,**kw):
        pst=self.get_object()
        usr=request.user
        pst.like.add(usr)
        return Response(data="Created")


# class CommentsView(ModelViewSet):
#     serializer_class=CommentSerializer
#     queryset=Comments.objects.all()
#     authentication_classes=[authentication.BasicAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     @action(methods=["get"],detail=True)
#     def likes(self,request,*args,**kw):
#         cmnt=self.get_object() #comment object
#         usr=request.user
#         cmnt.likes.add(usr)
#         return Response(data="created")
