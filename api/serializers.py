from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","username","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
# class PostSerializer(serializers.ModelSerializer):
#     user=serializers.CharField(read_only=True)
#     id=serializers.CharField(read_only=True)
#     class Meta:
#         model=Posts
#         fields=[
#             "id",
#             "title",
#             "image",
#             "user"
#         ]

class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    id=serializers.CharField(read_only=True)
    # post=serializers.CharField(read_only=True)
    created_date=serializers.DateField(read_only=True)
    # like_count=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=["id","comment","user","created_date"]

    def create(self, validated_data):
        pst=self.context.get("post")
        usr=self.context.get("user")
        return pst.comments_set.create(user=usr,**validated_data)


class PostSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    id=serializers.CharField(read_only=True)
    post_comments=CommentSerializer(read_only=True,many=True)
    like_count=serializers.CharField(read_only=True)

    class Meta:
        model=Posts
        fields=[
            "id",
            "title",
            "image",
            "user",
            "post_comments",
            "like_count"
        ]